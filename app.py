import streamlit as st

# تنظیمات پایه صفحه برای سازگاری کامل با موبایل
st.set_page_config(
    page_title="کارپرداز | دستیار قانون کار و بیمه",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# استایل اختصاصی راست‌چین (RTL) و فونت استاندارد فارسی
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
    * {
        direction: rtl;
        text-align: right;
        font-family: 'Vazirmatn', sans-serif !important;
    }
    .stTextInput input, .stNumberInput input {
        direction: ltr !important;
        text-align: left !important;
    }
    .result-box {
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ کارپرداز")
st.caption("دستیار هوشمند و محاسباتی قوانین کار و تأمین اجتماعی")

# ساخت تب‌ها برای بخش‌های مختلف اپلیکیشن
tab1, tab2, tab3 = st.tabs(["محاسبه سنوات", "محاسبه عیدی", "استعلام بیمه بیکاری"])

# ==================== تب ۱: سنوات ====================
with tab1:
    st.subheader("محاسبه سنوات پایان کار (ماده ۲۴ قانون کار)")
    st.write("به ازای هر سال کارکرد، معادل یک ماه آخرین حقوق پایه تعلق می‌گیرد.")
    
    salary_sanavat = st.number_input(
        "حقوق پایه ماهانه (تومان):", 
        min_value=0, 
        value=15000000, 
        step=500000,
        key="sanavat_sal"
    )
    days_worked = st.number_input(
        "تعداد روزهای کارکرد در سال جاری:", 
        min_value=1, 
        max_value=366, 
        value=365,
        key="sanavat_days"
    )
    
    if st.button("محاسبه مبلغ سنوات", type="primary", use_container_width=True):
        # فرمول: (حقوق پایه / ۳۰) * ۳۰ * (کارکرد / ۳۶۵)
        daily_rate = salary_sanavat / 30
        sanavat_amount = (daily_rate * 30) * (days_worked / 365)
        
        st.markdown(f"""
        <div class="result-box">
            <b>مبلغ سنوات قابل پرداخت:</b><br>
            <span style="font-size: 22px; color: #15803d;">{int(sanavat_amount):,} تومان</span>
        </div>
        """, unsafe_allow_html=True)

# ==================== تب ۲: عیدی ====================
with tab2:
    st.subheader("محاسبه عیدی و پاداش سالانه")
    st.write("حداقل عیدی ۲ برابر و حداکثر ۳ برابر حداقل دستمزد مصوب سال است.")
    
    salary_eidi = st.number_input(
        "حقوق پایه ماهانه کارگر (تومان):", 
        min_value=0, 
        value=15000000, 
        step=500000,
        key="eidi_sal"
    )
    months_worked = st.slider("تعداد ماه‌های کارکرد در سال:", 1, 12, 12)
    
    if st.button("محاسبه عیدی", type="primary", use_container_width=True):
        # مبنای محاسبه عیدی بر اساس ماه‌های کارکرد
        min_eidi = (salary_eidi * 2) * (months_worked / 12)
        max_eidi = (salary_eidi * 3) * (months_worked / 12)
        
        st.markdown(f"""
        <div class="result-box">
            <b>حداقل عیدی قانونی:</b> {int(min_eidi):,} تومان<br>
            <b>حداکثر سقف عیدی قانونی:</b> {int(max_eidi):,} تومان
        </div>
        """, unsafe_allow_html=True)

# ==================== تب ۳: درخت تصمیم بیمه بیکاری ====================
with tab3:
    st.subheader("بررسی مشمولیت بیمه بیکاری")
    
    q1 = st.radio("علت قطع همکاری چیست؟", [
        "اخراج / اتمام مدت قرارداد موقت",
        "استعفای کارگر",
        "حوادث قهریه (آتش‌سوزی، سیل، زلزله)"
    ])
    
    q2 = st.radio("وضعیت سابقه پرداخت حق بیمه در کارگاه آخر چگونه است؟", [
        "حداقل یک سال سابقه مستمر در آخرین کارگاه دارم",
        "کمتر از یک سال سابقه در کارگاه آخر دارم"
    ])
    
    married = st.checkbox("دارای همسر یا فرزند تحت تکفل هستم")
    
    if st.button("بررسی وضعیت استحقاق", use_container_width=True):
        if q1 == "استعفای کارگر":
            st.error("طبق ماده ۲ قانون بیمه بیکاری، استعفای داوطلبانه مشمول دریافت بیمه بیکاری نمی‌شود.")
        elif q1 == "اخراج / اتمام مدت قرارداد موقت" and q2 == "کمتر از یک سال سابقه در کارگاه آخر دارم":
            st.warning("در قراردادهای موقت، برای بهره‌مندی از بیمه بیکاری معمولاً حداقل ۱ سال سابقه در آخرین کارگاه الزامی است (مگر در موارد خاص با رأی اداره کار).")
        else:
            st.success("شما شرایط اولیه دریافت مقرری بیمه بیکاری را دارید.")
            st.info("نکته مهم: حداکثر ظرف مدت ۳۰ روز از تاریخ بیکاری باید در سامانه جامع روابط کار ثبت دادخواست نمایید.")
