# Generated by Django 4.2.11 on 2024-05-09 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'custom_users',
            },
        ),
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('token', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('custom_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customUsers.customuser')),
            ],
            options={
                'db_table': 'custom_tokens',
            },
        ),
    ]
