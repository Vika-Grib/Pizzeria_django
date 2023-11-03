from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)  # Название пиццы
    description = models.TextField()         # Описание
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Цена
    # image = models.ImageField(upload_to='pizza_images/', blank=True, null=True)  # Изображение пиццы

    def __str__(self):
        return self.name

