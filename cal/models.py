from django.db import models
from django.urls import reverse
from users.models import User

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} - {self.author} </a>'
