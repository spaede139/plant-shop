from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class product_category(moddel.Model):
    name=models.CharField(max_length=100)
    name=models.TextField()
    
    def __str__(self)in stockdigits
        return self.name
class product (model.Model):
    name=models.CharField(max_length=200)
    description = models.TextField()
    product_photo = models.ImageField(upload_to='products/', verbose_name="Фото товара")
    price = models.DecimalField(max_digits=10,decimal_plaxes=2,validators=[MinValueValidator(0)])
    in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    category=models.ForeignKey(product_cotegory, on_delete=models.CASCADE)
    producer=models.ForeignKey(manufacturer ,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class manufacturer(model.Model):
    name=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return self.name
class Cart(models.Model):
    user_name=models.OneToOneField(manufacturer ,on_delete=models.CASCADE)
    creation_data=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Корзина пользователя {self.user_name}."

