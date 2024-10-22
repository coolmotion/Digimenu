import random
from django.core.management.base import BaseCommand
from cart.models import Order, OrderItem
from main.models import Portion, Profile
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Generates random orders and their order items'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of orders to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        resturants = Profile.objects.all()  # Get all resturants
        portions = Portion.objects.all()  # Get all portions

        if not resturants.exists():
            self.stdout.write(self.style.ERROR("No restaurants found. Please add restaurants before running this command."))
            return

        if not portions.exists():
            self.stdout.write(self.style.ERROR("No portions found. Please add portions before running this command."))
            return

        for _ in range(total):
            # Randomly select a restaurant
            resturant = random.choice(resturants)

            # Create a random order
            order = Order.objects.create(
                phone=fake.phone_number(),
                table_no=random.randint(1, 20),
                amount_paid=random.uniform(10.0, 300.0),
                resturant=resturant
            )

            # Create order items for the order
            for _ in range(random.randint(1, 5)):  # Create 1 to 5 order items
                portion = random.choice(portions)
                OrderItem.objects.create(
                    order=order,
                    portion=portion,
                    quantity=random.randint(1, 10),
                    price=portion.price  # Assuming price is the price of the portion
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully added order: {order} with items'))

        self.stdout.write(self.style.SUCCESS(f'Successfully added {total} random orders'))
