# Generated by Django 3.0.5 on 2020-04-24 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='Question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='UserId',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
