# Generated by Django 5.1.2 on 2024-10-28 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0003_lead'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExhibitorTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('use_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exhibitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='exhibitors.exhibitorinfo')),
            ],
            options={
                'ordering': ['-use_count', 'name'],
                'unique_together': {('exhibitor', 'name')},
            },
        ),
    ]