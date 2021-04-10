from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class CommonBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Category(CommonBaseModel):
    category_name = models.CharField(max_length=255)
    category_slug = AutoSlugField(populate_from='category_name', unique_with=['category_name'])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_slug

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category',
                       args=[self.category_slug])


class Post(CommonBaseModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blog_category')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    body = models.TextField()
    # image = models.ImageField(upload_to='images/')
    image = models.ImageField(upload_to='images/')

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class PostImage(CommonBaseModel):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.post.title
