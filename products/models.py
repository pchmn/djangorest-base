from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from products.utils import unique_slugify


class Category(models.Model):
    """
    Représente les catégories de produits
    """
    name = models.CharField(max_length=200, verbose_name="Nom")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Représente un produit
    """
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    price = models.IntegerField(default=0, blank=True, verbose_name="Prix")
    category = models.ForeignKey(Category, verbose_name="Catégorie", related_name="products")
    image = models.ImageField(upload_to='media/product_image/', verbose_name="Image")

    def save(self, *args, **kwargs):
        # slug
        unique_slugify(self, self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)
