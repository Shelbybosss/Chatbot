from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__, static_url_path='/static')


def get_joke():
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_url)
    joke_data = response.json()

    if "joke" in joke_data:
        return joke_data["joke"]
    elif "setup" in joke_data and "delivery" in joke_data:
        return f"{joke_data['setup']} {joke_data['delivery']}"
    else:
        return "I couldn't fetch a joke at the moment."


def get_news():
    news_url = "https://newsapi.org/v2/top-headlines"
    api_key = "33063e97a44546d8ab8e58c6e0aca254"  # Replace with your News API key
    params = {"apiKey": api_key, "country": "us"}
    response = requests.get(news_url, params=params)
    news_data = response.json()
    articles = news_data.get("articles", [])

    if articles:
        random_article = random.choice(articles)
        return f"{random_article['title']} {random_article['url']}"
    else:
        return "No news available."


def get_chuck_norris_fact():
    chuck_norris_url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(chuck_norris_url)
    fact_data = response.json()
    return fact_data.get("value", "No Chuck Norris fact available.")


def get_trivia_question():
    trivia_url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(trivia_url)
    trivia_data = response.json()

    if "results" in trivia_data and trivia_data["results"]:
        question = trivia_data["results"][0]["question"]
        return f"Question: {question}"
    else:
        return "No trivia question available."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input'].lower()

    if "1" in user_input:
        response = get_joke()
    elif "2" in user_input:
        response = get_news()
    elif "3" in user_input:
        response = get_chuck_norris_fact()
    elif "4" in user_input:
        response = get_trivia_question()
    else:
        response = "I didn't understand that. Please choose a valid option."

    return render_template('index.html', response=response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
