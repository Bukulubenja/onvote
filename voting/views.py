from django.shortcuts import render, redirect
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Voter,Position,Candidate,Vote
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("vote")

        return render(
            request,
            "login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "login.html")



@login_required
def vote_view(request):

    voter = get_object_or_404(Voter, user=request.user)
    if Vote.objects.filter(voter=voter).exists():
        return render(request, "already_voted.html")
    with transaction.atomic():
        positions = Position.objects.all()
        candidates = Candidate.objects.all()

        if request.method == "POST":
            

            for position in positions:

                selected_candidate = request.POST.get(str(position.id))

                if selected_candidate:

                    Vote.objects.create(
                        voter=voter,
                        position=position,
                        candidate_id=selected_candidate
                    )

        return render(request, "success.html")

    return render(request, "vote.html", {
        "positions": positions,
        "candidates": candidates
    })

def logout_view(request):
    logout(request)
    return redirect("login")



def success_page(request):
    response = render(request, "success.html")
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response