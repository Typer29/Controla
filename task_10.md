# Task 10 — FastAPI webapi

## Mục tiêu
Cung cấp API ingest và quản trị để đồng bộ dữ liệu.

## Các bước chính
1. Scaffold `webapi/main.py` tạo app FastAPI và mount routers.
2. Tạo `webapi/core/settings.py`, `core/security.py`, `core/logging_setup.py`.
3. Implement routers:
   - `ingest.py` với `POST /v1/ingest/app-sessions` và `POST /v1/ingest/web-sessions`.
   - `catalog.py` với `GET /v1/catalog/apps`, `GET /v1/catalog/domains`.
   - `overrides.py` với `POST/GET /v1/overrides`.
   - `health.py` với `GET /v1/healthz`.
4. Sử dụng SQLAlchemy models và Pydantic schemas; tạo OpenAPI JSON.
5. Viết unit test cho các endpoint chính.

## Tài liệu tham chiếu
- Prompt.md §4
- Plan.md §4.6
- Work_Flow.md §4, §18
- File_Structure.md §1, §6

## Tiêu chí hoàn thành
- `uvicorn webapi.main:app --reload` khởi chạy được.
- Tests webapi pass và OpenAPI schema sinh ra tại `/openapi.json`.
