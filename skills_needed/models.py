from django.db import models


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    resource = models.CharField(max_length=300)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class JobPosition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    compensation = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title