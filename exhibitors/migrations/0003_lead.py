# Generated by Django 4.2.14 on 2024-10-14 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exhibitors', '0002_alter_exhibitorinfo_lead_scanning_enabled_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('pseudonymization_id', models.CharField(max_length=190)),
                ('scanned', models.DateTimeField()),
                ('scan_type', models.CharField(max_length=50)),
                ('device_name', models.CharField(max_length=50)),
                ('attendee', models.JSONField(null=True)),
                ('exhibitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exhibitors.exhibitorinfo')),
            ],
        ),
    ]
