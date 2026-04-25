from django.db import models
from django.contrib.auth.models import User
class Apod(models.Model) :
    title = models.CharField(max_length=265)
    explanation = models.TextField()
    url = models.URLField()
    media_type = models.CharField()
    date = models.DateField()
    note = models.TextField(blank=True , null=True)
    
    def __str__(self):
        return self.title 
    

class Favourite(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    apod = models.ForeignKey(Apod,on_delete=models.CASCADE,related_name="favourited_by")
    
    class Meta :
        unique_together = ('user','apod')