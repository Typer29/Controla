# Task 3 — Thiết lập skeleton Service & IPC

## Mục tiêu
Tạo Windows Service cơ bản với cấu hình, logging và kênh IPC cho Tray.

## Các bước chính
1. Viết `service/agent_service.py` kế thừa `win32serviceutil.ServiceFramework` (start/stop, control handler, chế độ `--debug`).
2. Xây dựng `service/agent_config.py` đọc `configs/agent.yaml` và biến môi trường.
3. Thêm `service/logging_setup.py` để nạp `configs/logging.yaml`.
4. Tạo `service/ipc.py` làm kênh IPC (named pipe hoặc socket) giữa Service và Tray.
5. Thêm `service/healthcheck.py` cung cấp trạng thái `/v1/healthz` nội bộ.
6. Tạo stub cho `idle_detector.py`, `session_aggregator.py`, `batcher.py`, `uploader.py` (chưa xử lý logic).

## Tài liệu tham chiếu
- Prompt.md §1, §4, §5
- Plan.md §3, §4.1, §4.2
- Work_Flow.md §4
- File_Structure.md §1, §7

## Tiêu chí hoàn thành
- Chạy `python service/agent_service.py --debug` khởi động không lỗi và ghi log "Service started".
