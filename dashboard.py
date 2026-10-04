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
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .stApp, .main, .block-container { background-color: #0e1117 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label { color: #fafafa; }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] { color: #a0a0a0 !important; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #667eea !important; font-weight: 700; }
    
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
    
    [data-testid="stSidebar"] { background-color: #1a1a2e !important; }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #fafafa !important; }
    
    .stDataFrame { background-color: #262730 !important; }
    
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
    
    .stAlert {
        background-color: #1a365d !important;
        color: #fafafa !important;
        border-left-color: #3182ce !important;
    }
    .stAlert p { color: #fafafa !important; }
    
    hr { border-color: #4a5568 !important; }
    
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stMultiSelect"] > div > div {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: #4a5568 !important;
    }
    div[data-testid="stRadio"] label { color: #fafafa !important; }
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
        path = Path(__file__).parent / "output" / "adventureworks.csv"
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

# --- فلتر القناة ---
channel_filter = st.sidebar.radio(
    "🛒 قناة البيع",
    ["الكل", "أونلاين (B2C)", "مندوبين (B2B)"],
    index=0
)

st.sidebar.markdown("---")

profit_filter = st.sidebar.radio(
    "💹 نوع الصفوف",
    ["الكل", "الرابحة فقط", "الخاسرة فقط", "المخفضة فقط"],
    index=0
)

# --- تطبيق الفلاتر ---
# base: السنة/الفئة/المنطقة فقط — تُستخدم لمقارنات القنوات حتى لا تتأثر
# بفلتر القناة أو بفلتر نوع الصفوف.
base = df[
    (df["OrderYear"].isin(selected_years)) &
    (df["CategoryName"].isin(selected_cats)) &
    (df["TerritoryID"].isin(selected_terr))
].copy()
filtered = base.copy()

# فلتر القناة
if channel_filter == "أونلاين (B2C)":
    filtered = filtered[filtered["OnlineOrderFlag"] == 1]
elif channel_filter == "مندوبين (B2B)":
    filtered = filtered[filtered["OnlineOrderFlag"] == 0]

# فلتر الربحية
if profit_filter == "الرابحة فقط":
    filtered = filtered[filtered["IsProfitable"]]
elif profit_filter == "الخاسرة فقط":
    if "IsLossMaking" in filtered.columns:
        filtered = filtered[filtered["IsLossMaking"]]
    else:
        filtered = filtered[filtered["Profit"] < 0]
elif profit_filter == "المخفضة فقط":
    if "IsDiscounted" in filtered.columns:
        filtered = filtered[filtered["IsDiscounted"]]
    else:
        filtered = filtered[filtered["UnitPriceDiscount"] > 0]



def margin_pct(d):
    """هامش الربح = مجموع الربح ÷ مجموع المبيعات."""
    s = d["LineTotal"].sum()
    return d["Profit"].sum() / s * 100 if s else float("nan")


def channel_summary_text(d):
    """ملخص هامش كل قناة داخل كل منطقة — محسوب من البيانات الحالية."""
    tc = d.groupby(["TerritoryID", "OnlineOrderFlag"]).agg(
        sales=("LineTotal", "sum"), profit=("Profit", "sum")
    ).reset_index()
    tc = tc[tc["sales"] > 0]
    tc["margin"] = tc["profit"] / tc["sales"] * 100
    b2b = tc[tc["OnlineOrderFlag"] == 0]
    b2c = tc[tc["OnlineOrderFlag"] == 1]
    lines = []
    if len(b2b):
        lines.append(
            f"• **مندوبين (B2B)**: هامش سالب في {int((b2b['margin'] < 0).sum())} "
            f"من {len(b2b)} مناطق (من {b2b['margin'].min():.1f}% إلى {b2b['margin'].max():.1f}%)"
        )
    if len(b2c):
        lines.append(
            f"• **أونلاين (B2C)**: هامش بين {b2c['margin'].min():.1f}% "
            f"و{b2c['margin'].max():.1f}% في {len(b2c)} مناطق"
        )
    return "\n\n".join(lines)


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

    if profit_filter in ("الرابحة فقط", "الخاسرة فقط"):
        st.warning(
            "⚠️ فلتر «نوع الصفوف» يختار الصفوف حسب نتيجتها، فتصبح الهوامش "
            "ونسبة الرابحة غير ممثِّلة. استخدمه لاستعراض الصفوف فقط."
        )

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

    # --- تحليل القنوات (تأثير مزيج القناة) ---
    st.subheader("📊 تحليل القنوات (تأثير مزيج القناة)")

    channel_df = base.groupby("OnlineOrderFlag").agg(
        المبيعات=("LineTotal", "sum"),
        الربح=("Profit", "sum"),
        عدد_البيوعات=("SalesOrderDetailID", "count"),
    ).reset_index()

    channel_df["الهامش_%"] = (
        channel_df["الربح"] / channel_df["المبيعات"] * 100
    ).round(2)

    channel_df["القناة"] = channel_df["OnlineOrderFlag"].map({
        0: "مندوبين (B2B)",
        1: "أونلاين (B2C)"
    })

    if len(channel_df) > 0:
        fig_channel = px.bar(
            channel_df, x="القناة", y="الهامش_%",
            title="هامش الربح حسب القناة",
            color="الهامش_%",
            color_continuous_scale="RdYlGn",
            text="الهامش_%",
            template="plotly_dark"
        )
        fig_channel.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig_channel, use_container_width=True)
        st.caption("مقارنة القنوات تتأثر بفلاتر السنة والفئة والمنطقة فقط.")

    st.info(
        "💡 **تأثير مزيج القناة**: الفرق بين المناطق ليس تسعيرًا إقليميًا — "
        "بل فرق بين قنوات البيع (B2B مقابل B2C).\n\n"
        + channel_summary_text(base)
    )

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

    # --- رؤى ذكية (الملخص التنفيذي فقط) ---
    st.markdown("---")
    st.subheader("🤖 رؤى ذكية")

    if len(filtered) > 0:
        insights = []

        # أعلى منطقة
        top_terr = filtered.groupby("TerritoryID")["LineTotal"].sum().idxmax()
        top_terr_pct = (filtered[filtered["TerritoryID"] == top_terr]["LineTotal"].sum() / filtered["LineTotal"].sum() * 100)
        insights.append(f"🗺️ **المنطقة {top_terr}** تقود بـ **{top_terr_pct:.1f}%** من المبيعات")

        # أعلى فئة
        top_cat = filtered.groupby("CategoryName")["LineTotal"].sum().idxmax()
        top_cat_pct = (filtered[filtered["CategoryName"] == top_cat]["LineTotal"].sum() / filtered["LineTotal"].sum() * 100)
        insights.append(f"📦 **{top_cat}** تمثل **{top_cat_pct:.1f}%** من المبيعات")

        # نسبة الخسارة
        loss_pct = (filtered["Profit"] < 0).mean() * 100
        insights.append(f"⚠️ **{loss_pct:.1f}%** من الصفوف خاسرة")

        # أفضل منتج
        top_product = filtered.groupby("ProductName")["LineTotal"].sum().idxmax()
        insights.append(f"🏆 **{top_product}** هو المنتج الأكثر مبيعًا")

        # أفضل سنة
        top_year = filtered.groupby("OrderYear")["LineTotal"].sum().idxmax()
        insights.append(f"📅 **{top_year}** كانت السنة الأفضل مبيعًا")

        for insight in insights:
            st.info(insight)


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
        الصفوف=("SalesOrderDetailID", "count"),
        الخاسرة=("Profit", lambda x: (x < 0).sum()),
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
        st.markdown("### 🔴 مناطق تحتاج تدخل")
        for _, row in loss_terr.iterrows():
            st.error(
                f"📍 المنطقة {int(row['TerritoryID'])} — "
                f"المبيعات: {format_currency(row['المبيعات'])} | "
                f"الخسارة: {format_currency(row['الربح'])} | "
                f"الهامش: {row['هامش_%']}%"
            )

    st.markdown("---")

    # --- العلاقة بين حصة المندوبين والهامش ---
    st.subheader("🔗 حصة المندوبين مقابل هامش المنطقة")

    if len(base) > 0:
        share_df = base.groupby("TerritoryID").agg(
            المبيعات=("LineTotal", "sum"),
            الربح=("Profit", "sum"),
            البنود=("SalesOrderDetailID", "count"),
            بنود_B2B=("OnlineOrderFlag", lambda s: (s == 0).sum()),
        ).reset_index()
        share_df["حصة_B2B_%"] = (share_df["بنود_B2B"] / share_df["البنود"] * 100).round(1)
        share_df["هامش_%"] = (share_df["الربح"] / share_df["المبيعات"] * 100).round(2)
        share_df["المنطقة"] = share_df["TerritoryID"].astype(str)

        fig_scatter = px.scatter(
            share_df, x="حصة_B2B_%", y="هامش_%",
            text="المنطقة", size="المبيعات",
            title="حصة المندوبين مقابل هامش الربح لكل منطقة",
            template="plotly_dark"
        )
        fig_scatter.update_traces(textposition="top center")
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("الحصة محسوبة على عدد بنود البيع، وحجم الدائرة = المبيعات.")

        st.subheader("📋 الهامش % حسب المنطقة والقناة")
        tc = base.groupby(["TerritoryID", "OnlineOrderFlag"]).agg(
            المبيعات=("LineTotal", "sum"),
            الربح=("Profit", "sum"),
        ).reset_index()
        tc["هامش_%"] = (tc["الربح"] / tc["المبيعات"] * 100).round(2)
        tc["القناة"] = tc["OnlineOrderFlag"].map({
            0: "مندوبين (B2B)",
            1: "أونلاين (B2C)"
        })
        pivot = tc.pivot(index="TerritoryID", columns="القناة", values="هامش_%").reset_index()
        st.dataframe(pivot, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- تحليل منتج محدد عبر المناطق والقنوات ---
    st.subheader("🔍 تحليل منتج عبر المناطق والقنوات")
    product_list = sorted(base["ProductName"].unique().tolist())
    if product_list:
        selected_product = st.selectbox("اختر منتجًا:", product_list)
        prod_data = base[base["ProductName"] == selected_product]

        if len(prod_data) > 0:
            by_terr = prod_data.groupby(["TerritoryID", "OnlineOrderFlag"]).agg(
                المبيعات=("LineTotal", "sum"),
                الكمية=("OrderQty", "sum"),
                الربح=("Profit", "sum"),
            ).reset_index()
            by_terr["السعر_الصافي"] = (by_terr["المبيعات"] / by_terr["الكمية"]).round(2)
            by_terr["القناة"] = by_terr["OnlineOrderFlag"].map({
                0: "مندوبين (B2B)",
                1: "أونلاين (B2C)"
            })
            by_terr["المنطقة"] = by_terr["TerritoryID"].astype(str)

            fig = px.bar(
                by_terr, x="المنطقة", y="السعر_الصافي",
                color="القناة", barmode="group",
                title=f"💲 السعر الصافي الموزون حسب المنطقة والقناة — {selected_product}",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("السعر الصافي = LineTotal ÷ OrderQty (موزون بالكمية وبعد الخصم).")

# ============================================================
# 🎯 تبويب 4: التوصيات
# ============================================================
with tab4:
    st.header("🎯 التوصيات والقرارات")

    st.info(
        "**🔍 الاكتشاف الرئيسي (تأثير مزيج القناة)**\n\n"
        "الفرق بين المناطق ليس \"فوضى تسعير\" — بل فرق بين **قنوات البيع**:\n\n"
        + channel_summary_text(base)
    )

    st.markdown("---")
    st.subheader("📊 دليل من البيانات")

    example_product = "Road-250 Black, 44"
    ex = base[base["ProductName"] == example_product]
    if len(ex) > 0:
        ex_t = ex.groupby(["TerritoryID", "OnlineOrderFlag"]).agg(
            البنود=("SalesOrderDetailID", "count"),
            المبيعات=("LineTotal", "sum"),
            الكمية=("OrderQty", "sum"),
            الربح=("Profit", "sum"),
        ).reset_index()
        ex_t["السعر_الصافي"] = (ex_t["المبيعات"] / ex_t["الكمية"]).round(0)
        ex_t["الهامش_%"] = (ex_t["الربح"] / ex_t["المبيعات"] * 100).round(1)
        ex_t["القناة"] = ex_t["OnlineOrderFlag"].map({
            0: "مندوبين (B2B)",
            1: "أونلاين (B2C)"
        })
        ex_t = ex_t[["TerritoryID", "القناة", "البنود", "السعر_الصافي", "الهامش_%"]]
        ex_t = ex_t.sort_values(["TerritoryID", "القناة"])
        st.markdown(f"**مثال: منتج `{example_product}`** — السعر الصافي والهامش لكل منطقة وقناة:")
        st.dataframe(ex_t, use_container_width=True, hide_index=True)
        st.caption("السعر الصافي = LineTotal ÷ OrderQty. قارن القناتين داخل المنطقة نفسها.")
    else:
        st.caption("لا توجد بيانات للمنتج المثال ضمن الفلاتر الحالية.")

    st.markdown("---")
    st.subheader("✅ التوصيات المُحدَّثة")

    recommendations = [
        ("🎯 مراجعة استراتيجية B2B", 
         "هامش المندوبين أقل بكثير من الأونلاين — راجع أسعار الجملة وحدودها الدنيا."),
        
        ("📉 حد أدنى لسعر الجملة", 
         "B2B لا يجب أن يبيع بأقل من التكلفة المعيارية."),
        
        ("🔍 تحليل القناة × المنطقة", 
         "الفرق الظاهر بين المناطق سببه اختلاف القنوات — اعزل القناة قبل الاستنتاج."),
        
        ("🏆 توسيع قناة الأونلاين", 
         "هامش مرتفع (≈40%) — افحص قابلية التوسع، فبنوده صغيرة (قطعة واحدة غالبًا)."),
        
        ("📊 افصل القناة دائمًا", 
         "لتفادي تأثير مزيج القناة — قارن المناطق داخل كل قناة."),
    ]

    for title, desc in recommendations:
        st.success(f"**{title}** — {desc}")

    st.markdown("---")
    st.subheader("💡 ملخص القنوات")
    st.caption("يتأثر بفلاتر السنة والفئة والمنطقة فقط.")

    b2b_df = base[base["OnlineOrderFlag"] == 0]
    b2c_df = base[base["OnlineOrderFlag"] == 1]

    c1, c2, c3 = st.columns(3)
    c1.metric("📉 ربح/خسارة B2B", format_currency(b2b_df["Profit"].sum()) if len(b2b_df) else "—")
    c2.metric("📈 ربح B2C", format_currency(b2c_df["Profit"].sum()) if len(b2c_df) else "—")
    c3.metric("📊 هامش B2B", f"{margin_pct(b2b_df):.2f}%" if len(b2b_df) else "—")


# ============================================================
# 🦶 Footer
# ============================================================
st.markdown("---")
st.caption("🚲 **AdventureWorks Analytics** | Built with ❤️ using Python & Streamlit | البيانات: AdventureWorks 2019")