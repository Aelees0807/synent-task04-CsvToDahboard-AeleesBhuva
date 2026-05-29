"""
Netflix Content Analytics Dashboard - Streamlit
Synent Technologies Data Science Internship - Task 4
Author: Aelees Bhuva
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Netflix branding
st.markdown("""
    <style>
    .main {
        background-color: #f8f8f8;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #E50914 0%, #B20710 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    h1 {
        color: #E50914;
    }
    .stButton>button {
        background-color: #E50914;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #B20710;
    }
    </style>
""", unsafe_allow_html=True)

# Helper Functions
@st.cache_data

def load_data(uploaded_file=None):
    """Load Netflix dataset from uploaded file or default"""
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            # Try to load default file bundled with the app repository
            df = pd.read_csv(r"D:\Internship SEM-4(Synent Infotech)\task-4\netflix_titles.csv")
        
        # Parse dates
        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
            df['year_added'] = df['date_added'].dt.year
            df['month_added'] = df['date_added'].dt.month
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_kpi_card(title, value, delta=None, icon="📊"):
    """Create a custom KPI card"""
    delta_html = ""
    if delta:
        color = "green" if delta > 0 else "red"
        arrow = "↑" if delta > 0 else "↓"
        delta_html = f'<p style="color: {color}; font-size: 16px; margin: 5px 0;">{arrow} {abs(delta):.1f}%</p>'
    
    st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 18px;">{icon} {title}</h3>
            <h1 style="margin: 10px 0; font-size: 36px;">{value}</h1>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def get_download_link(df, filename="data.csv"):
    """Generate download link for dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

# Main App
def main():
    # Header
    st.markdown("""
        <h1 style='text-align: center; color: #E50914; font-size: 48px;'>
            🎬 Netflix Content Analytics Dashboard
        </h1>
        <p style='text-align: center; color: #564d4d; font-size: 18px;'>
            Interactive Data Exploration & Insights
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=200)
    st.sidebar.markdown("## 📂 Data Upload")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload Netflix CSV file",
        type=['csv'],
        help="Upload your Netflix dataset CSV file"
    )
    
    # Load data
    df = load_data(uploaded_file)
    
    if df is None:
        st.warning("⚠️ Please upload a Netflix dataset CSV file to begin analysis.")
        st.info("💡 **Expected columns:** show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description")
        st.stop()
    
    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔍 Filters")
    
    # Content Type Filter
    content_types = ['All'] + list(df['type'].dropna().unique())
    selected_type = st.sidebar.selectbox("Content Type", content_types)
    
    # Year Filter
    if 'year_added' in df.columns:
        min_year = int(df['year_added'].min()) if not df['year_added'].isna().all() else 2008
        max_year = int(df['year_added'].max()) if not df['year_added'].isna().all() else 2021
        year_range = st.sidebar.slider(
            "Year Added",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
    
    # Country Filter
    if 'country' in df.columns:
        countries = ['All'] + sorted([c.strip() for c in df['country'].dropna().unique() if c != 'Unknown'])
        selected_country = st.sidebar.selectbox("Country", countries)
    
    # Apply Filters
    filtered_df = df.copy()
    
    if selected_type != 'All':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    
    if 'year_added' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['year_added'] >= year_range[0]) & 
            (filtered_df['year_added'] <= year_range[1])
        ]
    
    if 'country' in df.columns and selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country'].str.contains(selected_country, na=False)]
    
    # Sidebar Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dataset Info")
    st.sidebar.info(f"""
    **Total Records:** {len(df):,}  
    **Filtered Records:** {len(filtered_df):,}  
    **Columns:** {len(df.columns)}  
    **Date Range:** {df['release_year'].min():.0f} - {df['release_year'].max():.0f}
    """)
    
    # Download button
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Export Data")
    if st.sidebar.button("Download Filtered Data"):
        csv = filtered_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="netflix_filtered.csv">Click to Download</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
    
    # Main Dashboard Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "📈 Trends", 
        "🌍 Geographic", 
        "📋 Data Explorer"
    ])
    
    # TAB 1: OVERVIEW
    with tab1:
        st.markdown("## 📊 Executive Overview")
        
        # KPI Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_titles = len(filtered_df)
            create_kpi_card("Total Titles", f"{total_titles:,}", icon="🎬")
        
        with col2:
            if 'type' in filtered_df.columns:
                movie_count = len(filtered_df[filtered_df['type'] == 'Movie'])
                movie_pct = (movie_count / total_titles * 100) if total_titles > 0 else 0
                create_kpi_card("Movies", f"{movie_count:,}", delta=movie_pct, icon="🎥")
        
        with col3:
            if 'type' in filtered_df.columns:
                tv_count = len(filtered_df[filtered_df['type'] == 'TV Show'])
                tv_pct = (tv_count / total_titles * 100) if total_titles > 0 else 0
                create_kpi_card("TV Shows", f"{tv_count:,}", delta=tv_pct, icon="📺")
        
        with col4:
            if 'country' in filtered_df.columns:
                unique_countries = filtered_df['country'].dropna().nunique()
                create_kpi_card("Countries", f"{unique_countries}", icon="🌍")
        
        st.markdown("---")
        
        # Charts Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎭 Content Type Distribution")
            if 'type' in filtered_df.columns:
                type_counts = filtered_df['type'].value_counts()
                fig = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    color_discrete_sequence=['#E50914', '#221f1f'],
                    hole=0.4
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='white', width=2))
                )
                fig.update_layout(
                    showlegend=True,
                    height=400,
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⭐ Top 10 Genres")
            if 'listed_in' in filtered_df.columns:
                # Split and count genres
                all_genres = filtered_df['listed_in'].str.split(',').explode().str.strip()
                top_genres = all_genres.value_counts().head(10)
                
                fig = px.bar(
                    x=top_genres.values,
                    y=top_genres.index,
                    orientation='h',
                    color=top_genres.values,
                    color_continuous_scale=['#FFB3BA', '#E50914'],
                    labels={'x': 'Count', 'y': 'Genre'}
                )
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(t=30, b=0, l=0, r=0),
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Charts Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Rating Distribution")
            if 'rating' in filtered_df.columns:
                rating_counts = filtered_df['rating'].value_counts().head(10)
                fig = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    color=rating_counts.values,
                    color_continuous_scale='Reds',
                    labels={'x': 'Rating', 'y': 'Count'}
                )
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(t=30, b=0, l=0, r=0)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎬 Movie Duration Distribution")
            if 'type' in filtered_df.columns and 'duration' in filtered_df.columns:
                movies = filtered_df[filtered_df['type'] == 'Movie'].copy()
                if not movies.empty:
                    # Extract duration in minutes
                    movies['duration_min'] = movies['duration'].str.extract('(\d+)').astype(float)
                    
                    fig = px.histogram(
                        movies['duration_min'].dropna(),
                        nbins=30,
                        color_discrete_sequence=['#E50914'],
                        labels={'value': 'Duration (minutes)', 'count': 'Frequency'}
                    )
                    fig.update_layout(
                        showlegend=False,
                        height=400,
                        margin=dict(t=30, b=0, l=0, r=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: TRENDS
    with tab2:
        st.markdown("## 📈 Content Trends Over Time")
        
        # Yearly Trend
        st.markdown("### 📅 Content Added by Year")
        if 'year_added' in filtered_df.columns:
            yearly_data = filtered_df.groupby(['year_added', 'type']).size().reset_index(name='count')
            
            fig = px.line(
                yearly_data,
                x='year_added',
                y='count',
                color='type',
                markers=True,
                color_discrete_map={'Movie': '#E50914', 'TV Show': '#221f1f'},
                labels={'year_added': 'Year', 'count': 'Number of Titles', 'type': 'Content Type'}
            )
            fig.update_layout(
                height=500,
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📆 Monthly Addition Pattern")
            if 'month_added' in filtered_df.columns:
                month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
                
                monthly_counts = filtered_df['month_added'].value_counts().sort_index()
                monthly_data = pd.DataFrame({
                    'Month': [month_names.get(m, str(m)) for m in monthly_counts.index],
                    'Count': monthly_counts.values
                })
                
                fig = px.bar(
                    monthly_data,
                    x='Month',
                    y='Count',
                    color='Count',
                    color_continuous_scale='Reds',
                    labels={'Month': 'Month', 'Count': 'Titles Added'}
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Content by Release Decade")
            if 'release_year' in filtered_df.columns:
                filtered_df['decade'] = (filtered_df['release_year'] // 10) * 10
                decade_counts = filtered_df['decade'].value_counts().sort_index()
                
                fig = px.bar(
                    x=decade_counts.index.astype(str) + 's',
                    y=decade_counts.values,
                    color=decade_counts.values,
                    color_continuous_scale='Reds',
                    labels={'x': 'Decade', 'y': 'Number of Titles'}
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: GEOGRAPHIC
    with tab3:
        st.markdown("## 🌍 Geographic Distribution")
        
        # Top Countries
        st.markdown("### 🏆 Top 15 Content-Producing Countries")
        if 'country' in filtered_df.columns:
            # Split countries and count
            all_countries = filtered_df['country'].str.split(',').explode().str.strip()
            top_countries = all_countries[all_countries != 'Unknown'].value_counts().head(15)
            
            fig = px.bar(
                x=top_countries.values,
                y=top_countries.index,
                orientation='h',
                color=top_countries.values,
                color_continuous_scale=['#FFB3BA', '#E50914'],
                labels={'x': 'Number of Titles', 'y': 'Country'}
            )
            fig.update_layout(
                height=500,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Country Statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Regional Distribution")
            if 'country' in filtered_df.columns:
                # Create regions
                def categorize_region(country):
                    if pd.isna(country):
                        return 'Unknown'
                    country = str(country).lower()
                    if 'united states' in country or 'canada' in country:
                        return 'North America'
                    elif 'india' in country or 'japan' in country or 'south korea' in country or 'china' in country:
                        return 'Asia'
                    elif 'united kingdom' in country or 'france' in country or 'germany' in country or 'spain' in country:
                        return 'Europe'
                    else:
                        return 'Other'
                
                filtered_df['region'] = filtered_df['country'].apply(categorize_region)
                region_counts = filtered_df['region'].value_counts()
                
                fig = px.pie(
                    values=region_counts.values,
                    names=region_counts.index,
                    color_discrete_sequence=px.colors.sequential.Reds,
                    hole=0.4
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Content Type by Region")
            if 'region' in filtered_df.columns and 'type' in filtered_df.columns:
                region_type = pd.crosstab(filtered_df['region'], filtered_df['type'])
                
                fig = go.Figure()
                for col in region_type.columns:
                    fig.add_trace(go.Bar(
                        name=col,
                        x=region_type.index,
                        y=region_type[col],
                        marker_color='#E50914' if col == 'Movie' else '#221f1f'
                    ))
                
                fig.update_layout(
                    barmode='group',
                    height=400,
                    xaxis_title='Region',
                    yaxis_title='Count'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: DATA EXPLORER
    with tab4:
        st.markdown("## 📋 Data Explorer")
        
        # Search functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search in titles, directors, or cast", "")
        with col2:
            rows_to_show = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)
        
        # Apply search
        if search_term:
            mask = (
                filtered_df['title'].str.contains(search_term, case=False, na=False) |
                filtered_df.get('director', pd.Series()).str.contains(search_term, case=False, na=False) |
                filtered_df.get('cast', pd.Series()).str.contains(search_term, case=False, na=False)
            )
            display_df = filtered_df[mask]
        else:
            display_df = filtered_df
        
        # Display data
        st.markdown(f"**Showing {len(display_df):,} records**")
        
        # Select columns to display
        available_cols = display_df.columns.tolist()
        default_cols = ['type', 'title', 'country', 'release_year', 'rating', 'duration']
        display_cols = [col for col in default_cols if col in available_cols]
        
        selected_cols = st.multiselect(
            "Select columns to display",
            available_cols,
            default=display_cols
        )
        
        if selected_cols:
            st.dataframe(
                display_df[selected_cols].head(rows_to_show),
                use_container_width=True,
                height=400
            )
        
        # Summary Statistics
        st.markdown("---")
        st.markdown("### 📊 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Numerical Columns**")
            if 'release_year' in display_df.columns:
                st.write(display_df[['release_year']].describe())
        
        with col2:
            st.markdown("**Categorical Columns**")
            if 'type' in display_df.columns:
                st.write(display_df['type'].value_counts())
        
        with col3:
            st.markdown("**Missing Values**")
            missing = display_df.isnull().sum()
            missing_pct = (missing / len(display_df) * 100).round(2)
            missing_df = pd.DataFrame({
                'Missing': missing,
                'Percentage': missing_pct
            })
            st.write(missing_df[missing_df['Missing'] > 0])
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #564d4d;'>
            <p><strong>Netflix Content Analytics Dashboard</strong></p>
            <p>Synent Technologies Data Science Internship - Task 4</p>
            <p>Created by: Aelees Bhuva | 
            <a href='https://github.com/Aelees0807'>GitHub</a> | 
            <a href='https://linkedin.com/in/aelees-bhuva'>LinkedIn</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()