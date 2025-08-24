# Task 1 — Khởi tạo monorepo & công cụ dev

## Mục tiêu
Thiết lập skeleton monorepo theo File_Structure.md để chuẩn bị môi trường phát triển.

## Các bước chính
1. Tạo cây thư mục và các file meta: `README.md`, `LICENSE`, `.editorconfig`, `.gitignore`, `pyproject.toml`, `ruff.toml`, `pytest.ini`, `noxfile.py` hoặc `tasks.py`, `Makefile`.
2. Thiết lập thư mục `configs/` với `agent.yaml`, `logging.yaml`, `browser_selectors.yaml`, `secrets.example.env`.
3. Khởi tạo `scripts/` gồm `dev.ps1`, `seed_fake_data.py`, `db_migrate.py`, `export_csv.py`, `bench_foreground.py`, `health_check.ps1`.
4. Tạo `schema/` với `app_session.schema.json` và `web_session.schema.json`.
5. Di chuyển các tài liệu dự án hiện tại vào `docs/`.

## Tài liệu tham chiếu
- Prompt.md
- Plan.md §3
- File_Structure.md §1, §9
- Work_Flow.md §0

## Tiêu chí hoàn thành
- Cấu trúc thư mục đúng như mô tả trong File_Structure.md.
- Các file scaffold tồn tại với nội dung placeholder hợp lệ.
- Chạy `ruff` và `pytest` không lỗi (dù chưa có test).
