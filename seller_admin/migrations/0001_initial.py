# Generated by Django 3.1.4 on 2021-02-24 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile_pic',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('user_name', models.CharField(default='Name', max_length=50)),
                ('user_username', models.CharField(default='Email', max_length=255)),
                ('user_profile_img', models.CharField(default='Profile Image', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Seller_profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser')),
                ('description_about_seller', models.TextField(default='Description of seller')),
                ('skills_of_seller', models.TextField(default='Skill Set')),
                ('location_of_seller', models.CharField(default='Seller Location', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Verification_code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('user_username', models.CharField(max_length=254, unique=True)),
                ('user_verification_code', models.CharField(max_length=10)),
                ('user_active_status', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seller_portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_img', models.ImageField(upload_to='')),
                ('img_title', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(default='Product Name', max_length=100)),
                ('product_category', models.IntegerField(default=0)),
                ('product_subcategory', models.IntegerField(default=0)),
                ('product_short_description', models.TextField(default='Product Short Description', max_length=254)),
                ('product_details', models.TextField(default='Product Details', max_length=254)),
                ('product_price', models.CharField(default='Product Price', max_length=254)),
                ('product_old_price', models.CharField(default='Product Old Price', max_length=254)),
                ('product_InStocks', models.IntegerField(default=0)),
                ('product_img1', models.ImageField(upload_to='')),
                ('product_img2', models.ImageField(upload_to='')),
                ('product_img3', models.ImageField(upload_to='')),
                ('product_img4', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img5', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img6', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img7', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img8', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img9', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_img10', models.ImageField(blank=True, null=True, upload_to='')),
                ('prduct_adding_date', models.DateField(auto_now_add=True)),
                ('product_id', models.CharField(default='Product ID', max_length=30)),
                ('product_search_tags', models.TextField(default='Product Search Tags', max_length=254)),
                ('product_meta_title_for_search', models.CharField(default='Meta Title', max_length=150)),
                ('product_type_tag', models.CharField(default='Like New or Sale or Hot', max_length=50)),
                ('product_available_colors', models.TextField(default='Product colors', max_length=254)),
                ('product_condition', models.CharField(default='Like New or Used', max_length=254)),
                ('seller_identity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
