# Task 14 — Tests & tooling

## Mục tiêu
Thiết lập bộ kiểm thử đầy đủ và công cụ hỗ trợ phát triển.

## Các bước chính
1. Viết unit tests cho các module service, webapi, tray; thêm integration tests trong `tests/`.
2. Tạo script `scripts/seed_fake_data.py` sinh dữ liệu giả và `scripts/bench_foreground.py` benchmark collector.
3. Thiết lập ruff lint và (tuỳ chọn) mypy/pyright type-check.
4. Cập nhật `pytest.ini`, `noxfile.py`/`tasks.py` và `Makefile` để chạy lint+test tự động.

## Tài liệu tham chiếu
- Prompt.md §10
- Plan.md §4.10, §11
- Work_Flow.md §18
- File_Structure.md §5, §9

## Tiêu chí hoàn thành
- Chạy `ruff` và `pytest` trong CI cho toàn bộ repo pass.
- Script sinh dữ liệu giả tạo được dataset mẫu cho dashboard.
