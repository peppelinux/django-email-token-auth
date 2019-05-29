# Generated by Django 2.2.1 on 2019-05-28 11:30

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import email_token_auth.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_title', models.CharField(blank=True, max_length=12, null=True)),
                ('name', models.CharField(help_text='Nome o ragione sociale', max_length=256)),
                ('surname', models.CharField(max_length=135)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(blank=True, max_length=135, null=True)),
                ('common_name', models.CharField(blank=True, help_text='Nome o ragione sociale', max_length=256, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, help_text='nazionalità, cittadinanza', max_length=2)),
                ('city', models.CharField(blank=True, help_text='residenza', max_length=128, null=True)),
                ('tin', models.CharField(blank=True, help_text='Taxpayer Identification Number', max_length=24, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name_plural': 'Identità digitali',
            },
        ),
        migrations.CreateModel(
            name='IdentityToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(blank=True, default=uuid.uuid4, help_text='/access/$token', unique=True)),
                ('sent', models.BooleanField(default=False)),
                ('sent_to', models.CharField(blank=True, max_length=254, null=True)),
                ('sent_date', models.DateTimeField(blank=True, null=True)),
                ('valid_until', models.DateTimeField(blank=True, default=email_token_auth.utils.get_default_valid_until)),
                ('used', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='disable it if needed')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('identity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='email_token_auth.Identity')),
            ],
        ),
    ]
