from django.contrib import admin
# from .models import Profile_pic, Product, Seller_profile, Seller_portfolio,
from .models import *
# Register your models here.

admin.site.register(Profile_pic)
admin.site.register(Product)

#seller profile for showing skills and description about him in front-end
admin.site.register(Seller_profile)
admin.site.register(Seller_portfolio)

# seller verification code model
admin.site.register(Verification_code)

