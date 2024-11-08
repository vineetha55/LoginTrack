# Generated by Django 5.1.2 on 2024-10-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_Registration_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('mobile', models.IntegerField(null=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('updated_time', models.TimeField(auto_now=True)),
            ],
        ),
    ]
