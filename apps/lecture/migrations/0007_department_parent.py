# Generated by Django 2.1.2 on 2018-10-22 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0006_auto_20181023_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='lecture.Department'),
        ),
    ]
