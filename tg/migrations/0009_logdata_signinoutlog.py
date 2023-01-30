# Generated by Django 3.2.9 on 2022-01-07 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tg', '0008_poribohonroutes_imglink'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignInOutLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('uName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uSignInOut', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logType', models.CharField(max_length=250)),
                ('details', models.TextField()),
                ('uName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uLog', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]