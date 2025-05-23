# Generated by Django 4.2.7 on 2025-05-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filledform',
            old_name='timestamp',
            new_name='assigned_at',
        ),
        migrations.RemoveField(
            model_name='filledform',
            name='filled_text',
        ),
        migrations.AddField(
            model_name='filledform',
            name='txt_path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filledform',
            name='form_id',
            field=models.IntegerField(),
        ),
    ]
