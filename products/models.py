from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام کالا')
    slug = models.SlugField(unique=True, blank=True, verbose_name='اسلاگ')
    category = models.CharField(max_length=255, verbose_name='دسته بندی')
    brand = models.CharField(max_length=255, verbose_name='برند')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت')
    image = models.ImageField(upload_to='products/', verbose_name='تصویر کالا')
    image_thumbnail = ImageSpecField(source="image", processors=[ResizeToFill(800, 800)], format="JPEG", options={"quality": 85})
    stock = models.BooleanField(default=True, verbose_name='موجود')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    published_date = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'
        ordering = ['-published_date']



