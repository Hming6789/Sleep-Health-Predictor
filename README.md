# Sleep Health Predictor

Dự án này là một ứng dụng Web phân tích và dự đoán rủi ro về giấc ngủ dựa trên các yếu tố lối sống. Ứng dụng được xây dựng bằng **Streamlit** và sử dụng tập dữ liệu NHANES (2017-2018).

## 📁 Cấu trúc thư mục

- `app.py`: Mã nguồn chính của ứng dụng giao diện web Streamlit.
- `NHANES_2017_2018_sleep_lifestyle_merged.csv`: Tập dữ liệu về giấc ngủ và lối sống được thu thập từ NHANES 2017-2018.
- `phienban2.ipynb`: Jupyter Notebook chứa quá trình phân tích dữ liệu khám phá (EDA), huấn luyện mô hình và thử nghiệm ban đầu (bao gồm các bước áp dụng XAI - eXplainable AI).

## 🚀 Hướng dẫn cài đặt và chạy ứng dụng

1. **Cài đặt các thư viện cần thiết:**
   Bạn cần cài đặt các thư viện Python như `streamlit`, `pandas`, `numpy`, `scikit-learn`... Có thể sử dụng lệnh sau:
   ```bash
   pip install streamlit pandas numpy scikit-learn
   ```

2. **Chạy ứng dụng:**
   Mở terminal hoặc command prompt, di chuyển đến thư mục chứa dự án và chạy lệnh:
   ```bash
   streamlit run app.py
   ```

3. **Truy cập ứng dụng:**
   Sau khi chạy lệnh, trình duyệt web của bạn sẽ tự động mở ứng dụng tại địa chỉ `http://localhost:8501`.

## 🧠 Phân tích & Mô hình hóa
File `phienban2.ipynb` chứa quá trình huấn luyện và giải thích mô hình AI. Bạn có thể mở file này bằng Jupyter Notebook hoặc VS Code để xem chi tiết cách xử lý dữ liệu và đánh giá các yếu tố ảnh hưởng đến giấc ngủ.
