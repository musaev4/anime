from django.contrib import admin
from django.utils.html import format_html
from .models import Genre, Anime, Episode, Image, AnimeView, EpisodeView, Rating, Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

    class Media:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    readonly_fields = ('total_views',)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'status', 'type', 'release_date', 'total_episodes', 'display_genres', 'average_rating', 'total_views')
    list_filter = ('status', 'type', 'genres', 'release_date')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
    inlines = [ImageInline, EpisodeInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'release_date')
        }),
        ('Классификация', {
            'fields': ('genres', 'status', 'type')
        }),
        ('Статистика', {
            'fields': ('episodes',),
            'classes': ('collapse',)
        })
    )

    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Жанры'

    def total_episodes(self, obj):
        return obj.anime_episodes.count()

    total_episodes.short_description = 'Количество эпизодов'


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'release_date', 'total_views')
    list_filter = ('release_date', 'anime')
    search_fields = ('title', 'anime__title')
    raw_id_fields = ('anime',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'score')
    list_filter = ('score', 'anime')
    search_fields = ('user__username', 'anime__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'short_text', 'created_at')
    list_filter = ('created_at', 'anime')
    search_fields = ('user__username', 'anime__title', 'text')
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    short_text.short_description = 'Текст комментария'


@admin.register(AnimeView)
class AnimeViewAdmin(admin.ModelAdmin):
    list_display = ('anime', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at', 'anime')
    search_fields = ('anime__title', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)


@admin.register(EpisodeView)
class EpisodeViewAdmin(admin.ModelAdmin):
    list_display = ('episode', 'user', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at', 'episode__anime')
    search_fields = ('episode__title', 'user__username', 'ip_address')
    readonly_fields = ('viewed_at',)


# Настройка названий моделей
Genre._meta.verbose_name = 'Жанр'
Genre._meta.verbose_name_plural = 'Жанры'

Anime._meta.verbose_name = 'Аниме'
Anime._meta.verbose_name_plural = 'Аниме'

Episode._meta.verbose_name = 'Эпизод'
Episode._meta.verbose_name_plural = 'Эпизоды'

Rating._meta.verbose_name = 'Рейтинг'
Rating._meta.verbose_name_plural = 'Рейтинги'

Comment._meta.verbose_name = 'Комментарий'
Comment._meta.verbose_name_plural = 'Комментарии'

AnimeView._meta.verbose_name = 'Просмотр аниме'
AnimeView._meta.verbose_name_plural = 'Просмотры аниме'

EpisodeView._meta.verbose_name = 'Просмотр эпизода'
EpisodeView._meta.verbose_name_plural = 'Просмотры эпизодов'

# Настройка заголовка админ-панели
admin.site.site_header = 'Администрирование аниме-портала'
admin.site.site_title = 'Аниме-портал'
admin.site.index_title = 'Управление контентом'