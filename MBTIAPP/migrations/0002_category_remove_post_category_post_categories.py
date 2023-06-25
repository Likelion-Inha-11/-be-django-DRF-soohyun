# Generated by Django 4.2.1 on 2023-06-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MBTIAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='MBTIAPP.category'),
        ),
    ]
