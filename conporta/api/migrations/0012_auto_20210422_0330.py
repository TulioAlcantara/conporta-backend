# Generated by Django 3.1.7 on 2021-04-22 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_ordinance_pdf_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminunit',
            name='expedition_year',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminunit',
            name='last_issued_number',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminunit',
            name='last_proposed_number',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
    ]
