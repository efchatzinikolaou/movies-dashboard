import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from pathlib import Path

# Load datasets
df = pd.read_csv(r'movies-dashboard/04-dashboard/data_dashboard/df_final.csv')
df15 = pd.read_csv(r'movies-dashboard/04-dashboard/data_dashboard/heatmap3.csv')

# Set custom theme for a cleaner design
st.set_page_config(page_title="Film Production Dashboard of IMDb Movie Dataset", page_icon="🎬", layout="wide")

imdb_logo_path = Path(r'04-dashboard/images/IMDB_Logo_2016.png')


# Display the IMDb logo from the local path
st.image(imdb_logo_path, width=200)

# Prepare data for various visualizations
movies_per_year = df.groupby('release_year').agg(
    movie_count=('release_year', 'size'),
    total_revenue=('revenue', 'sum'),
    total_budget=('budget', 'sum'),
    total_profit=('profit', 'sum')
).reset_index()

movies_per_year = movies_per_year.sort_values('release_year')

# Movie measures per year plot
fig1 = px.line(
    movies_per_year,
    x='release_year',
    y='movie_count',
    title='Movies Measures Per Year',
    labels={'release_year': 'Year', 'movie_count': 'Number of Movies'},
    markers=True
)

# Dropdown buttons for different measures
fig1.update_layout(
    updatemenus=[{
        'buttons': [
            {'label': 'Movie Count', 'method': 'update', 'args': [{'y': [movies_per_year['movie_count']]}, {'title': 'Count of Movies Released Per Year'}]},
            {'label': 'Revenue', 'method': 'update', 'args': [{'y': [movies_per_year['total_revenue']]}, {'title': 'Total Revenue Per Year'}]},
            {'label': 'Budget', 'method': 'update', 'args': [{'y': [movies_per_year['total_budget']]}, {'title': 'Total Budget Per Year'}]},
            {'label': 'Profit', 'method': 'update', 'args': [{'y': [movies_per_year['total_profit']]}, {'title': 'Total Profit Per Year'}]}
        ],
        'direction': 'down',
        'showactive': True,
        'x': 0.17,
        'xanchor': 'left',
        'y': 1.15,
        'yanchor': 'top'
    }]
)

fig1.update_layout(
    title_font_size=20,
    plot_bgcolor='white',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Measure')
)

# Layout the dashboard with different sections
st.title('🎬 Film Production and Analytics Dashboard of IMDb Movies')

# Section for the Movie Measures Chart
st.subheader('📊 Movies Measures Per Year')
st.plotly_chart(fig1, use_container_width=True)

# Heatmap visualization
st.subheader('🌍 Production Countries Heatmap')
st.write('This heatmap visualizes the production countries based on id_count.')

heat_data = [[row['latitude'], row['longitude'], row['id_count']] for index, row in df15.iterrows()]
m = folium.Map(location=[df15['latitude'].mean(), df15['longitude'].mean()], zoom_start=2)
HeatMap(heat_data).add_to(m)

folium_static(m, height=600)

# Display bar charts with interactive features
st.header('💡 Top 20 Movies')

# Top 20 Movies by Revenue
top_20_revenue = df[['id_title', 'revenue', 'vote_count']].dropna(subset=['revenue'])
top_20_revenue = top_20_revenue[top_20_revenue['vote_count'] > 1000]
top_20_revenue = top_20_revenue.sort_values(by='revenue', ascending=False).head(20)

fig2 = px.bar(
    top_20_revenue,
    y='id_title',
    x='revenue',
    orientation='h',
    title="Top 20 Movies by Revenue",
    labels={'revenue': 'Revenue', 'id_title': 'Movie Title'},
    color='revenue',
    color_continuous_scale='Viridis',
    hover_data={'id_title': True, 'revenue': True, 'vote_count': False}
)

fig2.update_layout(
    xaxis_title='Revenue',
    yaxis_title='Movie Title',
    yaxis=dict(tickmode='array', tickvals=top_20_revenue['id_title'], autorange='reversed', tickangle=0),
    height=800,
    margin=dict(l=150, r=50, t=50, b=100),
    font=dict(size=12)
)

st.plotly_chart(fig2, use_container_width=True)

# Top 20 Movies by Budget
top_20_budget = df[['id_title', 'budget', 'vote_count']].dropna(subset=['budget'])
top_20_budget = top_20_budget[top_20_budget['vote_count'] > 1000]
top_20_budget = top_20_budget.sort_values(by='budget', ascending=False).head(20)

fig3 = px.bar(
    top_20_budget,
    y='id_title',
    x='budget',
    orientation='h',
    title="Top 20 Movies by Budget",
    labels={'budget': 'Budget', 'id_title': 'Movie Title'},
    color='budget',
    color_continuous_scale='Viridis',
    hover_data={'id_title': True, 'budget': True, 'vote_count': False}
)

fig3.update_layout(
    xaxis_title='Budget',
    yaxis_title='Movie Title',
    yaxis=dict(tickmode='array', tickvals=top_20_budget['id_title'], autorange='reversed', tickangle=0),
    height=800,
    margin=dict(l=150, r=50, t=50, b=100),
    font=dict(size=12)
)

st.plotly_chart(fig3, use_container_width=True)

# Top 20 Movies by Profit
top_20_profit = df[['id_title', 'profit', 'vote_count']].dropna(subset=['profit'])
top_20_profit = top_20_profit[top_20_profit['vote_count'] > 1000]
top_20_profit = top_20_profit.sort_values(by='profit', ascending=False).head(20)

fig4 = px.bar(
    top_20_profit,
    y='id_title',
    x='profit',
    orientation='h',
    title="Top 20 Movies by Profit",
    labels={'profit': 'Profit', 'id_title': 'Movie Title'},
    color='profit',
    color_continuous_scale='Viridis',
    hover_data={'id_title': True, 'profit': True, 'vote_count': False}
)

fig4.update_layout(
    xaxis_title='Profit',
    yaxis_title='Movie Title',
    yaxis=dict(tickmode='array', tickvals=top_20_profit['id_title'], autorange='reversed', tickangle=0),
    height=800,
    margin=dict(l=150, r=50, t=50, b=100),
    font=dict(size=12)
)

st.plotly_chart(fig4, use_container_width=True)


top_20_avg_vote = df[['id_title', 'vote_average', 'vote_count']].dropna(subset=['vote_average'])

# Filter for movies with more than 1000 votes
top_20_avg_vote = top_20_avg_vote[top_20_avg_vote['vote_count'] > 1000]

# Sort by Average Vote
top_20_avg_vote = top_20_avg_vote.sort_values(by='vote_average', ascending=False).head(20)

# Create the horizontal bar plot for Average Vote with more space for titles
fig5 = px.bar(
    top_20_avg_vote,
    y='id_title',
    x='vote_average',
    orientation='h',
    title="Top 20 Movies by Average Vote",
    labels={'vote_average': 'Average Vote', 'id_title': 'Movie Title'},
    color='vote_average',
    color_continuous_scale='Viridis',
    hover_data={'id_title': True, 'vote_average': True, 'vote_count': False}
)

# Reverse the y-axis
fig5.update_layout(
    xaxis_title='Average Vote',
    yaxis_title='Movie Title',
    yaxis=dict(
        tickmode='array',
        tickvals=top_20_avg_vote['id_title'],
        autorange='reversed',
        tickangle=0  # Ensure labels are horizontal
    ),
    showlegend=False,
    coloraxis_colorbar=dict(title='', tickvals=[], ticks=''),
    height=800,  # Increase height for more space
    margin=dict(l=150, r=50, t=50, b=100),  # Increase left margin
    font=dict(size=12)  # Adjust font size if needed
)

# Streamlit dashboard layout
col1, col2 = st.columns(2)

# Display the Average Vote plot in the first column
with col1:
    st.subheader('Top 20 Movies by Average Vote')
    st.plotly_chart(fig5)

# df2 for production companies processing
df2 = df.copy()
df2['production_companies'] = df2['production_companies'].str.split(',')
df2 = df2.explode('production_companies')
df2['production_companies'] = df2['production_companies'].str.strip()

# Function to generate the plot with filters for the chosen measure for production companies
def create_production_company_filtered_plot():
    # Get the top 10 production companies by revenue
    top_10_companies_revenue = df2.groupby('production_companies')['revenue'].sum().reset_index()
    top_10_companies_revenue = top_10_companies_revenue.sort_values(by='revenue', ascending=False).head(10)

    # Get the count for top 10 production companies (directly from the DataFrame)
    top_10_companies_revenue['count'] = top_10_companies_revenue['production_companies'].map(
        lambda x: df2[df2['production_companies'] == x]['id_title'].notna().sum()
    )

    # Create the initial plot for 'count'
    fig6 = px.bar(
        top_10_companies_revenue,
        x='production_companies',
        y='count',
        title="Top 10 Production Companies by Count",
        labels={'production_companies': 'Production Company', 'y': 'Count'},
        color='count',
        color_continuous_scale='Viridis',
        hover_data={'production_companies': True, 'count': True}
    )

    # Define the button actions for filtering by different measures
    fig6.update_layout(
        updatemenus=[{
            'buttons': [
                {'label': 'Count', 'method': 'update', 'args': [
                    {'x': [top_10_companies_revenue['production_companies']],'y': [top_10_companies_revenue['count']]},
                    {'title': 'Top 10 Production Companies by Count',
                     'xaxis': {'title': 'Production Company'},
                     'yaxis': {'title': 'Count'}}
                ]},
                {'label': 'Revenue', 'method': 'update', 'args': [
                    {'x': [top_10_companies_revenue['production_companies']],'y': [top_10_companies_revenue['revenue']]},
                    {'title': 'Top 10 Production Companies by Revenue',
                     'xaxis': {'title': 'Production Company'},
                     'yaxis': {'title': 'Revenue'}}
                ]},
                {'label': 'Budget', 'method': 'update', 'args': [
                    {'x': [top_10_companies_revenue['production_companies']],
                     'y': [top_10_companies_revenue['production_companies'].map(
                         lambda x: df2[df2['production_companies'] == x]['budget'].sum()
                     )]},
                    {'title': 'Top 10 Production Companies by Budget',
                     'xaxis': {'title': 'Production Company'},
                     'yaxis': {'title': 'Budget'}}
                ]},
                {'label': 'Profit', 'method': 'update', 'args': [
                    {'x': [top_10_companies_revenue['production_companies']],
                     'y': [top_10_companies_revenue['production_companies'].map(
                         lambda x: df2[df2['production_companies'] == x]['profit'].sum()
                     )]},
                    {'title': 'Top 10 Production Companies by Profit',
                     'xaxis': {'title': 'Production Company'},
                     'yaxis': {'title': 'Profit'}}
                ]}
            ],
            'direction': 'down',
            'showactive': True,
            'active': 0,
            'x': 0.17,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }],
        coloraxis_showscale=False,  # Remove the color scale bar
        yaxis=dict(tickangle=45),
        height=600,
        margin=dict(l=150, r=50, t=50, b=150)
    )

    # Show the plot
    st.plotly_chart(fig6)

# Call the function to create the plot with the dropdown filter for production companies
with col2:
    st.subheader('Top 10 Production Companies')
    create_production_company_filtered_plot()

# df3 for genres processing
df3 = df.copy()
df3['genres'] = df3['genres'].str.split(',')
df3 = df3.explode('genres')
df3['genres'] = df3['genres'].str.strip()

# Function to generate the plot with filters for the chosen measure for genres
def create_genre_filtered_plot():
    # Get the top 10 genres by count
    top_10_genres = df3['genres'].value_counts().reset_index()
    top_10_genres.columns = ['genre', 'count']
    top_10_genres = top_10_genres.head(10)

    # Create the initial plot for 'count'
    fig7 = px.bar(
        top_10_genres,
        x='genre',
        y='count',
        title="Top 10 Genres by Count",
        labels={'count': '', 'genre': 'Genre'},
        color='count',
        color_continuous_scale='Viridis',
        hover_data={'genre': True, 'count': True}
    )

    # Define the button actions for filtering by different measures
    fig7.update_layout(
        updatemenus=[{
            'buttons': [
                {'label': 'Count', 'method': 'update', 'args': [
                    {'x': [top_10_genres['genre']],'y': [top_10_genres['count']]},
                    {'title': 'Top 10 Genres by Count',
                     'xaxis': {'title': 'Genre'},
                     'yaxis': {'title': 'Count'}}
                ]},
                {'label': 'Revenue', 'method': 'update', 'args': [
                    {'x': [top_10_genres['genre']],'y': [top_10_genres['genre'].map(lambda x: df3[df3['genres'] == x]['revenue'].sum())]},
                    {'title': 'Top 10 Genres by Revenue',
                     'xaxis': {'title': 'Genre'},
                     'yaxis': {'title': 'Revenue'}}
                ]},
                {'label': 'Budget', 'method': 'update', 'args': [
                    {'x': [top_10_genres['genre']],'y': [top_10_genres['genre'].map(lambda x: df3[df3['genres'] == x]['budget'].sum())]},
                    {'title': 'Top 10 Genres by Budget',
                     'xaxis': {'title': 'Genre'},
                     'yaxis': {'title': 'Budget'}}
                ]},
                {'label': 'Profit', 'method': 'update', 'args': [
                    {'x': [top_10_genres['genre']],'y': [top_10_genres['genre'].map(lambda x: df3[df3['genres'] == x]['profit'].sum())]},
                    {'title': 'Top 10 Genres by Profit',
                     'xaxis': {'title': 'Genre'},
                     'yaxis': {'title': 'Profit'}}
                ]}
            ],
            'direction': 'down',
            'showactive': True,
            'active': 0,
            'x': 0.17,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }],
        coloraxis_showscale=False,  # Remove the color scale bar
        yaxis=dict(tickangle=45),
        height=600,
        margin=dict(l=150, r=50, t=50, b=150)
    )

    # Show the plot
    st.plotly_chart(fig7)

# Create columns for the genre plot
col3, col4 = st.columns(2)

# Call the function to create the plot with the dropdown filter for genres
with col3:
    st.subheader('Top 10 Genres by Count')
    create_genre_filtered_plot()

###

df_exploded = df.dropna(subset=['spoken_languages'])
df_exploded['spoken_languages'] = df_exploded['spoken_languages'].str.split(',')
df_exploded = df_exploded.explode('spoken_languages')

# Step 2: Count the occurrences of id_title by language
df4 = df_exploded.groupby('spoken_languages')['id_title'].nunique().reset_index()
df4.columns = ['language', 'count']

# Step 3: Sort the languages by count in descending order
df4 = df4.sort_values(by='count', ascending=False)

# Step 4: Get the top 4 languages
top_4_languages = df4.head(4)

# Combine the rest of the languages into 'Other'
other_languages = df4.iloc[4:]
other_count = other_languages['count'].sum()

# Step 5: Use pd.concat() to append 'Other'
top_4_languages = pd.concat([top_4_languages, pd.DataFrame({'language': ['Other'], 'count': [other_count]})], ignore_index=True)

# Step 6: Create the pie chart
fig8 = px.pie(
    top_4_languages,
    names='language',
    values='count',
    title='Top 4 Languages by Movie Count',
    color='language',
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Show the plot
st.plotly_chart(fig8)