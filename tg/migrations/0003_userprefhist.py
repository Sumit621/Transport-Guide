# Generated by Django 3.2.9 on 2021-12-03 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0002_auto_20211203_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPrefHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserName', models.CharField(max_length=250)),
                ('preferredRoutes', models.TextField()),
                ('history', models.TextField()),
            ],
        ),
    ]