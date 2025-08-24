# Task 5 — Queue SQLite & uploader

## Mục tiêu
Lưu trữ tạm thời các sự kiện và đồng bộ lên API an toàn.

## Các bước chính
1. Implement `service/storage/queue_sqlite.py` với schema queue và cơ chế dedupe theo hash.
2. Implement `service/storage/retention.py` để xoay DB và áp dụng TTL.
3. Xây dựng `service/batcher.py` gom sự kiện theo `batch.size` và `batch.interval_ms`.
4. Implement `service/uploader.py` sử dụng JWT + TLS, retry/backoff, queue offline khi mất mạng.
5. Viết `service/tests/test_queue_sqlite.py` và test uploader bằng API mock.

## Tài liệu tham chiếu
- Prompt.md §3, §4, §9
- Plan.md §4.5, §9
- Work_Flow.md §§4–8, §18
- File_Structure.md §7

## Tiêu chí hoàn thành
- Unit test queue SQLite pass.
- Service có thể ghi sự kiện vào queue và uploader gửi thành công tới API mock.
