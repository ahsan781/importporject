# Generated by Django 3.2.8 on 2021-10-17 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20211012_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvsaveddata',
            name='mobile',
            field=models.IntegerField(blank=True, max_length=50),
        ),
    ]