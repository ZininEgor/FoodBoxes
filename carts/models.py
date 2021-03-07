from django.db import models


class CartItem(models.Model):
    item = models.ForeignKey(
        to='items.Item',
        on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        to='Cart',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    @property
    def total_price(self):
        return self.price * self.quantity


class Cart(models.Model):
    items = models.ManyToManyField(
        to='items.Item',
        through=CartItem,
    )

    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
    )

    @property
    def total_coast(self):
        total_price_list = map(lambda item: item.total_price, self.cart_items.all())
        return sum(total_price_list)
