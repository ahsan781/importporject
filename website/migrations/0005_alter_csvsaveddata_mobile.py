# Generated by Django 3.2.8 on 2021-10-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_csvsaveddata_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvsaveddata',
            name='mobile',
            field=models.TextField(blank=True),
        ),
    ]
