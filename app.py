# app.py
from algo.initialize import*
from algo.apps import Pages, Components, Gate
from backend import Backend_apps

app = Bottle()
comps = Components()
pages = Pages(comps)
gate = Gate(comps, pages)
backend = Backend_apps(pages, comps, gate)

@app.route('/static/<filename:path>')
def static(filename):
    try:
        return static_file(filename, root='./static')
    except Exception as e:
        raise Error(f'Application log: {e}')
        abort(403, e)

@app.route('/')
def index():
    try:
        webpage = a.run(pages.page_manager('index', request, r))
    except Exception as e:
        abort(403, e)
    return webpage
    
@app.route('/<page>')
def controlla(page):
    try:
        webpage = a.run(pages.page_manager(page, request, r))
        return webpage
    except Exception as e:
        abort(403, e)
       
@app.route('/api/v1/models', method=['GET','POST', 'OPTIONS'])
def models():
    try:
        data = a.run(backend.dealer(request, r))
        return data
    except Exception as e:
        abort(403, e)
       
if __name__=="__main__":
    task = Thread(target=gate.keepalive, args=(env["url"],))
    task.start()
    
    run(app=app, host="0.0.0.0", port="8004", debug=True, reloader=True)
    
    