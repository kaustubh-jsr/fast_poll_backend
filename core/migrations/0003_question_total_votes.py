# Generated by Django 3.2.14 on 2022-07-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_choice_question_choice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]
