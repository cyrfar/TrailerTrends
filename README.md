# TrailerTrendz
The film industry is a complicated and fascinating multi-billion dollar market. In this repo, we build a model that uses information about movie trailer viewership (online search trends, etc) and other movie metadata to predict the initial ROI of a movie. The target variable, which we label as "success", is given by

success = opening weekend revenue/budget

The model could therefore be useful to movie marketers when devising strategies prior to the release date of a movie. This work was part of my three week long project as an [Insight Data Science Fellow](http://insightdatascience.com/) in NYC.

The first step in this project was getting the data. To this end, I
* used the Movie Database (TMDB) API to get basic movie metadata such as genre and budget.
* scraped Box Office Mojo (see scraper_BOM.py) to get opening weekend revenue and number of theaters playing the film.
* scraped youtube to get average number of views, likes and dislikes for the movi's trailers.
* used unofficial Google Trends API to extract time series data about trailer viewership.

