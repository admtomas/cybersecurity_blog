from turtle import title
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

#* --- Create model Manager ---
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


#* --- Create Model for The Blog Post ---
class Post(models.Model):
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/%d/%m/%Y/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    # Attach text editor to the body to style the article
    body=RichTextUploadingField()


    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

        def __str__(self):
            return self.title

    # Default and custom manager
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        #* specify app name and url name to which you want to reverse
        return reverse("blog:post_detail", args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

#* --- Create model for comments ---
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

#* --- Create model for About Page ---
class About(models.Model):
    title = models.CharField(max_length=255)
    body=RichTextUploadingField()

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.title