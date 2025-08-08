# Run project
1. cp env.dev .env
2. make dev 
3. make migrate
4. make import-records for admin user and groups and other
5. call api - (swagger) - /api/docs/
    1. login - (admin,admin) - /api/v1/token/
    2. create student api - /api/v1/students/
    3. create record_card - /v1/report-cards/
    4. add marks - /api/v1/report-cards/1/add-marks/
6. make superuser (optional)

7. look -> Makefile

# Explanation on query optimization:

1. Optimize query by selecting related [fields] to reduce database hits
    - queryset = ReportCard.objects.select_related('student').prefetch_related('marks__subject').all()
            - The `ReportCard.objects.select_related('student')` is used to create a SQL join and include the related `student` object in the query to avoid additional database    queries when accessing the `student` field on each `ReportCard`.
            - The `prefetch_related('marks__subject')` is used to execute a separate query to retrieve the related `marks` and their `subject` for all `ReportCard` instances in the queryset, which are then cached for each `ReportCard` to avoid additional database hits.

    - subjects = Subject.objects.in_bulk(subject_codes, field_name='code') # get all subjects at once.
            - This is used to retrieve multiple subjects in a single query by their codes. The `in_bulk` method returns a dictionary where the codes are keys and the corresponding subjects are values.

    - Mark.objects.bulk_create(marks_to_create)
            - This is used to create multiple marks in a single query. The `bulk_create` method takes a list of Mark objects as an argument and creates them in a single query.

    - subject_averages = Mark.objects.filter(
            report_card__student=student,
            report_card__year=year
        ).values(subjectName=F('subject__name')).annotate(avg_score=Avg('score'))
            - This is used to retrieve marks for a specific student in a specific year and calculate the average score for each subject.
            - The `F` object is used to reference fields on model instances directly in queries, allowing for operations using these field values.
            - The `.annotate()` method is used to add calculated fields to the queryset, in this case, calculating the average score for each subject using the `Avg()` function.
            
    - overall_average = Mark.objects.filter(
            report_card__student=student,
            report_card__year=year
        ).aggregate(total_avg=Avg('score'))
            - This is used to retrieve marks for a specific student in a specific year and calculate the average score for all subjects.
            - The `aggregate()` method is used to calculate the average score for all subjects using the `Avg()` function.