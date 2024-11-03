from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', unique=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    STATUS_CHOICES = (
        ('', 'Выберите статус'),
        ('ongoing', 'Онгоинг'),
        ('completed', 'Завершено'),
        ('announced', 'Анонс'),
    )
    TYPE_CHOICES = [
        ('', 'Выберите тип'),
        ('movie', 'Фильм'),
        ('tv', 'Тв Сериал'),
        ('ova', 'OVA'),
        ('ona', 'Спешл'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    release_date = models.DateField(verbose_name='Дата релиза')
    episodes = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='animes')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        verbose_name='Статус аниме'
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name='Тип аниме',

    )

    def __str__(self):
        return self.title

    @property
    def total_views(self):
        return self.views.count()

    def add_view(self, ip_address, user=None):
        view, created = AnimeView.objects.get_or_create(
            anime=self,
            ip_address=ip_address,
            user=user
        )
        return created

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.score for rating in ratings) / ratings.count(), 2)
        return 0


class Episode(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название эпизода")
    release_date = models.DateField(verbose_name="Дата выхода", auto_now_add=True)
    anime = models.ForeignKey(Anime, related_name='anime_episodes', on_delete=models.CASCADE, verbose_name="Аниме")
    video = models.FileField(upload_to='videos', verbose_name="Видео", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.release_date})"

    @property
    def total_views(self):
        return self.views.count()

    def add_view(self, ip_address, user=None):
        view, created = EpisodeView.objects.get_or_create(
            episode=self,
            ip_address=ip_address,
            user=user
        )
        return created


class Image(models.Model):
    anime = models.ForeignKey(to=Anime, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', verbose_name='Изображение')


class AnimeView(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anime', 'ip_address', 'user')


class EpisodeView(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('episode', 'ip_address', 'user')


class Rating(models.Model):
    anime = models.ForeignKey(to=Anime, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.user} - {self.anime} - {self.score}'


class Comment(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст коммента')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.text[:30]}'
