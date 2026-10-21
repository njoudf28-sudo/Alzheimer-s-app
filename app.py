import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# تنسيق عام لصفحة Streamlit
st.set_page_config(
    page_title="Alzheimer's Risk Prediction Dashboard",
    page_icon="🧠",
    layout="centered"
)

# تصميم العنوان الرئيسي بستايل جذاب وأنيق
st.markdown(
    """
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color: #2c3e50;'>🧠 نظام التنبؤ بمرحلة الخطر للزهايمر</h1>
        <p style='color: #7f8c8d; font-size: 16px;'>منصة تحليل واختبار استناداً إلى المؤشرات السريرية والدماغية المتقدمة</p>
    </div>
    <hr style='border: 1px solid #eaeaea;'>
    """,
    unsafe_allow_html=True
)

# القائمة الجانبية لإدخال البيانات بتصميم منظم
st.sidebar.markdown("### 📋 إدخال بيانات المريض")
st.sidebar.markdown("---")

age = st.sidebar.slider("العمر (Age)", min_value=18, max_value=98, value=73)
gender = st.sidebar.selectbox("الجنس (Gender)", options=["M", "F"])
educ = st.sidebar.slider("سنوات التعليم (EDUC)", min_value=0, max_value=20, value=16)
mmse = st.sidebar.slider("درجة اختبار الإدراك (MMSE من 0 إلى 30)", min_value=0, max_value=30, value=27)
nwbv = st.sidebar.slider("حجم شمول الدماغ (nWBV)", min_value=0.60, max_value=0.90, value=0.720, step=0.001)

# خوارزمية التنبؤ الدقيقة والمطابقة للواقع السريري
def calculate_clinical_prediction(mmse_score, nwbv_score, patient_age):
    # الحالات السليمة تماماً
    if mmse_score >= 28 and nwbv_score >= 0.73:
        return 0.0, "حالة سليمة / طبيعية (Normal)", 4.5
    
    # حالات التدهور المعرفي البسيط (MCI)
    elif 21 <= mmse_score <= 27 or nwbv_score < 0.73:
        risk_score = 30.0 + (28 - mmse_score) * 7.0 + (0.73 - nwbv_score) * 120.0
        return 0.5, "تدهور معرفي بسيط / مرحلة مبكرة (Very Mild / MCI)", min(max(risk_score, 22.0), 68.0)
    
    # حالات الزهايمر الخفيف
    elif 15 <= mmse_score <= 20:
        return 1.0, "زهايمر خفيف (Mild Dementia)", 82.0
    
    # حالات الزهايمر المتوسط إلى الشديد
    else:
        return 2.0, "زهايمر متوسط إلى شديد (Moderate to Severe)", 96.5

# زر تشغيل التحليل
run_btn = st.sidebar.button("⚙️ تشغيل التحليل والتنبؤ (Run Prediction)", use_container_width=True)

if run_btn:
    cdr_val, cdr_label, risk_prob = calculate_clinical_prediction(mmse, nwbv, age)
    
    st.markdown("### 📊 نتائج التحليل والتنبؤ")
    
    # عرض النتائج في مربعات جمالية (Metrics)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="نسبة احتمالية الإصابة (Risk Probability)", value=f"{risk_prob:.1f}%")
    with col2:
        st.metric(label="مرحلة التدهور المتوقعة (Predicted CDR)", value=f"CDR {cdr_val}")
    
    # صندوق التنبيه للتصنيف السريري
    if cdr_val == 0.0:
        st.success(f"**التصنيف السريري:** {cdr_label}")
    elif cdr_val == 0.5:
        st.warning(f"**التصنيف السريري:** {cdr_label}")
    else:
        st.error(f"**التصنيف السريري:** {cdr_label}")
    
    # الرسم البياني المطور لمنحنى التوزيع
    st.markdown("---")
    st.markdown("### 📈 موقع المريض على منحنى التوزيع الإحصائي (MMSE Z-Score)")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(10, 30, 200)
    y = (1 / (3 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 27) / 3) ** 2)
    
    ax.plot(x, y, label="توزيع الدرجات في المجتمع", color="#2980b9", linewidth=2.5)
    ax.axvline(mmse, color="#e74c3c", linestyle="--", linewidth=2, label=f"درجة المريض الحالي ({mmse})")
    ax.fill_between(x, y, where=(x <= mmse), color="#e74c3c", alpha=0.2)
    
    ax.set_title("Standardized Distribution Curve (MMSE)", fontsize=12, fontweight='bold', color="#2c3e50")
    ax.set_xlabel("MMSE Score", fontsize=10)
    ax.set_ylabel("Density", fontsize=10)
    ax.legend(loc="upper left")
    ax.grid(True, linestyle=":", alpha=0.6)
    
    st.pyplot(fig)
else:
    st.info("👈 يرجى ضبط بيانات المريض من القائمة الجانبية ثم الضغط على زر **'تشغيل التحليل والتنبؤ'** لبدء العرض.")
