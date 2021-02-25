from django.conf.urls import url,include
from . import views
urlpatterns = [

    # front-end part
    url(r'^base/$', views.front_base, name='frontBase'),
    url(r'^$', views.home, name='Home'),

    #front-end create account part
    url(r'^create/front/user/account/$', views.front_create_account, name='createFrontUserAccount'),
    #front-end login customer/visitors
    url(r'^login/customer/$', views.front_login_visitor, name='loginCustomer'),

    #front-end login visitor/customer part
    url(r'^login/front/user/$', views.login_page, name='LoginFrontUser'),

    # choose option to login in different page
    url(r'^choose/login/option/$', views.choose_option_to_login, name='chooseOptionToLogin'),

    #front-end logout visitor/customer
    url(r'^logout/visitor/$', views.front_logout_visitor, name='logOurvisitor'),

    #front-end wish-list part
    url(r'^front/user/wish/list/$', views.wish_list, name='frontWishList'),

    #front-end view-cart part
    url(r'^user/view/cart/$', views.cart_view, name='frontCartView'),

    #front-end view-cart part
    url(r'^user/checkout/$', views.checkout, name='frontCheckOut'),

    #front-end FAQs part
    url(r'^user/faqs/$', views.faqs, name='faqs'),

    #front-end contact us url
    url(r'^contact/us/$', views.contact_us, name='contactUs'),

    #front-end visitor profile page
    url(r'^customer/profile/$', views.customer_profile, name='customerProfile'),

    # front-end visitor/customer profile pic change url
    url(r'^customer/profile/pic/$', views.change_profile_pic, name='changeProfilePic'),

    # front-end visitor/customer account change password
    url(r'^customer/change/password/$', views.change_password, name='changePassword'),

    # job post url
    url(r'^post/job/$', views.post_job, name='postJob'),

    #front-end 404-error page
    url(r'^error/404/$', views.error_404_page, name='error_404'),


]


