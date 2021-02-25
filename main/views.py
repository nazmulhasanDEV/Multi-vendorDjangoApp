from django.shortcuts import render,redirect,get_object_or_404
from users.models import CustomUser
from super_admin.models import Contact_info, FAQs, FAQ_category, Newsletter_Subscriber,VisitorsMessage
from super_admin.models import Front_end_slider_list
from django.contrib import messages
from customer.models import Customer_account, Profile_edit, Customer_profile_pic
from users.models import CustomUser
from django.contrib.auth import authenticate, logout, login
from service.models import InPersonService_subcat, Posted_jobList, InPersonService_cat
# Service model represets Online Service Categories
from super_admin.models import Service_subcategory, Service
import random
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



#front-end part
def front_base(request):

    return render(request,'front_end/base.html')

#front-end home view
def home(request):

    if request.method == 'POST':
        newsletter_email = request.POST.get('newsletter_email')
        if newsletter_email != '' and len(Newsletter_Subscriber.objects.filter(subscriber_email=newsletter_email)) == 0:
            try:
                newsletters = Newsletter_Subscriber(subscriber_email=newsletter_email)
                newsletters.save()
                return redirect('Home')
            except:
                return redirect('Home')
        else:
            message = "Sorry! Try again to subscribe!"
            defined_error = "This e-mail already exists! Try with another!"
            # return render(request, '')
            return render(request,'front_end/404.html',{'msg':message, 'defined_error':defined_error})

    contact_info = Contact_info.objects.all().first()

    #slider for home page
    slider_list = Front_end_slider_list.objects.all()

    # grabing the inperson service subcats
    inperson_service_subcats = InPersonService_subcat.objects.all()

    # grabing online service sucategories
    online_service_subcats   = Service_subcategory.objects.all()

    # randomly grabing inperson service subcategories from database
    # inperson_serviceSubcats = random.choices(inperson_service_subcats, k=2)
    empty_inperson_serviceSubcats = []
    if len(inperson_service_subcats) != 0:
        inperson_serviceSubcats = random.choices(inperson_service_subcats, k=2)
        for x in inperson_serviceSubcats:
            empty_inperson_serviceSubcats.append(x)

    # randomly grabing online service subcategories from database
    # online_serviceSubcats = random.choices(online_service_subcats, k=2)
    empty_online_service_subcats = []
    if len(online_service_subcats) != 0:
        online_serviceSubcats = random.choices(online_service_subcats, k=2)
        for x in online_serviceSubcats:
            empty_online_service_subcats.append(x)

    #sending data to template
    home_context = {
        'contact_info'             : contact_info,
        'slider_list'              : slider_list,
        'inperson_service_subcats' : empty_inperson_serviceSubcats,
        'online_service_subcats'   : empty_online_service_subcats,
    }


    return render(request,'front_end/home.html', home_context)

#front-end register visitor/customer and create user account
def front_create_account(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    #creating customer/visitors account
    if request.method == 'POST':
        visitor_first_name         = request.POST.get('customer_fistname')
        visitor_last_name          = request.POST.get('customer_lastname')
        visitor_username           = request.POST.get('customer_username')
        visitor_email              = request.POST.get('customer_email')
        visitor_password           = request.POST.get('customer_password')
        visitor_confirm_password   = request.POST.get('customer_confirm_password')

        if visitor_first_name != '' and visitor_username != '' and visitor_email != '' and visitor_password != '':
            try:
                if len(visitor_password)<8:
                    messages.warning(request, "Your password must be 8 Characters!")
                    return redirect('createFrontUserAccount')

                else:
                    if visitor_password != visitor_confirm_password:
                        messages.warning(request, "Password did not match!")
                        return redirect('createFrontUserAccount')
                    elif len(CustomUser.objects.filter(email=visitor_email)) != 0:
                        messages.warning(request, "This email already exists!")
                        return redirect('createFrontUserAccount')
                    elif len(CustomUser.objects.filter(username=visitor_username)) != 0:
                        messages.warning(request, "Username already exists!")
                    else:
                        customer_name = visitor_first_name+' '+visitor_last_name
                        user = CustomUser.objects.create_user(email=visitor_email,username=visitor_username, name=customer_name, is_customer=True, password=visitor_password)
                        save_to_customer_model = Customer_account(customer_firstname=visitor_first_name, customer_lastname=visitor_last_name, customer_username=visitor_username,customer_email=visitor_email)
                        save_to_customer_model.save()
                        messages.success(request, "Thanks for creating account!")
                        return redirect('createFrontUserAccount')
            except:
                messages.warning(request, "Something wrong. Try again!")
                return redirect('createFrontUserAccount')


    return render(request,'front_end/create_account.html',{'contact_info':contact_info})

# front-end login visitor/customer
def front_login_visitor(request):

    if request.method == 'POST':
        email = request.POST.get('customer_email')
        password = request.POST.get('customer_password')

        if email != '' and password != '':
            authenticate_user = authenticate(request, email=email, password=password)
            if authenticate_user is not None:
                login(request, authenticate_user)
                return redirect('Home')
            else:
                messages.warning(request, "Wrong email or password!")
                return redirect('LoginFrontUser')

    return redirect('Home')

# front-end login visitor/customer
def front_logout_visitor(request):

    try:
        logout(request)
    except:
        pass

    return redirect('Home')

# front-end visitor/customer login page view
def login_page(request):

    #site contact info
    contact_info = Contact_info.objects.get(pk=1)

    return render(request,'front_end/login_register.html',{'contact_info':contact_info})

# choose option to login in different page
def choose_option_to_login(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    login_context = {
        'contact_info':contact_info,
    }

    return render(request, 'front_end/choose_option_to_login.html', login_context)


#front-end FAQ part
def faqs(request):

    #site FAQs
    faqs_category = FAQ_category.objects.all()
    faqs          = FAQs.objects.all()

    #site contact info
    contact_info = Contact_info.objects.get(pk=1)

    return render(request,'front_end/FAQ.html',{'faqs':faqs, 'faq_category':faqs_category,'contact_info':contact_info})

#contact us page for front-end
# @login_required(login_url='/')
def contact_us(request):

    if request.method == 'POST':
        visitors_name    = request.POST.get('name')
        visitors_email   = request.POST.get('email')
        visitors_phone   = request.POST.get('phone')
        message_subject  = request.POST.get('subject')  #it's optional
        visitors_message = request.POST.get('message')

        if visitors_name != '' and visitors_email != '' and visitors_phone != '' and visitors_message != '':
            try:
                if message_subject == '':
                    message_subject = 'Null'
                visitors_msg = VisitorsMessage(visitor_name=visitors_name,visitor_email=visitors_email,visitor_phone=visitors_phone,visitor_msg_subject=message_subject,visitor_msg=visitors_message)
                visitors_msg.save()
                messages.success(request, 'Message sent successfully!')
                return redirect('contactUs')
            except:
                messages.warning(request, "Message can't be sent!")
                return redirect('contactUs')

    contact_info = Contact_info.objects.all().first()

    return render(request, 'front_end/contact_us.html',{'contact_info':contact_info})


#front-end customer/visitor profile page
@login_required(login_url='/')
def customer_profile(request):

    if not request.user.is_customer:
        return redirect('/')

    contact_info = Contact_info.objects.all().first()

    # grabing data from edit_profile form
    if request.method == 'POST':
        customer_first_name    = request.POST.get('customer_first_name')
        customer_last_name     = request.POST.get('customer_last_name')
        customer_address       = request.POST.get('customer_address')
        country_name           = request.POST.get('country_name')
        state_name             = request.POST.get('state_name')
        customer_postcode      = request.POST.get('customer_postcode')

        if customer_first_name != '' and country_name != '' and state_name != '':
            try:
                pass
                #grabing customer account
                customer_account_model = Customer_account.objects.filter(customer_email=request.user).first()
                edit_profile_model = Profile_edit(
                    user_id             = request.user,
                    customer_account    = customer_account_model,
                    customer_firstname  = customer_first_name,
                    customer_lastname   = customer_last_name,
                    address             = customer_address,
                    country_name        = country_name,
                    state_name          = state_name,
                    postcode            = customer_postcode
                )
                edit_profile_model.save()
                messages.success(request, "You profile has been updated!")
                return redirect('customerProfile')

            except:
                messages.warning(request, "Can't be saved your data! Try again!")
                return redirect('customerProfile')
        else:
            messages.warning(request, "Please fill up the empty fields!")
            return redirect('customerProfile')

    # grabing profile pic
    customer_profile_pic = Customer_profile_pic.objects.filter(user_id=request.user).first()

    # grabing user name from CustomeUser model
    user      = CustomUser.objects.filter(email=request.user).first()
    user_name = user.name
    # grabing edited user full name
    edited_user_name  = Profile_edit.objects.filter(user_id=request.user).first()


    user_profile_name = ''

    if edited_user_name:
        user_first_name   = edited_user_name.customer_firstname
        user_last_name    = edited_user_name.customer_lastname
        user_full_name    = user_first_name +' '+ user_last_name
        user_profile_name = user_profile_name + user_full_name
    else:
        user_profile_name = user_profile_name + user_name

    # sending data to template
    customer_profile_context = {
        'contact_info'      : contact_info,
        'profile_pic'       : customer_profile_pic,
        'user_profile_name' : user_profile_name,
    }

    return render(request, 'front_end/customer_profile_page.html', customer_profile_context)

# customer profile pic changing view
@login_required(login_url='/')
def change_profile_pic(request):

    if not request.user.is_customer:
        return redirect('/')

    # grabing data to update profile picture
    if request.method == 'POST':
        try:
            profile_pic = request.FILES['profile_picture']
            if len(Customer_profile_pic.objects.filter(user_id=request.user)) > 0:
                fs = FileSystemStorage()
                del_old_img = get_object_or_404(Customer_profile_pic, user_id=request.user)
                fs.delete(del_old_img.profile_pic.name) # deleting old image
                profile_pic_model = Customer_profile_pic(user_id=request.user, profile_pic=profile_pic) # saving new data to database
                profile_pic_model.save()
                messages.success(request, "Profile picture has been updated!")
                return redirect('changeProfilePic')

            else:
                profile_pic_model = Customer_profile_pic(user_id=request.user, profile_pic=profile_pic) # saving new data to database
                profile_pic_model.save()
                messages.success(request, "Profile picture has been updated!")
                return redirect('changeProfilePic')
        except:
            messages.warning(request, "Profile picture can't be updated!")
            return redirect('changeProfilePic')

    # grabing profile pic
    customer_profile_pic = Customer_profile_pic.objects.filter(user_id=request.user).first()

    # grabing user name from CustomeUser model
    user = CustomUser.objects.filter(email=request.user).first()
    user_name = user.name
    # grabing edited user full name
    user_full_name = ''
    edited_user_name  = Profile_edit.objects.filter(user_id=request.user).first()
    if edited_user_name:
        user_first_name   = edited_user_name.customer_firstname
        user_last_name    = edited_user_name.customer_lastname
        full_name    = user_first_name+' '+user_last_name
        user_full_name = user_full_name + full_name

    user_profile_name = ''
    if edited_user_name:
        user_profile_name = user_profile_name + user_full_name
    else:
        user_profile_name = user_profile_name + user_name

    # grabing admin contact info
    contact_info = Contact_info.objects.all().first()

    # sending data to template
    customer_profile_pic = {
        'contact_info': contact_info,
        'profile_pic' : customer_profile_pic,
        'user_profile_name' : user_profile_name,
    }

    return render(request, 'front_end/customer_profile_page.html', customer_profile_pic)

# customer profile change password view
@login_required(login_url='/')
def change_password(request):

    if not request.user.is_customer:
        return redirect('/')

    # grabing data to update profile picture
    if request.method == 'POST':
        current_pass = request.POST.get('current_pass')
        new_pass = request.POST.get('new_pass')
        confirm_pass = request.POST.get('confirm_pass')

        if new_pass != confirm_pass:
            messages.warning(request, "Password didn't match!")
            return redirect('customerProfile')

        else:
            try:
                user = authenticate(request, email=request.user, password=current_pass)
                if user is not None:
                    if len(new_pass) < 8:
                        messages.warning(request, "Password must be in 8 characters!")
                        return redirect('customerProfile')
                    else:
                        user = get_object_or_404(CustomUser, email=request.user)
                        user.set_password(new_pass)
                        user.save()
                        messages.success(request, "Password has been updated!")
                        return redirect('customerProfile')
            except:
                messages.warning(request, "Password can't be changed!")
                return redirect('customerProfile')

    return render(request, 'front_end/customer_profile_page.html')

# job posting view
@login_required(login_url='/')
def post_job(request):

    if not request.user.is_customer:
        return redirect('/')


    # ajax request for getting service type
    # os = Online Service
    # ips = In Person Service
    selected_service_type = request.GET.get('selected_service_type')
    selected_category_by_service = request.GET.get('selected_category_by_service')

    # chaining with service type and service categories
    if selected_service_type != '':
        online_service_categories = Service.objects.all().values()
        inperson_service_categories = InPersonService_cat.objects.all().values()

        if selected_service_type == 'os':
            service_categories_by_type = list(online_service_categories)
            if request.is_ajax():
                return JsonResponse({'service_cats_by_service_type': service_categories_by_type})

        if selected_service_type == 'ips':
            service_categories_by_type = list(inperson_service_categories)
            if request.is_ajax():
                return JsonResponse({'service_cats_by_service_type': service_categories_by_type})

    # chainging with service categories and service subcategories
    if selected_category_by_service != '':
        selectedServiceType = request.GET.get('selected_serviceType')

        if selectedServiceType == 'os':
            selectedCategoryId                    = int(selected_category_by_service)
            online_service_subcategories_by_cat   = list(Service_subcategory.objects.filter(rel_with_cat=selectedCategoryId).values())
            if request.is_ajax():
                return JsonResponse({'service_subcats_by_cat': online_service_subcategories_by_cat})

        if selectedServiceType == 'ips':
            selectedCategoryId = int(selected_category_by_service)
            inperson_service_subcategories_by_cat = list(InPersonService_subcat.objects.filter(rel_with_cat=selectedCategoryId).values())
            if request.is_ajax():
                return JsonResponse({'service_subcats_by_cat': inperson_service_subcategories_by_cat})

    # grabing posted jobs data
    if request.method == 'POST':
        description_of_service = request.POST.get('description_of_service')
        attached_file          = request.FILES['attached_file']
        service_type           = request.POST.get('service_type')
        service_category       = request.POST.get('service_category_by_type')
        service_subcategory    = request.POST.get('service_subcategory')
        project_budget         = request.POST.get('project_budget')
        delivery_time          = request.POST.get('delivery_time')


        if description_of_service != '' and attached_file != '' and service_type != '' and service_category != '':
            try:
                if attached_file.size > 30720:
                    print("File size is not allowed!")

                if service_type == 'os':
                    os_subcat_model = Service_subcategory.objects.filter(pk=service_subcategory).first()# os means online service

                    converted_service_cat_id = int(service_category)
                    converted_service_subcat_id = int(service_subcategory)
                    converted_project_budget = int(project_budget)
                    converted_deliverty_time = int(delivery_time)

                    job_model = Posted_jobList(
                        user= request.user,
                        service_description= description_of_service,
                        attached_file= attached_file,
                        service_type_in_character= "Online Service",
                        service_type_id= service_type,
                        service_category_in_character = os_subcat_model.rel_with_cat.service_name,
                        service_cat_id= converted_service_cat_id,
                        service_subcat_id = converted_service_subcat_id,
                        service_subcategory_in_character = os_subcat_model.subcategory_name,
                        project_budget= converted_project_budget,
                        project_delivery_time= converted_deliverty_time
                    )
                    job_model.save()
                    messages.success(request, "Successfully posted your job!")
                    return redirect('postJob')

                if service_type =='ips':
                    ips_subcat = InPersonService_subcat.objects.filter(pk=service_subcategory).first()# ips means In Person Service

                    converted_service_cat_id = int(service_category)
                    converted_service_subcat_id = int(service_subcategory)
                    converted_project_budget = int(project_budget)
                    converted_deliverty_time = int(delivery_time)

                    job_model = Posted_jobList(
                        user= request.user,
                        service_description= description_of_service,
                        attached_file= attached_file,
                        service_type_in_character= "In Person Service",
                        service_type_id= service_type,
                        service_category_in_character = ips_subcat.rel_with_cat.name,
                        service_cat_id= converted_service_cat_id,
                        service_subcat_id = converted_service_subcat_id,
                        service_subcategory_in_character = ips_subcat.name,
                        project_budget= converted_project_budget,
                        project_delivery_time= converted_deliverty_time
                    )
                    job_model.save()
                    messages.success(request, "Successfully posted your job!")
                    return redirect('postJob')

            except:
                messages.warning(request, "Sorry! Can't post your job request!")
                return redirect('postJob')

    # grabing admin contact info
    contact_info = Contact_info.objects.all().first()

    job_post_context = {
        'contact_info': contact_info,
    }

    return render(request, 'front_end_customer/job_post.html', job_post_context)

#404 error page for front-end
def error_404_page(request):

    return render(request, 'front_end/404.html')



# this part is only for  product section not related with services

#front wish-list view
def wish_list(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request,'front_end/wish_list.html',{'contact_info':contact_info})

#front-end view-cart section view
def cart_view(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request,'front_end/view_cart.html',{'contact_info':contact_info})

#front-end checkout part
def checkout(request):

    #site contact info
    contact_info = Contact_info.objects.all().first()

    return render(request,'front_end/checkout.html',{'contact_info':contact_info})
