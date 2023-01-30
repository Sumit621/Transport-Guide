# Generated by Django 3.2.9 on 2022-01-04 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tg', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='poribohon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pReviews', to='tg.poribohonroutes'),
        ),
        migrations.AlterField(
            model_name='review',
            name='uName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uReviews', to=settings.AUTH_USER_MODEL),
        ),
    ]