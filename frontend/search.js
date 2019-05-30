let search_url = "http://localhost:5000/api/search";

function next(){
    location.href = "./quiz.html";
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
        const {label, url} = el;
        const className = el.class;
        let option = document.createElement('option');

        option.textContent = label+ '\t' + className;
        option.value = label;

        suggestion_list.appendChild(option);
    });
}