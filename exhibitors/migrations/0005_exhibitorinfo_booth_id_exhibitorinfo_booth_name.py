# Generated by Django 5.1.2 on 2024-10-30 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0004_exhibitortag'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitorinfo',
            name='booth_id',
            field=models.IntegerField(auto_created=True, null=True),
        ),
        migrations.AddField(
            model_name='exhibitorinfo',
            name='booth_name',
            field=models.CharField(default='Unnamed Booth', max_length=100),
            preserve_default=False,
        ),
    ]
