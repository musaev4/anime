# Generated by Django 5.1.2 on 2024-11-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_animeview_episodeview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='status',
            field=models.CharField(blank=True, choices=[('ongoing', 'Онгоинг'), ('completed', 'Завершено'), ('announced', 'Анонс')], max_length=10, null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='anime',
            name='type',
            field=models.CharField(blank=True, choices=[('movie', 'Фильм'), ('tv', 'Тв Сериал'), ('ova', 'OVA'), ('ona', 'Спешл')], max_length=10, null=True, verbose_name='Тип'),
        ),
    ]