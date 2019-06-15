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

async function speechControl() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        console.log("Got a result fro speech");
        const speechToText = event.results[0][0].transcript;

        console.log('Recorded Audio:', speechToText);
        let fact_buttons = document.getElementsByClassName('fact');

        // fuzzy string matching
        const fuzzyStrings = ['OK', 'Next'];
        let fuzzySet = FuzzySet(fuzzyStrings);
        let res = fuzzySet.get(speechToText);

        if (res === null) {
            console.log('no result returned from speech');
            return;
        }
        let indexOfAnswer = fuzzyStrings.indexOf(res[0][1]);

        next();

        console.log('got it!', res);

        validate(fact_buttons[indexOfAnswer]);
        fetchFacts();

    };

    recognition.onerror = (event) => {
        recognition.abort();
        console.log('Oops, speech recording failed...');
    };
    // restart recording audio
    recognition.onend = (event) => {
        console.log('speech recording ended...');
        recognition.start();
    };

    recognition.start();
}

async function fetchSuggestions(input){
    let suggestion_list = document.getElementById('filter');
    delete_suggestions(suggestion_list);

    const response = await fetch(search_url+`?fuzzy=${input.value}`);
    console.log('Input', input.value);

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