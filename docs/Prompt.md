ROLE / SYSTEM
Bạn là Senior Python Engineer. Hãy xây dựng một **Windows monitoring agent minh bạch** cho máy do tôi sở hữu, dùng để ghi nhận **ứng dụng đang dùng** và **trang web đang xem** (URL/tab title) cùng **thời lượng foreground**. 
Ràng buộc: 
- **Không dùng browser extension**. 
- **Không** hook bàn phím, **không** chụp màn hình, **không** đọc nội dung tài liệu/ô nhập. 
- Luôn có **biểu tượng khay hệ thống (Tray)**, cho phép **Pause/Resume**. 
- Minh bạch/tuân thủ: hiển thị thông báo và lấy **đồng ý** ngay lần đầu.

MỤC TIÊU
- Ghi phiên sử dụng ứng dụng và web với độ chính xác cao, tài nguyên thấp.
- Lưu cục bộ (SQLite) và có thể đồng bộ lên máy chủ (PostgreSQL/MySQL) qua API bảo mật.
- Cung cấp dashboard xem báo cáo thời gian theo ngày/tuần/tháng, Top app/domain, heatmap giờ.

KIẾN TRÚC TỔNG THỂ (monorepo)
- service/        : Windows Service (collector core)
- tray/           : Tray App (PySide/PyQt)
- collectors/     : uia_web/, proc_focus/, history_backfill/, etw_domain/
- webapi/         : FastAPI (REST) + OpenAPI schema
- webui/          : Dashboard (FastAPI template hoặc React)
- db/             : SQLAlchemy models + migrations
- pkg/            : đóng gói cài đặt (MSI/EXE), auto-update
- docs/           : HDSD, chính sách dữ liệu, gỡ bỏ
- tests/          : unit/integration, dữ liệu giả lập

YÊU CẦU CHỨC NĂNG

1) Collector — Ứng dụng & cửa sổ (proc_focus/)
- Theo dõi **process start/stop** qua WMI/ETW hoặc psutil: ghi `name`, `exe_path`, `pid`, `publisher` (nếu lấy được), `sha256` của file .exe.
- Theo dõi **foreground window** bằng `SetWinEventHook` (EVENT_SYSTEM_FOREGROUND) hoặc UIAutomation: mỗi lần đổi focus, cập nhật **app_session**.
- Ghi **window_title** định kỳ (1–2s) khi app ở foreground, cộng **active_seconds** khi không idle.
- **Idle detection**: dùng `GetLastInputInfo()`, ngưỡng mặc định 60s (config được). Khi idle: đóng/treo phiên đang mở, không cộng thời gian.

2) Collector — Web không dùng extension
- **UI Automation (bắt buộc)**:
  - Khi foreground là `chrome.exe`/`msedge.exe`/`firefox.exe`, dùng **IUIAutomation** tìm control thanh địa chỉ (role `Edit`/`ComboBox`, AutomationId thường gặp như “Address and search bar” trên Chromium). Đọc **URL** qua `ValuePattern.Value`. 
  - Lấy **tab title** từ cửa sổ/element tiêu đề. Chu kỳ poll 1–2s hoặc theo sự kiện đổi foreground.
  - Tạo/gộp **web_session** theo (browser, URL) với `started_at`, `ended_at`, `active_seconds`.
  - Fallback: nếu URL tạm thời không đọc được (VD trang nội bộ), vẫn ghi **domain** từ tiêu đề/tab hoặc từ ETW (mục 2c).
- **History Backfill (tùy chọn, nên bật)**:
  - Định kỳ (mỗi 5–10 phút), copy file SQLite History của Chromium/Firefox (vì file bị khóa) vào temp, đọc bảng `urls/visits` để backfill **URL + thời điểm truy cập**; map với khoảng thời gian foreground để ước lượng **active_seconds** còn thiếu.
- **ETW Network (tùy chọn, domain-level)**:
  - Nghe provider ETW `Microsoft-Windows-TCPIP / WinInet / MsQuic` để map **process ⇄ domain** (SNI/host). Chỉ lưu **domain**, không path. Dùng để kiểm chứng và lấp chỗ trống khi UIA/History miss.

3) Dữ liệu & Lược đồ (SQLAlchemy)
- Chuẩn hóa thời gian **UTC** trong DB; hiển thị theo timezone máy.
- Bảng cốt lõi:
  - `devices(id, hostname, os_version, installed_at, owner)`
  - `users(id, username, sid, display_name)`
  - `apps(id, name, publisher, exe_path, file_hash_sha256, category)`
  - `app_sessions(id, user_id, device_id, app_id, pid, started_at, ended_at, active_seconds, window_title_sample)`
  - `web_domains(id, domain, category)`
  - `web_sessions(id, user_id, device_id, domain_id, url, title, browser, started_at, ended_at, active_seconds)`
  - `overrides(id, target_type(app|domain|url), target_id, new_category, note, updated_by, updated_at)`
  - `audit_logs(id, actor, action, target, ts, detail_json)`
- Ràng buộc: index theo `(user_id, started_at)`, `(domain_id, started_at)`, `(app_id, started_at)`; unique tạm cho dedupe session overlap.

4) API & Đồng bộ (webapi/)
- **FastAPI** với các endpoint (JWT/TLS):
  - `POST /v1/ingest/app-sessions`
  - `POST /v1/ingest/web-sessions`
  - `GET /v1/catalog/apps`, `GET /v1/catalog/domains`
  - `POST /v1/overrides`, `GET /v1/overrides`
  - `GET /v1/healthz`
- Retry với exponential backoff; queue offline (SQLite) khi mất mạng; cơ chế **dedupe** sự kiện.

5) Tray App (tray/)
- PySide/PyQt: icon khay, menu: **Pause/Resume**, “Xem dữ liệu đang ghi”, “Chính sách & Quyền riêng tư”, “Thoát”.
- Trạng thái realtime (Recording/Paused). Khi Pause: collector ngừng tạo sự kiện mới.

6) Dashboard (webui/)
- Trang tổng quan: chọn khoảng thời gian; **Tổng thời gian** theo ngày/tuần/tháng; **Top 10 ứng dụng**, **Top 50 domain**; heatmap giờ sử dụng; drill-down tới session.
- Lọc theo người dùng/máy; **Export CSV**.
- Không hiển thị nội dung nhạy cảm (chỉ tên app, URL, title).

7) Bảo mật & Tuân thủ
- **Welcome/Consent** lần đầu: mô tả rõ dữ liệu thu thập, lưu `consented_at` + policy_version.
- **Minh bạch**: trang “Đang ghi những gì”; nút **Pause** rõ ràng.
- **TLS** cho mọi giao tiếp; JWT cho agent; **ký code** gói cài đặt.
- Xoay/nén log; chính sách lưu trữ (mặc định 90 ngày, cấu hình được).
- **KHÔNG** keylogger, **KHÔNG** chụp màn hình, **KHÔNG** ẩn tiến trình/service.

8) Đóng gói & Cập nhật (pkg/)
- Tạo Windows Service (nền) + shortcut Tray App. Hỗ trợ **auto-start**.
- **Auto-update an toàn**: kiểm tra chữ ký, rollback nếu lỗi. Tài liệu gỡ bỏ sạch.

9) Hiệu năng & Tin cậy
- Mục tiêu tài nguyên: CPU < 2%, RAM < 150MB.
- Batch ghi DB; tránh ghi quá thường xuyên.
- Health check: `/v1/healthz`, tự chẩn đoán quyền, trạng thái hook, hàng đợi.

10) Kiểm thử
- Unit test collector (UIA, idle, merge session), test đọc History file copy, test ETW giả lập.
- Integration test ingest API, dashboard queries.
- Script sinh dữ liệu giả.

ĐỊNH NGHĨA SỰ KIỆN (schema JSON gửi API)
- `AppSession`:
  {
    "user_id": "win-user-sid-or-name",
    "device_id": "device-guid",
    "app": {"name": "Photoshop", "exe_path": "C:\\...\\Photoshop.exe", "file_hash_sha256": "..."},
    "pid": 1234,
    "started_at": "2025-08-24T13:45:12Z",
    "ended_at": "2025-08-24T14:05:40Z",
    "active_seconds": 1228,
    "window_title_sample": "Untitled - Photoshop"
  }
- `WebSession`:
  {
    "user_id": "win-user",
    "device_id": "device-guid",
    "browser": "chrome",
    "url": "https://example.com/page",
    "title": "Example Page",
    "domain": "example.com",
    "started_at": "2025-08-24T13:50:00Z",
    "ended_at": "2025-08-24T14:03:10Z",
    "active_seconds": 790
  }

TIÊU CHÍ NGHIỆM THU
- Chuyển cửa sổ tạo/đóng **app_sessions** chính xác; idle không cộng thời gian.
- Khi foreground là trình duyệt, **UIA đọc được URL + title**, tạo **web_sessions** với thời lượng đúng.
- **History backfill** lấp các khoảng UIA bỏ lỡ; **ETW** bổ sung **domain** khi cả hai cách trên không khả dụng.
- Nút **Pause** hoạt động: khi bật Pause, **không** có sự kiện mới trong DB.
- Dashboard hiển thị **Top app/domain** và heatmap theo khoảng thời gian chọn; export CSV hoạt động.

GỢI Ý KỸ THUẬT (ưu tiên dùng)
- Python: `pywin32`, `comtypes` hoặc `uiautomation`/`pywinauto`, `psutil`, `sqlite3`, `sqlalchemy`, `fastapi`, `uvicorn`, `requests`, `watchdog`.
- ETW: `krabsetw` (qua module Python hoặc dịch vụ phụ C#), ghép sự kiện theo PID.
- Lịch sử trình duyệt: copy file SQLite `History/places.sqlite` sang temp trước khi đọc.
- Cấu hình qua file YAML/JSON: ngưỡng idle, chu kỳ poll, bật/tắt history/etw, TTL lưu trữ.

ĐẦU RA BẮT BUỘC
- Repo chạy được với hướng dẫn `README`: cài đặt, quyền, cấu hình, chạy service/tray/web.
- OpenAPI JSON cho webapi/, migrations DB, bộ dữ liệu giả, test pass.
- Bộ cài đặt Windows đã ký (hoặc script sign mock) + quy trình auto-update minh bạch.

LƯU Ý PHÁP LÝ
- Ứng dụng chỉ sử dụng trên thiết bị tôi sở hữu; luôn thông báo và lấy đồng ý người dùng trên máy. Không dùng để theo dõi trái phép.
