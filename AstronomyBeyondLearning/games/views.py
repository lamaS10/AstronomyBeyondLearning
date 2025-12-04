from django.shortcuts import render, redirect
import random

def all_games(request):
    return render(request, "games/all_games.html")



def true_false_game(request):

    facts = [
        {"statement": "Venus rotates backward compared to most planets.", "is_true": True},
        {"statement": "Mars has five moons.", "is_true": False},
        {"statement": "Jupiter is the largest planet in the solar system.", "is_true": True},
        {"statement": "The Sun is a planet.", "is_true": False},
    ]

    fact = random.choice(facts)

    user_answer = None
    result = None

    if request.method == "POST":
        user_answer = request.POST.get("answer")
        correct_answer = "true" if fact["is_true"] else "false"
        result = (user_answer == correct_answer)

    return render(request, "games/true_false.html", {
        "fact": fact,
        "result": result,
        "user_answer": user_answer,
    })

