from django.db import models
from store.models import  Product
from django.shortcuts import reverse
from store.models import Variation
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation, blank=True)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        return self.quantity*self.product.price

    def get_url(self):
        return reverse("store:product_details", args=[self.product.category.slug, self.product.slug])

    def __unicode__(self):
        return self.product