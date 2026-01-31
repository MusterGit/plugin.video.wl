import requests
import xbmcgui

#https://api.themoviedb.org/3/movie/{movie_id}/images
#https://api.themoviedb.org/3/tv/{series_id}/images
#https://image.tmdb.org/t/p/original/



d = xbmcgui.Dialog()
api_key = '0a076614ed06ed17dc3a6446c3f9ae2e'
#base_url_search = 'https://api.themoviedb.org/3/search/'
base_url_search = 'https://api.themoviedb.org/3/'


def tmdb_note(note):
    d.notification(f"TMDB Search", f"{note}", xbmcgui.NOTIFICATION_INFO, 2000)


def tmdb_response(url_splitter,params):
    url = base_url_search + str(url_splitter)
    try:
        response = requests.get(url ,params=params)
        if response.status_code == 200:
            data = response.json()
            return data
    except:
        return None

def tmdb_img_search(item):
    base_img_url = "https://image.tmdb.org/t/p/original"
    params = tmdb_img_param()
    url_splitter = f"{str(item['type'])}/{str(item['id'])}/images"
    data = tmdb_response(url_splitter,params)
    img_list ={'fanart':[],'poster':[]}
    if data: 
        for d in data['backdrops']:
            img_list['fanart'].append(str(base_img_url)+str(d['file_path']))
        for d in data['posters']:
            img_list['poster'].append(str(base_img_url)+str(d['file_path']))
        return img_list
    else:
        tmdb_note(f"keine Bilder")   
        return None

def tmdb_img_param():
    params = {
            'api_key': api_key,
            'include_image_language' : 'en,de,null',
            'language' : 'en-US'
        }  
    return params


def tmdb_search_param(term):
    params = {
            'api_key': api_key,
            'query' : term,
            'language' : 'de-DE',
            'page' : '1'
        }
    return params

def tmdb_search(term,mtype='search/multi'):
    params = tmdb_search_param(term)
    url_splitter = str(mtype)
    data = tmdb_response(url_splitter,params)
    if data: 
        if data['total_results'] > 0:
            return data['results']
        else:
            tmdb_note(f"keine Ergebnisse für {term}")
    else:
        tmdb_note(f"Fehler bei der Anfrage für Suchbegriff {term}")
    return None
