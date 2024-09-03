# Generated by Django 4.2.14 on 2024-09-02 09:37

from django.db import migrations, models
import django.db.models.deletion
import exhibitors.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pretixbase', '0005_alter_cachedcombinedticket_id_alter_cachedticket_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExhibitorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=190)),
                ('description', models.TextField(null=True)),
                ('url', models.URLField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('logo', models.ImageField(null=True, upload_to=exhibitors.models.exhibitor_logo_path)),
                ('key', models.CharField(default=exhibitors.models.generate_key, max_length=8)),
                ('lead_scanning_enabled', models.BooleanField(default=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pretixbase.event')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
