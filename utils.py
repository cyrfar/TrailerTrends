#The Movie Database (tmdb) API
import tmdbsimple as tmdb
tmdbKey = '441317b48174ab9861771dcda23dd5d2'
tmdb.API_KEY = tmdbKey

'----------------------------TMDB_API------------------------------------------------------'

def get_movie_info(id):
    '''return information about a movie given its id'''
    return tmdb.Movies(id).info(**{'append_to_response': 'trailers'})

def get_similar_movies(id):
    return tmdb.Movies(id).similar_movies()['results']

def get_url(id):
    '''return list of youtube trailer urls given movie id.
    head of list corresponds to most recent trailer.'''
    trailers = []
    for i in range(len(get_movie_info(id)['trailers']['youtube'])):
        source = get_movie_info(id)['trailers']['youtube'][i]['source']
        trailers.append("http://www.youtube.com/watch?v={0}".format(source))
    return trailers


'---------------------------------other-helper-functions-----------------------------------------'

def get_max_date(title):
    return peaks_series.loc[title].loc[peaks_series.loc[title]['peak_values'].idxmax()][0]

def get_second_max_date(title):
    if len(peaks_series.loc[title])>1:       
        df = peaks_series.loc[title][peaks_series.loc[title].peak_values != 100]
        return df.loc[df['peak_values'].idxmax()][0]
    else: return 0
    
def get_release_date(title):
    return df_final.loc[title].release_date

def dt_main(title):
        return (get_release_date(title) - get_max_date(title)).days
    
def dt_trailers(title):
    from dateutil import relativedelta
    if get_second_max_date(title) == 0:
        return 0
    else:
        return (get_max_date(title) - get_second_max_date(title)).days

def get_movie(title):
    return searches.loc[searches.title==title]['searches'].copy()

def views_proxy(title):  
    release_date = df2010[df2010.title == title].release_date.iloc[0]
    if get_second_max_date(title)!=0:
        start = min(get_max_date(title), get_second_max_date(title))
    else: 
        start = get_max_date(title)
    delta_t1 = (pd.to_datetime(datetime.datetime.today())- start).days
    delta_t2 = (release_date - start).days
    tot_views = youtube_trailers.loc[title][0]
    views_proxy = (tot_views/delta_t1)*(delta_t2)
    return np.round(views_proxy)

def like_score(df):
    return df_final['views']*df_final['likes']/(df_final['likes'] + df_final['dislikes'])

def like_score_proxy(df):
    return df_final['views_proxy']*df_final['likes']/(df_final['likes'] + df_final['dislikes'])

#function to make dt_trailers categorical 
def categorize(s):
    res =[]
    for v in s:
        if v==0:
            res.append('zero')
        elif v>0:
            res.append('pos')
        else: 
            res.append('neg')
    return res 