# Task 9 — Collector `etw_domain`

## Mục tiêu
Nghe ETW Network để map process ⇄ domain ở mức SNI/host.

## Các bước chính
1. Implement `service/collectors/etw_domain.py` (có thể dùng `krabsetw` hoặc module C# phụ) lắng các provider `Microsoft-Windows-TCPIP`, `WinInet`, `MsQuic`.
2. Parse sự kiện để lấy domain và PID, lưu vào queue ở mức domain (không path).
3. Kết hợp với `web_session` khi UIA/History không có URL.
4. Tùy chọn bật/tắt qua config `features.etw_domain`.
5. Viết test mô phỏng sự kiện ETW.

## Tài liệu tham chiếu
- Prompt.md §2 (ETW Network)
- Plan.md §4.4
- Work_Flow.md §8
- File_Structure.md §6, §7

## Tiêu chí hoàn thành
- Collector ghi nhận được domain cho process khi không đọc được URL.
- Test ETW giả lập pass.
