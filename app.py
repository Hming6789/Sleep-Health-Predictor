import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Sleep Risk Predictor",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH ---
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357abd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        background-color: white;
    }
    .risk-low {
        background-color: #d4edda;
        color: #155724;
        border-left: 5px solid #28a745;
    }
    .risk-medium {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .risk-high {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)


# --- MOCK MODEL & LIME ---
class MockModel:
    def __init__(self):
        self.classes_ = ['Low', 'Medium', 'High']
        
    def predict(self, input_data):
        bmi = input_data.get('bmi', 25)
        age = input_data.get('age', 30)
        sleep_hours = input_data.get('sleep_hours_weekday', 7)
        waist = input_data.get('waist', 80)
        
        risk_score = (bmi - 20) * 1.5 + (age - 30) * 0.2 + (8 - sleep_hours) * 5 + (waist - 70) * 0.3
        
        if risk_score > 35:
            return 'High'
        elif risk_score > 15:
            return 'Medium'
        else:
            return 'Low'

def get_mock_lime_explanation(input_data, prediction):
    if prediction == 'High':
        features = [
            ("BMI ≥ 25 (Thừa cân/Béo phì)", 0.35, "Tăng rủi ro"),
            ("Thời lượng ngủ < 6h", 0.28, "Tăng rủi ro"),
            ("Vòng eo vượt mức chuẩn", 0.18, "Tăng rủi ro"),
            ("Tuổi tác", 0.10, "Tăng rủi ro"),
            ("Tập thể dục thường xuyên", -0.08, "Giảm rủi ro")
        ]
    elif prediction == 'Medium':
        features = [
            ("Thời lượng ngủ không ổn định", 0.22, "Tăng rủi ro"),
            ("BMI ở ngưỡng thừa cân nhẹ", 0.15, "Tăng rủi ro"),
            ("Tần suất ngáy", 0.12, "Tăng rủi ro"),
            ("Tiền sử sức khỏe tốt", -0.15, "Giảm rủi ro"),
            ("Ít sử dụng bia/rượu", -0.10, "Giảm rủi ro")
        ]
    else:
        features = [
            ("Thời lượng ngủ đạt 7-8h", -0.45, "Giảm rủi ro"),
            ("BMI trong khoảng chuẩn (18.5 - 24.9)", -0.30, "Giảm rủi ro"),
            ("Vòng eo nhỏ", -0.15, "Giảm rủi ro"),
            ("Ít/Không có triệu chứng ngáy", -0.12, "Giảm rủi ro"),
            ("Sử dụng ít caffeine", 0.05, "Tăng rủi ro")
        ]
    
    return pd.DataFrame(features, columns=['Đặc trưng', 'Trọng số LIME', 'Loại ảnh hưởng'])

model = MockModel()


# --- SIDEBAR MENU ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3094/3094837.png", width=80)
    st.title("Sleep AI")
    st.markdown("Hệ thống phân tích rủi ro rối loạn giấc ngủ tích hợp XAI.")
    st.markdown("---")
    menu = st.radio("Menu Điều Hướng", [
        "🏠 Giới thiệu dự án", 
        "🔍 Đánh giá rủi ro & XAI"
    ])
    st.markdown("---")
    st.info("⚠️ **Lưu ý y tế:** Kết quả từ hệ thống chỉ mang tính tham khảo học thuật. Không thay thế chẩn đoán y khoa chuyên nghiệp.")


# --- TRANG: GIỚI THIỆU DỰ ÁN ---
if menu == "🏠 Giới thiệu dự án":
    st.title("🌙 Dự đoán Nguy cơ Rối loạn Giấc ngủ bằng Học Máy")
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### 🎯 Mục tiêu dự án
        Hệ thống này ứng dụng các mô hình **Học máy (Machine Learning)** để phân tích dữ liệu lối sống, sinh hoạt và thông tin sức khỏe của cá nhân, từ đó dự báo mức độ rủi ro mắc các chứng rối loạn giấc ngủ.

        """)
        
    with col2:
        st.image("https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
                 caption="Giấc ngủ chất lượng là nền tảng của sức khỏe", use_container_width=True)


# --- TRANG: ĐÁNH GIÁ RỦI RO & XAI ---
elif menu == "🔍 Đánh giá rủi ro & XAI":
    st.title("🔍 Đánh giá Rủi ro Giấc ngủ của bạn")
    st.markdown("Nhập thông tin bên dưới để AI phân tích. Kết quả kèm theo phần giải thích bằng **LIME** sẽ hiển thị ngay sau đó.")
    
    with st.form("prediction_form"):
        st.subheader("📋 1. Thông tin cá nhân & Chỉ số cơ thể")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            age = st.number_input("Tuổi", min_value=18, max_value=100, value=30)
        with col2:
            gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
        with col3:
            weight = st.number_input("Cân nặng (kg)", min_value=30.0, max_value=200.0, value=65.0)
        with col4:
            height = st.number_input("Chiều cao (cm)", min_value=100, max_value=250, value=165)
            
        bmi = round(weight / ((height/100)**2), 1)
        st.caption(f"*Chỉ số BMI dự tính của bạn: **{bmi}***")
        
        st.subheader("🛌 2. Thói quen & Giấc ngủ")
        col5, col6, col7 = st.columns(3)
        with col5:
            sleep_hours_weekday = st.number_input("Thời lượng ngủ ngày thường (giờ)", min_value=2.0, max_value=16.0, value=7.0, step=0.5)
            sleep_hours_weekend = st.number_input("Thời lượng ngủ cuối tuần (giờ)", min_value=2.0, max_value=16.0, value=8.0, step=0.5)
        with col6:
            snore = st.selectbox("Tần suất ngáy", ["Không bao giờ", "Thỉnh thoảng", "Thường xuyên", "Rất thường xuyên"])
            sleepiness = st.selectbox("Buồn ngủ ban ngày", ["Không", "Ít", "Trung bình", "Nhiều"])
        with col7:
            waist = st.number_input("Vòng eo (cm)", min_value=50, max_value=200, value=80)
            drinks = st.number_input("Sử dụng rượu/bia (ly/ngày)", min_value=0, max_value=20, value=0, step=1)
            
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("🚀 Phân tích & Dự đoán ngay")
        
    if submit_btn:
        input_data = {
            'age': age,
            'bmi': bmi,
            'sleep_hours_weekday': sleep_hours_weekday,
            'sleep_hours_weekend': sleep_hours_weekend,
            'waist': waist
        }
        
        with st.spinner("🤖 AI đang xử lý và trích xuất đặc trưng..."):
            time.sleep(1.5) 
            pred = model.predict(input_data)
            
            st.markdown("---")
            st.header("🎯 KẾT QUẢ DỰ ĐOÁN")
            
            # --- 1. Hiển thị Lớp Rủi ro ---
            if pred == 'Low':
                card_class = "risk-low"
                risk_text = "NGUY CƠ THẤP (LOW)"
                advice = "Tình trạng giấc ngủ của bạn tương đối ổn định. Hãy tiếp tục duy trì thói quen ngủ lành mạnh, tập thể dục đều đặn và ăn uống khoa học."
            elif pred == 'Medium':
                card_class = "risk-medium"
                risk_text = "NGUY CƠ TRUNG BÌNH (MEDIUM)"
                advice = "Bạn có một số dấu hiệu cần theo dõi thêm. Nên cân nhắc điều chỉnh thói quen ngủ, giảm thiểu stress và quan tâm hơn đến chất lượng giấc ngủ hàng ngày."
            else:
                card_class = "risk-high"
                risk_text = "NGUY CƠ CAO (HIGH)"
                advice = "Bạn có nhiều dấu hiệu rủi ro liên quan đến rối loạn giấc ngủ. Nên tối ưu hóa môi trường ngủ ngay lập tức và cân nhắc đi thăm khám bác sĩ chuyên khoa."
                
            st.markdown(f"""
            <div class="card {card_class}">
                <h2 style="margin:0; text-align:center;">{risk_text}</h2>
                <p style="text-align:center; font-size: 16px; margin-top: 10px; margin-bottom:0;">{advice}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # --- 2. Giải thích LIME (chỉ văn bản) ---
            st.header("🧠 GIẢI THÍCH MÔ HÌNH (XAI - LIME)")
            st.markdown("Vì sao mô hình lại kết luận bạn thuộc nhóm này? Thuật toán **LIME** bên dưới sẽ đánh giá mức độ đóng góp của từng đặc trưng đầu vào (kéo dự đoán sang rủi ro thấp hay đẩy lên rủi ro cao).")
            
            df_lime = get_mock_lime_explanation(input_data, pred)
            df_lime = df_lime.sort_values(by="Trọng số LIME", ascending=True)
            
            st.markdown("#### Phân tích chi tiết:")
            for index, row in df_lime.iterrows():
                icon = "🔴" if row['Trọng số LIME'] > 0 else "🟢"
                action = "làm tăng nguy cơ" if row['Trọng số LIME'] > 0 else "giúp duy trì nguy cơ thấp"
                st.write(f"{icon} **{row['Đặc trưng']}**: Yếu tố này {action}.")
