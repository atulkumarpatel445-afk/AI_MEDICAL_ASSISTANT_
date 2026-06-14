async function askAI(){

    let question =
    document.getElementById(
        "question"
    ).value;

    if(question===""){

        alert("Enter a question");

        return;
    }

    document.getElementById(
        "loading"
    ).style.display="block";

    try{

        let response =
        await fetch(
            "http://127.0.0.1:5000/chat",
            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    question:question

                })

            }
        );

        let data =
        await response.json();

        document.getElementById(
            "loading"
        ).style.display="none";

        document.getElementById(
            "answer"
        ).innerHTML =
        data.answer;

        speak(data.answer);

    }

    catch(error){

        document.getElementById(
            "loading"
        ).style.display="none";

        document.getElementById(
            "answer"
        ).innerHTML =
        "Error connecting backend";
    }
}

function startVoice(){

    const recognition =
    new webkitSpeechRecognition();

    recognition.lang =
    "en-US";

    recognition.start();

    recognition.onresult =
    function(event){

        let text =
        event.results[0][0].transcript;

        document.getElementById(
            "question"
        ).value = text;

        askAI();
    };
}

function speak(text){

    let speech =
    new SpeechSynthesisUtterance(
        text
    );

    speech.lang =
    "en-US";

    window.speechSynthesis.speak(
        speech
    );
}
async function analyzeReport(){

    const file =
    document.getElementById(
        "reportFile"
    ).files[0];

    if(!file){
        alert("Please select a report");
        return;
    }

    let formData =
    new FormData();

    formData.append(
        "file",
        file
    );

    let response =
    await fetch(
        "http://127.0.0.1:5000/analyze-report",
        {
            method:"POST",
            body:formData
        }
    );

    let data =
    await response.json();

    document.getElementById(
        "reportResult"
    ).innerHTML =
    data.analysis;
}