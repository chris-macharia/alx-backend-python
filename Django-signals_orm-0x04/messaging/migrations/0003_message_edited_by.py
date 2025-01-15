# Generated by Django 4.2.17 on 2025-01-14 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messaging', '0002_message_edited_messagehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='edited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edited_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]