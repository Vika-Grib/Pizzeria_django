from django.db import models

class Order(models.Model):
    unique_id = models.TextField(primary_key=True, unique=True, default='')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Цена
    title = models.TextField(max_length=100, default='')  # Название пиццы
    size = models.TextField(default='')  # Описание
    image = models.TextField(default=' ')  # Изображение пиццы
    order_id = models.TextField(default='')
    status = models.TextField(default='')
    pizza_id = models.TextField(default='')


    def __str__(self):
        return self.title

