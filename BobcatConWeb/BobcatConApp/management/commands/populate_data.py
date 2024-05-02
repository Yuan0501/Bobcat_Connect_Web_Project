from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from BobcatConApp.models import Event



class Command(BaseCommand):
    help = 'Adds sample events and parties to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Adding sample events and parties...'))
        # Creating party events
        Event.objects.create(name='Birthday Bash', category='party', date=datetime.now().date(), time=datetime.now().time(), location='Club XYZ')
        Event.objects.create(name='New Year Party', category='party', date=datetime.now().date(), time=datetime.now().time(), location='The Mansion')
        Event.objects.create(name='Summer BBQ', category='party', date=datetime.now().date() + timedelta(days=7), time=datetime.now().time(), location='Backyard')
        Event.objects.create(name='Graduation Celebration', category='party', date=datetime.now().date() + timedelta(days=14), time=datetime.now().time(), location='University Hall')
        Event.objects.create(name='Beach Party', category='party', date=datetime.now().date() + timedelta(days=21), time=datetime.now().time(), location='Sandy Beach')
        Event.objects.create(name='Housewarming Party', category='party', date=datetime.now().date() + timedelta(days=28), time=datetime.now().time(), location='New Apartment')

        # Creating activity events
        Event.objects.create(name='Hiking Trip', category='activity', date=datetime.now().date(), time=datetime.now().time(), location='Mountain Peak')
        Event.objects.create(name='Cooking Class', category='activity', date=datetime.now().date(), time=datetime.now().time(), location='Chefs Kitchen')
        Event.objects.create(name='Painting Workshop', category='activity', date=datetime.now().date() + timedelta(days=7), time=datetime.now().time(), location='Art Studio')
        Event.objects.create(name='Yoga Retreat', category='activity', date=datetime.now().date() + timedelta(days=14), time=datetime.now().time(), location='Mountain Resort')
        Event.objects.create(name='Camping Trip', category='activity', date=datetime.now().date() + timedelta(days=21), time=datetime.now().time(), location='National Park')
        Event.objects.create(name='Photography Tour', category='activity', date=datetime.now().date() + timedelta(days=28), time=datetime.now().time(), location='City Center')

        self.stdout.write(self.style.SUCCESS('Sample events and parties added successfully.'))
