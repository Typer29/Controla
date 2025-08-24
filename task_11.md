# Task 11 — Tray App

## Mục tiêu
Cung cấp giao diện khay hệ thống minh bạch cho người dùng với khả năng Pause/Resume.

## Các bước chính
1. Implement `tray/main.py` bằng PySide/PyQt hiển thị icon khay và menu.
2. Tạo `tray/ipc_client.py` kết nối đến service qua IPC để điều khiển Pause/Resume và lấy trạng thái.
3. Thêm icon `tray_recording.ico` và `tray_paused.ico` trong `tray/resources/icons/`.
4. Menu gồm: **Pause/Resume**, "Đang ghi gì", "Chính sách & Quyền riêng tư", "Thoát".
5. Viết unit test `tray/tests/test_tray_state.py`.

## Tài liệu tham chiếu
- Prompt.md §5
- Plan.md §4.7
- Work_Flow.md §3, §5, §6
- File_Structure.md §1, §6

## Tiêu chí hoàn thành
- Tray hiển thị icon, chuyển trạng thái Pause/Resume thành công và phản ánh lên service.
- Test tray pass.
