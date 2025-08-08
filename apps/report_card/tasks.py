from celery import shared_task

from apps.student.models import Student

@shared_task(queue="report_tasks")
def welcome_rcs(id):
    student = Student.objects.get(id=id)
    print('-=-=-==-===-=',student)
    return True