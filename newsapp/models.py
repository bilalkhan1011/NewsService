from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)

    def __str__ (self):
        return self.name


class Story (models.Model):
    headline = models.CharField(max_length = 64)
    categories = [ ('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), 
                  ('trivia', 'Trivia') ]
    category = models.CharField(max_length = 20, choices = categories, default = 'unknown')
    regions = [ ('uk', 'United Kingdom'), ('eu', 'European News'), ('w', 'World News') ]
    region = models.CharField(max_length = 64, choices = regions, default = 'unknown')
    author = models.ForeignKey(Author, on_delete = models.PROTECT)
    date = models.DateField()
    details = models.CharField(max_length = 128)

    def __str__ (self):
        return self.headline
