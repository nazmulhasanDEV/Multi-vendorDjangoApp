from django.conf.urls import url,include
from . import views
urlpatterns = [

    # online service categories
    url(r'^service/categories/$', views.service_categories, name='serviceCats'), # getting service category function

    # online service cat cards
    url(r'^service/categories/cards/$', views.service_categories_by_card, name='serviceCatsCards'), # getting service categories to show as card in category page

    # online service subcat list
    url(r'^service/subcat/(?P<pk>\d+)/$', views.service_subcats, name='serviceSubcat'),

    # inperson service cat url
    url(r'^inperson/service/cat/$', views.inperson_service_cat, name='inpersonServiceCat'),

    # inperson service subcat url
    url(r'^inperson/service/subcat/(?P<pk>\d+)/$', views.inperson_service_subcat, name='inpersonServiceSubcat'),

    # online service seller list
    url(r'^online/service/seller/list/(?P<pk>\d+)/$', views.online_service_seller_list, name='onlineServiceSellerList'),
    # online service seller details page
    url(r'^online/seller/details/(?P<pk>\d+)/$', views.online_service_details, name='onlineServiceSellerDetails'),


    # inperson service seller list
    url(r'^inperson/service/seller/list/(?P<pk>\d+)/$', views.inperson_service_seller_list, name='inpersonServiceSellerList'),
    #
    url(r'^inperson/service/seller/details/(?P<pk>\d+)/$', views.inperson_service_details, name='inpersonServiceSellerDetails'),


]


