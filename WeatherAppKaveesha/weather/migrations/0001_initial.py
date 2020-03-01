# Generated by Django 3.0.3 on 2020-02-29 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='Unassigned', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.Location')),
            ],
        ),
    ]
