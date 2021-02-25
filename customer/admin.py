from django.contrib import admin
from .models import Customer_account, Profile_edit, Customer_profile_pic


# Customer account model
admin.site.register(Customer_account)

# edit profile model
admin.site.register(Profile_edit)
# profile pic
admin.site.register(Customer_profile_pic)



