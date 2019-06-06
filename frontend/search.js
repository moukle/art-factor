let search_url = "http://localhost:5000/api/search";

function next(){
    let suggestion_list = document.getElementById('filter');
    location.href = "./quiz.html" + '#' + suggestion_list.dataset.uri;
    console.log('URI: '+ suggestion_list.dataset.uri);
}

function delete_suggestions(list){
    while(list.firstChild){
        list.removeChild(list.firstChild);
    }
}

async function fetchSuggestions(input){
    let suggestion_list = document.getElementById('filter');
    delete_suggestions(suggestion_list);

    const response = await fetch(search_url+`?fuzzy=${input.value}`);
    let data = await response.json();

    data.forEach( (el) => {
        const {label, uri} = el;
        const className = el.class;
        let option = document.createElement('option');
        suggestion_list.dataset.uri = uri;

        option.value = label;
        option.textContent = className;

        suggestion_list.appendChild(option);
    });
}