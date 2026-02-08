import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. LOAD CSS & ICON LIBRARY (FontAwesome)
# ==========================================
st.markdown(
    """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
<style>
    /* Styling Container Utama */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #2c3e50;
        font-weight: 700;
    }
    
    /* Styling Card Metrics Modern */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #4C72B0;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .metric-icon {
        color: #4C72B0;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .metric-label {
        color: #7f8c8d;
        font-size: 14px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #2c3e50;
        font-size: 28px;
        font-weight: 700;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Fungsi Helper untuk Membuat Metric Card dengan Icon
def create_card(icon, label, value, color="#4C72B0"):
    st.markdown(
        f"""
    <div class="metric-card" style="border-left-color: {color};">
        <i class="fa-solid {icon} metric-icon" style="color: {color};"></i>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ==========================================
# 3. DATA LOADING & PREPROCESSING
# ==========================================
@st.cache_data
def load_data():
    """Hybrid Data Loader dengan Mockup Fallback"""
    possible_paths = [
        "day.csv",
        "data/day.csv",
        "../data/day.csv",
        "dashboard/day.csv",
        os.path.join(os.path.dirname(__file__), "day.csv"),
    ]

    df = None
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df["dteday"] = pd.to_datetime(df["dteday"])
                break
            except:
                continue

    if df is None:
        np.random.seed(42)
        dates = pd.date_range(start="2011-01-01", end="2012-12-31", freq="D")
        n = len(dates)
        df = pd.DataFrame(
            {
                "dteday": dates,
                "season": np.random.choice([1, 2, 3, 4], n),
                "yr": [0 if d.year == 2011 else 1 for d in dates],
                "mnth": [d.month for d in dates],
                "holiday": np.random.choice([0, 1], n, p=[0.97, 0.03]),
                "weekday": [d.weekday() for d in dates],
                "workingday": [1 if d.weekday() < 5 else 0 for d in dates],
                "weathersit": np.random.choice([1, 2, 3], n, p=[0.6, 0.3, 0.1]),
                "temp": np.random.uniform(0.1, 0.9, n),
                "atemp": np.random.uniform(0.1, 0.9, n),
                "hum": np.random.uniform(0.3, 0.9, n),
                "windspeed": np.random.uniform(0.0, 0.6, n),
            }
        )
        base = 1000
        df["casual"] = (base * df["temp"] * 4) + np.random.normal(0, 200, n)
        df["casual"] = df.apply(
            lambda x: x["casual"] * 2 if x["workingday"] == 0 else x["casual"] * 0.5,
            axis=1,
        )
        df["registered"] = (base * 3) + (df["yr"] * 1500) + np.random.normal(0, 400, n)
        df["casual"] = df["casual"].abs().astype(int)
        df["registered"] = df["registered"].abs().astype(int)
        df["cnt"] = df["casual"] + df["registered"]
        df["dteday"] = pd.to_datetime(df["dteday"])

    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season_label"] = df["season"].map(season_map)
    weather_map = {
        1: "Clear/Cloudy",
        2: "Mist/Cloudy",
        3: "Light Snow/Rain",
        4: "Heavy Rain/Snow",
    }
    df["weather_label"] = df["weathersit"].map(weather_map)
    return df


raw_df = load_data()

# ==========================================
# 4. SIDEBAR
# ==========================================
with st.sidebar:

    st.markdown("---")

    # Profile menggunakan komponen native Streamlit
    with st.expander("Profil Analis", expanded=True):
        st.write("**Nama:** T.Sofia Chairani")
        st.write("**ID Dicoding:** tsofiachairani")

    st.markdown("---")
    st.subheader("Filter Data")

    min_date = raw_df["dteday"].min()
    max_date = raw_df["dteday"].max()
    date_range = st.date_input(
        "Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    season_filter = st.multiselect(
        "Pilih Musim",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"],
    )

    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    main_df = raw_df[
        (raw_df["dteday"] >= start_date)
        & (raw_df["dteday"] <= end_date)
        & (raw_df["season_label"].isin(season_filter))
    ]

# ==========================================
# 5. MAIN CONTENT
# ==========================================

st.markdown(
    "<h1 class='main-header'>Analisis Tren Peminjaman Sepeda</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "Dashboard interaktif untuk memahami perilaku pengguna sepeda (**Casual vs Registered**) berdasarkan faktor cuaca dan musim."
)
st.markdown("<br>", unsafe_allow_html=True)

# --- KPI CARDS SECTION ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    create_card(
        "fa-bicycle", "Total Peminjaman", f"{main_df['cnt'].sum():,}", "#4C72B0"
    )

with kpi2:
    val = int(main_df[main_df["workingday"] == 0]["casual"].mean())
    create_card("fa-person-walking-luggage", "Avg Peminjam", f"{val:,}", "#DD8452")

with kpi3:
    val = len(main_df[main_df["weathersit"] == 3])
    create_card(
        "fa-cloud-showers-heavy", "Hari Hujan / Salju", f"{val} Hari", "#55A868"
    )

with kpi4:
    try:
        top_season = main_df.groupby("season_label")["cnt"].sum().idxmax()
    except:
        top_season = "-"
    create_card("fa-sun", "Musim Teramai", f"{top_season}", "#C44E52")

st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["Cuaca", "Musim", "Cluster"])

# ==========================================
# TAB 1: WEATHER
# ==========================================
with tab1:
    st.markdown(
        "### Analisis Korelasi",
        unsafe_allow_html=True,
    )
    # Disclaimer Tab Cuaca
    st.caption(
        "ℹ️ Analisis ini difokuskan pada pengguna **Casual** khusus pada hari Weekend."
    )

    weekend_df = main_df[main_df["workingday"] == 0]

    col_chart, col_insight = st.columns([3, 1])

    with col_insight:
        st.info("Pilih faktor cuaca di bawah untuk mengubah visualisasi scatter plot.")
        x_axis = st.radio(
            "Faktor:",
            ["temp", "hum", "windspeed"],
            format_func=lambda x: {
                "temp": "Suhu",
                "hum": "Kelembapan",
                "windspeed": "Kecepatan Angin",
            }[x],
        )

    with col_chart:
        title_dict = {
            "temp": "Suhu",
            "hum": "Kelembapan",
            "windspeed": "Kecepatan Angin",
        }
        fig_weather = px.scatter(
            weekend_df,
            x=x_axis,
            y="casual",
            color="season_label",
            size="cnt",
            hover_data=["dteday", "weather_label"],
            title=f"{title_dict[x_axis]} vs Peminjaman",
            template="plotly_white",
            labels={x_axis: f"{title_dict[x_axis]} (Norm)", "casual": "Peminjaman"},
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        st.plotly_chart(fig_weather, use_container_width=True)

    st.markdown(
        "#### Heatmap Korelasi",
        unsafe_allow_html=True,
    )
    corr_matrix = weekend_df[["temp", "hum", "windspeed", "casual"]].corr()
    fig_corr = px.imshow(
        corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ==========================================
# TAB 2: SEASON
# ==========================================
with tab2:
    st.markdown(
        "### Analisis Musiman",
        unsafe_allow_html=True,
    )

    # Disclaimer Tab Season
    st.caption(
        "ℹ️ Analisis clustering ini dibuat khusus untuk melihat pola peminjaman pengguna **Casual**."
    )

    season_grp = (
        main_df.groupby("season_label")[["casual", "registered"]].mean().reset_index()
    )
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    season_grp["season_label"] = pd.Categorical(
        season_grp["season_label"], categories=season_order, ordered=True
    )
    season_grp = season_grp.sort_values("season_label")
    season_melt = season_grp.melt(
        id_vars="season_label", var_name="Tipe User", value_name="Rata-rata"
    )

    fig_season = px.bar(
        season_melt,
        x="season_label",
        y="Rata-rata",
        color="Tipe User",
        barmode="group",
        template="plotly_white",
        color_discrete_map={"casual": "#DD8452", "registered": "#4C72B0"},
        text_auto=".0f",
    )
    st.plotly_chart(fig_season, use_container_width=True)

    st.success(
        "Insight: Registered user sangat dominan, terutama di musim Fall (Gugur)."
    )

# ==========================================
# TAB 3: CLUSTERING
# ==========================================
with tab3:
    st.markdown(
        "### Segmentasi Cuaca",
        unsafe_allow_html=True,
    )
    # Disclaimer Tab Cluster
    st.caption(
        "ℹ️ Analisis clustering ini dibuat khusus untuk melihat pola peminjaman pengguna **Casual**."
    )

    seg_df = main_df[main_df["workingday"] == 0].copy()
    seg_df["temp_bin"] = pd.cut(
        seg_df["temp"], bins=[0, 0.33, 0.66, 1.0], labels=["Low", "Medium", "High"]
    )
    seg_df["hum_bin"] = pd.cut(
        seg_df["hum"], bins=[0, 0.4, 0.7, 1.0], labels=["Low", "Medium", "High"]
    )
    seg_df["wind_bin"] = pd.cut(
        seg_df["windspeed"], bins=[0, 0.2, 0.4, 1.0], labels=["Low", "Medium", "High"]
    )

    def get_weather_cluster(row):
        if (row["temp_bin"] == "High" or row["temp_bin"] == "Medium") and row[
            "wind_bin"
        ] == "Low":
            return "Perfect Ride"
        elif row["temp_bin"] == "Medium":
            return "Comfortable"
        else:
            return "Challenging"

    seg_df["weather_segment"] = seg_df.apply(get_weather_cluster, axis=1)
    seg_agg = seg_df.groupby("weather_segment")["casual"].mean().reset_index()

    fig_cluster = px.bar(
        seg_agg,
        x="weather_segment",
        y="casual",
        color="weather_segment",
        template="plotly_white",
        color_discrete_map={
            "Challenging": "#C44E52",
            "Comfortable": "#DD8452",
            "Perfect Ride": "#55A868",
        },
        text_auto=".0f",
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

st.markdown("---")
st.caption("© 2026 Bike Sharing Analysis Project")
