# Task 16 — CI/CD & rollout

## Mục tiêu
Thiết lập pipeline CI/CD và triển khai pilot để hoàn tất dự án.

## Các bước chính
1. Tạo workflow GitHub Actions trong `.github/workflows/`:
   - `ci.yml` chạy lint + test.
   - `build.yml` build artefact service/tray/webapi/webui.
   - `release.yml` ký số và tạo bản phát hành.
2. Thiết lập badges trạng thái CI trong README.
3. Thực hiện perf test mô phỏng đổi foreground 5–10 lần/giây trong 15 phút; đảm bảo CPU <2%, RAM <150MB.
4. Triển khai pilot trên 1–2 máy nội bộ, thu thập phản hồi và logs.
5. Đóng gói release `v1.0.0` và cập nhật CHANGELOG.

## Tài liệu tham chiếu
- Prompt.md §9, §10
- Plan.md §§5, 8, 11, 12
- Work_Flow.md §§17–18
- File_Structure.md §1, §5

## Tiêu chí hoàn thành
- CI xanh cho lint/test/build.
- Bản pilot chạy ổn định với chỉ số hiệu năng đạt mục tiêu.
- Release `v1.0.0` được tạo và ghi nhận trong CHANGELOG.
