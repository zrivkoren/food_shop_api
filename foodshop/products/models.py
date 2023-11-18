import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='uploads/categories/')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    image_large = models.ImageField(upload_to='uploads/products/large/')
    image_medium = models.ImageField(upload_to='uploads/products/medium/', blank=True, null=True)
    image_small = models.ImageField(upload_to='uploads/products/small/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image_large:
            img = Image.open(self.image_large.path)
            original_path = self.image_large.path

            output_size = (800, 800)
            img.thumbnail(output_size, Image.LANCZOS)
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            self.image_large.save(os.path.basename(self.image_large.path), ContentFile(img_io.getvalue()), save=False)

            output_size = (500, 500)
            img.thumbnail(output_size, Image.LANCZOS)
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            self.image_medium.save(os.path.basename(self.image_large.path), ContentFile(img_io.getvalue()), save=False)

            output_size = (300, 300)
            img.thumbnail(output_size, Image.LANCZOS)
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            self.image_small.save(os.path.basename(self.image_large.path), ContentFile(img_io.getvalue()), save=False)

            if os.path.exists(original_path):
                os.remove(original_path)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
