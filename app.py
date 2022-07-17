import random
import string
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

import pywhatkit
import wikipedia
import webbrowser
import os

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

from common import resp, GREETING_INPUTS, GREETING_RESPONSES

f = open('chatbot.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()

# converts to lowercase
nltk.download('punkt')  # This tokenizer divides a text into a list of sentences by using an unsupervised algorithm.
nltk.download('wordnet')  # WordNet is a semantically-oriented dictionary of English included in NLTK.
nltk.download('omw-1.4')
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words  `

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        robo_response = robo_response + "I'm sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


app = Flask(__name__)
app.static_folder = 'static'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'chatbot'
mysql = MySQL(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/bot")
def bot():
    return render_template("index.html")


@app.route("/subscribe", methods=['POST'])
def subscribe():
    if request.method == "POST":
        subscriber_email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM subscriber WHERE email = % s', (subscriber_email,))
        account = cursor.fetchone()
        if account:
            msg = 'Email already subscribed !'
        elif not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', subscriber_email):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO subscriber(email) VALUES (% s)', (subscriber_email,))
            mysql.connection.commit()
            msg = 'You have successfully Subscribed !'
    else:
        msg = 'Please fill out the form !'
    return render_template('home.html', msg=msg)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        contact_name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        phone = request.form['phone']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            msg0 = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO contact(name,email,subject,phone,message) VALUES (% s,%s,%s,%s,%s)',
                           (contact_name, email, subject, phone, message,))
            mysql.connection.commit()
            msg0 = 'We Have Got your message. We will contact you shortly !'
    else:
        msg0 = 'Please fill out the form !'
    return render_template('contact.html', msg0=msg0)


@app.route("/get")
def get_bot_response():

    user_response = request.args.get('msg')
    user_response = user_response.lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':
            userText = "You are welcome.."
            return userText
        else:
            if greeting(user_response) is not None:
                return greeting(user_response)

            if user_response == 'time' or user_response == 'what is the time':
                now = datetime.now()
                current_time = now.strftime("%I:%M:%p")
                return current_time

            if user_response in resp:
                userText = random.choice(resp[user_response])
                return userText

            if 'play' in user_response:
                song = user_response.replace('play','')
                try:
                    pywhatkit.playonyt(song)
                    UserText = "Playing On Youtube..."
                except:
                    UserText="Sorry! Can't find anything."    
                return UserText

            if 'news' in user_response:
                webbrowser.open("https://www.bbc.com/news")
                userText="Opening top news."
                return userText
                 
            if 'open code' in user_response:
                codepath="C:\\Users\\gouri\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codepath)
                user_text="Opening Vs code"
                return user_text

            if 'who is' or 'what is' in user_response:
                person=user_response.replace('who is','')
                try:
                    info=wikipedia.summary(person,1)
                except:
                    info="Sorry! Can't find anything."
                    return info
                return info

            else:
                userText = response(user_response)
                sent_tokens.remove(user_response)
                return userText

    else:
        userText = "Bye! take care.."
        return userText


if __name__ == "__main__":
    app.run()
