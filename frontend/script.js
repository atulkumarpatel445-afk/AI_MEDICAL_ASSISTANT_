async function askAI() {

    let question = document.getElementById("question").value;

    if (question === "") {
        alert("Enter a question");
        return;
    }

    document.getElementById("loading").style.display = "block";

    try {

        let response = await fetch(
            "http://127.0.0.1:5000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

        let data;

        // Handle non-2xx responses gracefully
        if (response.ok) {
            data = await response.json();
        } else {
            // Try parsing JSON error, otherwise read plain text
            try {
                data = await response.json();
            } catch (e) {
                const text = await response.text();
                data = { error: text || `HTTP ${response.status}` };
            }
        }

        console.log("Backend Response:", response.status, data);

        document.getElementById("loading").style.display = "none";

        if (!response.ok) {
            const err = data.error || data.message || `HTTP ${response.status}`;
            document.getElementById("answer").innerHTML = `Error: ${err}`;
            return;
        }

        let answer =
            data.answer ||
            data.response ||
            data.result ||
            data.message ||
            "No answer received";

        document.getElementById("answer").innerHTML = answer;

        speak(answer);

    } catch (error) {

        console.error(error);

        document.getElementById("loading").style.display = "none";

        document.getElementById("answer").innerHTML =
            "Error connecting backend";
    }
}

function startVoice() {

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult = function (event) {

        let text = event.results[0][0].transcript;

        document.getElementById("question").value = text;

        askAI();
    };
}

function speak(text) {

    let speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
}

async function analyzeReport() {

    const file = document.getElementById("reportFile").files[0];

    if (!file) {
        alert("Please select a report");
        return;
    }

    let formData = new FormData();

    formData.append("file", file);

    try {

        let response = await fetch(
            "http://127.0.0.1:5000/analyze-report",
            {
                method: "POST",
                body: formData
            }
        );

        let data;
        if (response.ok) {
            data = await response.json();
        } else {
            try {
                data = await response.json();
            } catch (e) {
                const text = await response.text();
                data = { error: text || `HTTP ${response.status}` };
            }
        }

        console.log("Report Response:", response.status, data);

        if (!response.ok) {
            document.getElementById("reportResult").innerHTML = `Error: ${data.error || 'Request failed'}`;
            return;
        }

        document.getElementById("reportResult").innerHTML =
            data.analysis ||
            data.result ||
            data.message ||
            "No analysis received";

    } catch (error) {

        console.error(error);

        document.getElementById("reportResult").innerHTML =
            "Error analyzing report";
    }
}