# backend.py
from algo.initialize import*
from analyze import db, get_live_matches

class Backend_apps:
    def __init__(self, pages, comps, gate):
        self.comps = comps
        self.pages = pages
        self.gate = gate
        
    async def dealer(self, request, response):
        try:
            incoming = await self.gate.way(request, response)
            if incoming:
                query = incoming["query"] or None
                ip = request.remote_addr
                analysis = await db(query.replace('vs', '-'), live=True)
                data = {"response": analysis}
            else:
                abort(403, "request missing data")
        except Exception as e:
            abort(403, e)
         
        # run await update_db() and return data concurrently
        return data
        
    async def update_db(self):
        await get_live_matches()
        
        
if __name__ == '__main__':
    pass