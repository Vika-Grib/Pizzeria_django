from django.db import models

class Product_pizza(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Цена
    title = models.TextField(max_length=100, default='')  # Название пиццы
    size = models.TextField(default='')         # Описание
    image = models.TextField(default=' ')  # Изображение пиццы
    order_id = models.TextField(default='')


    def __str__(self):
        return self.title
