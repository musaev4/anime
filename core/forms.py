import os

from django import forms

from project.settings import BASE_DIR
from .models import Anime, Genre, Comment, Rating


class AnimeForm(forms.ModelForm):
    images = forms.ImageField(
        label='Изображения',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 '
                     'file:rounded-full file:border-0 file:text-sm file:font-semibold '
                     'file:bg-red-500 file:text-white hover:file:bg-red-600',
            'style': '''
                appearance: none;
                background-color: transparent;
                border: none;
                padding: 0;
                outline: none;
            '''

        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.release_date:
            self.initial['release_date'] = self.instance.release_date.strftime('%Y-%m-%d')

        self.fields['release_date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500'
            }
        )

    class Meta:
        model = Anime
        fields = (
            'title',
            'description',
            'release_date',
            'genres',
            'episodes',
            'type',
            'status',
        )

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'Введите название',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'Введите описание',
                'rows': 4,
            }),
            'episodes': forms.NumberInput(attrs={
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500',
                'min': 0,
            }),
            'genres': forms.CheckboxSelectMultiple(attrs={
                'class': 'rounded bg-gray-700 border-gray-600 text-white focus:ring-red-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full bg-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500'
            })
        }
