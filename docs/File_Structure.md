# File\_Structure.md — Windows Monitoring Agent (không dùng extension)

**Phiên bản:** 1.0
**Ngày:** 24/08/2025
**Tài liệu tham chiếu:** Prompt.md, Plan.md, Diagram.md, Work\_Flow\.md

> Mục tiêu: Chuẩn hoá cấu trúc monorepo + tên file/thư mục + scaffold tối thiểu cho build/test/deploy. Tương thích Windows 10/11. Không dùng browser extension.

---

## 1) Cây thư mục tổng quan

```
monorepo/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ .gitattributes
├─ .editorconfig
├─ pyproject.toml                 # deps chung (nếu tách env, xem /service/pyproject.toml ...)
├─ ruff.toml                      # lint
├─ pytest.ini
├─ noxfile.py / tasks.py          # tiện ích dev (nox/invoke)
├─ Makefile                       # lệnh tắt (Windows hỗ trợ qua mingw/make hoặc dùng .ps1)
├─ .github/
│  └─ workflows/
│     ├─ ci.yml                   # lint+test
│     ├─ build.yml                # build artefacts (svc/tray/webapi/webui)
│     └─ release.yml              # tạo bản phát hành, ký số, upload installer
├─ configs/
│  ├─ agent.yaml                  # config runtime chung
│  ├─ logging.yaml                # cấu hình log
│  ├─ browser_selectors.yaml      # UIA selectors cho Chrome/Edge/Firefox
│  └─ secrets.example.env         # mẫu biến môi trường
├─ scripts/
│  ├─ dev.ps1                     # khởi chạy stack dev cục bộ
│  ├─ seed_fake_data.py           # sinh dữ liệu giả
│  ├─ db_migrate.py               # tiện ích chạy Alembic
│  ├─ export_csv.py               # xuất dữ liệu báo cáo
│  ├─ bench_foreground.py         # benchmark collector
│  └─ health_check.ps1            # kiểm tra nhanh /v1/healthz
├─ schema/
│  ├─ app_session.schema.json
│  └─ web_session.schema.json
├─ docs/
│  ├─ Prompt.md
│  ├─ Plan.md
│  ├─ Diagram.md
│  ├─ Work_Flow.md
│  ├─ File_Structure.md
│  ├─ PRIVACY_POLICY.md
│  ├─ SECURITY.md
│  ├─ CONTRIBUTING.md
│  └─ CHANGELOG.md
├─ db/
│  ├─ models/
│  │  ├─ base.py                  # Base=declarative_base()
│  │  ├─ device.py
│  │  ├─ user.py
│  │  ├─ app.py
│  │  ├─ app_session.py
│  │  ├─ web_domain.py
│  │  ├─ web_session.py
│  │  ├─ override.py
│  │  └─ audit_log.py
│  ├─ migrations/
│  │  ├─ env.py
│  │  └─ versions/                # alembic versions_*.py
│  ├─ queries/
│  │  ├─ reports.sql
│  │  └─ maintenance.sql
│  └─ local_dev.sqlite            # chỉ cho dev (gitignore trong thực tế)
├─ service/                        # Windows Service (agent core)
│  ├─ pyproject.toml              # deps riêng cho service
│  ├─ agent_service.py            # entry Windows service (pywin32)
│  ├─ agent_config.py
│  ├─ logging_setup.py
│  ├─ ipc.py                      # IPC với Tray
│  ├─ idle_detector.py            # GetLastInputInfo
│  ├─ session_aggregator.py       # gộp phiên app/web + quy tắc idle/merge
│  ├─ batcher.py
│  ├─ uploader.py                 # JWT/TLS, retry/backoff
│  ├─ healthcheck.py              # nội bộ
│  ├─ schemas.py                  # Pydantic schema cho queue
│  ├─ collectors/
│  │  ├─ __init__.py
│  │  ├─ proc_focus.py            # SetWinEventHook + process map
│  │  ├─ uia_web/
│  │  │  ├─ __init__.py
│  │  │  ├─ uia_reader.py         # đọc URL/title qua UIA
│  │  │  └─ selectors.py          # lớp trừu tượng hoá selector per-browser
│  │  ├─ history_backfill.py      # copy SQLite History & merge (optional)
│  │  └─ etw_domain.py            # listener ETW domain-level (optional)
│  ├─ storage/
│  │  ├─ queue_sqlite.py          # hàng đợi cục bộ + dedupe
│  │  └─ retention.py             # TTL + rotation
│  └─ tests/
│     ├─ test_idle_detector.py
│     ├─ test_session_aggregator.py
│     ├─ test_uia_reader.py
│     ├─ test_queue_sqlite.py
│     └─ fixtures/
├─ tray/                           # PySide/PyQt Tray App
│  ├─ pyproject.toml
│  ├─ main.py                      # icon khay, menu Pause/Resume
│  ├─ ipc_client.py
│  ├─ resources/
│  │  ├─ icons/
│  │  │  ├─ tray_recording.ico
│  │  │  └─ tray_paused.ico
│  │  └─ qrc.qrc
│  └─ tests/
│     └─ test_tray_state.py
├─ webapi/                         # FastAPI (ingest + quản trị nhẹ)
│  ├─ pyproject.toml
│  ├─ main.py                      # FastAPI app factory
│  ├─ core/
│  │  ├─ settings.py               # đọc env/agent.yaml
│  │  ├─ security.py               # JWT, TLS
│  │  └─ logging_setup.py
│  ├─ routers/
│  │  ├─ ingest.py                 # POST /v1/ingest/*
│  │  ├─ catalog.py                # GET catalogs
│  │  ├─ overrides.py
│  │  └─ health.py                 # GET /v1/healthz
│  ├─ schemas/
│  │  ├─ app_session.py
│  │  ├─ web_session.py
│  │  └─ common.py
│  └─ tests/
│     ├─ test_ingest.py
│     └─ test_health.py
├─ webui/                          # Dashboard (template hoặc React)
│  ├─ fastapi_templates/           # lựa chọn mặc định, nhẹ
│  │  ├─ templates/
│  │  │  ├─ base.html
│  │  │  ├─ dashboard.html
│  │  │  └─ report.html
│  │  └─ static/
│  │     ├─ css/
│  │     └─ js/
│  └─ react/                       # lựa chọn nâng cao (tuỳ chọn triển khai)
│     ├─ package.json
│     ├─ vite.config.ts
│     ├─ src/
│     │  ├─ main.tsx
│     │  ├─ App.tsx
│     │  ├─ components/
│     │  └─ pages/
│     └─ public/
├─ pkg/                            # đóng gói & cài đặt
│  ├─ pyinstaller/
│  │  ├─ service.spec              # build exe/dịch vụ
│  │  └─ tray.spec
│  ├─ wix/                         # WiX Toolset (MSI)
│  │  ├─ Product.wxs
│  │  └─ Bundle.wxs
│  ├─ nsis/                        # NSIS (EXE)
│  │  └─ installer.nsi
│  ├─ signing/
│  │  ├─ sign.ps1                  # ký số
│  │  └─ verify.ps1
│  └─ service/
│     ├─ install_service.ps1
│     └─ uninstall_service.ps1
└─ tests/                          # test tích hợp & e2e
   ├─ integration/
   │  ├─ test_end_to_end.py
   │  ├─ test_upload_retry.py
   │  └─ test_pause_resume.py
   ├─ perf/
   │  └─ test_perf_foreground.py
   └─ fixtures/
```

> Ghi chú: Các thư mục `pyproject.toml` con cho phép **độc lập môi trường** (service/tray/webapi có thể đóng gói riêng). Nếu dùng 1 môi trường chung, giữ dep trong `monorepo/pyproject.toml` và bỏ các file con.

---

## 2) Chuẩn đặt tên & ranh giới import

* **Python package**: snake\_case cho module; PascalCase cho class; UPPER\_CASE cho hằng.
* **Import boundaries**:

  * `service/collectors/*` **không** import ngược `webapi/` hoặc `webui/`.
  * `db/models/*` là lớp dùng chung; `service/storage/*` chỉ thao tác queue cục bộ, không truy cập DB server trực tiếp.
  * `webapi/routers/*` chỉ tương tác DB server, không chạm tệp cục bộ của agent.
* **Schemas**: dùng Pydantic trong `service/schemas.py` và `webapi/schemas/*` (không chéo import; chia sẻ bằng JSON Schema trong `/schema/`).

---

## 3) Cấu hình & bí mật

* `configs/agent.yaml`: tham số runtime (idle\_threshold, poll\_interval, bật/tắt history/etw, retention…).
* `configs/logging.yaml`: formatters/handlers/rotation.
* `configs/browser_selectors.yaml`: danh sách AutomationId/className cho Chrome/Edge/Firefox.
* `configs/secrets.example.env`: biến môi trường (JWT, TLS path, DSN); **không** commit secrets thật.
* **Ưu tiên**: cấu hình qua env > agent.yaml (override). Hot-reload an toàn cho tham số không phá vỡ collector.

---

## 4) Chuẩn build & đóng gói

* **PyInstaller**: spec riêng cho `service` và `tray`. Artefact: `agent_service.exe`, `agent_tray.exe`.
* **WiX** (MSI) & **NSIS** (EXE): cài service auto-start, tạo shortcut Tray, cài cert nếu cần.
* **Ký số**: scripts trong `pkg/signing`.
* **Auto-update**: quy trình tải, verify signature, restart an toàn (ghi trong `scripts/` + tài liệu trong `docs/`).

---

## 5) Tiêu chuẩn test & chất lượng

* **Unit** trong từng package con (`service/tests`, `webapi/tests`, `tray/tests`).
* **Integration/E2E** trong `monorepo/tests`.
* **Lint** bằng ruff/flake8; **type-check** (tuỳ chọn) mypy/pyright.
* **CI**: workflows chia stage (lint → unit → integ → build artefacts → sign/release).

---

## 6) Map thư mục ↔ hạng mục trong Plan/Work\_Flow

* `service/collectors/proc_focus.py` ↔ WBS 4.1; Workflow mục 5.
* `service/collectors/uia_web/` ↔ WBS 4.2; Workflow mục 6.
* `service/collectors/history_backfill.py` ↔ WBS 4.3; Workflow mục 7.
* `service/collectors/etw_domain.py` ↔ WBS 4.4; Workflow mục 8.
* `db/models/*` + `db/migrations/` ↔ WBS 4.5; ERD (Diagram).
* `webapi/routers/*` ↔ WBS 4.6; ingest & quản trị; Health `/v1/healthz`.
* `tray/` ↔ WBS 4.7; Pause/Resume IPC.
* `webui/` ↔ WBS 4.8; báo cáo & export.
* `pkg/` ↔ WBS 4.9; Installer + auto-update.
* `tests/` ↔ WBS 4.10; Integration/Perf; UAT theo Work\_Flow mục 18.

---

## 7) Scaffold tối thiểu (điểm chạm mã nguồn)

* `service/agent_service.py`: lớp `AgentService` kế thừa `win32serviceutil.ServiceFramework` (start/stop/control handler).
* `service/collectors/proc_focus.py`: đăng ký `SetWinEventHook(EVENT_SYSTEM_FOREGROUND)` + map PID → exe + băm SHA-256.
* `service/collectors/uia_web/uia_reader.py`: đọc URL qua UIA (`IUIAutomation`, `ValuePattern`).
* `service/session_aggregator.py`: merge rule (gap<5s), idle rule, overlap guard.
* `service/storage/queue_sqlite.py`: schema queue (app\_sessions/web\_sessions), upsert batch, dedupe theo hash.
* `webapi/main.py`: FastAPI app; mount `routers/ingest.py`, `catalog.py`, `overrides.py`, `health.py`.
* `webui/fastapi_templates/templates/dashboard.html`: bảng tổng thời gian, Top app/domain, heatmap.
* `pkg/service/install_service.ps1`: đăng ký dịch vụ; `uninstall_service.ps1` gỡ bỏ.

---

## 8) Quy ước versioning & changelog

* **SemVer** cho repo tổng thể; release tag `vMAJOR.MINOR.PATCH`.
* `docs/CHANGELOG.md` theo Keep a Changelog; tự động update qua release pipeline.

---

## 9) Hướng dẫn dev nhanh

1. Tạo venv & cài deps: `pip install -e service/ -e webapi/ -e tray/` (hoặc dùng `nox -s setup`).
2. Chạy DB cục bộ & migrations: `python scripts/db_migrate.py upgrade head`.
3. Chạy webapi: `uvicorn webapi.main:app --reload`.
4. Chạy service ở chế độ console: `python service/agent_service.py --debug`.
5. Chạy tray: `python tray/main.py`.
6. Mở dashboard: `http://localhost:8000` (template) hoặc `webui/react` (nếu dùng React).

---

## 10) Bảo mật & tuân thủ trong cấu trúc repo

* `docs/PRIVACY_POLICY.md`, `docs/SECURITY.md`: bắt buộc; liên kết từ Tray/WebUI.
* Không commit secrets; `.gitignore` mẫu cho `*.sqlite`, `*.pfx`, `*.env`.
* `pkg/signing/`: tách biệt khoá ký; chỉ chứa script, không chứa key thật.
* `schema/*.json`: làm chuẩn tham chiếu giữa agent ↔ webapi, giảm lệ thuộc import chéo.

---

## 11) Mở rộng tương lai (đặt chỗ trong repo)

* `collectors/win32_window_metrics.py`: thống kê kích thước/đa màn hình (không thu nội dung).
* `webapi/routers/policy.py`: cấu hình masking URL/title theo domain.
* `webui/pages/policies`: UI quản lý phân loại/overrides.

---

## 12) Checklist hoàn tất cấu trúc

* [ ] Repo root & metainfo (README, LICENSE, Editor/Lint).
* [ ] configs/\* và secrets.example.env.
* [ ] db/models + migrations khởi tạo.
* [ ] service skeleton (service, collectors, storage, aggregator, uploader).
* [ ] tray skeleton + icon.
* [ ] webapi skeleton + OpenAPI.
* [ ] webui template (hoặc React scaffold).
* [ ] pkg (PyInstaller, WiX/NSIS, signing, scripts).
* [ ] tests (unit, integration, perf).
* [ ] CI workflows (lint/test/build/release).
* [ ] Docs (Prompt/Plan/Diagram/Work\_Flow/File\_Structure, Privacy, Security, Changelog).
