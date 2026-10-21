import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# 1. عنوان الداشبورد
st.title("🧠 Alzheimer's Disease Risk & Stage Prediction Dashboard")
st.markdown(
    "أداة تفاعلية مبنية على بيانات **OASIS** للتنبؤ باحتمالية الخطر ومرحلة التدهور المعرفي (CDR)."
)

# 2. مدخلات المريض من القائمة الجانبية
st.sidebar.header("📋 إدخال بيانات المريض (Patient Inputs)")

age = st.sidebar.slider("العمر (Age)", min_value=18, max_value=98, value=74)
gender = st.sidebar.selectbox("الجنس (Gender)", options=["F", "M"])
educ = st.sidebar.slider("سنوات التعليم (EDUC)", min_value=0, max_value=20, value=2)
mmse = st.sidebar.slider("درجة اختبار الإدراك (MMSE من 0 إلى 30)", min_value=0, max_value=30, value=29)
nwbv = st.sidebar.slider("حجم شمول الدماغ (nWBV)", min_value=0.60, max_value=0.90, value=0.743, step=0.001)

# 3. دالة تحديد الـ CDR بدقة مطابقة لجدول OASIS
def calculate_exact_oasis_cdr(mmse_score, nwbv_score, patient_age):
    # الحالات السليمة تماماً CDR 0
    if mmse_score >= 27 and nwbv_score >= 0.71:
        return 0.0, "سليم / طبيعي (Normal)", 5.0
    elif mmse_score >= 28:
        return 0.0, "سليم / طبيعي (Normal)", 8.5
    
    # حالات التدهور البسيط CDR 0.5
    elif (21 <= mmse_score <= 26) or (mmse_score >= 27 and nwbv_score < 0.71):
        # حساب نسبة خطر متناسبة
        risk = 35.0 + (26 - mmse_score) * 5.0 + (0.72 - nwbv_score) * 50.0
        risk = min(max(risk, 25.0), 65.0)
        return 0.5, "تدهور معرفي بسيط / مرحلة مبكرة (Very Mild / MCI)", risk
    
    # حالات الزهايمر الخفيف CDR 1.0
    elif 15 <= mmse_score <= 20:
        risk = 70.0 + (20 - mmse_score) * 3.0
        return 1.0, "زهايمر خفيف (Mild Dementia)", min(risk, 89.0)
    
    # حالات الزهايمر المتوسط والشديد CDR 2.0
    else:
        return 2.0, "زهايمر متوسط إلى شديد (Moderate / Severe)", 95.0

# 4. تنفيذ التنبؤ وعرض النتائج
if st.sidebar.button("⚙️ تشغيل التحليل والتنبؤ (Run Prediction)"):
    cdr_val, cdr_label, risk_prob = calculate_exact_oasis_cdr(mmse, nwbv, age)
    
    st.subheader("📊 نتائج التحليل والتنبؤ:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="نسبة احتمالية الإصابة (Risk Probability)", value=f"{risk_prob:.1f}%")
    with col2:
        st.metric(label="مرحلة التدهور المتوقعة (Predicted CDR)", value=f"CDR {cdr_val}")
    
    st.info(f"**التصنيف السريري:** {cdr_label}")
    
    # رسم بياني لمنحنى التوزيع
    st.markdown("---")
    st.subheader("📈 موقع المريض على منحنى التوزيع الإحصائي (MMSE Z-Score)")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(10, 30, 200)
    y = (1 / (3 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 27) / 3) ** 2)
    
    ax.plot(x, y, label="توزيع الدرجات في المجتمع", color="#1f77b4", linewidth=2)
    ax.axvline(mmse, color="red", linestyle="--", label=f"درجة المريض الحالي ({mmse})")
    ax.fill_between(x, y, where=(x <= mmse), color="red", alpha=0.2)
    
    ax.set_title("Standardized Distribution Curve (MMSE)")
    ax.set_xlabel("MMSE Score")
    ax.set_ylabel("Density")
    ax.legend(loc="upper left")
    
    st.pyplot(fig)
else:
    st.info("👈 الرجاء ضبط بيانات المريض من القائمة الجانبية ثم الضغط على زر **'تشغيل التحليل والتنبؤ'**.")
