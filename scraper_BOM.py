#script to scrape opening weekend revenue from the Box Office Mojo and dump data to a file
import pandas as pd

def get_raw_data(title):
    import requests
    import numpy as np
    '''given a list of movie titles, get opening weekend info from BoxOfficeMojo'''
    t = str(title)
    url = "http://www.boxofficemojo.com/movies/?id=" + t.replace(' ','') + ".htm"
    s = requests.get(url).text
    pos1 = s.find('Domestic Summary')
    if pos1 == -1: 
        weekend_rev=0
        weekend_rev_mean =0
        return weekend_rev, weekend_rev_mean
    pos2 = s.find('The Players')
    pos3 = s.find('Charts')
    pos4 = s.find('Genres')
    positions = [pos2, pos3, pos4]
    a = np.array([len(s[pos1:pos2]), len(s[pos1:pos3]), len(s[pos1:pos4])])
    a = a[a!=0]
    s = s[pos1:positions[np.argmin(a)]]
    weekend_rev, weekend_rev_mean = parse_string(s)
    return weekend_rev, weekend_rev_mean

def parse_string(s):
    '''Extract total and mean opening weekend revenue'''
    pos1 = s.find('Opening&nbsp;Weekend:')
    if pos1==-1:
        rev = 0
    pos2 = s.find('$', pos1)
    pos3 = s.find('<',pos2)
    rev = s[pos2+1:pos3].replace(',','')
    
    pos4 = s.find('theaters', pos3)
    pos5 = s.find('average', pos4)
    mean_rev = s[pos4+11:pos5-1].replace(',','') 
    if rev[0]=='D' or rev[0]=='[':
        rev = 0
        mean_rev = 0
    return rev, mean_rev

def scrape_weekend_data(titles):
    import time
    import csv
    outf = open('data/opening_weekend_data.csv', 'a')
    writer = csv.writer(outf)
    outf.write('title, weekend_rev, weekend_rev_mean\n')
    with outf:
        for i, name in enumerate(titles):
            try:
                weekend_rev, weekend_rev_mean = get_raw_data(name)
                if weekend_rev!=0:
                    writer.writerow([name, weekend_rev, weekend_rev_mean])
                    print('{}: scraping opening weekend info for the movie {}'.format(i, name))
                    #time.sleep(1)
            except Exception as e:
                print(e, name, i)
            
titles = list(pd.read_csv('data/movies_metadata.csv').title)
scrape_weekend_data(titles)
