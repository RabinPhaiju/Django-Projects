import asyncio
from django.forms import BaseFormSet, HiddenInput, formset_factory
from django.shortcuts import get_object_or_404, render,get_list_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.template import loader
from django.views import View, generic

from .utils import handle_uploaded_file
from .models import ContactForm, Question,Choice, UploadFileForm
from django.utils import timezone

### We can use either generic views or function-based views

# ---------- Using generic views -----------
# TODO https://docs.djangoproject.com/en/5.1/ref/class-based-views/
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


# -------------- Class based views ----------------
# https://docs.djangoproject.com/en/5.1/topics/class-based-views/intro/
class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse("result")
    def post(self, request):
        # <view logic>
        return HttpResponse("post result")

class AsyncView(View):
    async def get(self, request, *args, **kwargs):
        # Perform io-blocking view logic using await, sleep for example.
        await asyncio.sleep(1)
        return HttpResponse("Hello async world!")


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
    # get_list_or_404() 
    # TODO https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/
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


# forms.Form
# https://docs.djangoproject.com/en/5.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/5.1/topics/forms/formsets/#using-more-than-one-formset-in-a-view
class BaseArticleFormSet(BaseFormSet):
    def get_deletion_widget(self):
        return HiddenInput(attrs={"class": "deletion"})

def contactFormset(request):
    ContactFormSet = formset_factory(ContactForm,extra=1,max_num=2) # formset=BaseArticleFormSet,can_delete=True)
    if request.method == "POST":
        formset = ContactFormSet(request.POST,request.FILES)
        if formset.is_valid():
            for form in formset:
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                sender = form.cleaned_data.get('sender')
                date = form.cleaned_data.get('date')
                cc_myself = form.cleaned_data.get('cc_myself')
                recipients = ["info@example.com"]
                if cc_myself:
                    recipients.append(sender)

                print(recipients[0]+" "+subject+" "+message+" "+sender+" "+str(date))
        formset = ContactFormSet()

        return render(request, "contact_form.html", {"form": formset,"message": "Thanks for contact"})
    else:
        formset = ContactFormSet(initial=[
            {
                'subject':'this is a subject',
                'message':'this is a message',
                'sender':'sender@gmail.com',
                'date':'2022-2-2',
                'cc_myself':True
            }
        ])

    return render(request, "contact_form.html", {"form": formset})

def contactForm(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        print(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            date = form.cleaned_data['date']
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)

            print(recipients[0]+" "+subject+" "+message+" "+sender+" "+str(date))
            return render(request, "contact_form.html", {"form": form,"message": "Thanks for contact"})
    else:
        form = ContactForm() #default way
    return render(request, "contact_form.html", {"form": form})
# ------------------using generic views ----------------
class ContactFormView(generic.FormView):
    template_name = "contact_form.html"
    form_class = ContactForm
    success_url = "/polls/contact/"

    def form_valid(self, form):
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]
        sender = form.cleaned_data["sender"]
        date = form.cleaned_data['date']
        cc_myself = form.cleaned_data["cc_myself"]

        recipients = ["info@example.com"]
        if cc_myself:
            recipients.append(sender)

        print(recipients[0]+" "+subject+" "+message+" "+sender+" "+str(date))
        return super().form_valid(form)

# File upload
# TODO https://docs.djangoproject.com/en/5.1/topics/http/file-uploads/#top
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid(): # validation
            handle_uploaded_file(request.FILES["file"])
            return render(request, "upload.html", {'form': form,"message": "File uploaded successfully"})
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
