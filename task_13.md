# Task 13 — Packaging & auto-update

## Mục tiêu
Đóng gói service + tray thành bộ cài đặt và hỗ trợ cập nhật an toàn.

## Các bước chính
1. Tạo spec PyInstaller cho `service` và `tray`, sinh `agent_service.exe` và `agent_tray.exe`.
2. Dựng installer (WiX MSI hoặc NSIS EXE) cài service auto-start và tạo shortcut Tray.
3. Thêm scripts ký số trong `pkg/signing/` (sử dụng cert giả trong dev).
4. Implement cơ chế auto-update: tải gói, verify chữ ký, restart an toàn, rollback nếu lỗi.
5. Tài liệu hoá quy trình cài đặt, cập nhật và gỡ bỏ.

## Tài liệu tham chiếu
- Prompt.md §8
- Plan.md §4.9
- Work_Flow.md §9, §12–15
- File_Structure.md §4

## Tiêu chí hoàn thành
- Tạo được installer chạy thử trên Windows và cài service + tray thành công.
- Auto-update thực hiện được với bản giả lập và đảm bảo không mất dữ liệu.
