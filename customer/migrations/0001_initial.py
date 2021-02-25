# Generated by Django 3.1.4 on 2021-02-24 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_register_date', models.DateField(auto_now_add=True)),
                ('customer_firstname', models.CharField(default='Name', max_length=50)),
                ('customer_lastname', models.CharField(default='Name', max_length=50)),
                ('customer_username', models.CharField(default='Userame', max_length=50)),
                ('customer_email', models.CharField(default='Email', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_profile_pic',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('profile_pic', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Profile_edit',
            fields=[
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('customer_firstname', models.CharField(blank=True, max_length=25, null=True)),
                ('customer_lastname', models.CharField(blank=True, max_length=25, null=True)),
                ('address', models.TextField(max_length=60)),
                ('country_name', models.CharField(max_length=15)),
                ('state_name', models.CharField(max_length=20)),
                ('postcode', models.CharField(blank=True, max_length=15, null=True)),
                ('customer_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer_account')),
            ],
        ),
    ]
