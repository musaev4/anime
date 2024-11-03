from django.urls import reverse
from collections import OrderedDict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import AnimeForm
from .models import Anime, Rating, Image, Comment
from django.db.models import Count, Avg


def home(request):
    anime_list = Anime.objects.prefetch_related(
        'images',
        'genres',
        'ratings'
    ).annotate(
        view_count=Count('ratings'),
        avg_rating=Avg('ratings__score')
    )

    trending_anime = anime_list.order_by('-view_count', '-avg_rating')[:6]
    popular_shows = anime_list.order_by('-avg_rating')[:6]
    top_viewed = anime_list.order_by('-view_count')[:4]
    banner_anime = anime_list.order_by('-view_count', '-avg_rating')[:5]

    context = {
        'trending_anime': trending_anime,
        'popular_shows': popular_shows,
        'top_viewed': top_viewed,
        'banner_anime': banner_anime

    }

    return render(request, 'index.html', context)


def anime_detail(request, pk):
    anime = get_object_or_404(Anime.objects.prefetch_related(
        'images',
        'genres',
        'anime_episodes',
        'comments__user',
        'ratings'
    ), pk=pk)
    ip_address = request.META.get('REMOTE_ADDR')
    anime.add_view(ip_address, request.user if request.user.is_authenticated else None)
    anime = get_object_or_404(Anime, id=pk)
    related_anime = []

    for genre in anime.genres.all():
        for related in genre.animes.all()[:3]:
            if related != anime:
                related_anime.append(related)
    unique_related_anime = list(OrderedDict.fromkeys(related_anime))

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Не хватает прав доступа!')
            return redirect('login')
        if 'rating' in request.POST:
            score = request.POST.get('rating')
            if score and score.isdigit():
                rating, created = Rating.objects.update_or_create(
                    anime=anime,
                    user=request.user,
                    defaults={'score': int(score)}
                )
                messages.success(request, 'Успешно дана оценка!')
        elif 'comment' in request.POST:
            comment_text = request.POST.get('comment')
            if comment_text:
                Comment.objects.create(
                    anime=anime,
                    user=request.user,
                    text=comment_text
                )
                messages.success(request, 'Комментарий успешно опубликован!')

        return redirect('anime:anime_detail', pk=pk)

    context = {
        'anime': anime,
        'related_anime': unique_related_anime
    }

    return render(request, 'anime/anime_detail.html', context)


def anime_create(request):
    form = AnimeForm()
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            anime = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(anime=anime, image=image)

            messages.success(request, f'Аниме "{anime.title}" успешно добавлено!')

            return redirect('anime:anime_detail', pk=anime.pk)

    context = {
        'form': form,
    }
    return render(request, 'anime/anime_create.html', context)


def anime_update(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    form = AnimeForm(instance=anime)
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            anime = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(anime=anime, image=image)
            messages.success(request, f'Аниме "{anime.title}" успешно обновлено!')
            return redirect('anime:anime_detail', anime.pk)

    context = {
        'form': form,
        'object': anime,
    }
    return render(request, 'anime/anime_update.html', context)


def delete_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, id=image_id)
        anime_id = image.anime.id
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def anime_delete(request, pk):
    anime = get_object_or_404(Anime, id=pk)
    title = anime.title
    anime.delete()
    messages.success(request, f'Аниме "{title}" успешно удалено!')
    return redirect('anime:home')


def anime_list(request):
    animes = Anime.objects.annotate(
        avg_rating=Avg('ratings__score'),
        view_count=Count('views')
    ).prefetch_related('images', 'genres')

    context = {
        'trending_anime': animes.order_by('-view_count')[:6],
        'top_viewed': animes.order_by('-view_count')[:5],
    }
    return render(request, 'anime/anime_list.html', context)
