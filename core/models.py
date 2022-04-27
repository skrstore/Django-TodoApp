from django.db import models


class User(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)
    pic_path = models.ImageField(upload_to='users')

    def __str__(self):
        return self.name


class Note(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
