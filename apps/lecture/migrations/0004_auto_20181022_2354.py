# Generated by Django 2.1.2 on 2018-10-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0003_auto_20181022_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='field',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='lecture field'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='language',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='type',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='lecture type'),
        ),
    ]
