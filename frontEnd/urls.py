from django.conf.urls import url,include
from . import views
urlpatterns = [

    #product list page url
    url(r'^product/list/$', views.product_list, name='productList'),

    #product details page url
    url(r'^product/details/$', views.product_details, name='productDetails'),

    #product items
    url(r'^women/clothing/items/$', views.women_clothing_items, name='womenClothingItems'),

    #male clothing items
    url(r'^male/clothing/items/$', views.male_clothing_items, name='maleClothingItem'),

    #kids clothing items
    url(r'^kids/clothing/items/$', views.kids_clothing_items, name='kidsClothingItem'),

    # all clothing items
    url(r'^all/clothing/items/$', views.all_clothing_items, name='allClothingItem'),

]


