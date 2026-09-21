// global api prefix
let api_prefix = '/api/v1';

// fetch-wrappers for API functions
async function createTale(tail_id, desc) {
    try {
        const response = await fetch(api_prefix + '/create-tale', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tail_id: tail_id, desc: desc })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload(); 
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

//updateTale
async function updateTale(tale_id, desc) {
    try {
        const response = await fetch(api_prefix + '/update-tale', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tale_id: tale_id, desc: desc })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload();
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function createTail(tie_id, desc) {
    try {
        const response = await fetch(api_prefix + '/create-tail', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tie_id: tie_id, desc: desc })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload(); 
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function createTie(desc, tie_type) {
    try {
        const response = await fetch(api_prefix + '/create-tie', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({desc: desc, tie_type: tie_type })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload(); 
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

//
async function updateTie(tie_id, desc, tie_type) {
    try {
        const response = await fetch(api_prefix + '/update-tie', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({tie_id: tie_id, desc: desc, tie_type: tie_type })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload();
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function updateTail(tail_id, desc, status) {
    try {
        const response = await fetch(api_prefix + '/update-tail', {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tail_id: tail_id, desc: desc, status: status })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload(); 
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function deleteTail(tail_id) {
    try {
        const response = await fetch(api_prefix + '/delete-tail', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tail_id: tail_id })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload(); 
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function deleteTie(tie_id) {
    try {
        const response = await fetch(api_prefix + '/delete-tie', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tie_id: tie_id })
        });
        const result = await response.json();
        //
        if (response.ok) {
            window.location.reload();
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function createUser() {
    try {
        const response = await fetch('/auth/register', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });
        const result = await response.json();
        //
        if (response.ok) {
            token_msg = `<div class="show_token">${result.message}
                            <div id="token" tabindex="0" onclick="navigator.clipboard.writeText(token.innerText)">${result.token}</div>
                         </div>`
            notie.force({text: token_msg }, function(){window.location.href = '/ties'});
        } else {
            notie.alert({ type: 3, text: "Ошибка в запросе: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}

async function loginUser(e, token) {
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: token })
        });
        const result = await response.json();
        //
        if (response.ok) {
            if (result.ok) window.location.href = result.redirect_url;
        } else {
            notie.alert({ type: 3, text: "Ошибка базы: " + result.detail});
        }
    } catch (error) {
        notie.alert({ type: 3, text: "Неизвестная ошибка"});
    }
}


console.log('API functions loaded..');
