from django.conf.urls import url,include
from . import views

urlpatterns = [

    #seller/vendor register and login url
    url(r'^register/user/$', views.register_user, name='registerUser' ),

    #admin panel url for seller/vendor
    url(r'^seller/admin/panel/$', views.seller_admin_base, name='sellerAdminBase'),
    #seller/vendor admin panel home page
    url(r'^seller/admin/panel/home/$', views.seller_admin_home, name='sellerAdminHome'),
    #seller/vendor admin panel profile setting
    url(r'^seller/admin/profile/setting/$', views.seller_admin_profile_setting, name='sellerAdminProfileSetting'),

    #admin panel login url for seller/vendor
    url(r'^seller/admin/panel/login/$', views.seller_login, name='sellerAdminLogin'),

    #logout vendors/sellers from admin panel
    url(r'^seller/admin/panel/logout/$', views.seller_logout, name='sellerAdminLogout'),

    # add profile_info for seller list and details
    url(r'^add/profile/info/seller/list/$', views.add_profile_info, name='addProfileInfo'),
    #delete profile info for seller list and details
    url(r'^del/profile/info/seller/list/(?P<pk>\d+)/$', views.delete_profile_info, name='delProfileInfo'),
    # add portfolio images
    url(r'^add/portfolio/img/$', views.add_portfolio_info, name='addPortfolioImg'),
    # Delete portfolio image
    url(r'^del/portfolio/img/(?P<pk>\d+)/$', views.delete_portfolio_img, name='delPortfolioImg'),


    #add online services
    url(r'^add/online/service/$', views.add_online_services, name="addOnlineServices"),
    # online service list by category
    url(r'^online/service/list/$', views.online_service_list_by_category, name="servicesListByCat"),
    #edit online service
    url(r'^edit/online/service/list/(?P<pk>\d+)/$', views.edit_online_service, name='editOnlineServiceList'),
    # delete online service
    url(r'^del/online/service/list/(?P<pk>\d+)/$', views.del_online_service, name='delOnlineServiceList'),


    #add inperson services
    url(r'^add/inperson/service/$', views.add_inperson_services, name="addInpersonServices"),
    # inperson service list by category
    url(r'^inperson/service/list/$', views.inperson_service_list_by_category, name="InpersonservicesListByCat"),
    # edit inperson service list
    url(r'^edit/inperson/service/list/(?P<pk>\d+)/$', views.edit_inperson_services, name="editInpersonservicesList"),
    url(r'^del/inperson/service/list/(?P<pk>\d+)/$', views.del_inperson_service, name="delInpersonServicesList"),


    # account setting url
    url(r'^seller/account/setting/$', views.account_setting, name='sellerAccountSetting'),
    # security question url
    url(r'^seller/security/question/setting/$', views.security_question_setting, name='sellerSecurityQuestionSetting'),
    #change security question
    url(r'^update/security/question/$', views.update_security_question_setting, name='updateSecurityQuestion'),

    # inperson service related jobs url
    url(r'^inperson/service/jobs/$', views.inperson_service_related_jobs, name='inpersonServiceRelatedJobs'),
    # online service related job url
    url(r'^online/service/jobs/$', views.online_service_related_jobs, name='onlineServiceRelatedJobs'),

    # verificatio code url
    url(r'^verification/code/(?P<username>\w+)/$', views.verification_code, name='sellerVerificationCode'),




    # *******************************Product part starts*********************************************
    #seller product  category
    url(r'^product/list/ByCategory/$', views.product_list_by_category, name='productListByCategory'),

    #add product
    url(r'^add/product/$', views.add_product, name='addProduct'),

    #product lists by their category
    url(r'^product/list/(?P<pk>\d+)/$', views.product_list, name='productList'),

    #edit product data
    url(r'^edit/product/(?P<pk>\d+)/$', views.edit_product, name='editProduct'),

    #delete product
    url(r'^del/product/(?P<pk>\d+)/$', views.delete_product, name="delProduct"),

    # *****************************ends product parts**************************************************

]

