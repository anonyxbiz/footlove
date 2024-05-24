# analyze.py
from algo.initialize import*
from footlive import bs4, get_soup, run, get_matches as live_matches
from ai import Wazingai

ai = Wazingai()

db_busy = False

async def load_balancer():
    global db_busy
    if db_busy:
        while True:
            a.sleep(2)
            if not db_busy:
                db_busy = True
                return True
        
async def get_matches():
    global db_busy
    await load_balancer()
    
    match_summaries = []
    
    with open("all_matches.json", "r") as f:
        matches = j_s.load(f)
        for i in matches:
            match = i['match']
            match_data = i['match_data']
            
            match_summaries.append({"match": match, "data": match_data})
    
    db_busy = False
    return match_summaries
    
async def get_live_matches():
    global db_busy
    await load_balancer()
    latest_scores = await live_matches(wtf=True)
    
    db_busy = False
    return latest_scores
    
async def find_match(word, array):
    matches = get_close_matches(word, array)
    if matches:
        return matches[0]   

async def get_game(team, live):
    teams = []
    live = True
   
    matches = await get_matches()
    
    for a, i in enumerate(matches):
        teams.append(i['match'])
        
    match = await find_match(team, teams)
    try:
        with open("all_matches.json", "r", encoding="UTF-8") as f:
            for i in j.load(f):
                if i['match'] == match:
                    match = i
    except Exception as e:
        Error(e)
    return match
 
async def main(prompt, live):

    match = await ai.chat(content)
    
    return match['ai']

async def db(team, live):
    if '•' in team:
        user = team.split('•')[1]
        team = team.split('•')[0]
    else:
        user = ''
        
    history = ''
    match = await get_game(team, live)
    if match:
        content = f"home: {match['match'].split('-')[0]}, away: {match['match'].split('-')[1]} " + ' | '.join(match['match_data'])
    else:
        content = team
            
    prompt = "Me: The current date and time is {}, use this to determine if the match has played already or it has not, the time the match should play is stated in the summary, the first intergers splitted by : are the match scores, eg. 2:0. and the intergers encapsulated in () are the first and second half scores, e.g. (1:0,1:0). Match stats are splitted by | for each fact, the first stats are always the the scores | first and second half scores, example: 2:0  (0:0,2:0) | another fact, now this >2:0< means the match is or ended with the scores being 2 for the home team and 0 for the away team, this >(0:0,2:0)< means the match ended with 0 for the home and away team in first half and second half 2 for the home team and 0 for the away team, please check on this and use the accurate and correct match scores, to determine if the match is currently playing compare the current date and time, to the date shown on the summary, if the match is currently playing, analyze the match stats of the summary and provide analysis of it, prediction and so on. Your task is to analyze this football match and provide detailed analysis, make an article out of it, your article should be greatly formatted, good punctuation and general article formatting. {}.\n The summary is below: \n{}\nYou: ".format(str(dt.now()), user, content)
    history += prompt
    
    match = await ai.aidata(history, "ip")
    match = match['WazingAI']['ai']
    history += match + '\n'
    
    return match
    
def analyze(game, live=True):
    analysis = run(db(game.replace('vs', '-'), live))
  
    return analysis
    
if __name__=="__main__":
    while True:
        match = input("Enter Match: ")
        summary = analyze(match)
        p(summary)
        p('\n')