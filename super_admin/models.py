from django.db import models
from users.models import CustomUser

# Contact Informations for front-end part
class Contact_info(models.Model):
    super_admin      = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    email            = models.CharField(default='Email', max_length=255)
    mobile           = models.CharField(default='014555', max_length=255)
    address          = models.TextField(default='Address', max_length=350)
    site_logo_url    = models.CharField(default='Logo url', max_length=255)
    site_logo_name   = models.CharField(default='Logo name', max_length=255)
    fb               = models.CharField(default='Facebook Link', max_length=450)
    tw               = models.CharField(default='Facebook Link', max_length=450)
    instagrm         = models.CharField(default='Facebook Link', max_length=450)
    pinterest        = models.CharField(default='Facebook Link', max_length=450)

    def __str__(self):
        return self.email +'|'+str(self.pk)

#site FAQs type
class FAQ_category(models.Model):

    faq_category = models.CharField(default='FAQ Category', max_length=255)

    def __str__(self):
        return self.faq_category + '|'+str(self.pk)

#Site FAQs

class FAQs(models.Model):

    faq_category_id = models.IntegerField(default=0)
    faq_category = models.CharField(default='FAQ', max_length=150)
    faq_question = models.CharField(default='FAQs', max_length=255)
    faq_ans  = models.TextField(default='FAQs Ans', max_length=450)

    def __str__(self):
        return "FAQ"+"|"+str(self.pk)

# newsletter subscriber list
class Newsletter_Subscriber(models.Model):

    subscriber_email = models.CharField(default='Email', max_length=255)
    subscribing_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subscriber_email+'|'+str(self.pk)

# visitor's message model
class VisitorsMessage(models.Model):

    visitor_name             = models.CharField(default='Name', max_length=60)
    visitor_email            = models.CharField(default='Email', max_length=255)
    visitor_phone            = models.CharField(default='Phone', max_length=20)
    visitor_msg_subject      = models.TextField(default='Subject', blank=True, null=True)
    visitor_msg              = models.TextField(default='Message')
    visitor_msg_sending_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.visitor_name+'|'+str(self.pk)

#seller list
class Seller(models.Model):

    username         = models.CharField(default='Username', max_length=150)
    name             = models.CharField(default='Name', max_length=150)
    service_provider = models.BooleanField(default=False)
    product_seller   = models.BooleanField(default=False)
    register_date    = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username+'|'+self.name


#Slider Home Page for Front-End
class Front_end_slider_list(models.Model):

    slider_img_name     = models.CharField(default='Image Name', max_length=255)
    slider_img_url      = models.CharField(default='Image url', max_length=255)
    slider_img_title    = models.CharField(default='Image title', max_length=255)
    slider_img_subtitle = models.CharField(default='Image subtitle', max_length=255)

    def __str__(self):
        return self.slider_img_name+'|'+str(self.pk)


#product category model
class Product_category(models.Model):

    category_name        = models.CharField(default='Category Name', max_length=35, unique=True)
    category_id          = models.IntegerField(default=0)
    category_adding_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.category_name +'|'+str(self.pk)

#product subcategories model
class Product_subcategory(models.Model):

    subcategory_name    =  models.CharField(default='Subcat', max_length=15, unique=True)
    cat_id              =  models.IntegerField(default=0)
    rel_with_cat        =  models.ForeignKey(Product_category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name +'|' + str(self.rel_with_cat)


# online services category model
class Service(models.Model):
    service_name    = models.CharField(default='Service Name', max_length=150, unique=True)
    service_id      = models.IntegerField(default=0)
    service_image   = models.ImageField(blank=True, null=True)
    adding_date     = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.service_name+ '|'+str(self.pk)

# Online service subcategory model
class Service_subcategory(models.Model):
    rel_with_cat     = models.ForeignKey(Service, on_delete=models.CASCADE)
    subcategory_name = models.CharField(default="Subcategory Name", max_length=150)
    cat_id           = models.IntegerField(default=0)
    service_subcat_img = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.subcategory_name+'|'+str(self.pk)

### You will found the offline service classes/Models in Service App

# add security question for the user to make their account secure



