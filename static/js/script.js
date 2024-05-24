var content = document.querySelector("#content");
var submit_chat = document.querySelector("#submit_chat");
var chat_box = document.querySelector('#you');

async function atyper(airesponse) {
    content.textContent = null;
    
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
            var data = {
  "response": "## The Strongest Hold On For 3-2 Victory Against Guabira: A Match Report\n\nLa Paz, Bolivia - The Strongest edged out Guabira in a thrilling encounter that finished 3-2 at Estadio Hernando Siles on May 24th, 2024. The match, filled with end-to-end action, saw The Strongest take an early lead, only to be pegged back by a resilient Guabira side. \n\nFirst Half Fireworks:\n\nThe home side drew first blood in the 10th minute, with Bruno Miranda capitalizing on a Caire M. assist to make it 1-0.  Guabira, however, responded with vigor. Montero R. leveled the score in the 26th minute, and just ten minutes later, Melgar C.A. gave the visitors the lead. \n\nJust when it seemed Guabira would go into halftime with a lead, The Strongest's Quintana A. found the back of the net in the 39th minute, assisted by Vasquez R., to equalize the score at 2-2.  Adding to the drama, Bruno Miranda scored his second of the night just before the halftime whistle, giving The Strongest a 3-2 lead going into the break. \n\nA Tense Second Half:\n\nThe second half saw a more cautious approach from both sides, with fewer clear-cut chances.  Guabira pushed hard for an equalizer, and the game became increasingly tense as the clock ticked down. \n\nDespite multiple substitutions and a flurry of late goals, including a penalty converted by Melgar C.A. in the 90+11th minute, Guabira could not find the elusive equalizer. \n\nKey Takeaways:\n\n Clinical Finishing From The Strongest: Despite Guabira's spirited performance, The Strongest ultimately secured the victory thanks to their clinical finishing in the final third. Bruno Miranda was the star of the show, netting a brace and proving to be a constant threat to the Guabira defense. \n Guabira's Fighting Spirit: Despite the loss, Guabira demonstrated their resilience and determination. They fought back from behind twice and created several scoring opportunities. With a little more composure in front of goal, they could have easily walked away with a point. \n End-to-End Action: The match was a thrilling spectacle for the fans, with both teams playing attacking football. The high number of goals and lead changes kept the fans on the edge of their seats throughout the 90 minutes.\n\nLooking Ahead:\n\nThis victory will be a confidence booster for The Strongest as they continue their campaign.  Guabira, on the other hand, will be looking to bounce back from this defeat and pick up points in their upcoming fixtures. \n"
}
        }
    } catch (e) {
        console.error(e);
    };
    if (data) {
        return data.response;
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