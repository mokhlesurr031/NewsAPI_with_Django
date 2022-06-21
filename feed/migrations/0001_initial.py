# Generated by Django 3.2 on 2022-06-21 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(blank=True, max_length=355, null=True)),
                ('thumbnail', models.CharField(blank=True, max_length=455, null=True)),
                ('source', models.CharField(blank=True, max_length=455, null=True)),
                ('country', models.CharField(blank=True, max_length=455, null=True)),
                ('detail_news', models.CharField(blank=True, max_length=455, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('next_update', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user_conf', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.userfeedconf')),
            ],
        ),
    ]
