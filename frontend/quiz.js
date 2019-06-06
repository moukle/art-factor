let base_url = "http://localhost:5000/api/fact";

$(document).ready(function () {
    let loader = document.getElementById('loader');
    let btn_group = document.getElementById('facts');

    fetchFacts().then(() => {
        loader.className = loader.className.replace(/\bactive\b/g, "inactive");
        btn_group.className = btn_group.className.replace(/\binactive\b/g, "active");
        transcriptSpeech();
    });
});

async function transcriptSpeech() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onresult = (event) => {
        const speechToText = event.results[0][0].transcript;
        console.log('Recorded:', speechToText);
        let fact_buttons = document.getElementsByClassName('fact');

        let button_txts = [];
        for (let fact of fact_buttons) {
            button_txts.push(fact.textContent);
        }

        let fuzzySet = FuzzySet(button_txts);
        let res = fuzzySet.get(speechToText);

        for (let i = 0; i < res.length; i++) {
            if (res[i][1] === fact_buttons[i].textContent) {
                validate(fact_buttons[i]);
                fetchFacts();
            }
        }
    };
    recognition.start();

    recognition.onend = (event)=>{
        recognition.start();
    };
}

/**
 * validate whether player guessed correctly
 * @param btn pressed by player
 */
function validate(btn) {
    if (btn.value === 'true') {
        btn.className += " " + "true";
    } else
        btn.className += " " + "false";
}

/**
 * randomize shuffle true and false facts
 * @param array contains all facts
 */
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

/**
 * resets style of fact buttons
 * @param fact_buttons
 */
function reset(fact_buttons) {
    [].forEach.call(fact_buttons, fact => {
        fact.className = fact.className.replace(/\btrue\b/g, "");
        fact.className = fact.className.replace(/\bfalse\b/g, "");
    })
}

/**
 * @var <json> data contains formatted response of http request
 * add facts to the button
 * @returns {Promise<void>}
 */
async function fetchFacts() {
    let filter_uri = window.location.hash.substring(1);
    let fact_buttons = document.getElementsByClassName('fact');

    const response = await fetch(base_url + `?persons=${filter_uri}`);
    let data = await response.json();

    shuffleArray(data);
    reset(fact_buttons);

    data.forEach((el, index) => {
        const {Fact} = el;
        const {factTrue, object, predicate, resource, subject} = Fact;
        let formatted_predicate = predicate.match(/[^/]+(?=\/$|$)/i);

        fact_buttons[index].textContent = subject + ' ' + formatted_predicate.toString().replace(/_/g, " ") + ' ' + object;
        fact_buttons[index].value = factTrue;
    });
}
