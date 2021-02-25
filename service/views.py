from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from super_admin.models import Service, Service_subcategory # online service category and subcategory
from .models import InPersonService_cat, InPersonService_subcat
from super_admin.models import Contact_info
from .models import OnlineServiceList, InPersonServiceList
from seller_admin.models import Seller_portfolio, Seller_profile, Profile_pic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.db.models import Q


# online Service categories by in sidenav
def service_categories(request):

    service_cats = Service.objects.all()

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    #sending data to template
    service_cats_context = {
        'contact_info':contact_info,
        'service_cats':service_cats
    }

    return render(request, 'front_service/online_service_categories.html', service_cats_context)

# online service categories in card
def service_categories_by_card(request):

    # grabing all service categories
    service_cats = Service.objects.all()

    #pagination part
    page = request.GET.get('page', 1)
    paginator = Paginator(service_cats, 1)

    try:
        cats_page_obj = paginator.page(page)
    except PageNotAnInteger:
        cats_page_obj = paginator.page(1)
    except EmptyPage:
        cats_page_obj = paginator.page(paginator.num_pages)

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # sending data to template
    card_context = {
        'contact_info' : contact_info,
        'service_cats' : service_cats,
        'cats_page_obj': cats_page_obj,
    }

    return render(request, 'front_service/online_service_cats_cards.html', card_context)

# online service subcats in card
# url is in service.urls
def service_subcats(request, pk):

    # grabing subcats data
    subcats = Service_subcategory.objects.filter(rel_with_cat=pk)

    #pagination part
    page = request.GET.get('page', 1)
    paginator = Paginator(subcats, 1)

    try:
        subcats_page_obj = paginator.page(page)
    except PageNotAnInteger:
        subcats_page_obj = paginator.page(1)
    except EmptyPage:
        subcats_page_obj = paginator.page(paginator.num_pages)

    cat = Service.objects.get(pk=pk)

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # sending data to template
    subcats_context = {
        'contact_info'   : contact_info,
        'pk'             : pk,
        'sub'            : subcats,
        'cat'            : cat,
        'subcat_page_obj': subcats_page_obj,
    }

    return render(request, 'front_service/online_service_subcats.html', subcats_context)

# In person service category
# url is in service.urls
def inperson_service_cat(request):

    # In person service category
    categories = InPersonService_cat.objects.all()

    #pagination part
    page = request.GET.get('page', 1)
    paginator = Paginator(categories, 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # sending data to template
    inperson_service_cat = {
        'contact_info'          :contact_info,
        'inperson_service_cats' :categories,
        'page_obj'              : page_obj,
    }

    return render(request, 'front_service/inperson_service_cat.html', inperson_service_cat)


# In person service category
# url is in service.urls
def inperson_service_subcat(request, pk):

    # In person service sub-category
    in_person_service_subcat = InPersonService_subcat.objects.filter(rel_with_cat=pk)

    #pagination part
    page = request.GET.get('page', 1)
    paginator = Paginator(in_person_service_subcat, 1)

    try:
        subcat_page_obj = paginator.page(page)
    except PageNotAnInteger:
        subcat_page_obj = paginator.page(1)
    except EmptyPage:
        subcat_page_obj = paginator.page(paginator.num_pages)

    # In person service cat
    cat = InPersonService_cat.objects.get(pk=pk)

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # sending data to template
    inpersonService_subcat = {
        'contact_info':contact_info,
        'pk':pk,
        'inperson_service_subcats':in_person_service_subcat,
        'cat':cat,
        #paginated data
        'subcat_page_obj': subcat_page_obj,
    }

    return render(request, 'front_service/inperson_service_subcat.html', inpersonService_subcat)


# online service seller list
def online_service_seller_list(request, pk):

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # seller list based on online service category
    seller_list = OnlineServiceList.objects.filter(service_subcategory=pk)

    return render(request, 'seller_list/online_sellerList_by_subcat.html', {'contact_info':contact_info, 'pk':pk, 'seller_list':seller_list})


# Online Service seller details page
def online_service_details(request, pk):


    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    #grabing seller by pk
    seller_details = OnlineServiceList.objects.get(pk=pk)
    seller_identity = seller_details.seller_id

    # grabing others services of this seller
    others_services_of_this_seller = OnlineServiceList.objects.filter(seller_id=seller_identity)
    # pack_others_services = []
    # for x in others_services_of_this_seller:
    #     if x.pk not in pack_others_services:
    #         pack_others_services.append(x.pk)
    # print(pack_others_services)

    # grabing seller profile info by pk
    seller_portfolio_info = Seller_profile.objects.get(user=seller_identity)
    #grabing seller portfolio images
    seller_portfolio_imgs = Seller_portfolio.objects.filter(user=seller_identity)

    # grabing profile picture of seller
    seller_profile_pic = get_object_or_404(Profile_pic, user=seller_identity)

    context = {
        'contact_info'                   : contact_info,
        'seller_details'                 : seller_details,
        'seller_portfolio_info'          : seller_portfolio_info,
        'seller_portfolio_imgs'          : seller_portfolio_imgs,
        'profile_pic'                    : seller_profile_pic,
        'others_services_of_this_seller' : others_services_of_this_seller,
        'pk'                             : pk,
    }

    return render(request, 'seller_list/online_seller_details.html', context)


# inperson service seller list
def inperson_service_seller_list(request, pk):

    #contact info or help center
    contact_info = Contact_info.objects.get(pk=1)

    # seller list based on online service category
    seller_list = InPersonServiceList.objects.filter(service_subcategory=pk)
    print(len(seller_list))

    return render(request, 'seller_list/inperson_sellerList_by_subcat.html', {'contact_info':contact_info, 'pk':pk, 'seller_list':seller_list})

# Inperson Service seller details page
def inperson_service_details(request, pk):


    #contact info or help center
    contact_info = Contact_info.objects.all().first()

    #grabing seller by pk
    inperson_seller_details = InPersonServiceList.objects.get(pk=pk)
    seller_identity = inperson_seller_details.seller_id

    # grabing seller profile info by pk
    # seller_profile_info = get_object_or_404(Seller_profile, user=seller_identity)
    seller_profile_info = Seller_profile.objects.filter(user=seller_identity).first()

    #grabing seller portfolio images
    seller_portfolio_imgs = Seller_portfolio.objects.filter(user=seller_identity)

    # grabing profile picture of seller
    # seller_profile_pic = get_object_or_404(Profile_pic, user=seller_identity)
    seller_profile_pic = Profile_pic.objects.filter(user=seller_identity).first()

    inperson_service_details_context = {
        'contact_info'           :contact_info,
        'inperson_seller_details': inperson_seller_details,
        'seller_portfolio_info'  : seller_profile_info,
        'seller_portfolio_imgs'  : seller_portfolio_imgs,
        'seller_profile_pic'     : seller_profile_pic,
    }

    return render(request, 'seller_list/inperson_seller_details.html', inperson_service_details_context)


