from django.core.management.base import BaseCommand

from faker import Faker

from ...models import Post

faker = Faker()


class Command(BaseCommand):
    help = "Insert Post data using Faker"

    def handle(self, *args, **options):
        Post.objects.all().delete()

        user_input = int(input("Enter number of posts: "))

        for _ in range(user_input):
            title = faker.job()
            Category.objects.create(title=title)

            print("Post created.....")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {user_input} posts")
        )
