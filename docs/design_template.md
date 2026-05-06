# Design Template

## Problem

Xây dựng một hệ thống tự động nghiên cứu và tổng hợp thông tin chuyên sâu. Thay vì bắt người dùng tự tra cứu Google và tổng hợp hàng tá bài báo, hệ thống cần nhận một câu hỏi (query), tự động tìm kiếm các tài liệu mới nhất, phân tích đa chiều (tìm ra mâu thuẫn, điểm yếu của tài liệu) và viết một bản báo cáo hoàn chỉnh, khách quan, có trích dẫn nguồn rõ ràng.

## Why multi-agent?

Sử dụng một LLM duy nhất (Single-agent) sẽ gặp nhiều giới hạn:
1. **Quá tải Context**: Prompt phải chứa quá nhiều lệnh (tìm kiếm, trích xuất, phân tích, viết bài), khiến LLM dễ bị mất tập trung (lost in the middle).
2. **Dễ ảo giác (Hallucination)**: Khi ôm đồm quá nhiều việc, AI thường tự bịa thêm thông tin thay vì bám sát vào kết quả tìm kiếm thực tế.
3. **Khó Debug/Kiểm soát**: Rất khó để biết AI đã hiểu sai ở bước nào (lúc phân tích hay lúc viết).

**Multi-agent** giải quyết điều này qua mô hình "chia để trị" (Divide & Conquer). Mỗi Agent đóng một vai trò hẹp, cụ thể (Tìm kiếm, Phân tích, Viết bài), giúp nâng cao chất lượng đầu ra, dễ dàng chèn thêm các bước kiểm duyệt (Critic) và tận dụng tốt nhất thế mạnh của mô hình.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Điều phối luồng công việc | `ResearchState` | Tên Agent tiếp theo | Mắc kẹt ở vòng lặp vô tận (Infinite loop). |
| Researcher | Tìm kiếm và tóm tắt sự kiện | `query`, `max_sources` | `sources`, `research_notes` | Lỗi API tìm kiếm, không tìm thấy tài liệu phù hợp. |
| Analyst | Đánh giá, tìm ra mâu thuẫn/điểm yếu | `research_notes` | `analysis_notes` | Suy diễn hời hợt, bịa đặt thêm thông tin. |
| Writer | Viết báo cáo cuối cùng | `research_notes`, `analysis_notes`| `final_answer` | Bỏ sót trích dẫn (citations), sai văn phong. |

## Shared state

- `request` (ResearchQuery): Đầu vào gốc (câu hỏi, đối tượng độc giả, số lượng nguồn).
- `iteration` (int): Bộ đếm số lượt đã chạy để làm Guardrail chống lặp.
- `route_history` (list[str]): Lịch sử đường đi qua các phòng ban để truy vết (Traceability).
- `sources` (list[SourceDocument]): Dữ liệu thô từ Search API.
- `research_notes` (str): Ghi chú tóm tắt (Fact) của Researcher.
- `analysis_notes` (str): Bài phân tích chuyên sâu của Analyst.
- `final_answer` (str): Báo cáo đầu ra cuối cùng của hệ thống.

## Routing policy

Hệ thống hoạt động theo mô hình **Hub-and-Spoke** (Mạng hình sao) với `Supervisor` ở trung tâm:
1. `Start` ➔ `Supervisor`.
2. Nếu state chưa có `research_notes` ➔ `Supervisor` điều hướng tới ➔ `Researcher` ➔ `Supervisor`.
3. Nếu state chưa có `analysis_notes` ➔ `Supervisor` điều hướng tới ➔ `Analyst` ➔ `Supervisor`.
4. Nếu state chưa có `final_answer` ➔ `Supervisor` điều hướng tới ➔ `Writer` ➔ `Supervisor`.
5. Đã đủ dữ liệu ➔ `Supervisor` trả kết quả `done` (Ngắt luồng).

## Guardrails

- **Max iterations:** Giới hạn 5 vòng lặp, nếu quá sẽ tự động gọi Writer để chốt kết quả, tránh tốn tiền.
- **Timeout:** 15s cho Search API và LLM calls.
- **Retry:** Dùng cơ chế retry mặc định của OpenAI API khi rớt mạng.
- **Fallback:** Nếu Search API (Tavily) lỗi/thiếu key, trả về dữ liệu mẫu (Mock data) thay vì làm sập chương trình.
- **Validation:** Bổ sung chấm điểm tự động bằng thuật toán LLM-as-a-judge trong khâu đánh giá (Benchmark).

## Benchmark plan

- **Query**: "What are the latest advancements in GraphRAG?"
- **Metric đo lường**:
  - `latency_seconds`: Tốc độ phản hồi.
  - `estimated_cost_usd`: Chi phí ước tính (token cost).
  - `quality_score`: Điểm chất lượng đầu ra (1-10) chấm bằng LLM Evaluator.
- **Expected outcome**:
  - **Single-agent (Baseline)**: Phản hồi nhanh, giá rẻ, nhưng nội dung chung chung, thiếu chiều sâu, điểm chất lượng chỉ khoảng 6/10.
  - **Multi-agent**: Thời gian phản hồi lâu hơn, tốn token hơn, nhưng báo cáo cực kỳ chất lượng, có tư duy phản biện, góc nhìn đa chiều, điểm đạt 8-9/10.
