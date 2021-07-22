# Generated by Django 3.2.3 on 2021-07-19 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='profilePics/defaultPP.jpg', upload_to='profilePics')),
                ('name', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeName', models.CharField(max_length=20)),
                ('uId', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageName', models.CharField(max_length=20)),
                ('packageDesc', models.CharField(max_length=512)),
                ('packageThumbnail', models.ImageField(default='package/thumbnails/defaultTN.png', upload_to='package/thumbnails')),
                ('packageItems', models.FileField(default='', upload_to='package/packages')),
                ('packageImages', models.CharField(default='', max_length=200)),
                ('sId', models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='users.store')),
                ('uId', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logAction', models.CharField(max_length=8)),
                ('logDesc', models.CharField(max_length=512)),
                ('logErrorCode', models.SmallIntegerField()),
                ('logActionStatus', models.BooleanField()),
                ('pId', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='users.package')),
                ('uId', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
