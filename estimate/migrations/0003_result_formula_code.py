# Generated by Django 3.2.9 on 2022-01-10 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0002_alter_result_formula_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_formula',
            name='code',
            field=models.CharField(default='', max_length=300),
        ),
    ]
