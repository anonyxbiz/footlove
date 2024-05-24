# app: footlive.py - football_livescore app.
# developer: anonyxbiz
from algo.initialize import*
from bs4 import BeautifulSoup as bs4 
from threading import Thread as T
from random import randint

kontrol = []
all_matches = []

async def get_soup(url):
    headers = {}
    try:
        r = rqs.get(url, headers=headers)
        if r.status_code >= 400:
            Error(r.text, "get_soup")
            
        return bs4(r.text, "html.parser")
    except Exception as e:
        raise Error(e, "get_soup")
  
async def compute_data(arg={"url": None}):
    try:
        r = await get_soup(arg['url'])
        if r:
            soup = r.find(id='main')
           
        if soup:
            match = soup.find("h3").text
            detail = soup.find_all(class_="detail")
            match_detail = []
            
            content = soup.find(id="detail-tab-content") or False
            
            match_data = {"match": match, "match_data": []}
            
            for a in detail:
                match_data["match_data"].append(a.text)           
            all_matches.append(match_data)
            return all_matches
                
    except Exception as e:
        raise Error(e, "compute_data")

async def kontrolla(arg):
    # manages threads seamlessly, enhancing performance
    try:
        while True:
            if len(kontrol) <= arg['max_workers']:
                kontrol.append(arg['job'])
                await compute_data(arg)
                break
            else:
                wait = randint(1, 5)
                await sleep(wait)
                
        for a, i in enumerate(kontrol):
            if i['job'] == arg['job']['job']:
                del kontrol[a]    
                 
    except Exception as e:
        raise Error(e, "kontrolla")        

async def save_matches(all_matches):
    try:
        with open("all_matches.json", "w", encoding="UTF-8") as f:
            j.dump(all_matches, f, indent=4, ensure_ascii=False)
                
            return 'Dumped {} Matches'.format(len(all_matches))
        
    except Exception as e:
        raise Error(e, "save_matches")
    
async def get_match_data(leagues, matches, url, max_workers, wtf):
    cnt = 0
    jobs = []
    
    try:
        for a, b in zip(leagues, matches):
            cnt += 1
            job = {'job': cnt}
            match_url = url+b['href']
         
            arg = {"max_workers": max_workers, 'run': kontrolla, 'url': match_url, 'job': job}
            t = T(target=sync_to_async, args=(arg,))
            jobs.append(t)
            t.start()
            
        for j in jobs:
            j.join()
        
        if wtf:
            save = await save_matches(all_matches) 
        
        return all_matches
             
    except Exception as e:
        raise Error(e, "get_match_data")                                       
async def get_matches(max_workers=100, wtf=False):
    url = ['https://www.livescore.cz','https://www.livescore.cz/?d=-1']
 
    try:
        soup = await get_soup(url[0])
        soup2 = await get_soup(url[1])
        leagues = soup.find(id="score-data").find_all("h4")
        for x in soup2.find(id="score-data").find_all("h4"):
           leagues.append(x)
           
        matches = soup.find(id="score-data").find_all("a")
        for y in soup2.find(id="score-data").find_all("a"):
            matches.append(y)
        
        if leagues and matches:
            a_m = await get_match_data(leagues, matches, url[0], max_workers, wtf)
            if a_m:
                return a_m
            
    except Exception as e:
        raise Error(e, "get_matches")                     

def sync_to_async(arg):
    try:
        run(arg['run'](arg))
    except Exception as e:
        raise Error(e, "sync_to_async")
    
if __name__=="__main__":
    o = a.run(get_matches(max_workers=200, wtf=True))
    p(o)