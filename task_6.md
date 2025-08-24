# Task 6 — Collector `proc_focus`

## Mục tiêu
Theo dõi process start/stop và foreground window để tạo `app_sessions`.

## Các bước chính
1. Implement `service/collectors/proc_focus.py` sử dụng `SetWinEventHook(EVENT_SYSTEM_FOREGROUND)` và `psutil`/WMI.
2. Ghi nhận `name`, `exe_path`, `pid`, `publisher` (nếu có), `sha256` file exe.
3. Cập nhật `session_aggregator` khi foreground đổi; lấy mẫu `window_title` định kỳ.
4. Tích hợp kiểm tra idle trước khi mở phiên mới.
5. Viết test mô phỏng sự kiện foreground.

## Tài liệu tham chiếu
- Prompt.md §1
- Plan.md §4.1
- Work_Flow.md §5, Phụ lục A.1
- File_Structure.md §6, §7

## Tiêu chí hoàn thành
- Chạy service, chuyển đổi giữa vài ứng dụng tạo `app_sessions` chính xác, idle không cộng thời gian.
