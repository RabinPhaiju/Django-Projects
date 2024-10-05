from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 3662f6b (added file/image upload)
from .models import Question,Choice,Car

class ChoiceInline(admin.TabularInline): # tabular
# class ChoiceInline(admin.StackedInline): # stacked
    model = Choice
    extra = 1 # default is 3

class QuestionAdmin(admin.ModelAdmin):
    # change order of the fields
    # fields = ["pub_date", "question_text"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_display = ('question_text','pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

# admin.site.register(Question) # default form
admin.site.register(Question,QuestionAdmin)


admin.site.register(Choice)
<<<<<<< HEAD
admin.site.register(Car)
=======
from .models import Question,Choice

admin.site.register(Question)
admin.site.register(Choice)
>>>>>>> c296fdb (added django5.1 tutorial)
=======
admin.site.register(Car)
>>>>>>> 3662f6b (added file/image upload)
