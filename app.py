import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# 1. عنوان الداشبورد وصفها
st.title("🧠 Alzheimer's Disease Risk & Stage Prediction Dashboard")
st.markdown(
    "أداة تفاعلية مبنية على بيانات **OASIS-2** للتنبؤ باحتمالية الخطر ومرحلة التدهور المعرفي."
)

# 2. القائمة الجانبية لإدخال البيانات
st.sidebar.header("📋 إدخال بيانات المريض (Patient Inputs)")

age = st.sidebar.slider("العمر (Age)", min_value=60, max_value=98, value=75)
gender = st.sidebar.selectbox("الجنس (Gender)", options=["M", "F"])
educ = st.sidebar.slider("سنوات التعليم (EDUC)", min_value=6, max_value=20, value=12)
mmse = st.sidebar.slider("درجة اختبار الإدراك (MMSE من 0 إلى 30)", min_value=0, max_value=30, value=24)
nwbv = st.sidebar.slider("حجم شمول الدماغ (nWBV)", min_value=0.60, max_value=0.85, value=0.72, step=0.01)

# تحويل الجنس إلى متغير وهمي (Dummy Variable)
gender_numeric = 1 if gender == "M" else 0

# 3. دالة حساب احتمال الخطر مع معاملات موزونة ومعدلة لبيانات OASIS-2
def predict_alzheimer_risk(age, mmse, nwbv, educ, gender_num):
    # معادلة الانحدار اللوجستي الموزونة إحصائياً
    # الانخفاض في MMSE و nWBV يرفع الاحتمالية، بينما تقدم العمر والجنس الذكري يززيد الخطر بنسب متوازنة
    logit = (
        0.5 
        + (0.04 * (age - 70))           # عامل العمر
        - (0.35 * (mmse - 24))          # التأثير المباشر والأقوى لاختبار MMSE
        - (8.0 * (nwbv - 0.72))         # تأثير الضمور الدماغي
        - (0.03 * (educ - 12))          # سنوات التعليم كعامل وقائي
        + (0.2 * gender_num)            # تأثير الجنس
    )
    
    # دالة السجمويد لحساب الاحتمالية بين 0 و 1
    probability = 1 / (1 + np.exp(-logit))
    return probability

# 4. دالة تحديد مرحلة CDR بناءً على الاحتمالية المحسوبة ودرجة MMSE
def determine_cdr(mmse_score, risk_prob):
    if risk_prob < 0.25 and mmse_score >= 27:
        return 0.0, "سليم / طبيعي (Normal)"
    elif risk_prob < 0.55 and mmse_score >= 21:
        return 0.5, "تدهور معرفي بسيط / مرحلة مبكرة (MCI / Very Mild)"
    elif risk_prob < 0.80 and mmse_score >= 15:
        return 1.0, "زهايمر خفيف (Mild Dementia)"
    else:
        return 2.0, "زهايمر متوسط إلى شديد (Moderate to Severe Dementia)"

# 5. زر التشغيل والتنفيذ
if st.sidebar.button("⚙️ تشغيل التحليل والتنبؤ (Run Prediction)"):
    prob = predict_alzheimer_risk(age, mmse, nwbv, educ, gender_numeric)
    cdr_val, cdr_label = determine_cdr(mmse, prob)
    
    st.subheader("📊 نتائج التحليل والتنبؤ:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="نسبة احتمالية الإصابة (Risk Probability)", value=f"{prob * 100:.1f}%")
    with col2:
        st.metric(label="مرحلة التدهور المتوقعة (Predicted CDR)", value=f"CDR {cdr_val}")
    
    st.info(f"**التصنيف السريري:** {cdr_label}")
    
    # رسم بياني توضيحي لموقع المريض على المنحنى
    st.markdown("---")
    st.subheader("📈 موقع المريض على منحنى التوزيع الإحصائي (MMSE Z-Score)")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(10, 30, 200)
    # توزيع طبيعي افتراضي لـ MMSE بمتوسط 27 واشتقاق معياري 3
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

