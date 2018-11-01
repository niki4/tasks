# Generated by Django 2.1.2 on 2018-11-01 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TaskParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=200)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='params',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks_app.TaskParam'),
        ),
        migrations.AddField(
            model_name='task',
            name='result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='tasks_app.Result'),
        ),
    ]
