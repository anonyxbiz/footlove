# apps.py
from algo.initialize import*
from cryptography.fernet import Fernet

class Pages:
    def __init__(s, comps):
        s.app = comps
        
    async def page_manager(s, page, request, response):
        ip = request.remote_addr
        set_res = await s.response_config(request, response)
        
        if not set_res:
            msg = 'You"re not supposed to be here'
            raise Error('Request Aborted from IP: {}, Error message: {}'.format(ip, msg))
            abort(403, msg)
                
        if os.path.isfile(f'static/page/{page}.html'):
            page_content = {'token': set_res, 'views': 'views'}
            return template(f'static/page/{page}.html', page_content=page_content)
            
        else:
            msg = "The page you're looking for cannot be found"
            raise Error('Request Aborted from IP: {}, Error message: {}'.format(ip, msg))
            
            abort(404, msg)
            
    async def response_config(s, request, response):
        verification = await s.verify_request(request, response, do='all')
        
        return verification
    
    async def verify_request(s, request, response, do):
        host = await s.app.get_header(request, 'Host')
        try:
            if do == 'all':
                ip = request.remote_addr
                token = await s.app.safe_tool(ip, 'encrypt')
                s.tokens = await s.app.update_db('read')
                
                s.tokens.append(token)
                await s.app.update_db('update', s.tokens)
                
            response.set_header('strict-transport-security', 'max-age=63072000; includeSubdomains')
            response.set_header('x-frame-options', 'SAMEORIGIN')
            response.set_header('x-xss-protection', '1; mode=block')
            response.set_header('x-content-type-options', 'nosniff')
            response.set_header('referrer-policy', 'origin-when-cross-origin')
            response.set_header('server', 'Secure')
            
            if do == 'all':
                return token
            else:
                return response
                
        except Exception as e:
            abort(406, e)            
                
class Components:
    def __init__(s):
        s.fer_key = csrf_key+'='
        s.allowed_origins = app_info['web_app_url'].replace('https://', '')
        s.db = 'algo/db.json'

    async def safe_tool(s, parent, action):
        try:
            s.fernet = Fernet(s.fer_key)
        except Exception as e:
            return False
        try:
            s.parent = parent.encode()
            try:
                if action == 'encrypt':
                    s.content = s.fernet.encrypt(s.parent)
                elif action == 'decrypt':
                    s.content = s.fernet.decrypt(s.parent)            
            except Exception as e:
                 return False
                
            return s.content.decode()
        except Exception as e:
            return False  
               
    async def get_json(s, r):    
        return j.loads(r.body.getvalue().decode('utf-8'))          
        
    async def get_header(s, request, value):
        try:  
            value = request.get_header(value)
            if not value:
                return None
            return value
        except:
            return None
    
    async def update_db(s, do, update=None):
        if do == 'read':
            if not os.path.exists(s.db):
                return []
            with open(s.db, 'r') as f:
                db = j.load(f)
                return db
        elif do == 'update':
            with open(s.db, 'w') as f:
                j.dump(update, f, indent=4)
                return True

class Gate:
    def __init__(self, comps, pages):
        self.comps = comps
        self.pages = pages
        
    async def way(self, request, response):
        try:
            await self.pages.verify_request(request, response, do='headers_only')
            
            csrf_token = await self.comps.get_header(request, 'validation')
            
            tokens = await self.comps.update_db('read')
            if csrf_token == None or csrf_token not in tokens:
                abort(406, "Invalid csrf token!")
            if request.method == "GET":
                return request.query
                    
            elif request.method == "POST": 
                return await self.comps.get_json(request)
            elif request.method == "OPTIONS":
                allowed_methods = ["GET", "POST"]
                response.headers["Allow"] = ", ".join(allowed_methods)
                abort(200, {"allow": allowed_methods})  
        except Exception as e:
            raise Error(e)

if __name__ == '__main__':
    pass