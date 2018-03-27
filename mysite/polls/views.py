from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from polls.models import *
from django.template import loader
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context) #render returns an HttpResponse object of the given template rendered with the given context.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', { 'question': question, 'error_message' : "You didn't select a choice." })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) #Reverse goes to urls.py, gets the required url and then calls the view mentioned in the path() function of that url.
