# Generated by Django 4.0.7 on 2022-09-28 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_authorisation_corapporteur_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorisation',
            name='corapporteur',
            field=models.CharField(blank=True, db_column='CoRapporteur', max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='authorisation',
            name='rapporteur',
            field=models.CharField(blank=True, db_column='Rapporteur', max_length=45, null=True),
        ),
    ]
