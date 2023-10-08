from django.core.management.base import BaseCommand

from faker import Faker

from ...models import Product, Category

faker = Faker()


class Command(BaseCommand):
    help = "None"

    def handle(self, *args, **options):
        Category.objects.all().delete()

        user_input = int(input("Enter number of categories: "))

        for _ in range(user_input):
            title = faker.job()
            Category.objects.create(title=title)

            print("Category created.....")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {user_input} categories")
        )
