from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.template import loader
from django.views import generic

from .utils import handle_uploaded_file
from .models import Question,Choice, UploadFileForm
from django.utils import timezone

### We can use either generic views or function-based views

# ---------- Using class-based views / generic views -----------
class IndexView(generic.ListView):
    """
    By default Listview uses template called <app name>/<model name>_list.html; we use template_name to tell ListView to use our existing "polls/index.html" template.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
            Generic view needs to know what model to use.
            Return the last five published questions.
        """
        # return Question.objects.order_by("-pub_date")[:5] # having bug of returning future questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    '''
    By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html. 
    '''
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        This method is not required. But for filtering the results.
        By default, if this method is not defined, then all the questions will be displayed.
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



# --------------- Using function-based views -----------------
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list }
    # option 1
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))

    # option 2
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # option 1
    # try:
        # question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
        # raise Http404("Question does not exist")
    
    # option 2
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data by key_name.
        post_choice = request.POST["choice"]
        selected_choice = question.choice_set.get(pk=post_choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Warning selected_choice.votes = selected_choice.votes + 1
        # https://docs.djangoproject.com/en/5.1/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing with POST data. 
        # This tip isn’t specific to Django; it’s good web development practice in general.
        # This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        
        # reverse helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view. 


# File upload
# https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/#top
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return render(request, "upload.html", {'form': form,"message": "File uploaded successfully"})
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})