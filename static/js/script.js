var content = document.querySelector("#content");
var submit_chat = document.querySelector("#submit_chat");
var chat_box = document.querySelector('#you');

async function atyper(airesponse) {
    content.textContent = null;
    var airesponse = JSON.stringify(airesponse, undefined, 2);
    
    for (let i = 0; i < airesponse.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1));
        content.textContent += airesponse[i];
    }

}
async function update_page(query) {
    const token = localStorage.getItem('token')

    let site_url = '/';
    const response = await fetch(`${site_url}api/v1/models`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'validation': token
        },
        body: JSON.stringify({
            'model': 'ai',
            'query': query,
        })
    });

    try {
        if (response.ok) {
            var data = await response.json();

        } else {
            var data = { "detail": [{ "link": "test", "test": "test" }], "all_visits": 1, "unique_visits": 1 }
        }
    } catch (e) {
        console.error(e);
    };
    if (data) {
        return data;
    };

}

window.addEventListener('load', async () => {
    const tokenMeta = document.querySelector('meta[name="token"]');
    const token = tokenMeta ? tokenMeta.getAttribute('content') : null;
    let client = false;
    
    if (localStorage.getItem('token')) {
        client = true;
    }
    if (token) {
        localStorage.setItem('token', token);
        tokenMeta.remove();
    } else {
        localStorage.setItem('token', 'token');
        tokenMeta.remove();
    }
    
    if (client) {
        //var chat = await update_page('continua');
        //atyper(chat);
    };
    
});

submit_chat.addEventListener('click', async ()=>{
    var query = chat_box.value;
    chat_box.value = null;
    var chat = await update_page(query);
    await atyper(chat);
});
chat_box.addEventListener('keydown', async (e) => {
    if (e.key === "Enter" && e.shiftKey) {
        var query = chat_box.value;
        chat_box.value = null;
        chat_box.focus();
        var chat = await update_page(query);
        await atyper(chat);
    }
});