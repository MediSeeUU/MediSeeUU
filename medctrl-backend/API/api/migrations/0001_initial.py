# Generated by Django 4.0.3 on 2022-03-30 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtcCode',
            fields=[
                ('atc_code', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=320)),
            ],
            options={
                'db_table': 'atc_code',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LegalBasis',
            fields=[
                ('legal_basis_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'legal_basis',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LegalScope',
            fields=[
                ('legal_scope_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'legal_scope',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MarketingAuthorisationHolder',
            fields=[
                ('mah_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=320)),
            ],
            options={
                'db_table': 'marketing_authorisation_holder',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('eu_nr', models.IntegerField(primary_key=True, serialize=False)),
                ('ema_nr', models.CharField(blank=True, max_length=45, null=True)),
                ('prime', models.TextField(blank=True, null=True)),
                ('orphan', models.TextField(blank=True, null=True)),
                ('atmp', models.TextField(blank=True, null=True)),
                ('ema_url', models.CharField(blank=True, max_length=320, null=True)),
            ],
            options={
                'db_table': 'medicine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProcedureType',
            fields=[
                ('procedure_type_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=320)),
            ],
            options={
                'db_table': 'procedure_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=320)),
            ],
            options={
                'db_table': 'region',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Substance',
            fields=[
                ('substance_id', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=320)),
            ],
            options={
                'db_table': 'substance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('eu_nr', models.OneToOneField(db_column='eu_nr', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.medicine')),
                ('substance_new', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'component',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MedicineName',
            fields=[
                ('eu_nr', models.OneToOneField(db_column='eu_nr', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.medicine')),
                ('start_date', models.DateField()),
                ('name', models.CharField(max_length=320)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'medicine_name',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('eu_nr', models.OneToOneField(db_column='eu_nr', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.medicine')),
                ('procedure_count', models.IntegerField()),
                ('comission_procedure_nr', models.IntegerField(blank=True, null=True)),
                ('ema_procedure_nr', models.IntegerField(blank=True, null=True)),
                ('procedure_date', models.DateField(blank=True, null=True)),
                ('decision_date', models.DateField(blank=True, null=True)),
                ('decision_nr', models.IntegerField(blank=True, null=True)),
                ('descision_url', models.CharField(blank=True, max_length=320, null=True)),
                ('annex_url', models.CharField(blank=True, max_length=320, null=True)),
            ],
            options={
                'db_table': 'procedure',
                'managed': False,
            },
        ),
    ]
