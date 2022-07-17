import requests

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "hii", "hiii", "hiiii",)
GREETING_RESPONSES = ["hi", "hii", "hey", "hi there", "hello", "I am glad! You are talking to me", "What's up?"]


def weather():
    city = "kolkata"
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=68cef33e0cd7fa77f8b5e1c02a81f432&units=metric").json()

    monsoon = res["weather"][0]["description"]
    temp = res["main"]["temp"]
    return monsoon, temp


name = "Hello mini"
monsoon, temp = weather()
mood = "Smiley"

resp = {
    "what is your name": [
        "They call me {0}".format(name),
        "I usually go by {0}".format(name),
        "My name is the {0}".format(name)
    ],

    "who are you":[
        "I am hellomini"
    ],

    "good morning": [
        "Good Morning.",
        "Have a nice day.",
        "Nice to hear you.",
        "Hello there!",
        "Rise and shine!",
        "Good day to you.",
    ],
    "good night": [
        "Good Night.",
        "Sweet Dreams.",
        "Lights out!",
        "Rest time for blossoms.",
        "Have a Good Sleep."
    ],

    "good evening": [
        "Have a wonderful evening!",
        "Have a great evening!",
        "I hope you have a great evening!",
        "I hope you enjoy your evening!",
        "Wishing you a fabulous evening.",
        "Have an amazing evening!"
    ],

    "are you a bot": [
        "yes i am a bot, but i am a good one. Let me prove it. How can i help you?"
    ],
    "where do you live": [
        "My Coordinate is 127.0.0.1",
        "I'm from localhost.",
        "You can find me on 127.0.0.1"
    ],
    "who made you": [
        "Its a secret.",
        "You might Know him.",
        "He is someone from human world."
    ],
    "weather report": [
        "The weather is {0}. It's {1} °C.".format(monsoon,temp),
        "It's {0} today. It's {1} °C outside.".format(monsoon,temp)
    ],

    "how are you": [
        "I am feeling {0}".format(mood),
        "{0}! How about you?".format(mood),
        "I am {0}! How about yourself?".format(mood),
    ],
    "are you ok":[
        "yes i am completely fine."
    ],
    "good":[
        "gald to hear that",
        "nice to hear that"
    ],
    "Ok":[
        'yup',
        'welcome'
    ]
}
