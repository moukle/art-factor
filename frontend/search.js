let search_url = "http://localhost:5000/api/search";

function next(){
    location.href = "./quiz.html";
}

async function fetchSuggestions(input){
    console.log('type');
    const response = await fetch(search_url+`?fuzzy=${input.value}`);
    let data = await response.json();
    alert(data);
    // data.forEach( (el) => {
    //     const {label, url} = el;
    //     const fact = el.class;
    //     alert(fact + label + url);
    // });
}