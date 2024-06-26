# Generated by Django 5.0.4 on 2024-05-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BobcatConApp', '0004_textbook_delete_textbooks'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('cardnumber', models.TextField()),
                ('expiry', models.TextField()),
                ('cvv', models.IntegerField()),
                ('limitremaining', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='textbook',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='textbook_images/'),
        ),
        migrations.AddField(
            model_name='textbook',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
