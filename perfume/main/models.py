from django.db import models
import logging

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

logger = logging.getLogger(__name__)

# Create your models here.
class Photo(models.Model):
    title = models.CharField("Название фото", max_length=256, null=False, blank=False)

    photo = models.ImageField("Фото", upload_to="media/common/")

    

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.id} - {self.title}"


class ProductVolume(models.Model):
    title = models.CharField("Название единицы объёма", max_length=256, null=False, blank=False)

    class Meta:
        verbose_name = "Объём продукции"
        verbose_name_plural = "Объёмы продукции"

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    titleRU = models.CharField("Название категории RU", max_length=256, null=False, blank=False)
    titleUZ = models.CharField("Название категории UZ", max_length=256, null=False, blank=False)


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.id} - {self.titleRU}"


class Product(models.Model):
    titleRU = models.CharField("Название продукта RU", max_length=256, default="Без названия", null=True, blank=True)
    titleUZ = models.CharField("Название продукта UZ", max_length=256, default="Без названия", null=True, blank=True)

    photo = models.ImageField("Фото", upload_to="media/products/")

    category = models.ManyToManyField(Category, verbose_name="Категория")

    descriptionRU = models.TextField("Описание на русском")
    descriptionUZ = models.TextField("Описание на узбекском")

    active = models.BooleanField("Активность", default=False)

    volume = models.ManyToManyField(ProductVolume, verbose_name="Объём")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.id} - {self.titleRU}"

    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    #     product = Product.objects.get(id=self.id)
    #     logger.error(product)
    #     logger.error(product.volume)


        


class PriceForVolume(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    volume = models.ForeignKey(ProductVolume, on_delete=models.CASCADE, verbose_name="Объём")

    price = models.PositiveIntegerField("Цена", default="0")

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"

    def __str__(self):
        return f"{self.product} - {self.volume}"


def save_product(sender, instance, pk_set, **kwargs):
    logger.error(sender.id)
    logger.error(sender)
    logger.error(instance)
    logger.error(f"pk_set {pk_set}")

    

    for a in pk_set:
        try:
            test = PriceForVolume.objects.filter(product=instance).get(volume=ProductVolume.objects.get(id=a))
        except Exception as e:
            price = PriceForVolume()
            price.product = instance
            price.volume = ProductVolume.objects.get(id=a)
            price.price = 0
            price.save()

            logger.error("price saved")



m2m_changed.connect(save_product, sender=Product.volume.through)

