import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
file_path = 'D:\\INTERNSHIP\\Project2\\Crop Production data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

data['Production'].fillna(data['Production'].mean(), inplace=True)

# Streamlit App
st.set_page_config(page_title='Crop Production Dashboard', layout='wide')
st.title('Crop Production Dashboard')

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #F5F5F5;
        padding: 20px;
    }
    .title {
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .section-title {
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        color: #4CAF50;
        margin-bottom: 10px;
        text-decoration: underline;
    }
    .plot-container {
        background-color: white;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar with data distribution tab
st.sidebar.title('Data Distribution')
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

# Show dataset and summary statistics
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subheader">Dataset</div>', unsafe_allow_html=True)
st.sidebar.dataframe(data.head())
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subheader">Summary Statistics</div>', unsafe_allow_html=True)
st.sidebar.dataframe(data.describe().transpose())
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Year range slider
year_range = st.slider('Year Range', min_value=int(data['Crop_Year'].min()), max_value=int(data['Crop_Year'].max()), value=(2000, 2015))

# Filter data based on year range
filtered_data = data[(data['Crop_Year'] >= year_range[0]) & (data['Crop_Year'] <= year_range[1])]

def plot_total_production_over_time(data):
    crop_production_year = data.groupby('Crop_Year')['Production'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(crop_production_year['Crop_Year'], crop_production_year['Production'], marker='o')
    ax.set_title('Total Crop Production Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Production (tonnes)')
    ax.grid(True)
    return fig

def plot_top_states(data):
    top_states = data.groupby('State_Name')['Production'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(top_states['State_Name'], top_states['Production'])
    ax.set_title('Top 10 States by Crop Production')
    ax.set_xlabel('State')
    ax.set_ylabel('Production (tonnes)')
    ax.set_xticks(range(len(top_states['State_Name'])))
    ax.set_xticklabels(top_states['State_Name'], rotation=90)
    return fig

def plot_total_production_by_season(data):
    seasonal_production = data.groupby('Season')['Production'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(seasonal_production['Season'], seasonal_production['Production'])
    ax.set_title('Total Crop Production by Season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Production (tonnes)')
    return fig

def plot_distribution_of_area(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data['Area'], bins=50, color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Area Cultivated')
    ax.set_xlabel('Area (hectares)')
    ax.set_ylabel('Frequency')
    return fig
# Pie Chart of Production by Season
def plot_pie_chart_season(data):
    seasonal_production = data.groupby('Season')['Production'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(seasonal_production['Production'], labels=seasonal_production['Season'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Crop Production by Season')
    return fig
def plot_average_production_per_year(data):
    average_production_year = data.groupby('Crop_Year')['Production'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(average_production_year['Crop_Year'], average_production_year['Production'], marker='o', color='green')
    ax.set_title('Average Crop Production per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Production (tonnes)')
    ax.grid(True)
    return fig

def plot_top_districts(data):
    top_districts = data.groupby('District_Name')['Production'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(top_districts['District_Name'], top_districts['Production'], color='orange')
    ax.set_title('Top 10 Districts by Crop Production')
    ax.set_xlabel('District')
    ax.set_ylabel('Production (tonnes)')
    ax.set_xticks(range(len(top_districts['District_Name'])))
    ax.set_xticklabels(top_districts['District_Name'], rotation=90)
    return fig

def plot_rice_production_over_time(data):
    rice_production_year = data[data['Crop'] == 'Rice'].groupby('Crop_Year')['Production'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(rice_production_year['Crop_Year'], rice_production_year['Production'], marker='o', color='brown')
    ax.set_title('Rice Production Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Production (tonnes)')
    ax.grid(True)
    return fig

def plot_heatmap(data):
    heatmap_data = data.pivot_table(values='Production', index='State_Name', columns='Crop_Year', aggfunc='sum').fillna(0)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(heatmap_data, cmap='YlGnBu', linecolor='white', linewidths=0.1, ax=ax)
    ax.set_title('Heatmap of Production by State and Year')
    return fig

def plot_stacked_area(data):
    area_data = data.groupby(['Crop_Year', 'Crop'])['Production'].sum().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(6, 4))
    area_data.plot(kind='area', stacked=True, ax=ax)
    ax.set_title('Stacked Area Chart of Crop Production Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Production (tonnes)')
    return fig

def plot_multiple_lines(data):
    area_data = data.groupby(['Crop_Year', 'Crop'])['Production'].sum().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(6, 4))
    area_data.plot(kind='line', ax=ax)
    ax.set_title('Multiple Line Chart of Crop Production Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Production (tonnes)')
    return fig

def plot_scatter_regression(data):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(x='Area', y='Production', data=data, scatter_kws={'alpha':0.5}, ax=ax)
    ax.set_title('Scatter Plot with Regression Line of Area vs Production')
    ax.set_xlabel('Area (hectares)')
    ax.set_ylabel('Production (tonnes)')
    return fig

# Bar Chart of Production by Crop Type
def plot_production_by_crop_type(data):
    crop_production = data.groupby('Crop')['Production'].sum().reset_index().sort_values(by='Production', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(crop_production['Crop'], crop_production['Production'], color='skyblue')
    ax.set_title('Production by Crop Type')
    ax.set_xlabel('Crop Type')
    ax.set_ylabel('Production (tonnes)')
    ax.set_xticklabels(crop_production['Crop'], rotation=90)
    return fig
# Box Plot of Production Distribution
def plot_production_distribution(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Crop', y='Production', data=data, ax=ax)
    ax.set_title('Production Distribution Across Crops')
    ax.set_xlabel('Crop Type')
    ax.set_ylabel('Production (tonnes)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    return fig

# Time Series of Production for Top Crops
def plot_time_series_top_crops(data, top_n=5):
    top_crops = data.groupby('Crop')['Production'].sum().nlargest(top_n).index
    filtered_data = data[data['Crop'].isin(top_crops)]
    fig, ax = plt.subplots(figsize=(10, 6))
    for crop in top_crops:
        crop_data = filtered_data[filtered_data['Crop'] == crop]
        ax.plot(crop_data['Crop_Year'], crop_data['Production'], marker='o', label=crop)
    ax.legend()
    ax.set_title('Time Series of Production for Top Crops')
    ax.set_xlabel('Year')
    ax.set_ylabel('Production (tonnes)')
    ax.grid(True)
    return fig


def plot_yield_distribution(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='Season', y='Production', data=data, ax=ax, scale='width', palette='pastel', linewidth=1.5)
    ax.set_title('Yield Distribution Across Seasons')
    ax.set_xlabel('Season')
    ax.set_ylabel('Yield')
    plt.xticks(rotation=45)
    plt.grid(True)
    return fig


col1, col2 = st.columns(2)

# Column 1
with col1:
    st.markdown('<div class="section-title">Total Crop Production Over Time</div>', unsafe_allow_html=True)
    st.pyplot(plot_total_production_over_time(filtered_data))

    st.markdown('<div class="section-title">Top 10 States by Production</div>', unsafe_allow_html=True)
    st.pyplot(plot_top_states(filtered_data))

    st.markdown('<div class="section-title">Total Production by Season</div>', unsafe_allow_html=True)
    st.pyplot(plot_total_production_by_season(filtered_data))

# Column 2
with col2:
    st.markdown('<div class="section-title">Distribution of Area Cultivated</div>', unsafe_allow_html=True)
    st.pyplot(plot_distribution_of_area(filtered_data))

    st.markdown('<div class="section-title">Production by Season</div>', unsafe_allow_html=True)
    st.pyplot(plot_pie_chart_season(filtered_data))

    st.markdown('<div class="section-title">Average Production per Year</div>', unsafe_allow_html=True)
    st.pyplot(plot_average_production_per_year(filtered_data))

# Second Row
col3, col4 = st.columns(2)

# Column 3
with col3:
    st.markdown('<div class="section-title">Top 10 Districts by Production</div>', unsafe_allow_html=True)
    st.pyplot(plot_top_districts(filtered_data))

    st.markdown('<div class="section-title">Rice Production Over Time</div>', unsafe_allow_html=True)
    st.pyplot(plot_rice_production_over_time(filtered_data))

    st.markdown('<div class="section-title">Production by Crop Type (Bar Chart)</div>', unsafe_allow_html=True)
    st.pyplot(plot_production_by_crop_type(filtered_data))

    st.markdown('<div class="section-title">Production Distribution Across Crops (Box Plot)</div>', unsafe_allow_html=True)
    st.pyplot(plot_production_distribution(filtered_data))

# Column 4
with col4:
    st.markdown('<div class="section-title">Heatmap of Production by State and Year</div>', unsafe_allow_html=True)
    st.pyplot(plot_heatmap(filtered_data))

    st.markdown('<div class="section-title">Stacked Area Chart of Crop Production Over Time</div>', unsafe_allow_html=True)
    st.pyplot(plot_stacked_area(filtered_data))

# Third Row
col5, col6 = st.columns(2)

# Column 5
with col5:
    st.markdown('<div class="section-title">Multiple Line Chart of Crop Production Over Time</div>', unsafe_allow_html=True)
    st.pyplot(plot_multiple_lines(filtered_data))

# Empty column to balance grid
with col6:
    st.markdown('<div class="section-title">Time Series of Production for Top Crops</div>', unsafe_allow_html=True)
    st.pyplot(plot_time_series_top_crops(filtered_data))

# Fourth Row
col7, col8 = st.columns(2)

# Column 7
with col7:
    st.markdown('<div class="section-title">Scatter Plot with Regression Line of Area vs Production</div>', unsafe_allow_html=True)
    st.pyplot(plot_scatter_regression(filtered_data))

# Empty column to balance grid
with col8:
    st.markdown('<div class="section-title">Yield Distribution Across Seasons (Violin Plot)</div>', unsafe_allow_html=True)
    st.pyplot(plot_yield_distribution(filtered_data))
