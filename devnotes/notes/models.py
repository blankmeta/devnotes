from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Theme(models.Model):
    title = models.TextField(max_length=50)
    slug = models.SlugField(unique=True, db_index=True)
    author = models.ManyToManyField(User, related_name='themes')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if Theme.objects.filter(slug=self.slug).exists():
            self.slug += '2'
        super(Theme, self).save(*args, **kwargs)

    def __str__(self):
        return f'Title - {self.title} | Slug - {self.slug}'

    def __repr__(self):
        return f'Title - {self.title} | Slug - {self.slug}'


class Note(models.Model):
    title = models.TextField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='notes')
    pub_date = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE,
                              related_name='notes')

    def __str__(self):
        return f'{self.title} {self.author}'

    def __repr__(self):
        return f'{self.title} {self.author}'

    class Meta:
        ordering = ['pub_date']
