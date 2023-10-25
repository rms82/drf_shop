from django.core.management.base import BaseCommand

from faker import Faker
from random import randint, choice

from ...models import Cart, CartItem, Product

faker = Faker()


class Command(BaseCommand):
    help = "Insert Cart data using Faker"

    def handle(self, *args, **options):
        CartItem.objects.all().delete()
        Cart.objects.all().delete()

        products = list(Product.objects.values_list('pk', flat=True))

        user_input = int(input("Enter number of carts: "))

        for _ in range(user_input):
            cart = Cart.objects.create()

            for sth in range(1, randint(2,10)):
                cartitem = CartItem.objects.create(
                    cart=cart,
                    product_id=choice(products),
                    quantity=randint(1,10)
                )

            print('Cart created.....')
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {user_input} carts')
        )


