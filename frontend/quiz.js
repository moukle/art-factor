let base_url = "http://localhost:5000/api/fact";

/**
 * show loader on start and
 * fetch facts from server
 */
$(document).ready(function () {
    let loader = document.getElementById('loader');
    let btn_group = document.getElementById('facts');

    fetchFacts().then(() => {
        show_loader(false);
        // loader.className = loader.className.replace(/\bactive\b/g, "inactive");
        // btn_group.className = btn_group.className.replace(/\binactive\b/g, "active");
        transcriptSpeech();
    });
});

function show_loader(isShowing) {
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
        const speechToText = event.results[0][0].transcript;

        console.log('Recorded Audio:', speechToText);
        let fact_buttons = document.getElementsByClassName('fact');


        // fuzzy string matching
        let fuzzySet = FuzzySet(['A', 'B', 'C']);
        let res = fuzzySet.get(speechToText, [0.51]);

        if (res.isEmpty()) {
            speak('SAY WHAT?');
        }else {
            let indexOfAnswer = res.indexOf(res[0][1]);


            // for (let i = 0; i < fact_buttons.length; i++) {
            //
            //     if (res[0][1] === fact_buttons[i].textContent) {
            console.log('got it!');
            validate(fact_buttons[indexOfAnswer]);
            fetchFacts();
            // return;
            //     }
            // }
        }
    };
    // start recording audio
    recognition.start();

    // restart recording audio
    recognition.onend = (event) => {
        recognition.start();
    };
}


function speak(speech) {
    let synth = window.speechSynthesis;
    let utterThis = new SpeechSynthesisUtterance(speech);

    let voices = synth.getVoices();
    utterThis.voice = voices[0];
    utterThis.pitch = 10;
    utterThis.rate = 10;
    synth.speak(utterThis);
}

/**
 * validate whether player guessed correctly
 * and return feedback accordingly
 * @param btn was pressed by a player
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
 * add facts sentences to the button text
 * @returns {Promise<void>}
 */
async function fetchFacts() {
    let filter_uri = window.location.hash.substring(1);
    let fact_buttons = document.getElementsByClassName('fact');

    setTimeout(() => {
        show_loader(true);
    }, 2000);

    const response = await fetch(base_url + `?persons=${filter_uri}`);
    let data = await response.json();

    show_loader(false);
    shuffleArray(data);
    reset(fact_buttons);

    data.forEach((el, index) => {
        const {Fact} = el;
        const {factTrue, sentence} = Fact;

        fact_buttons[index].textContent = sentence;
        fact_buttons[index].value = factTrue;
    });
}
