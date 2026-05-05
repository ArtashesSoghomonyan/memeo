from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    questions = Question.objects.all()
    return render(request, 'polls/index.html', {'questions': questions})


def vote(request, question_id):
    if not request.user.is_authenticated:
        # We send an empty response with the redirect header
        response = HttpResponse(status=204)  # 204 No Content
        response['HX-Redirect'] = reverse('login')
        return response

    question = get_object_or_404(Question, pk=question_id)

    # Check if the user already has a vote linked to ANY choice for this question
    already_voted = question.choice_set.filter(votes=request.user).exists()  # type: ignore

    if request.method == "POST" and not already_voted:
        choice_id = request.POST.get('choice')
        if choice_id:
            selected_choice = get_object_or_404(Choice, pk=choice_id)
            selected_choice.votes.add(request.user)
            # Update the variable since they just voted
            already_voted = True

    return render(
        request,
        'polls/partials/poll_card.html',
        {
            'question': question,
            'user_has_voted': already_voted,
        },
    )
