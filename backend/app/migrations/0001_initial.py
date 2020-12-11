# Generated by Django 3.0.8 on 2020-10-09 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorpusAnalysisResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('result', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapSquare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('number', models.IntegerField(null=True)),
                ('boundaries', models.CharField(max_length=252)),
                ('coordinates', models.CharField(max_length=252)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(null=True)),
                ('cleaned_src', models.CharField(max_length=252, null=True)),
                ('front_src', models.CharField(max_length=252, null=True)),
                ('back_src', models.CharField(max_length=252, null=True)),
                ('binder_src', models.CharField(max_length=252, null=True)),
                ('thumbnail_src', models.CharField(max_length=252, null=True)),
                ('cleaned_local_path', models.CharField(max_length=252, null=True)),
                ('front_local_path', models.CharField(max_length=252, null=True)),
                ('back_local_path', models.CharField(max_length=252, null=True)),
                ('binder_local_path', models.CharField(max_length=252, null=True)),
                ('shelfmark', models.CharField(max_length=252)),
                ('contains_sticker', models.BooleanField(null=True)),
                ('alt', models.CharField(max_length=252)),
                ('librarian_caption', models.CharField(max_length=252)),
                ('photographer_caption', models.CharField(max_length=252)),
                ('map_square', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MapSquare')),
            ],
        ),
        migrations.CreateModel(
            name='PhotographerAnalysisResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('result', models.TextField(null=True)),
                ('photographer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Photo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photographer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('number', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=252, null=True)),
                ('sentiment', models.CharField(max_length=252, null=True)),
                ('map_square', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.MapSquare')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoAnalysisResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('result', models.TextField(null=True)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Photo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='photographer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Photographer'),
        ),
        migrations.CreateModel(
            name='MapSquareAnalysisResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=252)),
                ('result', models.TextField(null=True)),
                ('map_square', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MapSquare')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together={('number', 'map_square')},
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_n', models.IntegerField(null=True)),
                ('label', models.IntegerField(null=True)),
                ('photos', models.ManyToManyField(to='app.Photo')),
            ],
            options={
                'unique_together': {('model_n', 'label')},
            },
        ),
    ]
