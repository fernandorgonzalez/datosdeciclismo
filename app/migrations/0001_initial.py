# Generated by Django 3.2.6 on 2021-08-16 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='atletas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('token_type', models.CharField(max_length=200)),
                ('expires_at', models.CharField(max_length=200)),
                ('expires_in', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('access_token', models.CharField(max_length=200)),
                ('athlete_id', models.CharField(max_length=200, unique=True)),
                ('username', models.CharField(max_length=200)),
                ('resource_state', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('sex', models.CharField(max_length=200)),
                ('premium', models.CharField(max_length=200)),
                ('summit', models.CharField(max_length=200)),
                ('created_at', models.CharField(max_length=200)),
                ('updated_at', models.CharField(max_length=200)),
                ('badge_type_id', models.CharField(max_length=200)),
                ('weight', models.CharField(max_length=200)),
                ('profile_medium', models.CharField(max_length=200)),
                ('profile', models.CharField(max_length=200)),
                ('friend', models.CharField(max_length=200)),
                ('follower', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Atletas',
                'ordering': ['firstname', 'lastname', 'athlete_id'],
            },
        ),
        migrations.CreateModel(
            name='actividades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=200)),
                ('año', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('dia', models.IntegerField()),
                ('tipo', models.CharField(choices=[('Ruta', 'Ruta'), ('Virtual', 'Virtual')], max_length=200)),
                ('altura', models.FloatField()),
                ('cadencia', models.FloatField()),
                ('distancia', models.FloatField()),
                ('potencia', models.FloatField()),
                ('pulsaciones', models.FloatField()),
                ('tiempo', models.FloatField()),
                ('velocidad', models.FloatField()),
                ('atleta', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.atletas')),
            ],
            options={
                'verbose_name_plural': 'Actividades',
                'ordering': ['-año', '-mes', '-dia', '-tipo'],
            },
        ),
    ]
