from django.db import models
from users.models import CustomUser
from seller_admin.models import Seller_profile


# In Person service category model
class InPersonService_cat(models.Model):

    name = models.CharField(default='Category', max_length=20)
    img  = models.ImageField()
    adding_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name+"|"+str(self.pk)

# In Person service subcategory model
class InPersonService_subcat(models.Model):

    name         = models.CharField(default='Subcategory', max_length=20)
    img          = models.ImageField()
    rel_with_cat = models.ForeignKey(InPersonService_cat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name+"|"+str(self.pk)



# Model for online service seller (list of all online service seller)
# ***typeMistake*** it will be *****OnlineServiceSellerList****
class OnlineServiceList(models.Model):

    seller_id              = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # relating with seller profile model
    # seller_profile         = models.ForeignKey(Seller_profile, on_delete=models.CASCADE, blank=True, null=True)

    service_title          = models.CharField(default="Service Title", max_length=60)
    service_description    = models.TextField(default='Service Description')
    service_related_img1   = models.ImageField()
    service_category       = models.IntegerField(default=0)
    service_subcategory    = models.IntegerField(default=0)
    seller_country         = models.CharField(max_length=30, default='USA')
    sellerCountryFullName  = models.CharField(max_length=30, default='USA')
    sellerStateFullName    = models.CharField(max_length=30, default='')
    seller_state           = models.CharField(max_length=30, default='')
    joining_date           = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.seller_id)+"|"+str(self.pk)

# Service Model for  In Person service (interested to provice In person service list of all Inperson service seller)
class InPersonServiceList(models.Model):

    seller_id              = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # relating with seller profile model
    # seller_profile         = models.ForeignKey(Seller_profile, on_delete=models.CASCADE, blank=True, null=True)

    service_title          = models.CharField(default="Service Title", max_length=60)
    service_description    = models.TextField(default='Service Description')
    service_related_img1   = models.ImageField()
    service_category       = models.IntegerField(default=0)
    service_subcategory    = models.IntegerField(default=0)
    seller_country         = models.CharField(max_length=30, default='USA')
    sellerCountryFullName  = models.CharField(max_length=30, default='USA')
    sellerStateFullName    = models.CharField(max_length=30, default='')
    seller_state           = models.CharField(max_length=30, default='')
    joining_date           = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.seller_id)+"|"+str(self.pk)


# posted service model
class Posted_jobList(models.Model):
    user                             = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_description              = models.TextField()
    attached_file                    = models.FileField(blank=True, null=True)
    service_type_id                  = models.CharField(max_length=50)
    service_type_in_character        = models.CharField(max_length=50)
    service_cat_id                   = models.IntegerField()
    service_category_in_character    = models.CharField(max_length=50)
    service_subcat_id                = models.IntegerField()
    service_subcategory_in_character = models.CharField(max_length=50)
    project_budget                   = models.IntegerField()
    project_delivery_time            = models.IntegerField()
    project_posted_at                = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user} PK: {self.pk}'

