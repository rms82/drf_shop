from django.core.management.base import BaseCommand

from faker import Faker

from blog.models import Category

faker = Faker()


class Command(BaseCommand):
    help = "Insert blog category data using Faker"

    def handle(self, *args, **options):
        Category.objects.all().delete()

        user_input = int(input("Enter number of Category: "))

        for _ in range(user_input):
            title = faker.job()
            Category.objects.create(name=title)

            print("Post created.....")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {user_input} category")
        )
