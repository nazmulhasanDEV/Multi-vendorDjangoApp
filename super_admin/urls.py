from django.conf.urls import url,include
from . import views

urlpatterns = [

    #admin panel base
    url(r'^super/admin/panel/$', views.super_admin_base, name='superAdminBase'),
    #admin panel home
    url(r'^super/admin/panel/home/$', views.super_admin_home, name='superAdminHome'),

    #super custom-admin login-register url
    url(r'^super/admin/login/register/$', views.super_admin_login_register, name='superAdminLoginRegister'),

    #super custom-admin login url
    url(r'^super/admin/login/$', views.super_admin_login, name='superAdminLogin'),
    #super custom-admin logout url
    url(r'^super/admin/logout/$', views.super_admin_logout, name='superAdminLogout'),

    #super admin setting url
    url(r'^super/admin/security/question/setting/$', views.super_admin_security_question_setting, name='superAdminSecurityQuestionSetting'),
    #super admin password setting url
    url(r'^super/admin/account/setting/$', views.super_admin_account_setting, name='superAdminAccountSetting'),

    #super custom-admin contact-info url
    url(r'^site/contact/info/$', views.site_contact_info, name='siteContactInfo'),
    #edit site contact info
    url(r'^edit/site/contact/info/(?P<pk>\d+)/$', views.edit_site_contact_info, name='editSiteContactInfo'),

    #add slider to home page
    url(r'^front-end/home/slider/$', views.add_slider_to_home_page, name='frontEndHomeSlider'),
    #delete slider for front-end home page
    url(r'^delete/front_end/home/slider/(?P<pk>\d+)/$', views.delete_slider_to_home_page, name='delSliderToHomePage'),
    #edit slider front-end home page
    url(r'^edit/front_end/home/slider/(?P<pk>\d+)/$', views.edit_slider_to_home_page, name='editSliderToHomePage'),


    #super custom-admin site faqs category
    url(r'^site/faqs/$', views.site_faqs_category, name='siteFaqsCategory'),
    # delte faq category
    url(r'^delete/faq/category/(?P<pk>\d+)/$', views.site_faq_category_delete, name='delFaqCategory'),
    #super admin site faqs and answer
    url(r'^site/faqs/answer/$', views.site_faqs_answer, name='siteFaqsAnswer'),
    #delete FAQ
    url(r'^site/faqs/delete/(?P<pk>\d+)/$', views.site_faqs_delete, name='siteFaqDelete'),


    # product category and subcategory adding and listing
    url(r'^add/category/list/$', views.add_category_and_cat_list, name='catAddList'),
    #delete product category
    url(r'^del/category/list/(?P<pk>\d+)/$', views.delete_product_category, name='delProductCategory'),

    #adding product subcategories
    url(r'^add/subcategory/(?P<pk>\d+)/$', views.add_subcategories, name='addSubCat'),
    #delete product subcategories
    url(r'^del/product/subcat/(?P<pk>\d+)/$', views.delete_subcategory, name='delProductSubcat'),

    #newsletter subscriber list url
    url(r'^newsletter/subscriber/list/$', views.newsletter_subscriber, name='newsltrSubcrbrList'),
    #delete subscriber from list
    url(r'^nesletter/subscriber/(?P<pk>\d+)/$', views.delete_subscriber, name='delSubscriber'),

    #visitors message list
    url(r'^visitor/message/list/$', views.visitors_message_list, name='visitorMsgList'),

    # delete visitors message list
    url(r'^del/visitor/message/list/(?P<pk>\d+)/$', views.delete_visitor_msg, name='delVisitorMsg'),

    #product seller list
    url(r'^online/seller/list/$', views.online_seller_list, name='onlineSellerList'),
    #Service provider list
    url(r'^service/provider/list/$', views.service_provider_list, name='serviceProviderList'),

    #customer list
    url(r'^customer/list/$', views.customer_list, name='customerList'),

    #add online service category
    url(r'^add/service/category/$', views.add_service_category, name='addServiceCat'),
    #delete online service category
    url(r'^del/service/category/(?P<pk>\d+)/$', views.del_service_categories, name='delServiceCat'),

    #add online service subcategories
    url(r'^add/service/subcat/(?P<pk>\d+)/$', views.add_service_subcategories, name="addServiceSubcat"),
    #delete service subcategories
    url(r'^del/service/subcat/(?P<pk>\d+)/$', views.del_service_subcat, name="delServiceSubcat"),


    # In person service categories
    url(r'^add/inperson/service/categories/$', views.inperson_service_cat, name='addInpersonServiceCat'),
    # delete In person service category
    url(r'^del/inperson/service/category/(?P<pk>\d+)/$', views.del_inperson_service_cat, name='delInpersonServiceCat'),

    # In person service subcat
    url(r'^add/inperson/subcat/(?P<pk>\d+)/$', views.add_inperson_service_subcat, name='addInpersonSubcat'),
    # del In person service subcat
    url(r'^del/inperson/subcat/(?P<pk>\d+)/$', views.del_inperson_service_subcat, name='delInpersonSubcat'),

    # In person service related posted job list by customer
    url(r'^posted/inperson/job/list/by/customer/$', views.inperosn_posted_job_list_by_customer, name='inPersonpostedJobListByCustomer'),
    # delete In Person service related posted job from list
    url(r'^del/job/from?list/(?P<pk>\d+)/$', views.del_inperson_posted_job_from_list, name='delInpersonJobPostFromList'),


    # online service related job list posted by customer
    url(r'^posted/online/job/list/by/customer/$', views.online_posted_job_list_by_customer, name='onlineJobListByCustomer'),
    # delete In Person service related posted job from list
    url(r'^del/job/from?list/(?P<pk>\d+)/$', views.del_online_posted_job_from_list, name='delOnlineJobPostFromList'),

    # add security question for user
    url(r'^add/security/question/For_user/$', views.add_security_question_for_user, name='addSecurityQuestionForUser'),

    # del security question for user
    url(r'^del/security/question/(?P<pk>\d+)/$', views.del_security_question_for_user, name='delSecurityQuestionForUser'),


    #error page(404 page url)
    url(r'^error/404/$', views.error_page_404, name='errorPage404'),

]

