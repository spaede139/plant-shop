from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.item_price()
        return total
    
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def item_price(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
class Profile(models.Model):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Покупатель'
        ADMIN = 'admin', 'Администратор'
        MANAGER = 'manager', 'Менеджер'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True, verbose_name='Полное имя')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес')
    favorite_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Любимая категория')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER, verbose_name='Роль')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.user.is_superuser
    
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()