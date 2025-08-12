from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
import re

def get_random_fact():
    """Fetch a random true fact from API"""
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=5)
        if r.status_code == 200:
            return r.json().get("text")
    except:
        pass
    return "Bananas grow on trees."  # fallback

def make_fake_fact():
    """Take a real fact and slightly change it to make it false"""
    fact = get_random_fact()

    if re.search(r"\d+", fact):  # if fact has a number, change it
        return re.sub(r"\d+", str(random.randint(1, 99)), fact)
    else:
        words = fact.split()
        if len(words) > 3:
            idx = random.randint(0, len(words)-1)
            words[idx] = random.choice(["unicorns", "chocolate", "aliens", "robots"])
            return " ".join(words)
        return fact + " in space."

def play_game(request):
    action = request.GET.get("action")

    if action == "next" or "statements" not in request.session:
        # New round
        fact1 = get_random_fact()
        fact2 = get_random_fact()
        lie = make_fake_fact()

        statements = [(fact1, "truth"), (fact2, "truth"), (lie, "lie")]
        random.shuffle(statements)
        request.session["statements"] = statements
        show_answer = False
    else:
        # Use saved round
        statements = request.session.get("statements", [])
        show_answer = (action == "reveal")

    return render(request, "game/play.html", {
        "statements": statements,
        "show_answer": show_answer
    })
