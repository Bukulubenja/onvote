from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Voter, Position, Candidate, Vote

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

    positions = Position.objects.all()

    if request.method == "POST":

        with transaction.atomic():

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
        "positions": positions
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




def admin_login(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:
                login(request, user)
                return redirect('dashboard')

            messages.error(
                request,
                "You are not authorized to access the admin dashboard."
            )

        else:
            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "admin_login.html"
    )




@login_required
def dashboard(request):

    if not request.user.is_staff:
        return HttpResponseForbidden("Access Denied")

    total_voters = Voter.objects.count()
    total_votes = Vote.objects.count()
    total_positions = Position.objects.count()
    total_candidates = Candidate.objects.count()

    voters_who_voted = Vote.objects.values('voter').distinct().count()
    turnout = round((voters_who_voted / total_voters) * 100, 1) if total_voters > 0 else 0

    results = []

    positions = Position.objects.all()

    for position in positions:

        position_votes = Vote.objects.filter(position=position)

        total_position_votes = position_votes.count()

        candidates = Candidate.objects.filter(position=position)

        candidates_data = []

        for candidate in candidates:

            votes = position_votes.filter(candidate=candidate).count()

            percentage = round(
                (votes / total_position_votes) * 100,
                1
            ) if total_position_votes > 0 else 0

            candidates_data.append({
                "candidate": candidate,
                "votes": votes,
                "percentage": percentage
            })

        candidates_data.sort(key=lambda x: x["votes"], reverse=True)

        results.append({
            "position": position,
            "candidates": candidates_data
        })

    return render(request, "dashboard.html", {
        "total_voters": total_voters,
        "total_votes": total_votes,
        "total_positions": total_positions,
        "total_candidates": total_candidates,
        "turnout": turnout,
        "results": results
    })