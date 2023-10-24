from django.db import models
from django.utils.text import slugify

from accounts.models import ProfileUser


# Create your models here.
class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategory",
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(TimeModel):
    author = models.ForeignKey(
        ProfileUser, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to="blog/img/")
    category = models.ManyToManyField(Category, related_name='posts')
    body = models.TextField()

    def save(obj, *args, **kwargs):
        obj.slug = slugify(obj.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(TimeModel):
    RATINGS = (
        ("1", "very bad"),
        ("2", "very"),
        ("3", "normal"),
        ("4", "good"),
        ("5", "very good"),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        ProfileUser, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=500)
    rating = models.CharField(max_length=2, choices=RATINGS)

    def __str__(self):
        return f"{self.user}-{self.post}"
