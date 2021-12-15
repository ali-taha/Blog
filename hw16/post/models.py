from django.db import models, IntegrityError
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from random import randint

User = get_user_model()

class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]

class Tag(models.Model):
    title = models.CharField(max_length=100,unique=True)   
    slug = models.SlugField(null=True)   

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]    

      


class Post(models.Model):
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(Category)
    """ the unique field is not used in the post title because of question number 2 """
    title = models.CharField(max_length=120)
    short_description = models.CharField(
        max_length=300, default="this is short description"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, default="SEO",blank=True)
    image = models.ImageField(upload_to="uploads", null=True, blank=True)
    like = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(null=True)

    """ check if have exception for slug unique, generate slug with randomnuber"""

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        qs = Post.objects.filter(slug=self.slug).order_by("-id")
        exists = qs.exists()
        while exists:
            randumber = randint(0, 10)
            new_slug = self.slug + str(randumber)
            self.slug = slugify(new_slug)
            qs = Post.objects.filter(slug=self.slug).order_by("-id")
            exists = qs.exists()
        return super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_at"]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    like = models.IntegerField(default=0)
    createed_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return f"post:{self.post},user:{self.user}"

    class Meta:
        ordering = ["post"]
