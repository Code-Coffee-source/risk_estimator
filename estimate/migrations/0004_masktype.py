# Generated by Django 3.2.5 on 2021-11-11 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0003_auto_20211028_0033'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='', max_length=225)),
                ('Code', models.CharField(default='', max_length=225)),
            ],
            options={
                'verbose_name': 'Masks',
                'verbose_name_plural': 'Mask Types',
            },
        ),
    ]
