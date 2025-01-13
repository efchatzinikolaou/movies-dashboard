**Analytics Dashboard of IMDb Movies (Streamlit, Pandas, Plotly, Folium)**
Film Production interactive dashboard! Analyze trends in the movie industry.

## Live Demo Site

https://moviev-dashboard.streamlit.app/


## Features

- **Dynamic Filtering**: Users can filter the sales data by various criteria, including:
    * id
    * title
    * vote_average
    * vote_count
    * status
    * release_date
    * revenue
    * runtime
    * adult
    * budget
    * imdb_id
    * original_language
    * original_title
    * overview
    * popularity
    * tagline
    * genres
    * production_companies
    * production_countries
    * spoken_languages
    * keywords
    * release_year
    * release_month
    * profit
- **Interactive Visualizations:** The dashboard utilizes Plotly to create a variety of interactive charts and tables, allowing users to drill down into the data and gain clearer understanding. Chart types include:
    * **Analyze** trends in the movie industry (most popular genres, highest-grossing movies).
    * Build **recommendation** systems ( based on genres or ratings).
    * Perform **financial analysis** (budget vs. revenue insights).
    * Visualize **trends** over time (movie releases by year).

- **Data Cleaning and Analysis (Pandas):** The dashboard utilizes Pandas for cleaning and analyzing the sales data loaded from CSV files. This may involve handling missing values, formatting data types, or filtering outliers to ensure accurate and insightful visualizations. The data retrieved from https://www.kaggle.com/datasets/anandshaw2001/imdb-data/data



## Run Locally

Clone the project

```bash
  git@github.com:efchatzinikolaou/movies-dashboard.git
```

Go to the project directory

```bash
  cd 04-dashboard
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run movie_dashboard_streamlit.py
```
