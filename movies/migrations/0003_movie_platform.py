# Generated by Django 4.0.5 on 2022-06-25 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_platform_movie_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movies.platform'),
            preserve_default=False,
        ),
    ]
