# Generated by Django 4.0.3 on 2022-06-02 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_savedselection'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='manually_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='procedure',
            name='manually_updated',
            field=models.BooleanField(default=False),
        ),
    ]
