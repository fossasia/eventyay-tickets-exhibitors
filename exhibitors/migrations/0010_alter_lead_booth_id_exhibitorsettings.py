# Generated by Django 5.1.2 on 2024-11-02 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0009_lead_booth_id_lead_booth_name_lead_exhibitor_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExhibitorSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('exhibitors_access_mail_subject', models.CharField(max_length=255)),
                ('exhibitors_access_mail_body', models.TextField()),
                ('allowed_fields', models.JSONField(default=list)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.event')),
            ],
            options={
                'unique_together': {('event',)},
            },
        ),
        migrations.AlterField(
            model_name='exhibitorinfo',
            name='booth_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='booth_id',
            field=models.CharField(max_length=100, unique=True),  # Changed to CharField
        ),
    ]
