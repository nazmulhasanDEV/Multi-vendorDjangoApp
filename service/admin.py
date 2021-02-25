from django.contrib import admin
from .models import InPersonService_cat, InPersonService_subcat, Posted_jobList

# all online service list based on seller
from .models import OnlineServiceList, InPersonServiceList


#In person service category
admin.site.register(InPersonService_cat)
#In person service subcategory
admin.site.register(InPersonService_subcat)

# online service list
admin.site.register(OnlineServiceList)

# InPerson service list
admin.site.register(InPersonServiceList)

# storing jobs posted by customer/buyer
admin.site.register(Posted_jobList)
