# Model

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["headline"]

## Commands

-- Create a few Reporters:
>>> r = Reporter(first_name="John", last_name="Smith", email="john@example.com")
>>> r.save()
>>> r2 = Reporter(first_name="Paul", last_name="Jones", email="paul@example.com")
>>> r2.save()

Create an Article:
>>> a = Article(id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
>>> a.save()

-- Create an Article via the Reporter object:
>>> new_article = r.article_set.create(headline="John's second story", pub_date=date(2005, 7, 29))

-- Create a new article:
>>> new_article2 = Article.objects.create(headline="Paul's story", pub_date=date(2006, 1, 17), reporter=r)
>>> new_article2.reporter
>>> new_article2.reporter.id
>>> r.article_set.all()

-- Add the same article to a different article set - check that it moves:
>>> r2.article_set.add(new_article2)
>>> new_article2.reporter.id
>>> new_article2.reporter

-- Note that in the last example the article has moved from John to Paul.

## lookups
>>>
>>> r.article_set.filter(headline__startswith="This")
>>> Article.objects.filter(reporter__first_name="John")
>>> Article.objects.filter(reporter__pk=1)
>>> Article.objects.filter(reporter__in=[1, 2]).distinct()
-- Querying in the opposite direction:
>>> Reporter.objects.filter(article__pk=1)
>>> Reporter.objects.filter(article=1)
>>> Reporter.objects.filter(article=a)

-- Counting in the opposite direction works in conjunction with distinct():
>>> Reporter.objects.filter(article__headline__startswith="This").count()
>>> Reporter.objects.filter(article__headline__startswith="This").distinct().count()

-- Queries can go round in circles:
>>> Reporter.objects.filter(article__reporter__first_name__startswith="John")
>>> Reporter.objects.filter(article__reporter__first_name__startswith="John").distinct()
>>> Reporter.objects.filter(article__reporter=r).distinct()

