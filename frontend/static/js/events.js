

document.querySelectorAll('.add_tale_x').forEach(e => {
    e.addEventListener('change', (event) => {
        // на андроиде неведомая херня - энтер не работает. Поэтому тупо обновляем по change
        // плюс добавлю легкое редактирование всего через notie.input
        // event.preventDefault();

        let tail_id = e.parentElement.getAttribute('data-tail-id');
        let tale_desc = e.value;
        if(tale_desc) createTale(parseInt(tail_id), tale_desc);
        else notie.alert({ type: 3, text: "Пустое описание!"});
        let curr_status = e.getAttribute('data-tail-status'); // TODO curr_status!!
        if(curr_status === "new") updateTail(parseInt(tail_id), null, "active");
    });
});

document.querySelectorAll('.tale-desc-edit').forEach(e => {
    e.addEventListener('dblclick', (event) => {
        let tale_id = e.dataset.taleId;
        notie.input({ text: 'Изменить описание', value: e.innerText}, function (value){
            if (value) updateTale(parseInt(tale_id), value.trim());
        });
    });
});


document.querySelectorAll('.add_tail_x').forEach(e => {
    e.addEventListener('change', () => {
        let tie_id = e.getAttribute('data-tie-id');
        let tail_desc = e.value;
        if(tail_desc) createTail(parseInt(tie_id), tail_desc);
        else notie.alert({ type: 3, text: "Пустое описание!"});
    });
});


document.querySelectorAll('.tail-desc').forEach(e => {
    e.addEventListener('dblclick', (event) => {
        let tail_id = e.parentElement.getAttribute('data-tail-id');
        let tail_desc = e.innerText;
        //
        notie.input({ text: 'Изменить название задачи', value: tail_desc}, function (value){
            if (value) updateTail(parseInt(tail_id), value.trim(), null);
        });
    });
});


document.querySelectorAll('.add_tie_x').forEach(e => {
    e.addEventListener('change', () => {
        let tie_desc = e.value;
        let tie_type = "base"
        createTie(tie_desc, tie_type);
    });
});


document.querySelectorAll('.checkbox select').forEach(e => {
    e.addEventListener('change', () => {
        if (e.dataset.level == 'tail'){
            let tail_id = e.closest('.list-element').dataset.tailId;
            if(e.value == "delete") deleteTail(tail_id);
            else updateTail(parseInt(tail_id), null, e.value);
        }
        else if (e.dataset.level == 'tie'){
            let tie_id = e.closest('.list-element').dataset.tieId;
            if(e.value == "delete") deleteTie(tie_id);
            else if(e.value == "rename") {
                let desc = e.parentElement.parentElement.getElementsByClassName('tie-desc')[0].innerText;
                notie.input({ text: 'Изменить название связки', value: desc}, function (value){
                    if (value) updateTie(parseInt(tie_id), value.trim(), null);
                });
            }
        }
    });
});

document.querySelector('#login_form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    loginUser(event, event.target.token.value);
});

document.querySelector('#create_user_button')?.addEventListener('click', (event) => {
    createUser();
});


console.log('EventListener loaded..');