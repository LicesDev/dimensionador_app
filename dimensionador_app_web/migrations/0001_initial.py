# Generated by Django 4.2.15 on 2024-10-02 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dimensiones',
            fields=[
                ('lpn', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('largo', models.FloatField()),
                ('alto', models.FloatField()),
                ('ancho', models.FloatField()),
                ('fecha', models.CharField(max_length=255)),
            ],
        ),
    ]
