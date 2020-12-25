# Generated by Django 3.1.4 on 2020-12-25 10:32

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='properti',
            old_name='kantropos',
            new_name='kantorpos',
        ),
        migrations.AlterField(
            model_name='order',
            name='bukti_pembayaran',
            field=models.ImageField(help_text='Maximum file size allowed is 3MB', null=True, upload_to=website.models.PathAndRename('images/bukti_pembayaran'), validators=[website.models.validate_image]),
        ),
        migrations.AlterField(
            model_name='produk',
            name='foto',
            field=models.ImageField(help_text='Maximum file size allowed is 3MB', upload_to=website.models.PathAndRename('images/produk'), validators=[website.models.validate_image], verbose_name='Foto produk'),
        ),
        migrations.AlterField(
            model_name='properti',
            name='foto',
            field=models.ImageField(help_text='Maximum file size allowed is 3MB', upload_to=website.models.PathAndRename('images/properti'), validators=[website.models.validate_image], verbose_name='Foto properti'),
        ),
    ]
