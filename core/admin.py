from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Anime, Episode, Image, Rating, Comment


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'episodes', 'average_rating', 'display_genres']
    list_filter = ['genres', 'release_date']
    search_fields = ['title', 'description']
    filter_horizontal = ['genres']
    inlines = [ImageInline, EpisodeInline, CommentInline]

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Жанры'


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'anime', 'release_date']
    list_filter = ['release_date', 'anime']
    search_fields = ['title', 'anime__title']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'anime', 'image_preview']
    list_filter = ['anime']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'score']
    list_filter = ['score', 'anime']
    search_fields = ['user__username', 'anime__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'anime', 'text_preview', 'created_at']
    list_filter = ['created_at', 'anime']
    search_fields = ['user__username', 'anime__title', 'text']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст'
