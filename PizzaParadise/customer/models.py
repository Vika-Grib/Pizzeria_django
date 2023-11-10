from django.db import models

class Order(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField(max_length=100, default='')  # Название пиццы
    big_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Цена
    medium_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Цена
    thin_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Цена
    ingredients = models.TextField(default='')         # Описание
    image = models.TextField(default=' ')  # Изображение пиццы
    status = models.TextField(default='')

    def __str__(self):
        return self.title

