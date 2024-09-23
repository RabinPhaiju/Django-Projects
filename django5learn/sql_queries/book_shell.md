# Command

## ![Aggregation](https://docs.djangoproject.com/en/5.1/topics/db/aggregation/)

>>> Book.objects.count()
>>> Book.objects.filter(publisher__name="BaloneyPress").count()

>>> Book.objects.aggregate(Avg("price", default=0))
>>> Book.objects.aggregate(Max("price", default=0))
>>> Book.objects.aggregate(price_diff=Max("price", output_field=FloatField()) - Avg("price"))

>>> pubs = Publisher.objects.annotate(num_books=Count("book"))

## Generating aggregates over a QuerySet
>>>
>>> Book.objects.all().aggregate(Avg("price")) # redundant all()
>>> Book.objects.aggregate(Avg("price")) # same as above
--
>>> Book.objects.aggregate(average_price=Avg("price"))
-- generate more than one aggregate
>>> Book.objects.aggregate(Avg("price"), Max("price"), Min("price"))

## Generating aggregates for each item in a QuerySet
>>>
>>> q = Book.objects.annotate(Count("authors"))
>>> q[0]
<Book: The Definitive Guide to Django>
>>> q[0].authors__count
2
>>> q[1]
<Book: Practical Django Projects>
>>> q[1].authors__count
1
-- OR -- (same)
>>> q = Book.objects.annotate(num_authors=Count("authors"))
>>> q[0].num_authors
2
>>> q[1].num_authors
1

## Combining multiple aggregations
>>>
>>> book = Book.objects.first()
>>> book.authors.count()
>>> book.store_set.count()
>>> q = Book.objects.annotate(Count("authors"), Count("store"))
>>> q[0].authors__count
>>> q[0].store__count

##  Count aggregate has a distinct parameter
>>>
>>> q = Book.objects.annotate(Count("authors", distinct=True), Count("store", distinct=True))
>>> q[0].authors__count
>>> q[0].store__count

## oins and aggregates
>>>
>>> Store.objects.annotate(min_price=Min("books__price"), max_price=Max("books__price"))
>>> Store.objects.aggregate(min_price=Min("books__price"), max_price=Max("books__price"))
>>> Store.objects.aggregate(youngest_age=Min("books__authors__age"))

## Following relationships backwards
>>>
>>> Publisher.objects.annotate(Count("book"))
>>> Publisher.objects.aggregate(oldest_pubdate=Min("book__pubdate"))
>>> Author.objects.annotate(total_pages=Sum("book__pages"))
>>> Author.objects.aggregate(average_rating=Avg("book__rating"))

## Aggregations and other QuerySet clauses
>>>
>>> Book.objects.filter(name__startswith="Django").annotate(num_authors=Count("authors"))
>>> Book.objects.filter(name__startswith="Django").aggregate(Avg("price"))
--
>>> Book.objects.annotate(num_authors=Count("authors")).filter(num_authors__gt=1)
--
>>> highly_rated = Count("book", filter=Q(book__rating__gte=7))
>>> Author.objects.annotate(num_books=Count("book"), highly_rated_books=highly_rated)

## order_by()
>>>
>>> Book.objects.annotate(num_authors=Count("authors")).order_by("num_authors")

## Aggregating annotations
>>>
>>> Book.objects.annotate(num_authors=Count("authors")).aggregate(Avg("num_authors"))



## ![Search](https://docs.djangoproject.com/en/5.1/topics/db/search/)

## Standard textual queries (small names only)
>>>
>>> Author.objects.filter(name__contains="Terry")
-- case-insensitive match (icontains)
>>> Author.objects.filter(name__icontains="terry")
-- When dealing with non-English names, a further improvement is to use unaccented comparison:
>>> Author.objects.filter(name__unaccent__icontains="Helen")
-- Another option would be to use a trigram_similar comparison, which compares sequences of letters
>>> Author.objects.filter(name__unaccent__lower__trigram_similar="Hélène")
--- Now we have a different problem - the longer name of “Helena Bonham Carter” doesn’t show up as it is much longer.

## Document-based search (There are many alternatives for using searching software like Elastic and Solr)
>>>
>>> Entry.objects.filter(body_text__search="cheese")
>>> Entry.objects.annotate(search=SearchVector("blog__tagline", "body_text"),).filter(search="cheese")


## ![Full text search](https://docs.djangoproject.com/en/5.1/ref/contrib/postgres/search/)