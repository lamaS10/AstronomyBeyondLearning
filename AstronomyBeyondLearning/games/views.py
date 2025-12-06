from django.shortcuts import render, redirect
import random
import json
from pathlib import Path

def load_questions():
    file_path = Path(__file__).resolve().parent / "questions.json"
    with open(file_path, "r") as f:
        return json.load(f)


def game(request):
    return render(request, "games/game.html")

def multiple_choice_game(request):

    if request.GET.get("reset_quiz"):
        request.session.pop("questions", None)
        request.session.pop("score", None)
        request.session.pop("q_index", None)

        if request.GET.get("go_back"):
            return redirect("games:game")

    TOTAL = 5

    if "questions" not in request.session:
        all_q = load_questions()
        random.shuffle(all_q)
        request.session["questions"] = all_q[:TOTAL]
        request.session["score"] = 0
        request.session["q_index"] = 0

    questions = request.session["questions"]
    q_index = request.session["q_index"]
    score = request.session["score"]

    if request.GET.get("next"):
        request.session["q_index"] = q_index + 1
        return redirect("games:multiple_choice")
    
    if q_index >= TOTAL:
        return render(request, "games/mc_quiz.html", {
            "game_over": True,
            "score": score,
            "total": TOTAL
        })

    current = questions[q_index]


    if request.method == "POST":
        selected = request.POST.get("answer")
        correct = current["correct"]

        # إذا الوقت انتهى وما جاوب المستخدم
        if selected == "NONE":
            return render(request, "games/mc_quiz.html", {
                "question": current,
                "feedback": True,
                "selected": None,
                "correct": correct,
                "correct_text": current["options"][correct],
                "index": q_index + 1,
                "score": score,
                "total": TOTAL,
                "show_next": True,
                "time_out": True
            })

        # إذا المستخدم جاوب فعلاً
        if selected == correct:
            request.session["score"] = score + 1

        return render(request, "games/mc_quiz.html", {
            "question": current,
            "feedback": True,
            "selected": selected,
            "correct": correct,
            "correct_text": current["options"][correct],
            "index": q_index + 1,
            "score": request.session["score"],
            "total": TOTAL,
            "show_next": True
        })


        return render(request, "games/mc_quiz.html", {
            "question": current,
            "feedback": True,
            "selected": selected,
            "correct": correct,
            "correct_text": current["options"][correct],
            "index": q_index + 1,
            "score": request.session["score"],
            "total": TOTAL,
            "show_next": True
        })

    return render(request, "games/mc_quiz.html", {
        "question": current,
        "score": score,
        "index": q_index + 1,
        "total": TOTAL
    })
