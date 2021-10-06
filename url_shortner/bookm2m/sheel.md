In [4]: b1 = Book(title='Networking')

In [5]: b1.save()

In [6]: b2 = Book(title='Raspberry')

In [7]: b2.save()

In [9]: a1= Author(name="Rabin")

In [10]: a1.save()

In [11]: a2 = Author(name='rabina')

In [12]: a2.save()

In [13]: Authored(book=b1,author=a2).save()

In [14]: Authored(book=b2,author=a1).save()

In [15]: Authored(book=b2,author=a2).save()

In [16]: b1.authors.values()
Out[16]: <QuerySet [{'id': 2, 'name': 'rabina'}]>

In [17]: a1.books.values()
Out[17]: <QuerySet [{'id': 2, 'title': 'Raspberry'}]>

In [18]: b2.authors.values()
Out[18]: <QuerySet [{'id': 1, 'name': 'Rabin'}, {'id': 2, 'name': 'rabina'}]>

In [19]: a2.books.values()
Out[19]: <QuerySet [{'id': 1, 'title': 'Networking'}, {'id':
2, 'title': 'Raspberry'}]>
