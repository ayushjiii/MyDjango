from django.db import models

class Apod(models.Model) :
    title = models.CharField(max_length=265)
    explanation = models.TextField()
    url = models.URLField()
    media_type = models.CharField()
    date = models.DateField()
    favourite = models.BooleanField(default=False)
    note = models.TextField(blank=True , null=True)
    
    def __str__(self):
        return self.title 
    
