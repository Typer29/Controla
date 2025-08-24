# Task 8 — Collector `history_backfill`

## Mục tiêu
Backfill URL và thời điểm truy cập từ lịch sử trình duyệt để lấp các khoảng UIA bỏ lỡ.

## Các bước chính
1. Implement `service/collectors/history_backfill.py` sao chép file History SQLite sang thư mục tạm và đọc bảng `urls/visits`.
2. Map các visit với khoảng thời gian foreground để ước lượng `active_seconds` còn thiếu.
3. Cho phép cấu hình chu kỳ (5–10 phút) trong `agent.yaml`.
4. Viết test giả lập file History bị khóa.

## Tài liệu tham chiếu
- Prompt.md §2 (History Backfill)
- Plan.md §4.3
- Work_Flow.md §7
- File_Structure.md §6, §7

## Tiêu chí hoàn thành
- Các URL bỏ lỡ bởi UIA được backfill vào DB cục bộ.
- Unit test history backfill pass.
