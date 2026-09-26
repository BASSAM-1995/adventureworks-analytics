# ============================================================
# dashboard.py — AdventureWorks Analytics (Dark Mode)
# لوحة تحليل مبيعات تفاعلية
# التشغيل: streamlit run dashboard.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# ⚙️ إعداد الصفحة
# ============================================================
st.set_page_config(
    page_title="AdventureWorks Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🎨 CSS — Dark Mode Only
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }
    
    /* الخلفية العامة */
    .stApp, .main, .block-container {
        background-color: #0e1117 !important;
    }
    
    /* النصوص */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #fafafa;
    }
    
    /* العناوين الرئيسية */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* بطاقات المقاييس */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] { 
        color: #a0a0a0 !important; 
        font-weight: 600; 
    }
    [data-testid="stMetricValue"] { 
        color: #667eea !important; 
        font-weight: 700; 
    }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #1a1a2e;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        color: #fafafa;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e !important;
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #fafafa !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: #262730 !important;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* صناديق التنبيه */
    .stAlert {
        background-color: #1a365d !important;
        color: #fafafa !important;
        border-left-color: #3182ce !important;
    }
    .stAlert p { color: #fafafa !important; }
    
    /* Dividers */
    hr { border-color: #4a5568 !important; }
    
    /* Selectbox / Multiselect / Radio */
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stMultiSelect"] > div > div {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: #4a5568 !important;
    }
    div[data-testid="stRadio"] label {
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 💰 دالة تنسيق العملة
# ============================================================
def format_currency(value):
    """تحويل الأرقام الكبيرة إلى B/M/K — بدون $"""
    if pd.isna(value) or value == 0:
        return "0"
    abs_val = abs(value)
    if abs_val >= 1e9:
        return f"{value/1e9:.2f}B"
    elif abs_val >= 1e6:
        return f"{value/1e6:.2f}M"
    elif abs_val >= 1e3:
        return f"{value/1e3:.1f}K"
    return f"{value:,.0f}"

# ============================================================
# 📂 تحميل البيانات
# ============================================================
@st.cache_data(ttl=3600)
def load_data():
    try:
        path = Path("output/adventureworks.csv")
        if not path.exists():
            st.error(f"❌ لم يُعثر على الملف: {path}")
            return pd.DataFrame()
        df = pd.read_csv(path)
        df["OrderDate"] = pd.to_datetime(df["OrderDate"])
        return df
    except Exception as e:
        st.error(f"🔥 خطأ في التحميل: {e}")
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.warning("⚠️ لا توجد بيانات — شغّل `ETL.ipynb` أولًا.")
    st.stop()


# ============================================================
# 🔄 زر التحديث
# ============================================================
if st.sidebar.button("🔄 تحديث البيانات", use_container_width=True):
    st.cache_data.clear()
    st.rerun()


# ============================================================
# 🎯 العنوان
# ============================================================
st.markdown('<div class="main-header">🚲 AdventureWorks Analytics</div>', unsafe_allow_html=True)
st.caption(f"📊 {len(df):,} صف | 📅 {df['OrderDate'].min().date()} → {df['OrderDate'].max().date()}")


# ============================================================
# 🎛️ الفلاتر الجانبية
# ============================================================
st.sidebar.markdown("## 🎛️ الفلاتر")

years = sorted(df["OrderYear"].unique().tolist())
selected_years = st.sidebar.multiselect("📅 السنة", years, default=years)

categories = sorted(df["CategoryName"].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect("📦 الفئة", categories, default=categories)

territories = sorted(df["TerritoryID"].unique().tolist())
selected_terr = st.sidebar.multiselect("🗺️ المنطقة", territories, default=territories)

st.sidebar.markdown("---")
profit_filter = st.sidebar.radio(
    "💹 نوع الصفوف",
    ["الكل", "الرابحة فقط", "الترويجية فقط"],
    index=0
)

# --- تطبيق الفلاتر ---
filtered = df[
    (df["OrderYear"].isin(selected_years)) &
    (df["CategoryName"].isin(selected_cats)) &
    (df["TerritoryID"].isin(selected_terr))
].copy()

if profit_filter == "الرابحة فقط":
    filtered = filtered[filtered["IsProfitable"]]
elif profit_filter == "الترويجية فقط":
    filtered = filtered[~filtered["IsProfitable"]]

st.sidebar.markdown("---")
st.sidebar.metric("📊 الصفوف المعروضة", f"{len(filtered):,}")

# --- زر التنزيل ---
if len(filtered) > 0:
    st.sidebar.download_button(
        label="📥 تنزيل البيانات المفلترة",
        data=filtered.to_csv(index=False).encode("utf-8-sig"),
        file_name="adventureworks_filtered.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# 📊 التبويبات
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 الملخص التنفيذي",
    "📦 المنتجات والفئات",
    "🗺️ المناطق",
    "🎯 التوصيات"
])


# ============================================================
# 📊 تبويب 1: الملخص التنفيذي
# ============================================================
with tab1:
    st.header("📊 الملخص التنفيذي")

    # --- KPIs ---
    total_sales = filtered["LineTotal"].sum()
    total_profit = filtered["Profit"].sum()
    margin = (total_profit / total_sales * 100) if total_sales else 0
    orders = filtered["SalesOrderID"].nunique()
    customers = filtered["CustomerID"].nunique()
    qty = filtered["OrderQty"].sum()
    avg_order = total_sales / orders if orders else 0
    profitable_pct = (filtered["IsProfitable"].sum() / len(filtered) * 100) if len(filtered) else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 المبيعات", format_currency(total_sales))
    col2.metric("💵 الربح", format_currency(total_profit))
    col3.metric("📊 هامش الربح", f"{margin:.2f}%")
    col4.metric("🧾 الطلبات", f"{orders:,}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("📦 الكمية", f"{qty:,}")
    col6.metric("👥 العملاء", f"{customers:,}")
    col7.metric("🛒 متوسط الطلب", format_currency(avg_order))
    col8.metric("✅ نسبة الرابحة", f"{profitable_pct:.1f}%")

    st.markdown("---")

    # --- الرسوم البيانية ---
    col_a, col_b = st.columns(2)

    with col_a:
        by_year = filtered.groupby("OrderYear").agg(
            المبيعات=("LineTotal", "sum"),
            الربح=("Profit", "sum")
        ).reset_index()
        fig1 = px.bar(
            by_year, x="OrderYear", y=["المبيعات", "الربح"],
            title="📅 الأداء حسب السنة",
            barmode="group",
            color_discrete_sequence=["#667eea", "#2ecc71"],
            template="plotly_dark"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        by_cat = filtered.groupby("CategoryName")["LineTotal"].sum().reset_index()
        fig2 = px.pie(
            by_cat, values="LineTotal", names="CategoryName",
            title="📦 توزيع المبيعات حسب الفئة",
            hole=0.4,
            template="plotly_dark"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # --- الاتجاه الشهري ---
    monthly = filtered.groupby(["OrderYear", "OrderMonth"]).agg(
        المبيعات=("LineTotal", "sum"),
        الربح=("Profit", "sum")
    ).reset_index()
    monthly["التاريخ"] = pd.to_datetime(
        monthly["OrderYear"].astype(str) + "-" + monthly["OrderMonth"].astype(str) + "-01"
    )

    fig3 = px.line(
        monthly, x="التاريخ", y=["المبيعات", "الربح"],
        title="📈 الاتجاه الشهري للمبيعات والأرباح",
        markers=True,
        color_discrete_sequence=["#667eea", "#2ecc71"],
        template="plotly_dark"
    )
    st.plotly_chart(fig3, use_container_width=True)


# ============================================================
# 📦 تبويب 2: المنتجات والفئات
# ============================================================
with tab2:
    st.header("📦 تحليل المنتجات والفئات")

    # --- أداء الفئات ---
    st.subheader("📊 أداء الفئات")

    cat_perf = filtered.groupby("CategoryName").agg(
        المبيعات=("LineTotal", "sum"),
        الربح=("Profit", "sum"),
        الصفوف=("IsProfitable", "count"),
        الخاسرة=("IsProfitable", lambda x: (~x).sum()),
    ).reset_index()
    cat_perf["هامش_%"] = (cat_perf["الربح"] / cat_perf["المبيعات"] * 100).round(2)
    cat_perf["نسبة_خاسرة_%"] = (cat_perf["الخاسرة"] / cat_perf["الصفوف"] * 100).round(1)
    cat_perf = cat_perf.sort_values("الربح", ascending=False)

    st.dataframe(cat_perf, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- أفضل/أسوأ المنتجات ---
    col_a, col_b = st.columns(2)

    with col_a:
        top_products = (filtered.groupby("ProductName")["LineTotal"]
                        .sum().nlargest(10).reset_index())
        fig = px.bar(
            top_products, x="LineTotal", y="ProductName",
            orientation="h",
            title="🏆 أفضل 10 منتجات",
            color="LineTotal",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        loss_products = (filtered[filtered["Profit"] < 0]
                         .groupby("ProductName")["Profit"]
                         .sum().nsmallest(10).reset_index())
        fig = px.bar(
            loss_products, x="Profit", y="ProductName",
            orientation="h",
            title="⚠️ أكثر 10 منتجات خسارة",
            color="Profit",
            color_continuous_scale="Reds_r",
            template="plotly_dark"
        )
        fig.update_layout(yaxis={"categoryorder": "total descending"}, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 🗺️ تبويب 3: المناطق
# ============================================================
with tab3:
    st.header("🗺️ تحليل المناطق")

    terr_perf = filtered.groupby("TerritoryID").agg(
        المبيعات=("LineTotal", "sum"),
        الربح=("Profit", "sum"),
        العملاء=("CustomerID", "nunique"),
        الطلبات=("SalesOrderID", "nunique"),
    ).reset_index()
    terr_perf["هامش_%"] = (terr_perf["الربح"] / terr_perf["المبيعات"] * 100).round(2)
    terr_perf = terr_perf.sort_values("الربح", ascending=False)

    st.subheader("📊 أداء المناطق")
    st.dataframe(terr_perf, use_container_width=True, hide_index=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.bar(
            terr_perf, x="TerritoryID", y="المبيعات",
            title="💰 المبيعات حسب المنطقة",
            color="الربح",
            color_continuous_scale="RdYlGn",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.bar(
            terr_perf, x="TerritoryID", y="هامش_%",
            title="📊 هامش الربح حسب المنطقة",
            color="هامش_%",
            color_continuous_scale="RdYlGn",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- تنبيهات المناطق الخاسرة ---
    loss_terr = terr_perf[terr_perf["الربح"] < 0]

    if len(loss_terr) > 0:
        st.markdown("### 🔴 مناطق تحتاج تدخل فوري")
        for _, row in loss_terr.iterrows():
            st.error(
                f"📍 المنطقة {int(row['TerritoryID'])} — "
                f"المبيعات: {format_currency(row['المبيعات'])} | "
                f"الخسارة: {format_currency(row['الربح'])} | "
                f"الهامش: {row['هامش_%']}%"
            )

    st.markdown("---")

    # --- تحليل منتج محدد عبر المناطق ---
    st.subheader("🔍 تحليل منتج عبر المناطق")
    product_list = sorted(filtered["ProductName"].unique().tolist())
    if product_list:
        selected_product = st.selectbox("اختر منتجًا:", product_list)
        prod_data = filtered[filtered["ProductName"] == selected_product]

        if len(prod_data) > 0:
            by_terr = prod_data.groupby("TerritoryID").agg(
                متوسط_السعر=("UnitPrice", "mean"),
                الربح=("Profit", "sum"),
            ).reset_index()

            fig = px.bar(
                by_terr, x="TerritoryID", y="متوسط_السعر",
                title=f"💲 متوسط سعر البيع حسب المنطقة — {selected_product}",
                color="الربح",
                color_continuous_scale="RdYlGn",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 🎯 تبويب 4: التوصيات
# ============================================================
with tab4:
    st.header("🎯 التوصيات والقرارات")

    st.info("""
    **🔍 الاكتشاف الرئيسي**
    
    المشكلة ليست في منتج معين — بل في **فوضى التسعير بين المناطق**.
    نفس المنتج يُباع بفروقات سعرية تصل إلى **70%** — بعضها أقل من التكلفة.
    """)

    st.markdown("---")
    st.subheader("📊 دليل من البيانات")

    st.markdown("""
    **مثال: منتج `Road-250 Black, 44`**
    
    | المنطقة | متوسط السعر | النتيجة |
    |:---:|:---:|:---:|
    | 9 | $2,331 | ✅ ربح 33% |
    | 8 | $2,197 | ✅ ربح 28% |
    | 7 | $1,910 | ✅ ربح 5% |
    | 4 | $1,565 | ❌ خسارة -8% |
    | 2 | $1,373 | ❌ خسارة -15% |
    
    **نفس المنتج** — فرق سعر **70%**.
    """)

    st.markdown("---")
    st.subheader("✅ التوصيات")

    recommendations = [
        ("🎯 توحيد سياسة التسعير", "لا يمكن أن يُباع نفس المنتج بفرق 70% بين المناطق."),
        ("📉 حد أدنى للسعر", "لا بيع بأقل من 110% من التكلفة المعيارية."),
        ("🔍 مراجعة عقود المناطق الخاسرة", "المناطق 2، 3، 5 تبيع تحت التكلفة — إعادة تفاوض."),
        ("🏆 نسخ نموذج المنطقة 9", "هامش 32% — الأعلى في كل المناطق. دراسة أسباب نجاحها."),
        ("📅 إدارة موسمية للتخفيضات", "تتركز في يونيو، سبتمبر، ديسمبر — تخطيط مسبق."),
    ]

    for title, desc in recommendations:
        st.success(f"**{title}** — {desc}")

    st.markdown("---")
    st.subheader("💡 القيمة المتوقعة")

    loss_terr = filtered[filtered["Profit"] < 0]
    total_loss = abs(loss_terr["Profit"].sum())

    c1, c2, c3 = st.columns(3)
    c1.metric("📉 الخسائر الحالية", format_currency(total_loss))
    c2.metric("📈 الربح المتوقع", format_currency(total_loss * 1.5))
    c3.metric("🎯 الهامش المستهدف", "10%+")


# ============================================================
# 🤖 رؤى ذكية
# ============================================================
st.markdown("---")
st.subheader("🤖 رؤى ذكية")

if len(filtered) > 0:
    insights = []

    # --- أعلى منطقة ---
    top_terr = filtered.groupby("TerritoryID")["LineTotal"].sum().idxmax()
    top_terr_pct = (filtered[filtered["TerritoryID"] == top_terr]["LineTotal"].sum() / filtered["LineTotal"].sum() * 100)
    insights.append(f"🗺️ **المنطقة {top_terr}** تقود بـ **{top_terr_pct:.1f}%** من المبيعات")

    # --- أعلى فئة ---
    top_cat = filtered.groupby("CategoryName")["LineTotal"].sum().idxmax()
    top_cat_pct = (filtered[filtered["CategoryName"] == top_cat]["LineTotal"].sum() / filtered["LineTotal"].sum() * 100)
    insights.append(f"📦 **{top_cat}** تمثل **{top_cat_pct:.1f}%** من المبيعات")

    # --- نسبة الترويجية ---
    promo_pct = (~filtered["IsProfitable"]).mean() * 100
    insights.append(f"⚠️ **{promo_pct:.1f}%** من الصفوف بعروض ترويجية")

    # --- أفضل منتج ---
    top_product = filtered.groupby("ProductName")["LineTotal"].sum().idxmax()
    insights.append(f"🏆 **{top_product}** هو المنتج الأكثر مبيعًا")

    # --- السنة الأفضل ---
    top_year = filtered.groupby("OrderYear")["LineTotal"].sum().idxmax()
    insights.append(f"📅 **{top_year}** كانت السنة الأفضل مبيعًا")

    for insight in insights:
        st.info(insight)


# ============================================================
# 🦶 Footer
# ============================================================
st.markdown("---")
st.caption("🚲 **AdventureWorks Analytics** | Built with ❤️ using Python & Streamlit | البيانات: AdventureWorks 2019")