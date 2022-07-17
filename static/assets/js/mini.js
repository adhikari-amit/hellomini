
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_IMG = "static/icon.png";
const PERSON_IMG = "static/man.png";
const BOT_NAME = "mini";
const PERSON_NAME = "You";

msgerForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  let msg = msgText.replace("?", "");
  botResponse(msg);
});

function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
`;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(rawText) {
  // Bot Response
  $.get("/get", { msg: rawText }).done(function (data) {
    console.log(rawText);
    console.log(data);

    const msgText = data;
    textToAudio(msgText);
    appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
  });
}

function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

document.getElementById("msg-info-time").innerHTML = formatDate(
  new Date()
);

function textToAudio(msg) {
  let speech = new SpeechSynthesisUtterance();
  speech.lang = "en-US";
  speech.text = msg;
  speech.volume = 1;
  speech.rate = 1;
  speech.pitch = 1;
  voices = speechSynthesis.getVoices();
  if (voices.length !== 0) {
    speech.voice = voices[1];
    window.speechSynthesis.speak(speech);
  }
}

function detectvoice() {
  var recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.onresult = function (event) {
    document.getElementById("textInput").value =
      event.results[0][0].transcript;
  };
  recognition.start();
}
