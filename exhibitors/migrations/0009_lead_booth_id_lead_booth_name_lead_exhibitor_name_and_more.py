# Generated by Django 5.1.2 on 2024-10-30 20:56

from django.db import migrations, models

import exhibitors.models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0008_alter_exhibitorinfo_booth_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='booth_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='booth_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='exhibitor_name',
            field=models.CharField(default='', max_length=190),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exhibitorinfo',
            name='booth_id',
            field=models.IntegerField(default=exhibitors.models.generate_booth_id, unique=True),
        ),
    ]
