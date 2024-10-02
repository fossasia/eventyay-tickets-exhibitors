# Generated by Django 4.2.14 on 2024-09-16 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0005_alter_cachedcombinedticket_id_alter_cachedticket_id_and_more'),
        ('exhibitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitorinfo',
            name='lead_scanning_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ExhibitorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('exhibitor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_assignments', to='exhibitors.exhibitorinfo')),
                ('item', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exhibitor_assignment', to='pretixbase.item')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]