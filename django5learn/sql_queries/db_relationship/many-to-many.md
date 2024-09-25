# Many-To-Many Relationships

## Models

class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline

## Commands

-- Create a few Publications:
>>> p1 = Publication(title="The Python Journal")
>>> p1.save()
>>> p2 = Publication(title="Science News")
>>> p2.save()
>>> p3 = Publication(title="Science Weekly")
>>> p3.save()

-- Create an Article:
>>> a1 = Article(headline="Django lets you build web apps easily")
>>> a1.save()
>>> a1.publications.add(p1)

-- Create and add a Publication to an Article in one step using create():
>>> new_publication = a2.publications.create(title="Highlights for 
Children")

-- Article objects have access to their related Publication objects:
>>> a1.publications.all()
>>> a2.publications.all()

-- Publication objects have access to their related Article objects:
>>> p2.article_set.all()
>>> p1.article_set.all()
>>> Publication.objects.get(id=4).article_set.all()

-- Many-to-many relationships can be queried using lookups across relationships:
>>> Article.objects.filter(publications__id=1)
>>> Article.objects.filter(publications__pk=1)
>>> Article.objects.filter(publications=1)
>>> Article.objects.filter(publications=p1)
>>> Article.objects.filter(publications__title__startswith="Science")
>>> Article.objects.filter(publications__title__startswith="Science").distinct()

-- The count() function respects distinct() as well:
>>> Article.objects.filter(publications__title__startswith="Science").count()
>>> Article.objects.filter(publications__title__startswith="Science").distinct().count()
>>> Article.objects.filter(publications__in=[1, 2]).distinct()
>>> Article.objects.filter(publications__in=[p1, p2]).distinct()

-- Reverse m2m queries are supported (i.e., starting at the table that doesn’t have a ManyToManyField):
>>> Publication.objects.filter(id=1)
>>> Publication.objects.filter(pk=1)
>>> Publication.objects.filter(article__headline__startswith="NASA")
>>> Publication.objects.filter(article__id=1)
>>> Publication.objects.filter(article__pk=1)
>>> Publication.objects.filter(article=1)
>>> Publication.objects.filter(article=a1)
>>> Publication.objects.filter(article__in=[1, 2]).distinct()
>>> Publication.objects.filter(article__in=[a1, a2]).distinct()

