# ai.py
from algo.initialize import*
from algo.apps import Components
from googleapiclient.discovery import build
import google.generativeai as genai

class Analytics:
    queries = [{'ip': '192.160.100.1', 'queries': [{"detail": {"query": 'query', "output": 'reply', "combined": 'chat'}}]}]
    def __init__(self):
        pass
                
    async def user_queries(self, ip, query):
        user_data = None
        for i in self.queries:
            if ip == i['ip']:
                i['queries'][0]['detail']['combined'] += query['detail']['combined']
                user_data = i
                break
            
        if user_data == None:
            user_data = {'ip': ip, 'queries': [query]}
            self.queries.append(user_data)

        return user_data

    async def user_chats(self, ip):
        for i in self.queries:
            if ip == i['ip']:
                user_data = i
                p(self.queries)
                return user_data 
        return False
        
    async def remove_user(self, ip):
        for i, user in enumerate(self.queries):
            if user['ip'] == ip:
                p(self.queries)
                del self.queries[i]
                return True
        return True
        
class Wazingai: 
    def __init__(ai, model='gemini-1.5-pro-latest'):
        ai.api_key = env["api_key"]
        ai.model = model
        genai.configure(api_key=ai.api_key)
        ai.model = genai.GenerativeModel(ai.model)
        ai.analytics = Analytics()
        
    async def chat(ai, text):
        ai.response = {'status': 'fail', 'ai': ''}
        prompt = text
        
        try:
            r = ai.model.generate_content(prompt, safety_settings={'SEXUALLY_EXPLICIT':'block_none','HARASSMENT':'block_none','HATE_SPEECH':'block_none'})
            
            try:
                if r.text:
                    ai.response['ai'] = r.text.replace("*", "")
                    ai.response['status'] = 'processed'
            except Exception as e:
                p(e)
                ai.response['ai'] = str(r.candidates)
                
        except Exception as e:
            ai.response['ai'] = 'fail'
        
        return ai.response
        
    async def aidata(ai, query, ip):
        try:
            if query == 'del':
                await ai.analytics.remove_user(ip)
                return {'detail': 'session cleaned'}
                
            all_chats = await ai.analytics.user_chats(ip)
            if all_chats:
                chats = all_chats['queries'][0]['detail']['combined']
                if query == 'continua': query = 'hi again, where were we'
                content = str(chats) + f'Me: {query}\nYou: '
            else:
                if query == 'continua':
                    query = 'hi there'
                    
                content = f'Me: {query}\nYou: '
                
            reply = await ai.chat(content)
            
            if reply and reply['status'] == 'processed':
                try:
                    chat = f'Me: {query}\nYou: {reply["ai"]}\n'
                
                    detail = {"detail": {"query": query, "output": reply, "combined": chat}}
    
                    data = await ai.analytics.user_queries(ip, detail)
                except Exception as e:
                    p(e)
                  
            else:
                reply = 'Request was blocked'
            
        except Exception as e:
            p(e)
            return 'Something went wrong'
            
        return {"WazingAI": reply}
    
if __name__ == "__main__":
    m = Wazingai()
    while True:
        ip = '192.168.100.1'
        content = 'Hi'
        data = a.run(m.aidata(content, ip))
        
        p(data)
        break
        


