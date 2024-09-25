# Commands

## Create
>>>
>>> from sql_queries.models import Blog,Author,Entry
>>> b = Blog(name="Rabin blog", tagline="All the latest Rabs new;.")
>>> b.save()
>>> a = Author(name="Rabin", email="<RqDmX@example.com>")
>>> a.save()
>>> e = Entry(
     headline="Rabin's entry",
     body_text="Rabin's entry body",
     pub_date="2005-05-01",
)
>>> e.save()

## Update
>>>
>>> b5.name = "New name"
>>> b5.save()

## Saving ForeignKey and ManyToManyField fields
>>>
>>> e.blog = b
>>> e.authors.add(a)
>>> e.save()

## Add to ManyToManyField
>>>
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)
>>> entry.save()

## Create and add Author to Entry in one step
>>>
>>> entry.authors.create(name="Rabin")

## Retrieving objects
>>>
>>> Blog.objects
>>> Blog.objects.all()

## Retrieving (Author objects has acess to Entry objects)
>>>
>>> a1 = Author.objects.get(name="Rabin")
>>> a1.entry_set.all()

## Retrieving specific objects with filters
>>>
>>> Entry.objects.filter(pub_date__year=2005)
>>> Entry.objects.all().filter(pub_date__year=2005) ## with default manager

## Chaining filters
>>>
>>> Entry.objects.filter(headline__startswith="Ra").exclude(
     pub_date__gte=datetime.date.today()
 ).filter(pub_date__gte=datetime.date(2005, 5, 1))

## QuerySets are lazy
>>>
>>> q = Entry.objects.filter(headline__startswith="What")
>>> q = q.filter(pub_date__lte=datetime.date.today())
>>> q = q.exclude(body_text__icontains="food")
>>> print(q)

## Retrieving a single object with get()
>>>
>>> one_entry = Entry.objects.get(pk=0)
>>> Entry.objects.get(headline__exact="Ra")
>>> Entry.objects.all()[:5]
>>> Entry.objects.order_by("headline")[0]
>>> Entry.objects.order_by("headline")[0:1].get()

## Field lookup
>>>
>>> Entry.objects.filter(pub_date__lte="2005-05-01")
>>> Entry.objects.filter(blog_id=4)

## Count and distinct
>>>
>>> Entry.objects.filter(authors__name__startswith="R").distinct().count()
>>> Entry.objects.filter(authors__name__startswith="R").distinct()
>>> Entry.objects.filter(authors__name__startswith="R").count()

## Lookups that span relationships

- This spanning can be as deep as you’d like.
- It works backwards, too. While it can be customized, by default you refer to a “reverse” relationship in a lookup using the lowercase name of the model.
>>>
>>> Blog.objects.filter(entry__headline__contains="Lennon")
>>> Blog.objects.filter(entry__authors__name="Lennon")
>>> Blog.objects.filter(entry__authors__name__contains="Lennon")
>>> Blog.objects.filter(entry__authors__name__isnull=True)
>>> Blog.objects.filter(entry__authors__isnull=False, entry__authors__name__isnull=True)

## Spanning multi-valued relationships
>>>
>>> - To select all blogs containing at least one entry from 2008 having “Lennon” in its headline
>>> Blog.objects.filter(entry__headline__contains="Lennon", entry__pub_date__year=2008)

>>> - Otherwise, to perform a more permissive query selecting any blogs with merely some entry with “Lennon” in its headline and some entry from 2008
>>> Blog.objects.filter(entry__headline__contains="Lennon").filter(
    entry__pub_date__year=2008
)
>>> Blog.objects.exclude(
    entry__in=Entry.objects.filter(
        headline__contains="Lennon",
        pub_date__year=2008,
    ),
)

## Filters can reference fields on the model
>>>
>>> Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))
>>> Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks") * 2)
>>> Entry.objects.filter(rating__lt=F("number_of_comments") + F("number_of_pingbacks"))
>>> Entry.objects.filter(authors__name=F("blog__name"))
>>> Entry.objects.filter(mod_date__gt=F("pub_date") + timedelta(days=3))
>>> Entry.objects.filter(pub_date__year=F("mod_date__year"))
>>> Entry.objects.aggregate(first_published_year=Min("pub_date__year"))

## The pk lookup shortcut
>>>
>>> Blog.objects.get(id__exact=14)  # Explicit form
>>> Blog.objects.get(id=14)  # __exact is implied
>>> Blog.objects.get(pk=14)  # pk implies id__exact
-- Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1, 4, 7])
-- Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)
>>>
-- pk lookups also work across joins
>>> Entry.objects.filter(blog__id=3) 
-- retrieve all the entries that contain a percent sign,
>>> Entry.objects.filter(headline__contains="%")

## Caching and QuerySets
>>>
>>> print([e.headline for e in Entry.objects.all()])
>>> print([e.pub_date for e in Entry.objects.all()])
-- same database query will be executed twice
-- To avoid this problem, save the QuerySet and reuse it
>>> queryset = Entry.objects.all()
>>> print([p.headline for p in queryset])  # Evaluate the query set.
>>> print([p.pub_date for p in queryset])  # Reuse the cache from the evaluation.

## When QuerySets are not cached
>>>
-- repeatedly getting a certain index in a queryset object will query the database each time
>>> queryset = Entry.objects.all()
>>> print(queryset[5])  # Queries the database
>>> print(queryset[5])  # Queries the database again
-- if the entire queryset has already been evaluated, the cache will be checked instead:
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset]  # Queries the database
>>> print(queryset[5])  # Uses cache
>>> print(queryset[5])  # Uses cache


## Asynchronous queries
>>>
-- writing asynchronous views or code, you cannot use the ORM
--  it will block up the event loop
-- get() or delete() - has an asynchronous variant (aget() or adelete()), and when you iterate over results, you can use asynchronous iteration (async for) instead.

## Query iteration
>>>
-- async for entry in Authors.objects.filter(name__startswith="A"):
    ...
