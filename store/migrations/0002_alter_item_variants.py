# Generated by Django 4.0.5 on 2022-06-30 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='variants',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.item'),
        ),
    ]
