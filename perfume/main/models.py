from django.db import models
import logging

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from datetime import date, timedelta
from django.utils import timezone



logger = logging.getLogger(__name__)

# Create your models here.
class Photo(models.Model):
    title = models.CharField("Название фото", max_length=256, null=False, blank=False)

    photo = models.ImageField("Фото", upload_to="media/common/")

    def save(self, *args, **kwargs):
        self.title = self.title.replace("'","")
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.id} - {self.title}"


class BannerPhoto(models.Model):
    title = models.CharField("Название фото", max_length=256, null=False, blank=False)

    photo = models.ImageField("Фото", upload_to="media/common/")
    description = models.CharField("Краткое описание", max_length=1024, null=True, blank=True)

    active = models.BooleanField("Активность", default=False)

    class Meta:
        verbose_name = "Фото для баннеров"
        verbose_name_plural = "Фото для баннеров"

    def __str__(self):
        return f"{self.id} - {self.title}"





class Category(models.Model):
    title = models.CharField("Название категории RU", max_length=256, null=False, blank=False)
    subCat = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.id} - {self.title}"


class GroupCategory(models.Model):
    title = models.CharField("Название группы категорий", max_length=256, null=False, blank=False)

    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = "Группа категорий"
        verbose_name_plural = "Группы категорий"

    def __str__(self):
        return f"{self.id} - {self.title}"


class Brand(models.Model):
    title = models.CharField("Название бренда", max_length=256, default="Без названия", null=True, blank=True)
    photo = models.ImageField("Пиктограмма",upload_to="media/brandPricture/")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.title

class FreeOption(models.Model):
    title = models.CharField("Название бренда", max_length=256, default="Без названия", null=True, blank=True)
    picture = models.ImageField("Пиктограмма",upload_to="media/optionPictures/")

    class Meta:
        verbose_name = "Опция"
        verbose_name_plural = "Опции"

    def save(self, *args, **kwargs):
        self.title = self.title.replace("'","")
        super(FreeOption, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class FreeOptionGroup(models.Model):
    title = models.CharField("Название бренда", max_length=256, default="Без названия", null=True, blank=True)
    options = models.ManyToManyField(FreeOption, verbose_name="Список опций", blank=True)

    class Meta:
        verbose_name = "Группа опций"
        verbose_name_plural = "Группы опций"

    def save(self, *args, **kwargs):
        self.title = self.title.replace("'","")
        super(FreeOptionGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField("Название продукта RU", max_length=256, default="Без названия", null=True, blank=True)

    photo = models.ManyToManyField(Photo, verbose_name="Фото")

    category = models.ManyToManyField(Category, verbose_name="Категория")

    options = models.ManyToManyField(FreeOptionGroup, verbose_name="Опции")

    descriptionRU = models.TextField("Описание на русском")

    active = models.BooleanField("Активность", default=False)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.id} - {self.title}"


class FavouriteProducts(models.Model):
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Популярные товары {self.id}"


class TempProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    optionGroup = models.ForeignKey(FreeOptionGroup, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey(FreeOption, on_delete=models.CASCADE, null=True, blank=True)

    price = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Временный продукт"
        verbose_name_plural = "Временные продукты"

    def __str__(self):
        return f"{self.id} - {self.product.title}"

class Cart(models.Model):
    products = models.ManyToManyField(TempProduct, blank=True)
    userId = models.PositiveIntegerField("ID пользователя")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"{self.id}"



class TempOrder(models.Model):
    products = models.ManyToManyField(TempProduct)

    firstName = models.CharField("Имя", max_length=1024, default="Без названия", null=True, blank=True)
    lastName = models.CharField("Имя", max_length=1024, default="Без названия", null=True, blank=True)

    address = models.TextField("Адрес")
    comment = models.TextField("Комментарий")
    
    phone = models.PositiveIntegerField("Номер телефона", default=0)
    creationDate = models.DateTimeField("Дата создания заказа", default=timezone.now, null=False, blank=False)

    # False - cash
    # True - card

    class Meta:
        verbose_name = "Временный заказ"
        verbose_name_plural = "Временные заказы"

    def __str__(self):
        return f"{self.id}"


class Order(models.Model):
    tempOrder = models.ForeignKey(TempOrder, on_delete=models.CASCADE)

    creationDate = models.DateTimeField("Дата создания заказа", default=timezone.now, null=False, blank=False)

    class Meta:
        verbose_name = "Временный заказ"
        verbose_name_plural = "Временные заказы"

    def __str__(self):
        return f"{self.id}"

        
class PriceForOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    option = models.ForeignKey(FreeOptionGroup, on_delete=models.CASCADE, verbose_name="Объём")

    price = models.PositiveIntegerField("Цена", default="0")

    class Meta:
        verbose_name = "Цена на опцию"
        verbose_name_plural = "Цены на опции"

    def __str__(self):
        return f"{self.product} - {self.option}"




def save_product(sender, instance, pk_set, **kwargs):
    logger.error(sender.id)
    logger.error(sender)
    logger.error(instance)
    logger.error(f"pk_set {pk_set}")

    for a in pk_set:
        try:
            test = PriceForOption.objects.filter(product=instance).get(option=FreeOptionGroup.objects.get(id=a))
        except Exception as e:
            price = PriceForOption()
            price.product = instance
            price.option = FreeOptionGroup.objects.get(id=a)
            price.price = 0
            price.save()

            logger.error("price saved")



m2m_changed.connect(save_product, sender=Product.options.through)

