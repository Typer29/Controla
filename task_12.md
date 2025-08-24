# Task 12 — Dashboard webui

## Mục tiêu
Hiển thị báo cáo thời gian sử dụng ứng dụng/web và hỗ trợ export CSV.

## Các bước chính
1. Chọn phương án FastAPI template hoặc React; scaffold `webui/` tương ứng.
2. Xây dựng trang dashboard: chọn khoảng thời gian, tổng thời gian ngày/tuần/tháng, Top app/domain, heatmap theo giờ, drill-down session.
3. Thêm bộ lọc theo user/máy và chức năng **Export CSV**.
4. Kết nối tới API để lấy dữ liệu; sử dụng queries trong `db/queries/reports.sql` nếu cần.
5. Viết test giao diện cơ bản (snapshot hoặc integration).

## Tài liệu tham chiếu
- Prompt.md §6
- Plan.md §4.8
- Work_Flow.md §14, §18
- File_Structure.md §6

## Tiêu chí hoàn thành
- Dashboard chạy tại `http://localhost:8000` (template) hoặc trong môi trường React.
- Các báo cáo và export CSV hoạt động đúng dữ liệu mẫu.
