# Generated by Django 3.1 on 2020-09-23 04:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20200916_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.IntegerField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
