# Generated by Django 2.0.4 on 2018-06-10 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180525_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrummygoals',
            name='target_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.GoalStatus'),
        ),
    ]
