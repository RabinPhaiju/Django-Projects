# Model

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name} the place"

class Restaurant(models.Model):
    place = models.OneToOneField(Place,
        on_delete=models.CASCADE,primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name

## Commands

-- Create a couple of Places:
>>> p1 = Place(name="Demon Dogs", address="944 W. Fullerton")
>>> p1.save()
>>> p2 = Place(name="Ace Hardware", address="1013 N. Ashland")
>>> p2.save()

-- Create a Restaurant. Pass the “parent” object as this object’s primary key:
>>> r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
>>> r.save()

-- A Restaurant can access its place:
>>> r.place

-- The place can access its restaurant:
>>> p1.restaurant

## You can query the models using lookups across relationships:

>>> Restaurant.objects.get(place=p1)
>>> Restaurant.objects.get(place__pk=1)
>>> Restaurant.objects.filter(place__name__startswith="Demon")
>>> Restaurant.objects.exclude(place__address__contains="Ashland")

-- This also works in reverse:
>>> Place.objects.get(pk=1)
>>> Place.objects.get(restaurant__place=p1)
>>> Place.objects.get(restaurant=r)
>>> Place.objects.get(restaurant__place__name__startswith="Demon")

