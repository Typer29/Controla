# Task 7 — Collector `uia_web`

## Mục tiêu
Ghi URL và title của tab trình duyệt foreground mà không dùng extension.

## Các bước chính
1. Implement `service/collectors/uia_web/uia_reader.py` dùng UIAutomation tìm Address Bar (`Edit`/`ComboBox`) và đọc URL + tab title.
2. Xây dựng `service/collectors/uia_web/selectors.py` và cập nhật `configs/browser_selectors.yaml`.
3. Poll 1–2s hoặc theo sự kiện foreground để gộp `web_session` theo `(browser, URL)`.
4. Fallback: nếu không đọc được URL, lưu domain từ title hoặc chờ ETW.
5. Viết `service/tests/test_uia_reader.py`.

## Tài liệu tham chiếu
- Prompt.md §2
- Plan.md §4.2
- Work_Flow.md §6, Phụ lục A.2
- File_Structure.md §6, §7

## Tiêu chí hoàn thành
- Tỷ lệ lấy URL thành công ≥95% trên Chrome/Edge/Firefox trong thử nghiệm thủ công.
- Unit test `test_uia_reader.py` pass.
