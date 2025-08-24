# Task 2 — Thiết kế schema & DB layer

## Mục tiêu
Xây dựng mô hình dữ liệu và migration cơ sở để lưu `app_sessions` và `web_sessions`.

## Các bước chính
1. Tạo package `db/models/` với các model: `base.py`, `device.py`, `user.py`, `app.py`, `app_session.py`, `web_domain.py`, `web_session.py`, `override.py`, `audit_log.py`.
2. Khởi tạo Alembic trong `db/migrations/` và tạo migration đầu tiên.
3. Soạn `db/queries/reports.sql` và `db/queries/maintenance.sql`.
4. Tạo `db/local_dev.sqlite` (bỏ qua trong git).
5. Cập nhật `schema/*.schema.json` tương ứng.

## Tài liệu tham chiếu
- Prompt.md §3
- Plan.md §4.5, Phụ lục 13.1
- Diagram.md (ERD)
- File_Structure.md §1, §6
- Work_Flow.md §5–6

## Tiêu chí hoàn thành
- Chạy `python scripts/db_migrate.py upgrade head` tạo schema thành công.
- Các model được import bởi service và webapi.
