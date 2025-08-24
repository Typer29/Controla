# Task 4 — Idle detector & Session aggregator

## Mục tiêu
Ghi nhận trạng thái idle và gộp phiên ứng dụng/web chính xác.

## Các bước chính
1. Implement `service/idle_detector.py` sử dụng `GetLastInputInfo`, đọc ngưỡng từ config.
2. Implement `service/session_aggregator.py` với quy tắc merge (gap<5s), xử lý idle và chống chồng lấn.
3. Viết unit test: `service/tests/test_idle_detector.py`, `service/tests/test_session_aggregator.py`.
4. Tích hợp các module vào `agent_service` và xuất metric đơn giản.

## Tài liệu tham chiếu
- Prompt.md §1
- Plan.md §4.1, §4.2, §9
- Work_Flow.md §§5–6, Phụ lục A.1
- File_Structure.md §7

## Tiêu chí hoàn thành
- `pytest service/tests/test_idle_detector.py service/tests/test_session_aggregator.py` pass.
- Khi idle vượt ngưỡng, phiên đang mở được đóng và không cộng thời gian.
