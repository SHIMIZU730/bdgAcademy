# Generated by Django 2.0.2 on 2023-05-20 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chatgpt_answer_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_1', models.CharField(max_length=254)),
                ('answer_2', models.CharField(max_length=254)),
                ('answer_3', models.CharField(max_length=254)),
                ('answer_4', models.CharField(max_length=254)),
                ('answer_5', models.CharField(max_length=254)),
                ('answer_6', models.CharField(max_length=254)),
                ('answer_7', models.CharField(max_length=254)),
                ('answer_8', models.CharField(max_length=254)),
                ('answer_9', models.CharField(max_length=254)),
                ('answer_10', models.CharField(max_length=254)),
                ('answer_11', models.CharField(max_length=254)),
                ('answer_12', models.CharField(max_length=254)),
                ('answer_13', models.CharField(max_length=254)),
                ('answer_14', models.CharField(max_length=254)),
                ('answer_15', models.CharField(max_length=254)),
                ('create_user', models.CharField(max_length=254)),
                ('create_date', models.DateField()),
            ],
        ),
    ]
