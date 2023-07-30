# Generated by Django 4.2.2 on 2023-07-30 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_alter_car_gear_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestauction',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userinauction',
            name='status',
            field=models.CharField(choices=[('watcher', 'watcher'), ('participant', 'participant'), ('withdrawer', 'withdrawer'), ('waiting', 'waiting')], max_length=50),
        ),
    ]