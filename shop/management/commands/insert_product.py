from django.core.management.base import BaseCommand

from faker import Faker
from random import randint, choice, sample

from ...models import Product, Category

faker = Faker()


class Command(BaseCommand):
    help = "Insert Product data using Faker"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        categories = list(Category.objects.values_list('pk', flat=True))

        user_input = int(input("Enter number of products: "))

        for _ in range(user_input):
            title = faker.company()
            description = faker.paragraph(nb_sentences=5)
            price = randint(1,9999)
            inventory = randint(0,100)
            category = sample(categories, randint(1, 10))
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                inventory=inventory,
            )
            for item in category:
                product.category.add(item)

            print('Product created.....')
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {user_input} products')
        )


