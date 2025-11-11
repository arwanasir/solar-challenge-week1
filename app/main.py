import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Solar Analysis Dashboard", layout="wide")

st.title("🌞 Solar Farm Analysis Dashboard")
st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo")


@st.cache_data
def load_data():
    benin = pd.read_csv('data/benin_clean.csv')
    sierra_leone = pd.read_csv('data/sierraleone_clean.csv')
    togo = pd.read_csv('data/togo_clean.csv')

    benin['Country'] = 'Benin'
    sierra_leone['Country'] = 'Sierra Leone'
    togo['Country'] = 'Togo'

    return pd.concat([benin, sierra_leone, togo], ignore_index=True)


df = load_data()


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
