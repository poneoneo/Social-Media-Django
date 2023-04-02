from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

#Un Profile doit avoir un compte utilisateur    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    id_user = models.IntegerField(auto_created=True)
    Bio = models.TextField(blank = True)
    profileimg = models.ImageField(upload_to = "profile_images", default = "blank-profile-picture.png")
    location = models.CharField(max_length=150, blank = True) 

    def __str__(self):
        return self.user.username
        

