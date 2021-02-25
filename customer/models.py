from django.db import models
from users.models import CustomUser

# model to save buyers/Customers account
class Customer_account(models.Model):

    account_register_date  = models.DateField(auto_now_add=True)
    customer_firstname     = models.CharField(default='Name', max_length=50)
    customer_lastname      = models.CharField(default='Name', max_length=50)
    customer_username      = models.CharField(default='Userame', max_length=50)
    customer_email         = models.CharField(default='Email', max_length=50)

    def __str__(self):
        return self.customer_username +'|'+str(self.pk)

# Edit Profile Model buyer/customer
class Profile_edit(models.Model):
  user_id              = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
  customer_account     = models.ForeignKey(Customer_account, on_delete=models.CASCADE)
  customer_firstname   = models.CharField(max_length=25, blank=True, null=True)
  customer_lastname    = models.CharField(max_length=25, blank=True, null=True)
  address              = models.TextField(max_length=60)
  country_name         = models.CharField(max_length=15)
  state_name           = models.CharField(max_length=20)
  postcode             = models.CharField(max_length=15, blank=True, null=True)

  def __str__(self):
      return f'User: {self.user_id}'

#  profile picture model for customer

class Customer_profile_pic(models.Model):
    user_id     = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField()

    def __str__(self):
        return f'User: {self.user_id}'


