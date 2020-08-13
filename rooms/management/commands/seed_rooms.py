import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command register test rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many room do you want to register?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 10),
                "price": lambda x: random.randint(10000, 300000),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        for pk in created_clean:
            room_choice = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room_choice,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                amenity_choice = random.randint(0, 15)
                if amenity_choice % 2 == 0:
                    room_choice.amenities.add(a)

            for f in facilities:
                facility_choice = random.randint(0, 15)
                if facility_choice % 2 == 0:
                    room_choice.facilities.add(f)

            for r in house_rules:
                rule_choice = random.randint(0, 15)
                if rule_choice % 2 == 0:
                    room_choice.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS("Test rooms registered"))
