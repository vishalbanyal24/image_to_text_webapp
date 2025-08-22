from django.db import models

# Create your models here.

class ImageDescription(models.Model):
    image_file = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    image_local_path = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.image_file:
            return f"Image: {self.image_file.name}"
        elif self.image_url:
            return f"URL: {self.image_url}"
        elif self.image_local_path:
            return f"Local Path: {self.image_local_path}"
        return "No Image"