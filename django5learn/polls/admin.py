from django.contrib import admin

# Register your models here.
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
admin.site.register(Car)