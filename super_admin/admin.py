from django.contrib import admin
from .models import Contact_info, FAQ_category, FAQs, Newsletter_Subscriber, VisitorsMessage, Seller, Front_end_slider_list, Product_category
from .models import Product_subcategory, Service, Service_subcategory


admin.site.register(Contact_info)
admin.site.register(FAQ_category)
admin.site.register(FAQs)
#visitor subscriber list
admin.site.register(Newsletter_Subscriber)

#visitors message model
admin.site.register(VisitorsMessage)

#seller list model
admin.site.register(Seller)

#Front-end home page slider model
admin.site.register(Front_end_slider_list)
#product categories
admin.site.register(Product_category)
#product subcategories
admin.site.register(Product_subcategory)

#services category
admin.site.register(Service)
#services subcategory
admin.site.register(Service_subcategory)


