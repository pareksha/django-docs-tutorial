from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from polls.models import *
from django.template import loader
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.pub_date <= timezone.now():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        return HttpResponse(status=404)

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

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
