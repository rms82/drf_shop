from django.core.management.base import BaseCommand

from faker import Faker
from random import randint, choice, sample

from blog.models import Post, Category
from accounts.models import ProfileUser

faker = Faker()


class Command(BaseCommand):
    help = "Insert Post data using Faker"

    def handle(self, *args, **options):
        Post.objects.all().delete()
        categories = list(Category.objects.values_list('pk', flat=True))
        users = list(ProfileUser.objects.values_list('pk', flat=True))

        user_input = int(input("Enter number of Posts: "))

        for _ in range(user_input):
            title = faker.company()
            body = faker.paragraph(nb_sentences=5)
            category = sample(categories, randint(1, 10))
            post = Post.objects.create(
                author_id=choice(users),
                title=title,
                body=body,
            )
            for item in category:
                post.category.add(item)

            print('Product created.....')
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {user_input} posts')
        )


