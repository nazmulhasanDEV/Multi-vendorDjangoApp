from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from users.models import CustomUser, Security_question, Answer
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from super_admin.models import Contact_info, FAQ_category, FAQs, Newsletter_Subscriber,VisitorsMessage
from super_admin.models import Seller, Front_end_slider_list, Product_category, Product_subcategory, Service, Service_subcategory # "Service" and "Service_subcategory" models are for online services
from customer.models import Customer_account
from service.models import Posted_jobList, InPersonService_cat, InPersonService_subcat # These models for In Person service models
from users.models import Security_question

@login_required(login_url='/super/admin/login/')
def super_admin_base(request):
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    return render(request,'super_admin/base.html')

#super custom-admin home
@login_required(login_url='/super/admin/login/')
def super_admin_home(request):

    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    return render(request, 'super_admin/home.html')

#super custom-admin login-register part
def super_admin_login_register(request):

    return render(request,'super_admin/login_register.html')

#super custom-admin login part
def super_admin_login(request):

    if request.method == 'POST':
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')

        if email != '' and password != '':
            try:
                admin = CustomUser.objects.get(email=email).is_admin
                if admin == True:
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request,user)
                        return redirect('superAdminHome')

                    else:
                        messages.warning(request,'User not found!!')
                else:
                    messages.warning(request, "You are not admin!")
            except:
                messages.warning(request, "User Not Found!!")

    return render(request,'super_admin/login_register.html')

#super admin logout part
def super_admin_logout(request):
    logout(request)
    return redirect('superAdminLoginRegister')

#site contact_info part
@login_required(login_url='/super/admin/login/')
def site_contact_info(request):

    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        contact_email   = request.POST.get('contact_email')
        mobile_number   = request.POST.get('mobile_number')
        facebook_link   = request.POST.get('facebook_link')
        twitter_link    = request.POST.get('twitter_link')
        instagram_link  = request.POST.get('instagram_link')
        pinterest_link  = request.POST.get('pinterest_link')
        contact_address = request.POST.get('contact_address')

        if contact_email != '' and mobile_number != '' and facebook_link != '' and twitter_link != '' and instagram_link != '' and pinterest_link != '' and contact_address != '':
            try:
                del_site_logo    = Contact_info.objects.all().first()
                fd               = FileSystemStorage() #deleting past site logo
                fd.delete(del_site_logo.site_logo_name)

                save_contact_info = Contact_info.objects.all().first()
                site_logo         = request.FILES['site_logo']
                fs                = FileSystemStorage() #updating new site logo

                site_logo_name = fs.save(site_logo.name, site_logo)
                logo_url       = fs.url(site_logo_name)

                save_contact_info.email         = contact_email
                save_contact_info.mobile        = mobile_number
                save_contact_info.address       = contact_address
                save_contact_info.site_logo_url = logo_url
                save_contact_info.site_logo_name= site_logo_name
                save_contact_info.fb            = facebook_link
                save_contact_info.tw            = twitter_link
                save_contact_info.instagrm      = instagram_link
                save_contact_info.pinterest     = pinterest_link
                save_contact_info.save()
                messages.success(request, "Successfully updated contact info!")
                return redirect('siteContactInfo')
            except:
                save_contact_info = Contact_info.objects.all().first()
                site_logo         = request.FILES['site_logo']
                fs                = FileSystemStorage() #updating new site logo

                site_logo_name    = fs.save(site_logo.name, site_logo)
                logo_url          = fs.url(site_logo_name)

                save_contact_info.email           = contact_email
                save_contact_info.mobile          = mobile_number
                save_contact_info.address         = contact_address
                save_contact_info.site_logo_url   = logo_url
                save_contact_info.site_logo_name  = site_logo_name
                save_contact_info.fb              = facebook_link
                save_contact_info.tw              = twitter_link
                save_contact_info.instagrm        = instagram_link
                save_contact_info.pinterest       = pinterest_link
                save_contact_info.save()
                messages.success(request, "Successfully updated contact info!")
                return redirect('siteContactInfo')

    #grabing data from models
    contact_info = Contact_info.objects.all().first()

    return render(request, 'super_admin/contact_info.html',{'contact_info':contact_info})


#edit site contact_info part
@login_required(login_url='/super/admin/login/')
def edit_site_contact_info(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        contact_email   = request.POST.get('contact_email')
        mobile_number   = request.POST.get('mobile_number')
        facebook_link   = request.POST.get('facebook_link')
        twitter_link    = request.POST.get('twitter_link')
        instagram_link  = request.POST.get('instagram_link')
        pinterest_link  = request.POST.get('pinterest_link')
        contact_address = request.POST.get('contact_address')

        if contact_email != '' and mobile_number != '' and facebook_link != '' and twitter_link != '' and instagram_link != '' and pinterest_link != '' and contact_address != '':
            try:
                site_logo         = request.FILES['site_logo']
                fs                = FileSystemStorage() #updating new site logo

                convert_file_name   =  str(site_logo)
                file_extension      =  convert_file_name.split('.')
                original_extension  =  file_extension[len(file_extension)-1].lower()

                if original_extension == 'png' or original_extension == 'jpg' or original_extension == 'jpeg' or original_extension == 'svg':

                    #delete old site logo
                    del_site_logo    = Contact_info.objects.all().first()
                    fd               = FileSystemStorage() #deleting past site logo
                    fd.delete(del_site_logo.site_logo_name)

                    site_logo_name = fs.save(site_logo.name, site_logo)
                    logo_url       = fs.url(site_logo_name)

                    #updating with informations & site logo
                    save_contact_info = Contact_info.objects.all().first()

                    save_contact_info.email         = contact_email
                    save_contact_info.mobile        = mobile_number
                    save_contact_info.address       = contact_address
                    save_contact_info.site_logo_url = logo_url
                    save_contact_info.site_logo_name= site_logo_name
                    save_contact_info.fb            = facebook_link
                    save_contact_info.tw            = twitter_link
                    save_contact_info.instagrm      = instagram_link
                    save_contact_info.pinterest     = pinterest_link
                    save_contact_info.save()
                    messages.success(request, "Successfully updated contact info!")
                    return redirect('siteContactInfo')
            except:
                save_contact_info = Contact_info.objects.all().first()
                save_contact_info.email           = contact_email
                save_contact_info.mobile          = mobile_number
                save_contact_info.address         = contact_address
                # save_contact_info.site_logo_url   = logo_url
                # save_contact_info.site_logo_name  = site_logo_name
                save_contact_info.fb              = facebook_link
                save_contact_info.tw              = twitter_link
                save_contact_info.instagrm        = instagram_link
                save_contact_info.pinterest       = pinterest_link
                save_contact_info.save()
                messages.success(request, "Successfully updated contact info!")
                return redirect('siteContactInfo')

    #grabing data from models
    contact_info = Contact_info.objects.get(pk=1)

    return render(request, 'super_admin/edit_site_contact_info.html',{'pk':pk, 'contact_info':contact_info})


# add slider to home
@login_required(login_url='/super/admin/login/')
def add_slider_to_home_page(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':

        slider_title      =  request.POST.get('slider_title')
        slider_sub_title  =  request.POST.get('slider_subtitle')

        if slider_title != '' and slider_sub_title != '':
            try:
                slider_img          =  request.FILES['slider_img']
                fs                  =  FileSystemStorage()

                convert_file_name   =  str(slider_img)
                file_extension      =  convert_file_name.split('.')
                original_extension  =  file_extension[len(file_extension)-1].lower()

                if original_extension == 'png' or original_extension == 'jpg' or original_extension == 'jpeg':

                    slider_img_name  =  fs.save(slider_img.name, slider_img)
                    slider_img_url   =  fs.url(slider_img_name)

                    slider_model     =  Front_end_slider_list(slider_img_name=slider_img_name, slider_img_url=slider_img_url, slider_img_title=slider_title, slider_img_subtitle=slider_sub_title)
                    slider_model.save()

                    messages.success(request, 'New slider saved successfully!')

            except:
                pass

    #grab all slider's from database
    slider_list = Front_end_slider_list.objects.all()

    return render(request, 'super_admin/add_slider.html',{'slider_list':slider_list})


# delete slider to home
@login_required(login_url='/super/admin/login/')
def delete_slider_to_home_page(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        slider = Front_end_slider_list.objects.get(pk=pk)
        fd     = FileSystemStorage()
        fd.delete(slider.slider_img_name)
        slider.delete()
        messages.success(request, "Slider deleted!!")
        return redirect('frontEndHomeSlider')

    except:
        messages.warning(request, "Slider can't be deleted!!")
        return redirect('frontEndHomeSlider')

    return redirect('frontEndHomeSlider')


#edit slider to home
@login_required(login_url='/super/admin/login/')
def edit_slider_to_home_page(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    #grab slider data
    slider_data = Front_end_slider_list.objects.get(pk=pk)

    if request.method == 'POST':
        slider_title      =  request.POST.get('slider_title')
        slider_sub_title  =  request.POST.get('slider_subtitle')

        if slider_title != '' and slider_sub_title != '':
            try:
                slider_img          =  request.FILES['slider_img']
                fs                  =  FileSystemStorage()

                convert_file_name   =  str(slider_img)
                file_extension      =  convert_file_name.split('.')
                original_extension  =  file_extension[len(file_extension)-1].lower()

                if original_extension == 'png' or original_extension == 'jpg' or original_extension == 'jpeg' or original_extension == 'jfif':

                    old_slider_img = Front_end_slider_list.objects.get(pk=pk)
                    fd = FileSystemStorage()
                    fd.delete(old_slider_img.slider_img_name)

                    slider_img_name                   =  fs.save(slider_img.name, slider_img)
                    slider_img_url                    =  fs.url(slider_img_name)

                    exact_slider                      = Front_end_slider_list.objects.get(pk=pk)
                    exact_slider.slider_img_name      =  slider_img_name
                    exact_slider.slider_img_url       =  slider_img_url
                    exact_slider.slider_img_title     =  slider_title
                    exact_slider.slider_img_subtitle  =  slider_sub_title
                    exact_slider.save()

                    messages.success(request, 'Successfully update slider!')
                    return redirect('frontEndHomeSlider')

            except:
                exact_slider                      = Front_end_slider_list.objects.get(pk=pk)
                exact_slider.slider_img_title     =  slider_title
                exact_slider.slider_img_subtitle  =  slider_sub_title
                exact_slider.save()
                messages.success(request, "Slider updated successfully!")
                return redirect('frontEndHomeSlider')

    return render(request, 'super_admin/edit_slider.html',{'slider_data':slider_data, 'pk':pk})


#super admin add faq category part
@login_required(login_url='/super/admin/login/')
def site_faqs_category(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        faq_category = request.POST.get('faq_category')
        if faq_category != '':
            try:
                faq_category = FAQ_category(faq_category=faq_category)
                faq_category.save()
                messages.success(request, 'Successfully added FAQ category!')
            except:
                messages.warning(request, 'Failed to add new FAQ category!')

    #grab the FAQ all the categories
    faq_list = FAQ_category.objects.all()

    return render(request, 'super_admin/site_faqs_category.html',{'faq_category_list':faq_list})

#super admin delete faq category part
@login_required(login_url='/super/admin/login/')
def site_faq_category_delete(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        faq = FAQ_category.objects.filter(pk=pk)
        faq.delete()
        messages.success(request, 'Successfully deleted FAQ category!')
        return redirect('siteFaqsCategory')
    except:
        messages.warning(request, 'Failed to delete FAQ category!')

    return redirect('siteFaqsCategory')

#super admin delete faq category part
@login_required(login_url='/super/admin/login/')
def site_faqs_answer(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    faq_categories = FAQ_category.objects.all()

    if request.method == 'POST':
        faq_question        = request.POST.get('faq_question')
        faq_category_id   = request.POST.get('faq_category')
        faq_answer        = request.POST.get('faq_answer')

        if faq_question != '' and faq_category_id != '' and faq_answer != '':
            try:
                faq_category_name = FAQ_category.objects.get(pk=faq_category_id).faq_category #getting category name
                faqs              = FAQs(faq_category_id=faq_category_id, faq_category= faq_category_name,faq_question= faq_question,faq_ans=faq_answer)
                faqs.save()
                messages.success(request, "Successfully added!")
            except:
                messages.warning(request, "Failed to add FAQ!")

    faqs = FAQs.objects.all()

    return render(request, 'super_admin/faq_questions_answer.html',{'faq_categories':faq_categories, 'faqs':faqs})


#super admin delete faq category part
@login_required(login_url='/super/admin/login/')
def site_faqs_delete(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        faq = FAQs.objects.filter(pk=pk)
        faq.delete()
        messages.success(request, 'Successfully deleted FAQ!')
        return redirect('siteFaqsAnswer')
    except:
        messages.warning(request, 'Failed to delete FAQ!')

    return render(request, 'super_admin/faq_questions_answer.html')

#super admin product category
@login_required(login_url='/super/admin/login/')
def add_category_and_cat_list(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        category_name = request.POST.get('add_category')

        if category_name != '':
            try:
                capitalize_cat_name = category_name.capitalize()
                category_model = Product_category(category_name=capitalize_cat_name, category_id=0)
                category_model.save()
                messages.success(request, "New category has been added!")
                return redirect('catAddList')
            except:
                messages.warning(request, "Category name may be exist!")
                return redirect('catAddList')

    categories = Product_category.objects.all()

    return render(request, 'super_admin/add_category_and_list.html', {'product_categories':categories})


#super admin delete product category
@login_required(login_url='/super/admin/login/')
def delete_product_category(request, pk):

    try:
        category = Product_category.objects.filter(pk=pk)
        category.delete()
        messages.success(request, "Category has been deleted!")
        return redirect('catAddList')
    except:
        messages.warning(request, "Category can't be deleted!")
        return redirect('catAddList')

    return render('catAddList')


#super admin product subcategories
@login_required(login_url='/super/admin/login/')
def add_subcategories(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        subcat_name = request.POST.get('add_subcategory')

        if subcat_name != '':
            try:
                category = Product_category(pk=pk)#grabbing category name to save as "rel_with_cat"
                capitalize_subcat = subcat_name.capitalize()
                sub_category = Product_subcategory(subcategory_name=capitalize_subcat, cat_id=pk, rel_with_cat=category)
                sub_category.save()
                messages.success(request, "New sub-category has been added!")
                return redirect('addSubCat', pk=pk)
            except:
                messages.warning(request, "New category name can't be added!")
                return redirect('addSubCat', pk=pk)

    subcategories = Product_subcategory.objects.filter(rel_with_cat=pk)

    return render(request, 'super_admin/add_subcategories.html', {'pk': pk, 'subcat_list':subcategories})


#delete product subcategories
@login_required(login_url='/super/admin/login/')
def delete_subcategory(request, pk):
    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        subcat = Product_subcategory.objects.get(pk=pk)
        category_id = subcat.cat_id
        subcat.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('addSubCat', pk=category_id)
    except:
        subcat = Product_subcategory.objects.get(pk=pk)
        category_id = subcat.cat_id
        messages.warning(request, "Can't be deleted!")
        return redirect('addSubCat', pk=category_id)

    return render(request, 'super_admin/add_subcategories.html', {'pk': pk})

# add online service categories
@login_required(login_url='/super/admin/login/')
def add_service_category(request):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        service_cat_name = request.POST.get('add_service_category')
        service_cat_img  = request.FILES['service_cat_img']

        if service_cat_name != '':
            try:
                capitalize_service_name = service_cat_name.capitalize()
                service_cat_model = Service(service_name=capitalize_service_name, service_id=0, service_image=service_cat_img)
                service_cat_model.save()
                messages.success(request, "New service category has been added!")
                return redirect("addServiceCat")

            except:
                messages.warning(request, "New service category name can't be added!")
                return redirect("addServiceCat")

    #grabing all service category name
    service_cat_list = Service.objects.all()

    return render(request, 'super_admin/add_service_category.html', {'service_cat_list':service_cat_list})

# add online service subcategories
@login_required(login_url='/super/admin/login/')
def del_service_categories(request,pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        # grabing the subcategories under categories
        subcats_under_cat = Service_subcategory.objects.filter(rel_with_cat=pk)

        # deleting the subcats under cats
        for x in subcats_under_cat:
            fss = FileSystemStorage()
            fss.delete(x.service_subcat_img.name)

        fs = FileSystemStorage()
        service_category = Service.objects.get(pk=pk)
        fs.delete(service_category.service_image.name)
        service_category.delete()
        messages.success(request, "Successfully deleted!!")
        return redirect("addServiceCat")
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect("addServiceCat")

    return redirect("addServiceCat")


#add online service subcategories
@login_required(login_url='/super/admin/login/')
def add_service_subcategories(request, pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        service_subcat_name = request.POST.get('add_service_subcategory')
        subcat_img          = request.FILES['subcat_img']

        if service_subcat_name != '':

            capitalize_name = service_subcat_name.capitalize()
            query1          = Q(subcategory_name=capitalize_name)
            query2          = Q(cat_id=pk)
            length_of_subcat_under_cat = len(Service_subcategory.objects.filter(query1 & query2))

            if length_of_subcat_under_cat == 0:

                try:
                    capitalize_service_subcat_name = service_subcat_name.capitalize()
                    service_subcat_model           = Service_subcategory(rel_with_cat=Service(pk=pk), subcategory_name=capitalize_service_subcat_name, cat_id=pk, service_subcat_img=subcat_img)
                    service_subcat_model.save()
                    messages.success(request, "New sub-category has been added!")
                    return redirect("addServiceSubcat", pk=pk)
                except:
                    messages.warning(request, "New sub-category can't be added!")
                    return redirect("addServiceSubcat", pk=pk)

            else:
                messages.warning(request, "Subcategory already exists!!")
                return redirect("addServiceSubcat", pk=pk)
    #grabing service subcat list
    service_subcat_list = Service_subcategory.objects.filter(cat_id=pk)#or filter(rel_with_cat=pk)

    return render(request, "super_admin/add_service_subcategory.html", {'pk':pk, 'service_subcat_list':service_subcat_list})



#add online service subcategories
@login_required(login_url='/super/admin/login/')
def del_service_subcat(request, pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        fs = FileSystemStorage()
        service_subcat = Service_subcategory.objects.get(pk=pk)
        cat_id         = service_subcat.cat_id
        fs.delete(service_subcat.service_subcat_img.name)
        service_subcat.delete()
        messages.success(request, "Successfully deleted!")
        return redirect("addServiceSubcat", pk=cat_id)
    except:
        service_subcat = Service_subcategory.objects.get(pk=pk)
        cat_id         = service_subcat.cat_id
        messages.warning(request, "Can't be deleted!")
        return redirect("addServiceSubcat", pk=cat_id)

    return redirect("addServiceSubcat", pk=pk)


#add in person service categories
@login_required(login_url='/super/admin/login/')
def inperson_service_cat(request):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':

        cat_name = request.POST.get('add_service_category')
        cat_img  = request.FILES['service_cat_img']

        if cat_name != '':
            try:
                cat_name_capitalize = cat_name.capitalize()
                inperson_service_cat_model = InPersonService_cat(name=cat_name_capitalize, img= cat_img)
                inperson_service_cat_model.save()
                messages.success(request, "New category has been added!")
                return redirect('addInpersonServiceCat')
            except:
                messages.warning(request, "New category can't be added!!")
                return redirect('addInpersonServiceCat')

    # grabing all inperson service categories
    service_cat_list = InPersonService_cat.objects.all()

    return render(request, 'super_admin/add_inperson_category.html', {'inperson_service_cats': service_cat_list})


# delete in person service categories
@login_required(login_url='/super/admin/login/')
def del_inperson_service_cat(request, pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        # grabing the subcategories under the parent category
        subcat_under_this_cat = InPersonService_subcat.objects.filter(rel_with_cat=pk)

        # deleting the sucategory under the parent category
        for x in subcat_under_this_cat:
            fss = FileSystemStorage()
            fss.delete(x.img.name)

        fs = FileSystemStorage()
        cat = InPersonService_cat.objects.get(pk=pk)
        fs.delete(cat.img.name) #deleting the category image
        cat.delete() # finally deleting the category
        messages.success(request, "Category has been deleted!")
        return redirect('addInpersonServiceCat')
    except:
        messages.warning(request, "Category can't be deleted!")
        return redirect('addInpersonServiceCat')

    return redirect('addInpersonServiceCat')


# delete in person service sub-categories
@login_required(login_url='/super/admin/login/')
def add_inperson_service_subcat(request, pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        inperson_service_subcat_name = request.POST.get('add_service_subcategory')
        inperson_service_subcat_img = request.FILES['subcat_img']

        if inperson_service_subcat_name != '':
            capitalize_name = inperson_service_subcat_name.capitalize()
            query1 = Q(name=capitalize_name)
            query2 = Q(rel_with_cat=pk)
            # searching the length of subcategory in a particular category by pk
            length_of_subcat = len(InPersonService_subcat.objects.filter(query1 & query2))

            if length_of_subcat == 0:

                try:
                    capitalize_subcat_name = inperson_service_subcat_name.capitalize()# capitalizing the input subcategory name
                    subcat_model           = InPersonService_subcat(name=capitalize_subcat_name, img=inperson_service_subcat_img, rel_with_cat=InPersonService_cat(pk=pk))
                    subcat_model.save()
                    messages.success(request, "New subcategory has been added!")
                    return redirect('addInpersonSubcat', pk=pk)

                except:
                    messages.warning(request, "This subcategoy can't be added!")
                    return redirect('addInpersonSubcat', pk=pk)

            else:
                messages.warning(request, "Subcategory already exists!")
                return redirect('addInpersonSubcat', pk=pk)

    #grabing all the subcategories based on pk
    subcat_list = InPersonService_subcat.objects.filter(rel_with_cat=pk)

    return render(request,'super_admin/add_inperson_subcategory.html', {'pk':pk, 'inperson_subcat_list':subcat_list})


# delete in person service sub-categories
@login_required(login_url='/super/admin/login/')
def del_inperson_service_subcat(request, pk):

    # verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    subcat = InPersonService_subcat.objects.get(pk=pk)
    cat_id = subcat.rel_with_cat.pk # grabing the category id of this subcategory

    try:
        fs = FileSystemStorage()
        fs.delete(subcat.img.name)
        subcat.delete()
        messages.success(request, "Subcategory has been deleted!")
        return redirect('addInpersonSubcat', pk=cat_id)
    except:
        messages.warning(request, "Subcategory can't be deleted!!")
        return redirect('addInpersonSubcat', pk=cat_id)

    return redirect('addInpersonSubcat', pk=cat_id)

#newsletter subscriber list
@login_required(login_url='/super/admin/login/')
def newsletter_subscriber(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    subscriber_list = Newsletter_Subscriber.objects.all()

    return render(request, 'super_admin/subscriber_list.html', {'sbscrber_list':subscriber_list})

#delete newsletter subscriber
@login_required(login_url='/super/admin/login/')
def delete_subscriber(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        subscriber = Newsletter_Subscriber.objects.filter(pk=pk)
        subscriber.delete()
        messages.success(request, "Successfully deleted!")
        return redirect('newsltrSubcrbrList')
    except:
        messages.warning(request, "Failed to delete subscriber!")
        return redirect('newsltrSubcrbrList')

    return redirect('newsltrSubcrbrList')


#visitors message list
@login_required(login_url='/super/admin/login/')
def visitors_message_list(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    visitor_msg_list = VisitorsMessage.objects.all()

    return render(request, 'super_admin/visitors_message_list.html',{'visitor_msg_list':visitor_msg_list})

# delete visitors message list
@login_required(login_url='/super/admin/login/')
def delete_visitor_msg(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        visitor_msg = VisitorsMessage.objects.filter(pk=pk)
        visitor_msg.delete()
        messages.success(request, 'Succesfully deleted the message!')
        return redirect('visitorMsgList')
    except:
        messages.warning(request, "Message can't be deleted!")
        return redirect('visitorMsgList')

    return redirect('visitorMsgList')


# product seller list
@login_required(login_url='/super/admin/login/')
def online_seller_list(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    return render(request, 'super_admin/online_seller_list.html',{'selller_list':seller_list})


# Service seller list
@login_required(login_url='/super/admin/login/')
def service_provider_list(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    seller_list = Seller.objects.all()

    return render(request, 'super_admin/service_provider_list.html',{'selller_list':seller_list})

# Service seller list
@login_required(login_url='/super/admin/login/')
def customer_list(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    customerList = Customer_account.objects.all()

    return render(request, 'super_admin/customer_list.html', {'customer_list':customerList})


# Super admin setting
@login_required(login_url='/super/admin/login/')
def super_admin_security_question_setting(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    # grabing Security question model
    security_question_model = Security_question.objects.all()

    if request.method == 'POST':
        question = request.POST.get('security_question')
        answer   = request.POST.get('answer')

        if question != '' and answer != '':
            question = get_object_or_404(Security_question, pk=question)
            answer_model = Answer(user=request.user,user_question=question,user_answer=answer)
            answer_model.save()
            messages.success(request, "Answer has been added!")
            return redirect('superAdminSecurityQuestionSetting')

    # grabing the security question
    added_security_question = get_object_or_404(Answer, user=request.user)

    # sending data to template
    question_context = {
        'security_questions' : security_question_model,
        'added_security_question' : added_security_question,
    }

    return render(request, 'super_admin/admin_security_question_setting.html', question_context)


# Super admin setting
@login_required(login_url='/super/admin/login/')
def super_admin_account_setting(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    user = get_object_or_404(CustomUser, email=request.user)

    # getting emails of user

    user_email = user.email
    email_to_array = user_email.split('@')
    toStr = email_to_array[0]
    toStar = ''
    for x in range(len(toStr)-1):
        toStar = toStar+"*"
    prefix_of_email = toStr[0]+toStar+toStr[len(toStr)-1]+'@'+email_to_array[1]


    # getting data to change password
    if request.method == 'POST':
        old_pass     = request.POST.get('old_password')
        new_pass     = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        if new_pass != confirm_pass:
            messages.warning(request, "Password did not matched!")
            return redirect('superAdminAccountSetting')
        else:
            if len(new_pass)<8:
                messages.warning(request, "Password must have to 8 characters!")
                return redirect('superAdminAccountSetting')

            else:
                authenticate_user = authenticate(request, email=request.user, password=old_pass)

                if authenticate_user is not None:
                    user = CustomUser.objects.get(email=request.user)
                    user.set_password(new_pass)
                    user.save()
                    return redirect('superAdminLoginRegister')

    # sending data to template
    admin_context = {
        'user' : user,
        'prefix_of_email': prefix_of_email,
    }

    return render(request, 'super_admin/admin_account_setting.html', admin_context)

# Inperson service related job list posted by customer
@login_required(login_url='/super/admin/login/')
def inperosn_posted_job_list_by_customer(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    # grabing all the Inperson Related posted jobs by customer
    inperson_posted_jobList_by_customer = Posted_jobList.objects.filter(service_type_id='ips')

    joblist_context = {
        'inperson_job_list': inperson_posted_jobList_by_customer,
    }

    return render(request, 'super_admin/inperson_posted_job_list_by_customer.html', joblist_context)

# Delete In Person service related  posted job from the list
@login_required(login_url='/super/admin/login/')
def del_inperson_posted_job_from_list(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    # grabing all the online job list posted by customer
    try:
        inperson_posted_job_by_customer = get_object_or_404(Posted_jobList, pk=pk)
        fs = FileSystemStorage()
        fs.delete(inperson_posted_job_by_customer.attached_file.name)
        inperson_posted_job_by_customer.delete()
        messages.success(request, "Job post has been removed!")
        return redirect('inPersonpostedJobListByCustomer')

    except:
        messages.warning(request, "Job post can't be removed!")
        return redirect('inPersonpostedJobListByCustomer')

    # download_BfXTl1k.jfif
    return redirect('inPersonpostedJobListByCustomer')


# grabing Online service related job list posted by customer
@login_required(login_url='/super/admin/login/')
def online_posted_job_list_by_customer(request):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    # graning all the online job list posted by customer
    online_posted_jobList_by_customer = Posted_jobList.objects.filter(service_type_id='os')

    joblist_context = {
        'online_job_list': online_posted_jobList_by_customer,
    }

    return render(request, 'super_admin/online_posted_job_list_by_customer.html', joblist_context)


# Delete Online service related  posted job from the list
@login_required(login_url='/super/admin/login/')
def del_online_posted_job_from_list(request, pk):

    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    # grabing all the online job list posted by customer
    try:
        online_posted_job_by_customer = get_object_or_404(Posted_jobList, pk=pk)
        fs = FileSystemStorage()
        fs.delete(online_posted_job_by_customer.attached_file.name)
        online_posted_job_by_customer.delete()
        messages.success(request, "Job post has been removed!")
        return redirect('onlineJobListByCustomer')

    except:
        messages.warning(request, "Job post can't be removed!")
        return redirect('onlineJobListByCustomer')

    # download_BfXTl1k.jfif
    return redirect('onlineJobListByCustomer')


# add security question for user
@login_required(login_url='/super/admin/login/')
def add_security_question_for_user(request):
    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    if request.method == 'POST':
        sequrity_question_for_user = request.POST.get('add_sequrity_question_for_user')

        if sequrity_question_for_user != '':
            try:
                security_question_model = Security_question(question=sequrity_question_for_user)
                security_question_model.save()
                messages.success(request, "Security has been added!")
                return redirect('addSecurityQuestionForUser')
            except:
                messages.warning(request, "Security can't be added!")
                return redirect('addSecurityQuestionForUser')

        else:
            messages.warning(request, "Empty fields are not allowed!")
            return redirect('addSecurityQuestionForUser')

    # grabing all the security question from database model
    security_questions = Security_question.objects.all()

    sec_question_context = {
        'security_questions' : security_questions,
    }

    return render(request, 'super_admin/add_security_question_for_user.html', sec_question_context)

# del security question for user
@login_required(login_url='/super/admin/login/')
def del_security_question_for_user(request, **kwargs):
    #verifying whether the user is the super admin or not
    if not request.user.is_admin:
        return redirect('superAdminLoginRegister')

    try:
        get_sec_question = Security_question.objects.filter(pk=kwargs['pk']).first()
        get_sec_question.delete()
        return redirect('addSecurityQuestionForUser')
    except:
        messages.warning(request, "Can't be deleted!")
        return redirect('addSecurityQuestionForUser')

    return redirect('addSecurityQuestionForUser')


#error page(404 page)
def error_page_404(request):

    return render(request, 'super_admin/404.html')



