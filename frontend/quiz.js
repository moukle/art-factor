let base_url = "http://localhost:5000/api";

/**
 * show loader on start and
 * fetch facts from server
 */
$(document).ready(function () {
    fetchFacts().then(() => {
        show_loader(false);
        transcriptSpeech();
    });
});

function show_loader(isShowing) {
    let loader = document.getElementById('loader');
    let btn_group = document.getElementById('facts');

    if (isShowing) {
        loader.className = loader.className.replace(/\binactive\b/g, "active");
        btn_group.className = btn_group.className.replace(/\bactive\b/g, "inactive");
    } else {
        loader.className = loader.className.replace(/\bactive\b/g, "inactive");
        btn_group.className = btn_group.className.replace(/\binactive\b/g, "active");
    }
}

/***
 * records audio and detects answers;
 * answers will be matched with the fact sentences
 * @returns {Promise<void>}
 */
async function transcriptSpeech() {
    let recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        console.log("Got a result fro speech");
        const speechToText = event.results[0][0].transcript;

        console.log('Recorded Audio:', speechToText);
        let fact_buttons = document.getElementsByClassName('fact');

        // fuzzy string matching
        const fuzzyStrings = ['Option A', 'Option B', 'Option C'];
        let fuzzySet = FuzzySet(fuzzyStrings);
        let res = fuzzySet.get(speechToText);

        if (res === null) {
            console.log('no result returned from speech');
            return;
        }
        let indexOfAnswer = fuzzyStrings.indexOf(res[0][1]);

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


function speak(speech) {
    let synth = window.speechSynthesis;
    let utterThis = new SpeechSynthesisUtterance(speech);

    let voices = synth.getVoices();
    utterThis.voice = voices[4];
    utterThis.lang = 'en-US';

    synth.speak(utterThis);
}

/**
 * validate whether player guessed correctly
 * and return feedback accordingly
 * @param btn was pressed by a player
 */
async function validate(btn) {
    const isCorrect = (btn.value === 'true');
    await fetch(base_url+ "/answer" + `?userId=666&selectedTrueFact=${isCorrect}`);

    if (btn.value === 'true') {
        btn.className += " " + "true";
        speak('Correct! What a champ!');
    } else {
        btn.className += " " + "false";
        speak('Incorrect! Try harder');
    }
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
 * add facts sentences to the button text
 * @returns {Promise<void>}
 */
async function fetchFacts() {
    let filter_uri = window.location.hash.substring(1);
    console.log('filtered:', filter_uri);

    let fact_buttons = document.getElementsByClassName('fact');

    console.log('fetch fact');
    const response = await fetch(base_url+ "/fact" + `?userID=666&subjects=${filter_uri}`);
    let data = await response.json();
    console.log('finished fetching');
    show_loader(false);
    shuffleArray(data);
    reset(fact_buttons);

    create_facts(data);
    // data.forEach((el, index) => {
    //     console.log('index:', index);
    //     const {Fact} = el;
    //     const {factTrue, sentence} = Fact;
    //
    //     fact_buttons[index].textContent = sentence;
    //     fact_buttons[index].value = factTrue;
    // });
}

function create_facts(data){
    let facts_div = document.getElementById('facts');

    while(facts_div.firstChild){
        facts_div.removeChild(facts_div.firstChild);
    }
// <button class="fact" onclick="validate(this); fetchFacts();">
//         </button>
    data.forEach((el, index) => {
        const {Fact} = el;
        const {factTrue, sentence} = Fact;

        let fact_btn = document.createElement('button');
        fact_btn.className = "fact";
        fact_btn.textContent = sentence;
        fact_btn.value = factTrue;
        fact_btn.onclick = ()=>{
        validate(fact_btn);
        fetchFacts();
        };

        facts_div.appendChild(fact_btn);
    });

}