import csv
from laptop.models import Laptop,Brand

# python manage.py runscript laptop_load
def run():
    fhand = open('laptop/lap.csv')
    reader = csv.reader(fhand)
    next(reader) # Advance pass the header | Skip header

    Laptop.objects.all().delete()
    Brand.objects.all().delete()

    for row in reader:
        print(row)

        b,created = Brand.objects.get_or_create(name=row[1])
        c = Laptop(name = row[0],brand = b,weight=row[2])
        c.save()