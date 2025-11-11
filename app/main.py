import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Solar Analysis Dashboard", layout="wide")

st.title("🌞 Solar Farm Analysis Dashboard")
st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo")

st.markdown(
    "Upload cleaned CSV files to compare solar potential across countries")

# File uploader for all 3 countries
st.sidebar.header(" Upload Cleaned Data Files")

st.sidebar.markdown("Upload your cleaned CSV files:")
benin_file = st.sidebar.file_uploader("Benin Data", type=['csv'], key="benin")
sierra_file = st.sidebar.file_uploader(
    "Sierra Leone Data", type=['csv'], key="sierra")
togo_file = st.sidebar.file_uploader("Togo Data", type=['csv'], key="togo")


@st.cache_data
def load_data(benin_file, sierra_file, togo_file):
    countries_data = []

    if benin_file is not None:
        benin = pd.read_csv(benin_file)
        benin['Country'] = 'Benin'
        countries_data.append(benin)

    if sierra_file is not None:
        sierra = pd.read_csv(sierra_file)
        sierra['Country'] = 'Sierra Leone'
        countries_data.append(sierra)

    if togo_file is not None:
        togo = pd.read_csv(togo_file)
        togo['Country'] = 'Togo'
        countries_data.append(togo)

    if countries_data:
        return pd.concat(countries_data, ignore_index=True)
    else:
        # Return empty dataframe if no files uploaded
        return pd.DataFrame()


# Load data based on uploaded files
df = load_data(benin_file, sierra_file, togo_file)

# Rest of your dashboard code remains the same...
if not df.empty:
    # Your existing visualization code here
    selected_countries = st.sidebar.multiselect(
        "Select Countries:",
        options=df['Country'].unique(),
        default=df['Country'].unique()
    )
    # ... continue with your existing dashboard code

else:
    st.info("👆 Please upload cleaned CSV files in the sidebar to begin analysis")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", width=300)


st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=['Benin', 'Sierra Leone', 'Togo'],
    default=['Benin', 'Sierra Leone', 'Togo']
)

selected_metric = st.sidebar.selectbox(
    "Select Solar Metric:",
    options=['GHI', 'DNI', 'DHI', 'Tamb']
)


filtered_df = df[df['Country'].isin(selected_countries)]

col1, col2, col3 = st.columns(3)
if selected_countries:
    avg_value = filtered_df[selected_metric].mean()
    max_country = filtered_df.groupby(
        'Country')[selected_metric].mean().idxmax()
    max_value = filtered_df.groupby('Country')[selected_metric].mean().max()

    col1.metric("Average", f"{avg_value:.1f}")
    col2.metric("Best Country", max_country)
    col3.metric("Best Value", f"{max_value:.1f}")


st.subheader(f"{selected_metric} Distribution by Country")

if selected_countries:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=filtered_df, x='Country', y=selected_metric, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("Please select at least one country")


st.subheader("Country Rankings")
ranking = df.groupby('Country').agg({
    'GHI': 'mean',
    'DNI': 'mean',
    'DHI': 'mean',
    'Tamb': 'mean'
}).round(1).sort_values('GHI', ascending=False)

st.dataframe(ranking.style.highlight_max(color='lightgreen'))
