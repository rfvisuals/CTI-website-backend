# Generated by Django 3.0.7 on 2021-03-13 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_organization_cti_contributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='org_tag',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]