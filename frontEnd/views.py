from django.shortcuts import render, redirect, get_object_or_404
from super_admin.models import Contact_info

# front-end product page view
def product_list(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/product_page.html',{'contact_info':contact_info})

# front-end product details page
def product_details(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/product_details.html',{'contact_info':contact_info})

# front-end male clothing  items
def male_clothing_items(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/male_clothing.html',{'contact_info':contact_info})

# front-end women clothing items
def women_clothing_items(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/women_clothing_items.html',{'contact_info':contact_info})

# front-end women clothing items
def kids_clothing_items(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/kids_clothing_items.html',{'contact_info':contact_info})

# front-end all clothing items
def all_clothing_items(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/all_clothing.html',{'contact_info':contact_info})



# seller list by service category & subcategory
# def seller_listBy_service_subcat(request, pk):
#
#     return render(request, '')
