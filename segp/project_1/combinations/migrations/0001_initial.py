# Generated by Django 3.1.3 on 2021-01-23 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('combination_score', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_update', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
