from django.db import models
from users.models import CustomUser
# Create your models here.

class Profile_pic(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    user_name = models.CharField(default='Name', max_length=50)
    user_username = models.CharField(default='Email', max_length=255)
    user_profile_img = models.CharField(default='Profile Image', max_length=255)

    def __str__(self):
        return self.user_name+'|'+self.user_username


# seller profile for showing in front-end part
class Seller_profile(models.Model):

    user                     = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    description_about_seller = models.TextField(default="Description of seller")
    skills_of_seller         = models.TextField(default="Skill Set")
    location_of_seller       = models.CharField(default="Seller Location", max_length=50)

    def __str__(self):
        return str(self.user)

# seller portfolio model
class Seller_portfolio(models.Model):
    user           = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # seller_profile = models.ForeignKey(Seller_profile, on_delete=models.CASCADE)
    portfolio_img  = models.ImageField()
    img_title      = models.CharField(max_length=30)

    def __str__(self):
        return str(self.user)+'|'+str(self.pk)



# seller verification code by user
class Verification_code(models.Model):
    user_email             = models.EmailField(max_length=254, unique=True)
    user_username          = models.CharField(max_length=254, unique=True)
    user_verification_code = models.CharField(max_length=10)
    user_active_status     = models.BooleanField(default=False)
    sent_at                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user_username}'



# product(like clothing, shoes, pants etc..) adding model
class Product(models.Model):
    seller_identity                = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_name                   = models.CharField(default='Product Name', max_length=100)
    product_category               = models.IntegerField(default=0)
    product_subcategory            = models.IntegerField(default=0)
    product_short_description      = models.TextField(default="Product Short Description", max_length=254)
    product_details                = models.TextField(default="Product Details", max_length=254)
    product_price                  = models.CharField(default="Product Price", max_length=254)#product new price
    product_old_price              = models.CharField(default="Product Old Price", max_length=254)
    product_InStocks               = models.IntegerField(default=0)
    product_img1                   = models.ImageField()
    product_img2                   = models.ImageField()
    product_img3                   = models.ImageField()
    product_img4                   = models.ImageField(blank=True, null=True)
    product_img5                   = models.ImageField(blank=True, null=True)
    product_img6                   = models.ImageField(blank=True, null=True)
    product_img7                   = models.ImageField(blank=True, null=True)
    product_img8                   = models.ImageField(blank=True, null=True)
    product_img9                   = models.ImageField(blank=True, null=True)
    product_img10                  = models.ImageField(blank=True, null=True)
    prduct_adding_date             = models.DateField(auto_now_add=True)
    product_id                     = models.CharField(default='Product ID', max_length=30)
    product_search_tags            = models.TextField(default='Product Search Tags', max_length=254)
    product_meta_title_for_search  = models.CharField(default="Meta Title", max_length=150)
    product_type_tag               = models.CharField(default='Like New or Sale or Hot', max_length=50)#it's like hot,new, small
    product_available_colors       = models.TextField(default='Product colors', max_length=254)
    product_condition              = models.CharField(default="Like New or Used", max_length=254)

    def __str__(self):
        return self.product_name+'|'+str(self.pk)
