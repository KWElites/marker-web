# Generated by Django 3.2.3 on 2021-07-13 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='profilePics/defaultPP.jpg', upload_to='profilePics'),
        ),
    ]