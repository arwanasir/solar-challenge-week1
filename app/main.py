import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import io
from math import radians


st.set_page_config(
    page_title="Solar Farm Analytics",
    page_icon="☀️",
    layout="wide"
)


st.title("☀️ Solar Farm Analytics Dashboard")
st.markdown(
    "Upload your cleaned CSV files to analyze solar potential across countries")


st.sidebar.header(" Upload Data")
st.sidebar.info("Upload your cleaned CSV files for each country")


benin_file = st.sidebar.file_uploader("Benin Data", type=['csv'], key="benin")
sierra_leone_file = st.sidebar.file_uploader(
    "Sierra Leone Data", type=['csv'], key="sierra")
togo_file = st.sidebar.file_uploader("Togo Data", type=['csv'], key="togo")


def load_and_process_file(uploaded_file, country_name):
    """Load and process individual country file"""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df['Country'] = country_name
            return df
        except Exception as e:
            st.error(f"Error loading {country_name} data: {e}")
            return None
    return None


def create_wind_rose(df, wind_speed_col='WS', wind_dir_col='WD'):
    """Create a wind rose plot"""
    if wind_speed_col not in df.columns or wind_dir_col not in df.columns:
        return None

    wind_data = df[[wind_speed_col, wind_dir_col]].dropna()
    if len(wind_data) == 0:
        return None

    fig = px.bar_polar(
        wind_data,
        r=wind_speed_col,
        theta=wind_dir_col,
        template="plotly_white",
        title="Wind Rose - Wind Speed vs Direction",
        color=wind_speed_col,
        color_continuous_scale=px.colors.sequential.Plasma
    )

    return fig


def perform_anova_test(df):
    """Perform ANOVA test on GHI values across countries"""
    if 'GHI' not in df.columns or 'Country' not in df.columns:
        return None

    country_groups = []
    countries = df['Country'].unique()

    for country in countries:
        country_data = df[df['Country'] == country]['GHI'].dropna()
        country_groups.append(country_data)

    if len(country_groups) >= 2:
        f_stat, p_value = stats.f_oneway(*country_groups)
        return f_stat, p_value, countries
    return None


if benin_file and sierra_leone_file and togo_file:
    with st.spinner("Loading and processing data..."):

        benin_df = load_and_process_file(benin_file, "Benin")
        sierra_leone_df = load_and_process_file(
            sierra_leone_file, "Sierra Leone")
        togo_df = load_and_process_file(togo_file, "Togo")

        if all(df is not None for df in [benin_df, sierra_leone_df, togo_df]):
            combined_df = pd.concat(
                [benin_df, sierra_leone_df, togo_df], ignore_index=True)

            st.session_state.combined_df = combined_df
            st.session_state.data_loaded = True

            st.success("✅ All data loaded successfully!")
        else:
            st.error("Failed to load one or more files")


if 'data_loaded' in st.session_state and st.session_state.data_loaded:
    df = st.session_state.combined_df

    st.subheader("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{len(df):,}")

    with col2:
        st.metric("Countries", df['Country'].nunique())

    with col3:
        if 'GHI' in df.columns:
            st.metric("Avg GHI", f"{df['GHI'].mean():.1f} W/m²")

    with col4:
        if 'Tamb' in df.columns:
            st.metric("Avg Temp", f"{df['Tamb'].mean():.1f} °C")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🌞 Solar Radiation", "📈 Advanced Analysis", "🌪️ Wind Analysis", "📋 Data Summary"])

    with tab1:
        st.subheader("Solar Radiation Analysis")

        col1, col2 = st.columns(2)

        with col1:
            if 'GHI' in df.columns:
                fig = px.box(df, x='Country', y='GHI',
                             title="GHI Distribution by Country")
                st.plotly_chart(fig, use_container_width=True)

            if 'DNI' in df.columns:
                fig = px.box(df, x='Country', y='DNI',
                             title="DNI Distribution by Country")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'DHI' in df.columns:
                fig = px.box(df, x='Country', y='DHI',
                             title="DHI Distribution by Country")
                st.plotly_chart(fig, use_container_width=True)

            if all(col in df.columns for col in ['GHI', 'Tamb', 'RH']):
                sample_df = df.sample(min(1000, len(df)))
                fig = px.scatter(sample_df, x='Tamb', y='GHI',
                                 size='RH', color='Country',
                                 title="Bubble Chart: GHI vs Temperature (Bubble Size = RH)",
                                 hover_data=['RH'],
                                 size_max=30)
                st.plotly_chart(fig, use_container_width=True)
            elif all(col in df.columns for col in ['GHI', 'Tamb', 'BP']):
                sample_df = df.sample(min(1000, len(df)))
                fig = px.scatter(sample_df, x='Tamb', y='GHI',
                                 size='BP', color='Country',
                                 title="Bubble Chart: GHI vs Temperature (Bubble Size = BP)",
                                 hover_data=['BP'],
                                 size_max=30)
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Advanced Analysis")

        col1, col2 = st.columns(2)

        with col1:

            if 'Cleaning' in df.columns:
                st.subheader("🧹 Cleaning Impact Analysis")

                if 'ModA' in df.columns or 'ModB' in df.columns:
                    cleaning_effect = df.groupby('Cleaning').agg({
                        'ModA': 'mean' if 'ModA' in df.columns else None,
                        'ModB': 'mean' if 'ModB' in df.columns else None,
                        'GHI': 'mean' if 'GHI' in df.columns else None
                    }).dropna(axis=1, how='all')

                    if not cleaning_effect.empty:
                        st.write(
                            "**Average Sensor Readings by Cleaning Status:**")
                        st.dataframe(cleaning_effect, use_container_width=True)

                        cleaning_effect_reset = cleaning_effect.reset_index()
                        fig = px.bar(cleaning_effect_reset.melt(id_vars='Cleaning'),
                                     x='Cleaning', y='value', color='variable',
                                     title="Sensor Readings Before/After Cleaning",
                                     labels={'Cleaning': 'Cleaning Event (0=No, 1=Yes)', 'value': 'Average Reading'})
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(
                        "No sensor data (ModA/ModB) available for cleaning impact analysis")
            else:
                st.info("No 'Cleaning' column found in dataset")

        with col2:

            st.subheader("📊 Statistical Significance Testing")

            anova_result = perform_anova_test(df)
            if anova_result:
                f_stat, p_value, countries = anova_result

                st.metric("ANOVA F-statistic", f"{f_stat:.4f}")
                st.metric("P-value", f"{p_value:.6f}")

                if p_value < 0.05:
                    st.success(
                        "**Statistically Significant**: GHI differences between countries are significant (p < 0.05)")
                else:
                    st.warning(
                        "**Not Statistically Significant**: No significant GHI differences between countries (p ≥ 0.05)")

                st.write(f"**Countries tested:** {', '.join(countries)}")
            else:
                st.info(
                    "ANOVA test requires 'GHI' and 'Country' columns with sufficient data")

            if 'GHI' in df.columns and 'Country' in df.columns:
                st.subheader("GHI Statistics by Country")
                ghi_stats = df.groupby('Country')['GHI'].agg(
                    ['mean', 'std', 'count']).round(2)
                st.dataframe(ghi_stats, use_container_width=True)

    with tab3:
        st.subheader("Wind Analysis")

        col1, col2 = st.columns(2)

        with col1:

            if all(col in df.columns for col in ['WS', 'WD']):
                st.subheader("🌪️ Wind Rose")
                wind_rose_fig = create_wind_rose(df)
                if wind_rose_fig:
                    st.plotly_chart(wind_rose_fig, use_container_width=True)
                else:
                    st.warning("Insufficient wind data for wind rose")
            else:
                st.info(
                    "Wind rose requires 'WS' (wind speed) and 'WD' (wind direction) columns")

            if 'WS' in df.columns:
                fig = px.histogram(df, x='WS', color='Country',
                                   title="Wind Speed Distribution by Country",
                                   nbins=30)
                st.plotly_chart(fig, use_container_width=True)

        with col2:

            if 'WS' in df.columns:
                st.subheader("Wind Speed Analysis")

                ws_stats = df.groupby('Country')['WS'].agg(
                    ['mean', 'max', 'std']).round(2)
                st.dataframe(ws_stats, use_container_width=True)

                if 'GHI' in df.columns:
                    sample_df = df.sample(min(500, len(df)))
                    fig = px.scatter(sample_df, x='WS', y='GHI', color='Country',
                                     title="Wind Speed vs Solar Radiation (GHI)",
                                     trendline="lowess")
                    st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Data Summary & Recommendations")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Sample Data**")
            st.dataframe(df.head(10), use_container_width=True)

        with col2:
            st.write("**Column Information**")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Non-Null Count': df.count()
            })
            st.dataframe(col_info, use_container_width=True)

            if 'Country' in df.columns:
                st.write("**Records per Country**")
                country_counts = df['Country'].value_counts()
                fig = px.pie(values=country_counts.values, names=country_counts.index,
                             title="Data Distribution by Country")
                st.plotly_chart(fig, use_container_width=True)

        st.subheader("🎯 Strategic Recommendations")

        if 'GHI' in df.columns:
            ghi_ranking = df.groupby('Country')[
                'GHI'].mean().sort_values(ascending=False)
            best_country = ghi_ranking.index[0]
            best_ghi = ghi_ranking.iloc[0]

            st.success(f"""
            **Primary Recommendation**: **{best_country}** shows the highest solar potential with average GHI of **{best_ghi:.1f} W/m²**
            
            **Key Insights**:
            - **Solar Potential**: {best_country} has {best_ghi:.1f} W/m² average GHI
            - **Statistical Significance**: {'Significant differences' if perform_anova_test(df) and perform_anova_test(df)[1] < 0.05 else 'No significant differences'} between countries
            - **Data Quality**: {df['GHI'].isna().sum() if 'GHI' in df.columns else 'N/A'} missing GHI values
            """)

            if 'Cleaning' in df.columns:
                cleaning_freq = df['Cleaning'].value_counts(
                    normalize=True).get(1, 0)
                st.info(
                    f"**Maintenance Insight**: {cleaning_freq:.1%} of records indicate cleaning events")

            if all(col in df.columns for col in ['WS', 'WD']):
                st.info(
                    "**Wind Analysis**: Wind patterns available for site optimization")

else:

    st.info("""
    ### 📋 How to use this dashboard:
    
    1. **Upload your cleaned CSV files** for each country using the file uploaders in the sidebar
    2. **Make sure you have files for all three countries**: Benin, Sierra Leone, and Togo
    3. **The dashboard will automatically load** and analyze the data once all files are uploaded
    
    ### 🔧 Expected CSV format:
    Your CSV files should contain solar measurement data with columns like:
    - `GHI`, `DNI`, `DHI` (solar radiation metrics)
    - `Tamb` (temperature), `RH` (humidity), `WS` (wind speed)
    - `WD` (wind direction), `Cleaning` (maintenance events)
    - `ModA`, `ModB` (sensor readings)
    
    *Note: The dashboard will work with whatever columns your files contain*
    """)
