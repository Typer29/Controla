# Plan.md — Windows Monitoring Agent (không dùng extension)

**Phiên bản:** 1.0
**Ngày:** 24/08/2025
**Chủ dự án:** (điền tên)
**Repo:** monorepo theo cấu trúc trong Prompt.md

---

## 0) Tóm tắt & Bối cảnh

Xây dựng agent giám sát minh bạch chạy trên Windows (máy thuộc sở hữu của bạn), ghi lại **ứng dụng** và **trang web đang xem** (URL + tiêu đề tab) cùng **thời lượng foreground**; **không** keylogger, **không** chụp màn hình, **không** extension trình duyệt. Có **Tray icon** cho **Pause/Resume**. Dữ liệu lưu cục bộ (SQLite) và có thể **đồng bộ** lên server (PostgreSQL/MySQL) qua API bảo mật.

---

## 1) Phạm vi (Scope)

### 1.1 In-scope

* Collector ứng dụng & cửa sổ (process start/stop, foreground window, idle detection).
* Collector web không dùng extension (UIAutomation bắt buộc; History backfill; ETW domain optional).
* Lược đồ dữ liệu & migrations; chuẩn hoá thời gian UTC.
* Web API ingest (FastAPI) + xác thực JWT/TLS.
* Tray App (PySide/PyQt) với Pause/Resume, trạng thái.
* Dashboard báo cáo (FastAPI template/React tuỳ chọn): tổng quan, Top app/domain, heatmap, export CSV.
* Đóng gói cài đặt (MSI/EXE), auto-update an toàn, ký code (hoặc mock ký).
* Tài liệu hoá (README, chính sách dữ liệu, gỡ bỏ, vận hành).

### 1.2 Out-of-scope

* Keylogger, chụp màn hình, đọc nội dung tài liệu/ô nhập.
* Theo dõi trên hệ điều hành khác ngoài Windows (v1).
* Chính sách chặn ứng dụng/trang web chủ động (blocking).

---

## 2) Mục tiêu & Chỉ số thành công

* **Độ chính xác**: ghi phiên foreground đúng > 95% (đối chiếu log thủ công).
* **Tài nguyên**: CPU trung bình < 2%, RAM < 150 MB.
* **Độ bền dữ liệu**: không mất sự kiện khi mất mạng (queue offline), đồng bộ retry với backoff.
* **Minh bạch**: có Consent lần đầu, Tray luôn hiển thị, Pause hoạt động (không ghi sự kiện khi Pause).
* **Báo cáo**: Dashboard hiển thị Top app/domain, heatmap, lọc theo thời gian; export CSV hoạt động.

---

## 3) Kiến trúc tổng quan

Monorepo:

```
service/        # Windows Service (collector core)
tray/           # Tray App (PySide/PyQt)
collectors/     # uia_web/, proc_focus/, history_backfill/, etw_domain/
webapi/         # FastAPI (REST) + OpenAPI schema
webui/          # Dashboard (FastAPI template hoặc React)
db/             # SQLAlchemy models + migrations
pkg/            # Đóng gói cài đặt (MSI/EXE), auto-update
docs/           # HDSD, chính sách dữ liệu, gỡ bỏ
tests/          # unit/integration, dữ liệu giả
```

Luồng dữ liệu cục bộ → queue (SQLite) → (tuỳ chọn) đồng bộ → server DB (PostgreSQL/MySQL). Healthcheck `/v1/healthz`.

---

## 4) Work Breakdown Structure (WBS)

### 4.1 collectors/proc\_focus (ứng dụng & cửa sổ)

* Tạo service Windows, đăng ký `SetWinEventHook(EVENT_SYSTEM_FOREGROUND)`.
* WMI/ETW hoặc `psutil` theo dõi process start/stop; tính `file_hash_sha256`.
* Bộ đếm `active_seconds` theo app session; **Idle detection** bằng `GetLastInputInfo()` (mặc định 60s, config được).
* Gộp/đóng session khi đổi foreground/idle.
* Log minimal; batch ghi DB.

### 4.2 collectors/uia\_web (web không dùng extension)

* UIA cho Chrome/Edge/Firefox: tìm Address Bar (role `Edit`/`ComboBox`, AutomationId quen thuộc); đọc **URL**, lấy **tab title**.
* Poll 1–2s hoặc theo sự kiện foreground; gộp `web_session` theo (browser, URL).
* Fallback nếu không đọc được URL: chỉ lưu **domain** từ title hoặc tín hiệu ETW.

### 4.3 collectors/history\_backfill (tuỳ chọn, nên bật)

* Định kỳ copy file History SQLite của Chromium/Firefox sang temp; đọc `urls/visits`.
* Map visits với khoảng thời gian foreground để ước lượng `active_seconds` còn thiếu.

### 4.4 collectors/etw\_domain (tuỳ chọn)

* Subservice nghe ETW: `Microsoft-Windows-TCPIP / WinInet / MsQuic`.
* Map **process ⇄ domain** (SNI/Host). Lưu **domain** (không path) để kiểm chứng/lấp chỗ trống.

### 4.5 db/ (mô hình dữ liệu & migrations)

* Bảng: `devices, users, apps, app_sessions, web_domains, web_sessions, overrides, audit_logs`.
* Index & unique tạm để chống trùng lặp.
* Migrations (Alembic).

### 4.6 webapi/ (ingest + quản trị)

* Endpoint ingest: `POST /v1/ingest/app-sessions`, `POST /v1/ingest/web-sessions`.
* Catalog: `GET /v1/catalog/apps`, `GET /v1/catalog/domains`.
* Overrides: `POST/GET /v1/overrides`; Health: `GET /v1/healthz`.
* Bảo mật: TLS, JWT cho agent; rate-limit nhẹ.

### 4.7 tray/

* Tray icon; menu: **Pause/Resume**, “Đang ghi gì”, “Chính sách & Quyền riêng tư”, “Thoát”.
* IPC với service để bật/tắt ghi nhận.

### 4.8 webui/

* Dashboard: phạm vi thời gian, tổng thời gian theo ngày/tuần/tháng; Top app/domain; heatmap theo giờ; drill-down session.
* Lọc theo user/máy; Export CSV.

### 4.9 pkg/

* Tạo installer (MSI/EXE): cài service, auto-start, tạo shortcut Tray.
* Auto-update an toàn (kiểm tra chữ ký, rollback).

### 4.10 tests/

* Unit: collector (UIA, idle, merge session), đọc History copy, ETW giả lập.
* Integration: ingest API, dashboard queries.
* Dữ liệu giả lập & test performance nhẹ.

### 4.11 docs/

* README cài đặt/chạy; chính sách dữ liệu & consent; hướng dẫn gỡ bỏ; vận hành & sự cố thường gặp.

---

## 5) Lộ trình & Mốc (đề xuất 6 tuần)

> Có thể co giãn theo nhân lực; ghi mốc theo ngày nếu đã có lịch.

* **Tuần 1:** Khởi tạo repo, models DB + migrations; proc\_focus collector (foreground + idle); khung Tray; cấu hình YAML/JSON.
* **Tuần 2:** UIA Web (Chrome/Edge/Firefox) lấy URL + title; ghép session; unit tests cơ bản.
* **Tuần 3:** WebAPI ingest + JWT/TLS; queue offline & dedupe; kết nối DB server; dashboard MVP (tổng quan, top app/domain).
* **Tuần 4:** History backfill; tối ưu hiệu năng (CPU/RAM); export CSV; healthcheck.
* **Tuần 5:** ETW domain (optional); auto-update; installer; hoàn thiện docs/consent.
* **Tuần 6:** Hardening & kiểm thử tích hợp, đo lường chỉ số, sửa lỗi; chốt DoD, sign-off.

---

## 6) Quản lý yêu cầu & Cấu hình

* **File cấu hình** (YAML/JSON):

  * `idle_threshold_seconds`, `poll_interval_ms`, bật/tắt: `history_backfill`, `etw_domain`.
  * `db.local.path`, `api.base_url`, `agent.jwt`, `tls.cert_path`.
  * `retention_days`, `log.level`, `batch.size`, `batch.interval_ms`.
* **Biến môi trường**: override các khoá nhạy cảm (token, đường dẫn cert).

---

## 7) Bảo mật & Tuân thủ

* Consent lần đầu: hiển thị rõ dữ liệu thu thập; lưu `consented_at`, `policy_version`.
* Minh bạch: trang “Đang ghi những gì”, nút Pause; không chạy ẩn.
* TLS mọi giao tiếp; JWT cho agent; audit log hành vi admin.
* Xoay/nén log; TTL dữ liệu (mặc định 90 ngày, cấu hình được).

---

## 8) Rủi ro & Giảm thiểu

* **UIA không đọc được URL** (layout thay đổi):

  * *Giảm thiểu:* nhiều selector dự phòng; cập nhật danh sách AutomationId; fallback domain từ title/ETW; backfill History.
* **Khoá file History**: copy sang temp trước khi đọc.
* **Tốn tài nguyên khi poll**: điều chỉnh chu kỳ, batch ghi DB, debounce sự kiện.
* **Quyền & driver**: chạy với đặc quyền tối thiểu; ký code để giảm cảnh báo.
* **Sai phân loại app/domain**: cơ chế `overrides` để sửa bằng tay.

---

## 9) Definition of Done (DoD)

* Agent ghi **app\_sessions** đúng khi đổi cửa sổ; idle không cộng thời gian.
* Foreground trình duyệt → **URL + title** được ghi bằng UIA; tạo **web\_sessions** với `active_seconds` đúng.
* **History backfill** lấp khoảng missed; **ETW domain** bổ sung khi cần.
* **Pause** hoạt động: khi Pause, không phát sinh sự kiện trong DB.
* Dashboard hiển thị **Top app/domain**, heatmap; export CSV OK.
* CPU < 2%, RAM < 150MB (đo bằng perf test nhẹ).
* Tài liệu & installer đầy đủ; auto-update chạy an toàn.

---

## 10) Ma trận trách nhiệm (RACI mẫu)

| Hạng mục          | R           | A         | C     | I   |
| ----------------- | ----------- | --------- | ----- | --- |
| proc\_focus       | Dev A       | Tech Lead | QA    | PM  |
| uia\_web          | Dev B       | Tech Lead | Dev A | PM  |
| history\_backfill | Dev B       | Tech Lead | DBA   | PM  |
| etw\_domain       | Dev C       | Tech Lead | Sec   | PM  |
| db & migrations   | DBA         | Tech Lead | Devs  | PM  |
| webapi            | Dev A       | Tech Lead | Sec   | PM  |
| tray              | Dev C       | Tech Lead | UX    | PM  |
| webui             | Dev D       | Tech Lead | UX    | PM  |
| pkg & auto-update | Dev C       | Tech Lead | Sec   | PM  |
| tests & QA        | QA          | QA Lead   | Devs  | PM  |
| docs              | Tech Writer | PM        | Devs  | All |

---

## 11) Kế hoạch kiểm thử

* **Unit**: Idle detector, session merger, UIA URL parser, History reader.
* **Integration**: ingest API, dedupe queue, dashboard queries.
* **Perf**: mô phỏng đổi foreground 5–10 lần/giây trong 15 phút; đo CPU/RAM/IO.
* **UAT**: checklist DoD; kịch bản Pause/Resume; mất mạng & retry.

---

## 12) Kế hoạch triển khai & Rollout

* Giai đoạn **Pilot** trên 1–2 máy nội bộ; theo dõi logs/metrics.
* Ký code, tạo installer; thử auto-update (kênh dev → prod).
* Checklist gỡ bỏ sạch (uninstall) & khôi phục trạng thái.

---

## 13) Phụ lục

### 13.1 Mô hình dữ liệu (tóm tắt)

* `apps, app_sessions, web_domains, web_sessions, overrides, devices, users, audit_logs`.
* Index theo `(user_id, started_at)`, `(domain_id, started_at)`, `(app_id, started_at)`; unique tạm cho dedupe.

### 13.2 API (tóm tắt)

* `POST /v1/ingest/app-sessions`, `POST /v1/ingest/web-sessions`.
* `GET /v1/catalog/*`, `POST/GET /v1/overrides`, `GET /v1/healthz`.

### 13.3 Cấu hình mẫu (YAML)

```yaml
idle_threshold_seconds: 60
poll_interval_ms: 1000
features:
  history_backfill: true
  etw_domain: false
storage:
  sqlite_path: data/agent.db
  retention_days: 90
api:
  base_url: https://server.local
  jwt: "<token>"
  tls_cert_path: certs/agent.pfx
logging:
  level: INFO
batch:
  size: 100
  interval_ms: 1000
```

### 13.4 Open questions (điền thêm nếu cần)

* Mức độ chi tiết về title/URL cần ẩn bớt? (masking)
* Có cần đa ngôn ngữ cho UI Tray/Dashboard?
* Chính sách giữ liệu theo nhóm người dùng?
