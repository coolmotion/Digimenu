import random
from django.core.management.base import BaseCommand
from main.models import Product, Portion, Category, Profile
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Adds random products and their portions to the Product model'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of products to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        categories = Category.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR("No categories found. Please add categories before running this command."))
            return

        for _ in range(total):
            # Randomly select a category for the product
            category = random.choice(categories)
            
            # Use the restaurant associated with this category
            restaurant = category.resturant
            
            # Create a random product
            product = Product.objects.create(
                name=fake.word(),
                resturant=restaurant,  # Set the restaurant based on the category's restaurant
                menu=category,
                description=fake.sentence(),
                stock=random.randint(1, 50),
                is_available=bool(random.getrandbits(1)),
            )

            # Create portions for the product
            for _ in range(random.randint(1, 3)):  # Create 1 to 3 portions
                Portion.objects.create(
                    product=product,
                    name=fake.word(),
                    price=random.uniform(5.0, 50.0),
                    size=random.choice(['small', 'medium', 'large']),
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name} with portions'))

        self.stdout.write(self.style.SUCCESS(f'Successfully added {total} random products'))
