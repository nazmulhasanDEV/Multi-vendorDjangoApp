from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import CustomUser, Answer
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Profile_pic, Seller_portfolio, Seller_profile
from super_admin.models import Seller, Product_category, Product_subcategory
# Online service categories and subcategories
from super_admin.models import Service, Service_subcategory
from seller_admin.models import Product
from seller_admin.models import Profile_pic, Seller_profile # Seller_profile for showing in front end seller list
from service.models import OnlineServiceList, InPersonService_cat, InPersonService_subcat, InPersonServiceList, Posted_jobList
import random
import string
from django.core.paginator import Paginator, EmptyPage, Page, PageNotAnInteger
from users.models import Security_question, Answer
from .models import Seller_profile
from django.contrib import messages
# importing tests.py file
from .tests import star_replace

# importing uuid for generating random number and verification email sending part
import uuid
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Verification_code
import datetime
# import date_time_conversion.dateTime_conversion as dateTimeConverter
from .date_time_conversion import dateTime_conversion as dateTimeConverter


# seller register view
def register_user(request):

    random_val = str(uuid.uuid4()).replace('-', '').upper()[:8]
    print(random_val)

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('seller_type')

        if name != '' and username != '' and password != '' and user_type != '':

            if len(CustomUser.objects.filter(email=email)) != 0:
                messages.warning(request, "This email already exists! Try with new email!")
                return redirect('registerUser')

            if len(CustomUser.objects.filter(username=username)) != 0:
                messages.warning(request, "This username already exists! Try with another!")
                return redirect('registerUser')

            if password == confirm_password:
                if user_type == 'ss':
                    try:
                        # generating random number as verification code
                        verification_code = str(uuid.uuid4()).replace('-', '').upper()[:8]

                        template = render_to_string('seller_admin/mail.html', {'name':name, 'verification_code':verification_code})
                        send_email = EmailMessage(
                            'Verification mail',
                            template,
                            settings.EMAIL_HOST_USER,
                            [email]
                        )
                        send_email.fail_silently=False
                        # send_email.send()

                        if send_email.send():
                            # saving user information to database
                            user = CustomUser.objects.create_user(email=email, username=username,name=name,is_service_seller=True,is_seller=True,password=password)
                            save_to_super_admin_model = Seller(username=username, name=name, service_provider=True, product_seller=False)
                            # save_to_super_admin_model.save()

                            # saving verification code to the database
                            verificatio_code_model = Verification_code(
                                user_email=email,
                                user_username=username,
                                user_verification_code=verification_code,
                                user_active_status=False
                            )
                            verificatio_code_model.save()
                            return redirect('sellerVerificationCode', username=username)
                        else:
                            messages.warning(request, "Verification E-mail can't be sent!")
                            return redirect('registerUser')

                    except:
                        messages.warning(request, "The email you used does not exist!")
                        return redirect('registerUser')


                # if user_type == 'ps':
                #     user = CustomUser.objects.create_user(email=email, username=username,name=name,is_service_seller=False,is_seller=True,password=password)
                #     save_to_super_admin_model = Seller(username=username, name=name, service_provider=False, product_seller=True)
                #     save_to_super_admin_model.save()

    return render(request,'register_login/base.html')

# verificatio code page
def verification_code(request, username):

    verification_code_model = Verification_code.objects.filter(user_username=username).first()

    if verification_code_model:

        if request.method == 'POST':
            verification_code = request.POST.get('verification_code')

            if verification_code != '':

                # converting the mail sending and input code in milliseconds
                mail_sent_time_in_milliseconds = verification_code_model.sent_at.timestamp()
                inpt_time_in_milliseconds = datetime.datetime.now().timestamp()
                time_distance = inpt_time_in_milliseconds - mail_sent_time_in_milliseconds

                if time_distance < 86400000:
                    if verification_code_model.user_verification_code == verification_code:
                        verification_code_model.user_active_status = True
                        verification_code_model.save()
                        return redirect('registerUser')
                    else:
                        messages.warning(request, "Wrong verification code!")
                        return redirect('sellerVerificationCode', username=username)
                else:
                    user = CustomUser.objects.get(username=username)
                    user.delete()
                    messages.warning(request, "Account does not exist!")
                    return redirect('registerUser')

    else:
        messages.warning(request, "Username does not exist!")
        return redirect('registerUser')

    return render(request, 'seller_admin/verification_code.html', {'username': username})

#seller base page and extended this page
@login_required(login_url='/register/user/')
def seller_admin_base(request):

    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    base_context = {
        'seller_profile_pic'           : user_profile,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/base.html', base_context)


#seller/vendor home page
@login_required(login_url='/register/user/')
def seller_admin_home(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    #sending data to template
    home_context = {
        'seller_profile_pic'           : user_profile,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }
    return render(request,'seller_admin/home.html', home_context)

#seller/vendor profile setting page
@login_required(login_url='/register/user/')
def seller_admin_profile_setting(request):
    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    if request.method == 'POST':
        try:

            user_profile_img   =  request.FILES['upload_profile_img']
            fs                 =  FileSystemStorage()

            convert_file_name  =  str(user_profile_img)
            file_extension     =  convert_file_name.split('.')
            original_extension =  file_extension[len(file_extension)-1].lower()

            if original_extension == 'png' or original_extension == 'jpg' or original_extension == 'jpeg' or original_extension == 'jfif':

                profile_img_name   =  fs.save(user_profile_img.name, user_profile_img)
                profile_img_url    =  fs.url(profile_img_name)

                save_img_database  =  Profile_pic(user=request.user, user_name= request.user.name, user_username=request.user.username, user_profile_img=profile_img_url)
                save_img_database.save()
                messages.success(request, 'You successfully updated your profile picture!')
        except:
            pass

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    #sending data to template
    profile_context = {
        'seller_profile_pic'           : user_profile,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request,'seller_admin/profile_setting.html', profile_context)

#vendor/seller login part
def seller_login(request):

    if request.method == 'POST':
        seller_type = request.POST.get('seller_type')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if seller_type != '' and email != '' and password != '':
            try:
                identify = CustomUser.objects.get(email=email)
                seller_verification_status = Verification_code.objects.filter(user_email=email).first()

                if (identify.is_seller == True or identify.is_service_seller == True) and seller_verification_status.user_active_status == True:
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('sellerAdminHome')
                    else:
                        messages.warning(request, 'User not found!')
                else:
                    messages.warning(request, "You are not vendor or Service Provider!")
            except:
                messages.warning(request, "Don't have any account!")

    return render(request,'register_login/base.html')

#vendor/seller logout part
def seller_logout(request):
    logout(request)
    return redirect('registerUser')

# add/update seller profile info for front-end seller list and details
@login_required(login_url='/register/user/')
def add_profile_info(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    if request.method == 'POST':
        seller_and_service_description = request.POST.get('seller_and_service_description')
        seller_skill_set               = request.POST.get('seller_skill_set')
        seller_state_name              = request.POST.get('seller_state_name')
        seller_country_name            = request.POST.get('seller_state_name')

        # dictionary for indicating state name by their values
        state = {
        'AL': 'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California',
        'CO':'Colorado','CT':'Connecticut', 'DE':'Delaware', 'DC':'District Of Columbia',
        'FL':'Florida', 'GA':'Georgia','HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois',
        'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky','LA':'Louisiana', 'ME':'Maine',
        'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota','MS':'Mississippi',
        'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey',
        'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma',
        'OR':'Oregon','PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota',
        'TN':'Tennessee', 'TX':'Texas','UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia',
        'WI':'Wisconsin', 'WY':'Wyoming'
             }

        if seller_and_service_description != '':

            try:
                seller_exect_location = state[seller_state_name]+", "+"United States"
                # grabing 'Seller_profile' model for adding data to show in seller list
                seller_profile = Seller_profile(user= request.user, description_about_seller=seller_and_service_description, skills_of_seller=seller_skill_set, location_of_seller=seller_exect_location)
                seller_profile.save()
                messages.success(request, "Profile Info has been added!")
                return redirect('addProfileInfo')
            except:
                messages.warning(request, "Can't be added your profile info!!")
                return redirect('addProfileInfo')

    # grabing the profile info
    profile_info = Seller_profile.objects.filter(user=request.user)

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    profileInfo_context = {
        'profile_info'                 : profile_info,
        'seller_profile_pic'           : user_profile,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }
    return render(request, "seller_admin/add_profile_info_for_seller_list.html", profileInfo_context)


# add/update portfolio images
@login_required(login_url='/register/user/')
def add_portfolio_info(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    if request.method == 'POST':
        portfolio_img_title   = request.POST.get('portfolio_img_title')
        portfolio_img         = request.FILES['portfolio_img']


        if portfolio_img_title != '' and portfolio_img != '':
            try:
                if len(Seller_portfolio.objects.filter(user=request.user)) <= 4:
                    # seller_profile = Seller_profile.objects.get(user=request.user)#getting the seller profile
                    # seller_profile=seller_profile,
                    seller_portfolio_model = Seller_portfolio(user=request.user, portfolio_img=portfolio_img,img_title=portfolio_img_title)
                    seller_portfolio_model.save()
                    messages.success(request, "New image has been added!")
                    return redirect('addPortfolioImg')
                else:
                    messages.warning(request, "Maximum four images are allowed!")
                    return redirect('addPortfolioImg')

            except:
                messages.warning(request, "Image can't be added!")
                return redirect('addPortfolioImg')

    # grabing the profile info
    profile_info = Seller_profile.objects.filter(user=request.user)

    #grabing 'seller_portfolio' model
    seller_portfolio_info = Seller_portfolio.objects.filter(user=request.user)
    # paginating data
    page = request.GET.get('page', 1)
    paginator = Paginator(seller_portfolio_info, 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    portfolio_context = {
        'profile_info'                 : profile_info,
        'seller_profile_pic'           : user_profile,
        'seller_portfolio_info'        : seller_portfolio_info,
        'page_obj'                     : page_obj,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, "seller_admin/upload_portfolio_img.html", portfolio_context)


# Delete portfolio image
@login_required(login_url='/register/user/')
def delete_portfolio_img(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    try:
        fs = FileSystemStorage()
        seller_portfolio_model = get_object_or_404(Seller_portfolio, pk=pk)
        fs.delete(seller_portfolio_model.portfolio_img.name)
        seller_portfolio_model.delete()
        messages.success(request, "Image has been deleted!")
        return redirect('addPortfolioImg')
    except:
        messages.warning(request, "Image can't be deleted!")
        return redirect('addPortfolioImg')


    return redirect('addPortfolioImg')


# delete seller profile info for front-end seller list and details
@login_required(login_url='/register/user/')
def delete_profile_info(request, pk):

    try:
        seller_profile_info_model = Seller_profile.objects.filter(pk=pk)
        seller_profile_info_model.delete()
        messages.success(request, "Profile info has been deleted!!")
        return redirect('addProfileInfo')
    except:
        messages.success(request, "Profile info can't be deleted!!")
        return redirect('addProfileInfo')

    return redirect('addProfileInfo')


#add online services function
@login_required(login_url='/register/user/')
def add_online_services(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)


    # online service categories
    online_service_cats    = Service.objects.all()
    # online service categories
    online_service_subcats = Service_subcategory.objects.all()

    # dictionary for indicating state name by their values
    state = {
        'AL': 'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado',
        'CT':'Connecticut', 'DE':'Delaware', 'DC':'District Of Columbia', 'FL':'Florida', 'GA':'Georgia',
        'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky',
        'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota',
        'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey',
        'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon',
        'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas',
        'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'
    }

    if request.method == 'POST':

        service_title       = request.POST.get('online_service_title')
        service_description = request.POST.get('online_service_details')
        service_subcategory = request.POST.get('online_service_subcategory')
        service_img         = request.FILES['online_service_img']
        seller_country      = request.POST.get('seller_country')
        seller_state      = request.POST.get('seller_state_name')

        seller_state_name = state[seller_state]# full name of seller state


        if service_title != '':

            try:
                # grabing online service model to store data
                service_cat = Service_subcategory.objects.get(pk=service_subcategory).cat_id
                online_serviceList_model = OnlineServiceList(seller_id=request.user, service_title=service_title, service_description=service_description, service_category=service_cat, service_subcategory=service_subcategory, service_related_img1=service_img, seller_country=seller_country, sellerCountryFullName='United States', sellerStateFullName=seller_state_name,  seller_state=seller_state)
                online_serviceList_model.save()
                messages.success(request, "New Service has been added!")
                return redirect('servicesListByCat')

            except:
                messages.warning(request, "Can't be added! Please check your information!!")
                return redirect('addOnlineServices')

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    add_OnlineService_context = {
        'seller_profile_pic'           : user_profile,
        'service_cats'                 : online_service_cats,
        'service_subcats'              : online_service_subcats,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/add_online_service.html', add_OnlineService_context)


# edit online services list
@login_required(login_url='/register/user/')
def edit_online_service(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    # online service categories
    online_service_cats    = Service.objects.all()
    # online service categories
    online_service_subcats = Service_subcategory.objects.all()

    # grabing old data
    service_old_info = OnlineServiceList.objects.get(pk=pk)
    service_cat      = Service.objects.get(pk=service_old_info.service_category)
    service_subcat   = Service_subcategory.objects.get(pk=service_old_info.service_subcategory)

    if request.method == 'POST':
        online_service_title       = request.POST.get('online_service_title')
        online_service_details     = request.POST.get('online_service_details')
        online_service_subcategory = request.POST.get('online_service_subcategory')

        if online_service_title != '' and online_service_details != '' and online_service_subcategory != '':

            service_edited_subcat_name = Service_subcategory.objects.get(pk=online_service_subcategory).pk
            service_edited_cat_name    = Service_subcategory.objects.get(pk=online_service_subcategory).rel_with_cat.pk

            try:
                service_edited_img  = request.FILES.getlist('service_image')
                fs                  = FileSystemStorage()
                service_list_model  = OnlineServiceList.objects.get(pk=pk)
                fs.delete(service_list_model.service_related_img1.name)

                service_list_model.service_title        = online_service_title
                service_list_model.service_description  = online_service_details
                service_list_model.service_related_img1 = service_edited_img[0]
                service_list_model.service_category     = service_edited_cat_name
                service_list_model.service_subcategory  = service_edited_subcat_name
                service_list_model.save()
                return redirect('servicesListByCat')

            except:
                service_list_model  = OnlineServiceList.objects.get(pk=pk)
                service_list_model.service_title        = online_service_title
                service_list_model.service_description  = online_service_details
                service_list_model.service_category     = service_edited_cat_name
                service_list_model.service_subcategory  = service_edited_subcat_name
                service_list_model.save()
                return redirect('servicesListByCat')

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    #sending data to template
    online_service_edit_context = {
        'pk':pk,
        'seller_profile_pic'           : user_profile,
        'service_old_info'             : service_old_info,
        'service_cats'                 : online_service_cats,
        'service_subcats'              : online_service_subcats,
        'service_cat'                  : service_cat,
        'service_subcat'               : service_subcat,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/edit_online_service_list.html', online_service_edit_context)


# online service list by category
@login_required(login_url='/register/user/')
def online_service_list_by_category(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    # grabing service list
    online_service_list = OnlineServiceList.objects.filter(seller_id=request.user)
    service_subcat      = Service_subcategory.objects.all()

     # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    #sending data to template
    online_serviceList_context = {
        'seller_profile_pic'           : user_profile,
        'service_subcat'               : service_subcat,
        'online_service_list'          : online_service_list,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/online_service_list_by_category.html', online_serviceList_context)

# delete online services list
@login_required(login_url='/register/user/')
def del_online_service(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    try:
        online_service_model = OnlineServiceList.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(online_service_model.service_related_img1.name)
        online_service_model.delete()
        messages.success(request, "Your service has been deleted!")
        return redirect('servicesListByCat')
    except:
        messages.error(request, "Sorry! Can't be deleted!")
        return redirect('servicesListByCat')

    return redirect('servicesListByCat')


#add inperson services function
@login_required(login_url='/register/user/')
def add_inperson_services(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)


    # inperson service categories
    inperson_service_cats    = InPersonService_cat.objects.all()
    # inperson service sub-categories
    inperson_service_subcats = InPersonService_subcat.objects.all()


    # dictionary for indicating state name by their values
    state = {
        'AL': 'Alabama', 'AK':'Alaska', 'AZ':'Arizona', 'AR':'Arkansas', 'CA':'California', 'CO':'Colorado',
        'CT':'Connecticut', 'DE':'Delaware', 'DC':'District Of Columbia', 'FL':'Florida', 'GA':'Georgia',
        'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois', 'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucky',
        'LA':'Louisiana', 'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan', 'MN':'Minnesota',
        'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey',
        'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon',
        'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas',
        'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'
    }

    if request.method == 'POST':
        inperson_service_title         = request.POST.get('inperson_service_title')
        inperson_service_details       = request.POST.get('inperson_service_details')
        inperson_service_subcategory   = request.POST.get('inperson_service_subcategory')
        inperson_service_img           = request.FILES['inperson_service_img']
        seller_country                 = request.POST.get('seller_country')
        seller_state                   = request.POST.get('seller_state_name')

        if inperson_service_title != '':

            try:
                seller_state_name = state[seller_state] #grabing seller state name from state dict
                service_cat = InPersonService_subcat.objects.get(pk=inperson_service_subcategory).rel_with_cat.pk
                inperson_service_list_model =  InPersonServiceList(seller_id=request.user, service_title=inperson_service_title,service_description=inperson_service_details,service_related_img1=inperson_service_img,service_category=service_cat,service_subcategory=inperson_service_subcategory, seller_country=seller_country, sellerCountryFullName="United States", sellerStateFullName=seller_state_name, seller_state=seller_state)
                inperson_service_list_model.save()
                messages.success(request, "New Service has been added!")
                return redirect('InpersonservicesListByCat')
            except:
                messages.warning(request, "Sorry")
                return redirect('addInpersonServices')

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    #sending data to template
    addInperson_service_context = {
        'seller_profile_pic'           : user_profile,
        'service_cats'                 : inperson_service_cats,
        'service_subcats'              : inperson_service_subcats,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }


    return render(request, 'seller_admin/add_inperson_service.html', addInperson_service_context)

# inperson service list by category
@login_required(login_url='/register/user/')
def inperson_service_list_by_category(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)

    # grabing service list
    inperson_service_list = InPersonServiceList.objects.filter(seller_id=request.user)
    service_subcat      = InPersonService_subcat.objects.all()

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    inpersonService_list_context = {
        'seller_profile_pic'           : user_profile,
        'service_subcat'               : service_subcat,
        'inperson_service_list'        : inperson_service_list,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/inperson_service_list_by_category.html', inpersonService_list_context)


#edit inperson services function
@login_required(login_url='/register/user/')
def edit_inperson_services(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username)
    user_profile = ''
    for x in user:
        user_profile = user_profile + (x.user_profile_img)


    # inperson service categories
    inperson_service_cats    = InPersonService_cat.objects.all()
    # inperson service sub-categories
    inperson_service_subcats = InPersonService_subcat.objects.all()

    #grabing old data
    inperson_service_model = InPersonServiceList.objects.get(pk=pk)
    service_cat            = InPersonService_cat.objects.get(pk=inperson_service_model.service_category)
    service_subcat         = InPersonService_subcat.objects.get(pk=inperson_service_model.service_subcategory)

    if request.method == 'POST':
        inperson_service_title       = request.POST.get('inperson_service_title')
        inperson_service_details     = request.POST.get('inperson_service_details')
        inperson_service_subcategory = request.POST.get('inperson_service_subcategory')

        if inperson_service_title != '' and inperson_service_details != '' and inperson_service_subcategory != '':

            service_edited_subcat_name = InPersonService_subcat.objects.get(pk=inperson_service_subcategory).pk
            service_edited_cat_name    = InPersonService_subcat.objects.get(pk=inperson_service_subcategory).rel_with_cat.pk

            try:
                service_edited_img  = request.FILES.getlist('inperson_service_img')
                fs                  = FileSystemStorage()
                service_list_model  = InPersonServiceList.objects.get(pk=pk)
                fs.delete(service_list_model.service_related_img1.name)

                service_list_model.service_title        = inperson_service_title
                service_list_model.service_description  = inperson_service_details
                service_list_model.service_related_img1 = service_edited_img[0]
                service_list_model.service_category     = service_edited_cat_name
                service_list_model.service_subcategory  = service_edited_subcat_name
                service_list_model.save()
                return redirect('InpersonservicesListByCat')

            except:
                service_list_model  = InPersonServiceList.objects.get(pk=pk)

                service_list_model.service_title        = inperson_service_title
                service_list_model.service_description  = inperson_service_details
                service_list_model.service_category     = service_edited_cat_name
                service_list_model.service_subcategory  = service_edited_subcat_name
                service_list_model.save()
                return redirect('InpersonservicesListByCat')

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    editInperson_service_context = {
        'pk'                           : pk,
        'seller_profile_pic'           : user_profile,
        'service_cats'                 : inperson_service_cats,
        'service_subcats'              : inperson_service_subcats,
        'inperson_service_model'       : inperson_service_model,
        'service_cat_for_edit'         : service_cat,
        'service_subcat_for_edit'      : service_subcat,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
    }

    return render(request, 'seller_admin/edit_inperson_service.html', editInperson_service_context)


# delete online services list
@login_required(login_url='/register/user/')
def del_inperson_service(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    try:
        inperson_service_model = InPersonServiceList.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(inperson_service_model.service_related_img1.name)
        inperson_service_model.delete()
        messages.success(request, "Your service has been deleted!")
        return redirect('InpersonservicesListByCat')
    except:
        messages.error(request, "Sorry! Can't be deleted!")
        return redirect('InpersonservicesListByCat')

    return redirect('InpersonservicesListByCat')


# account setting page
@login_required(login_url='/register/user/')
def account_setting(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username).first()
    # user_profile = user.user_profile_img
    user_profile = ''
    if user:
        user_profile += user.user_profile_img


    # grabing the user
    user = get_object_or_404(CustomUser, email=request.user)
    user_email = user.email
    toArray    = user_email.split('@')
    toStr      = toArray[0]
    toStar     = '*'

    for x in range(len(toStr)):
        toStar = toStar+'*'
    hashed_mail = toStr[0]+toStar+toStr[len(toStr)-1]+'@'+toArray[1]

    # checking is the user added security question
    check_security_question = Answer.objects.filter(user=request.user).first()

    # changing password
    if request.method == 'POST':
        old_pass     = request.POST.get('old_password')
        new_pass     = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')

        if new_pass != confirm_pass:
            messages.warning(request, "Password didn't match!")
            return redirect('sellerAccountSetting')
        else:
            if len(new_pass) < 8:
                messages.warning(request, "Password must be in 8 characters!")
                return redirect('sellerAccountSetting')
            else:
                if check_security_question is not None:
                    security_question_ans  = request.POST.get('security_questions_answer')
                    given_sec_question_ans = Answer.objects.get(user=request.user).user_answer

                    if security_question_ans == given_sec_question_ans:
                        authenticate_user = authenticate(request, email=request.user, password=old_pass)
                        if authenticate_user is not None:
                            user = get_object_or_404(CustomUser, email=request.user)
                            user.set_password(new_pass)
                            user.save()
                            messages.success(request, "Password has been changed! Login with new password!")
                            return redirect('sellerAccountSetting')
                    else:
                        messages.warning(request, "Wrong answer!")
                        return redirect('sellerAccountSetting')
                else:
                    authenticate_user = authenticate(request, email=request.user, password=old_pass)
                    if authenticate_user is not None:
                        user = get_object_or_404(CustomUser, email=request.user)
                        user.set_password(new_pass)
                        user.save()
                        messages.success(request, "Password has been changed! Login with new password!")
                        return redirect('sellerAccountSetting')

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    account_context = {
        'hashed_mail'                  : hashed_mail,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
        'seller_profile_pic'           : user_profile,
        'check_security_question_exist_or_not'  : check_security_question,
    }

    return render(request, 'seller_admin/account_settng.html', account_context)


# security question setting views
@login_required(login_url='/register/user/')
def security_question_setting(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username).first()
    # user_profile = user.user_profile_img
    user_profile = ''
    if user:
        user_profile += user.user_profile_img


    # grabing the question model
    question_model = Security_question.objects.all()

    # saving security questions to database
    if request.method == 'POST':
        question = request.POST.get('security_question')
        answer   = request.POST.get('security_question_answer')

        if question != '' and answer != '':
            original_question = get_object_or_404(Security_question, pk=question)
            save_to_model = Answer(user=request.user, user_question=original_question, user_answer=answer)
            save_to_model.save()
            messages.success(request, 'Security answer has been added!')
            return redirect('sellerSecurityQuestionSetting')


    # checking is the user added security question
    check_security_question = Answer.objects.filter(user=request.user).first()
    security_question_answer = check_security_question.user_answer
    # used custom encrypt function from .tests.py
    encrypt_with_star = star_replace(security_question_answer)

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    security_question_context = {
        'question_list'                : question_model,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
        'seller_profile_pic'           : user_profile,
        'check_security_question'      : check_security_question,
        'encrypted_security_answer'    : encrypt_with_star,
    }

    return render(request, 'seller_admin/security_question.html', security_question_context)


# # change security question setting views
@login_required(login_url='/register/user/')
def update_security_question_setting(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username).first()
    # user_profile = user.user_profile_img
    user_profile = ''
    if user:
        user_profile += user.user_profile_img


    # grabing the question model
    question_model = Security_question.objects.all()

     # checking is the user added security question
    check_security_question = Answer.objects.filter(user=request.user).first()

    # changin security questions
    if request.method == 'POST':
        old_sec_question_ans         = request.POST.get('old_security_question_answer')
        new_security_question        = request.POST.get('new_security_question')
        new_security_question_answer = request.POST.get('new_security_question_answer')

        if old_sec_question_ans != '' and new_security_question != '' and new_security_question_answer != '':
            given_sec_question_ans = Answer.objects.filter(user=request.user).first().user_answer
            if given_sec_question_ans == old_sec_question_ans:
                # getting security quetion identity
                new_sec_question = Security_question.objects.filter(pk=new_security_question).first()
                # saving new security question and answer to database
                sec_ans_model = Answer(user=request.user, user_question=new_sec_question, user_answer=new_security_question_answer)
                sec_ans_model.save()
                messages.success(request, "New security question has been updated!")
                return redirect('updateSecurityQuestion')
            else:
                messages.success(request, "Wrong answer!")
                return redirect('updateSecurityQuestion')
                # saving new security question


    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    update_security_question_context = {
        'question_list'                : question_model,
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
        'seller_profile_pic'           : user_profile,
        'check_security_question'      : check_security_question,
    }

    return render(request, 'seller_admin/update_security_question.html', update_security_question_context)


# In person service related job list view
@login_required(login_url='/register/user/')
def inperson_service_related_jobs(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username).first()
    user_profile = user.user_profile_img

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # checking and grabing whether seller added any service to the service list
    inpersonService_model = InPersonServiceList.objects.filter(seller_id=request.user)

    # listing all the subcategories exist in In Person service list model by seller
    subcat_idList_in_inperson_serviceList_model = []
    for x in inpersonService_model:
        if x.service_subcategory not in subcat_idList_in_inperson_serviceList_model:
            subcat_idList_in_inperson_serviceList_model.append(x.service_subcategory)
    print(subcat_idList_in_inperson_serviceList_model)

    inperson_related_jobs_posted_by_customer = []
    for x in subcat_idList_in_inperson_serviceList_model:
        posted_JOBLIST = Posted_jobList.objects.filter(service_subcat_id=x, service_type_id='ips')
        for y in posted_JOBLIST:
            inperson_related_jobs_posted_by_customer.append(y)
    print(inperson_related_jobs_posted_by_customer)


    # sending data to template
    inperson_job_context = {
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
        'jobs_posted_byCustomer'       : inperson_related_jobs_posted_by_customer,
        'seller_profile_pic'           : user_profile,
    }

    return render(request, 'seller_admin/inperson_service_related_job_list.html', inperson_job_context)


# Online service related job list view
@login_required(login_url='/register/user/')
def online_service_related_jobs(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    #grabing seller profile pic
    user = Profile_pic.objects.filter(user_username=request.user.username).first()
    user_profile = user.user_profile_img

    # grabing seller profile model
    is_seller_profile_info_exist = Seller_profile.objects.filter(user=request.user).first()

    # sending data to template
    online_job_context = {
        'is_seller_profile_info_exist' : is_seller_profile_info_exist,
        'seller_profile_pic'           : user_profile,
    }

    return render(request, 'seller_admin/online_service_related_job_list.html', online_job_context)


#******for product section ******* Dont' delete or add any info here **********


# seller admin product list by category
@login_required(login_url='/register/user/')
def product_list_by_category(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    product_categories = Product_category.objects.all()
    #all products
    all_products = Product.objects.all()

    return render(request, 'seller_admin/product_list_by_category.html', {'product_categories':product_categories, 'all_products': all_products})


# products by their category name
@login_required(login_url='/register/user/')
def product_list(request, pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    all_products = Product.objects.filter(product_category=pk)

    return render(request, 'seller_admin/product_list.html', {'pk':pk, 'all_products':all_products})


# seller admin product list by category
@login_required(login_url='/register/user/')
def add_product(request):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    product_categories_model = Product_category.objects.all()
    product_subcatgories_model = Product_subcategory.objects.all()

    cats_of_subcats  = []
    for x in product_subcatgories_model:
        cats_of_subcats.append(x.cat_id)

    if request.method == 'POST':
        product_name                 = request.POST.get('product_name')
        product_search_tag           = request.POST.get('product_search_tag')
        product_short_description    = request.POST.get('product_short_description')
        product_search_title         = request.POST.get('product_search_title')
        product_description          = request.POST.get('product_description')
        product_img                  = request.FILES.getlist('product_img')
        product_subcategory          = request.POST.get('product_subcategory')
        product_old_price            = request.POST.get('product_old_price')
        product_new_price            = request.POST.get('product_new_price')
        product_in_stock             = request.POST.get('product_in_stock')
        product_available_colors     = request.POST.get('product_available_colors')
        product_condition            = request.POST.get('product_condition')

        len_product_img  = len(product_img)

        if len_product_img <3 :
            messages.warning(request, "Upload at least 3 images!!")
            return redirect('addProduct')

        # if product_name != '' and product_search_tag != '' and product_description != '' and product_short_description != '' and product_in_stock != '':
        if product_name != '':
            try:
                #making random id for each product
                randint1          = random.randint(100,999)
                randint2          = random.randint(1000,99000)
                rand_str          = random.choices(string.ascii_letters, k=3)
                rand_str1         = random.choices(string.ascii_letters, k=3)
                final_rand_str    = ''
                final_rand_str1   = ''
                for x in rand_str:
                    final_rand_str = final_rand_str+x
                for y in rand_str1:
                    final_rand_str1 = final_rand_str1+y
                product_random_id   = str(randint1)+final_rand_str+str(randint2)+final_rand_str1

                #grabing product category and subcategory name
                if len(Product_subcategory.objects.filter(pk=product_subcategory)) > 0:
                    product_subcat = Product_subcategory.objects.get(pk=product_subcategory)
                    product_cat    = product_subcat.cat_id

                    product_model = Product()
                    if len_product_img == 3:
                        product_model = Product(
                            seller_identity           = request.user,
                            product_category          = product_cat,
                            product_name              = product_name,
                            product_subcategory       = product_subcategory,
                            product_short_description = product_short_description,
                            product_details           = product_description,
                            product_price             = product_new_price,
                            product_old_price         = product_old_price,
                            product_InStocks          = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1              = product_img[0],
                            product_img2              = product_img[1],
                            product_img3              = product_img[2],
                            product_id                = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 4:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_cat,
                            product_name               = product_name,
                            product_subcategory        = product_subcategory,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 5:
                        product_model = Product(
                            seller_identity              = request.user,
                            product_category             = product_cat,
                            product_name                 = product_name,
                            product_subcategory          = product_subcategory,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price                = product_new_price,
                            product_old_price            = product_old_price,
                            product_InStocks             = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 6:
                        product_model = Product(
                            seller_identity              =request.user,
                            product_category             = product_cat,
                            product_name                 = product_name,
                            product_subcategory          = product_subcategory,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price             = product_new_price,
                            product_old_price         = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_img6                 = product_img[5],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 7:
                        product_model = Product(
                            seller_identity              =request.user,
                            product_category             = product_cat,
                            product_name                 = product_name,
                            product_subcategory          = product_subcategory,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price                = product_new_price,
                            product_old_price            = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_img6                 = product_img[5],
                            product_img7                 = product_img[6],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 8:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_cat,
                            product_name               = product_name,
                            product_subcategory        = product_subcategory,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_img5               = product_img[4],
                            product_img6               = product_img[5],
                            product_img7               = product_img[6],
                            product_img8               = product_img[7],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 9:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_cat,
                            product_name               = product_name,
                            product_subcategory        = product_subcategory,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_img5               = product_img[4],
                            product_img6               = product_img[5],
                            product_img7               = product_img[6],
                            product_img8               = product_img[7],
                            product_img9               = product_img[8],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 10:
                        product_model = Product(
                            seller_identity             =request.user,
                            product_category            = product_cat,
                            product_name                = product_name,
                            product_subcategory         = product_subcategory,
                            product_short_description   = product_short_description,
                            product_details             = product_description,
                            product_price               = product_new_price,
                            product_old_price           = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                = product_img[0],
                            product_img2                = product_img[1],
                            product_img3                = product_img[2],
                            product_img4                = product_img[3],
                            product_img5                = product_img[4],
                            product_img6                = product_img[5],
                            product_img7                = product_img[6],
                            product_img8                = product_img[7],
                            product_img9                = product_img[8],
                            product_img10               = product_img[9],
                            product_id                  = product_random_id
                        )
                        product_model.save()

                    messages.success(request, "Successfully added new product!")
                    return redirect('addProduct')
                else:
                    product_cat = Product_category.objects.get(pk=product_subcategory)
                    product_model = Product()
                    if len_product_img == 3:
                        product_model = Product(
                            seller_identity           = request.user,
                            product_category          = product_subcategory,
                            product_name              = product_name,
                            product_subcategory       = 0,
                            product_short_description = product_short_description,
                            product_details           = product_description,
                            product_price             = product_new_price,
                            product_old_price         = product_old_price,
                            product_InStocks          = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1              = product_img[0],
                            product_img2              = product_img[1],
                            product_img3              = product_img[2],
                            product_id                = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 4:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_subcategory,
                            product_name               = product_name,
                            product_subcategory        = 0,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 5:
                        product_model = Product(
                            seller_identity              = request.user,
                            product_category             = product_subcategory,
                            product_name                 = product_name,
                            product_subcategory          = 0,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price                = product_new_price,
                            product_old_price            = product_old_price,
                            product_InStocks             = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 6:
                        product_model = Product(
                            seller_identity              =request.user,
                            product_category             = product_subcategory,
                            product_name                 = product_name,
                            product_subcategory          = 0,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price             = product_new_price,
                            product_old_price         = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_img6                 = product_img[5],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 7:
                        product_model = Product(
                            seller_identity              =request.user,
                            product_category             = product_subcategory,
                            product_name                 = product_name,
                            product_subcategory          = 0,
                            product_short_description    = product_short_description,
                            product_details              = product_description,
                            product_price                = product_new_price,
                            product_old_price            = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                 = product_img[0],
                            product_img2                 = product_img[1],
                            product_img3                 = product_img[2],
                            product_img4                 = product_img[3],
                            product_img5                 = product_img[4],
                            product_img6                 = product_img[5],
                            product_img7                 = product_img[6],
                            product_id                   = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 8:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_subcategory,
                            product_name               = product_name,
                            product_subcategory        = 0,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_img5               = product_img[4],
                            product_img6               = product_img[5],
                            product_img7               = product_img[6],
                            product_img8               = product_img[7],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 9:
                        product_model = Product(
                            seller_identity            = request.user,
                            product_category           = product_subcategory,
                            product_name               = product_name,
                            product_subcategory        = 0,
                            product_short_description  = product_short_description,
                            product_details            = product_description,
                            product_price              = product_new_price,
                            product_old_price          = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1               = product_img[0],
                            product_img2               = product_img[1],
                            product_img3               = product_img[2],
                            product_img4               = product_img[3],
                            product_img5               = product_img[4],
                            product_img6               = product_img[5],
                            product_img7               = product_img[6],
                            product_img8               = product_img[7],
                            product_img9               = product_img[8],
                            product_id                 = product_random_id
                        )
                        product_model.save()
                    if len_product_img == 10:
                        product_model = Product(
                            seller_identity             =request.user,
                            product_category            = product_subcategory,
                            product_name                = product_name,
                            product_subcategory         = 0,
                            product_short_description   = product_short_description,
                            product_details             = product_description,
                            product_price               = product_new_price,
                            product_old_price           = product_old_price,
                            product_InStocks           = product_in_stock,
                            product_search_tags       = product_search_tag,
                            product_meta_title_for_search = product_search_title,
                            product_condition             = product_condition,
                            product_available_colors      = product_available_colors,
                            product_img1                = product_img[0],
                            product_img2                = product_img[1],
                            product_img3                = product_img[2],
                            product_img4                = product_img[3],
                            product_img5                = product_img[4],
                            product_img6                = product_img[5],
                            product_img7                = product_img[6],
                            product_img8                = product_img[7],
                            product_img9                = product_img[8],
                            product_img10               = product_img[9],
                            product_id                  = product_random_id
                        )
                        product_model.save()
                    messages.success(request, "Successfully added new product!")
                    return redirect('addProduct')

            except:
                messages.warning(request, "Can't be added new product!")
                return redirect('addProduct')

    return render(request, 'seller_admin/add_product.html', {'product_subcats':product_subcatgories_model, 'product_cats':product_categories_model, 'cats_of_subcats':cats_of_subcats})


# edit products
@login_required(login_url='/register/user/')
def edit_product(request,pk):
    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    product_categories_to_edit = Product_category.objects.all()
    product_subcatgories_model = Product_subcategory.objects.all()

    product_old_info           = Product.objects.get(pk=pk)

    product_cat_name           = Product_category.objects.get(pk=product_old_info.product_category).category_name

    cats_of_subcats  = []
    for x in product_subcatgories_model:
        cats_of_subcats.append(x.cat_id)

    if request.method == 'POST':
        product_name                 = request.POST.get('product_name')
        product_search_tag           = request.POST.get('product_search_tag')
        product_short_description    = request.POST.get('product_short_description')
        product_search_title         = request.POST.get('product_search_title')
        product_description          = request.POST.get('product_description')
        product_img                  = request.FILES.getlist('product_img')
        product_subcat_or_cat        = request.POST.get('product_subcategory_or_cat')
        product_old_price            = request.POST.get('product_old_price')
        product_new_price            = request.POST.get('product_new_price')
        product_in_stock             = request.POST.get('product_in_stock')
        product_available_colors     = request.POST.get('product_available_colors')
        product_condition            = request.POST.get('product_condition')

        if product_name != '':
            try:
                len_product_img  = len(product_img) # getting length of uploaded product image

                if len(Product_subcategory.objects.filter(pk=product_subcat_or_cat)) > 0:

                    if len_product_img != 0 and len_product_img < 3:
                        messages.warning(request, "Upload at least three images!")
                        return redirect('editProduct', pk=pk)

                    if len_product_img == 0:
                        product_model = Product.objects.get(pk=pk)
                        #getting product category id
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_description
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 3:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        #deleting previous images
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_description
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 4:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 5:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 6:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 7:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 8:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 9:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.product_img9              = product_img[8]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                    if len_product_img == 10:
                        product_model = Product.objects.get(pk=pk)
                        product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_new_cat_id
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = product_subcategory
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.product_img9              = product_img[8]
                        product_model.product_img10              = product_img[9]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_new_cat_id)
                else:
                    if len_product_img != 0 and len_product_img < 3:
                        messages.warning(request, "Upload at least three images!")
                        return redirect('editProduct', pk=pk)
                    if len_product_img == 0:
                        product_model = Product.objects.get(pk=pk)
                        #getting product category id
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_description
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 3:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        #deleting previous images
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_description
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 4:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id

                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 5:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 6:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 7:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 8:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 9:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.product_img9              = product_img[8]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
                    if len_product_img == 10:
                        product_model = Product.objects.get(pk=pk)
                        # product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id #getting product cat id
                        fs = FileSystemStorage()
                        if product_model.product_img1:
                            fs.delete(product_model.product_img1.name)
                        if product_model.product_img2:
                            fs.delete(product_model.product_img2.name)
                        if product_model.product_img3:
                            fs.delete(product_model.product_img3.name)
                        if product_model.product_img4:
                            fs.delete(product_model.product_img4.name)
                        if product_model.product_img5:
                            fs.delete(product_model.product_img5.name)
                        if product_model.product_img6:
                            fs.delete(product_model.product_img6.name)
                        if product_model.product_img7:
                            fs.delete(product_model.product_img7.name)
                        if product_model.product_img8:
                            fs.delete(product_model.product_img8.name)
                        if product_model.product_img9:
                            fs.delete(product_model.product_img9.name)
                        if product_model.product_img10:
                            fs.delete(product_model.product_img10.name)

                        product_model.product_category          = product_subcat_or_cat
                        product_model.product_name              = product_name
                        product_model.product_subcategory       = 0
                        product_model.product_short_description = product_short_descriptio
                        product_model.product_details           = product_description
                        product_model.product_price             = product_new_price
                        product_model.product_old_price         = product_old_price
                        product_model.product_InStocks          = product_in_stock
                        product_model.product_search_tags       = product_search_tag
                        product_model.product_meta_title_for_search = product_search_title
                        product_model.product_condition             = product_condition
                        product_model.product_available_colors      = product_available_colors
                        product_model.product_img1              = product_img[0]
                        product_model.product_img2              = product_img[1]
                        product_model.product_img3              = product_img[2]
                        product_model.product_img4              = product_img[3]
                        product_model.product_img5              = product_img[4]
                        product_model.product_img6              = product_img[5]
                        product_model.product_img7              = product_img[6]
                        product_model.product_img8              = product_img[7]
                        product_model.product_img9              = product_img[8]
                        product_model.product_img10              = product_img[9]
                        product_model.save()
                        messages.success(request, "Successfully updated product info!")
                        return redirect('productList', pk=product_subcat_or_cat)
            except:
                messages.warning(request, "Sorry to update!")
                return redirect('editProduct',pk=pk)
                # if len_product_img == 0:
                #         product_model = Product.objects.get(pk=pk)
                #         #getting product category id
                #         product_new_cat_id = Product_subcategory.objects.get(pk=product_subcat_or_cat).cat_id
                #
                #         product_model.product_category          = product_new_cat_id
                #         product_model.product_name              = product_name
                #         product_model.product_subcategory       = product_subcategory
                #         product_model.product_short_description = product_short_description
                #         product_model.product_details           = product_description
                #         product_model.product_price             = product_new_price
                #         product_model.product_old_price         = product_old_price
                #         product_model.product_InStocks          = product_in_stock
                #         product_model.product_search_tags       = product_search_tag
                #         product_model.product_meta_title_for_search = product_search_title
                #         product_model.product_condition             = product_condition
                #         product_model.product_available_colors      = product_available_colors
                #         product_model.save()
                #         messages.success(request, "Successfully updated product info!")
                #         return redirect('productList', pk=product_new_cat_id)


    return render(request, 'seller_admin/edit_product.html', {'pk':pk,'cats_of_subcats':cats_of_subcats,'product_subcats':product_subcatgories_model, 'product_old_info':product_old_info, 'product_cats_to_edit':product_categories_to_edit, 'product_cat_name':product_cat_name})

# delete products
@login_required(login_url='/register/user/')
def delete_product(request,pk):

    # verify whether user logged-in or not
    if not request.user.is_seller and not request.user.is_service_seller:
        return redirect('registerUser')

    product_cat = Product.objects.get(pk=pk)
    product_cat_id = product_cat.product_category

    try:
        fs = FileSystemStorage()
        product = Product.objects.get(pk=pk)
        product_cat = product.product_category

        if product.product_img1:
            fs.delete(product.product_img1.name)
        if product.product_img2:
            fs.delete(product.product_img2.name)
        if product.product_img3:
            fs.delete(product.product_img3.name)
        if product.product_img4:
            fs.delete(product.product_img4.name)
        if product.product_img5:
            fs.delete(product.product_img5.name)
        if product.product_img6:
            fs.delete(product.product_img6.name)
        if product.product_img7:
            fs.delete(product.product_img7.name)
        if product.product_img8:
            fs.delete(product.product_img8.name)
        if product.product_img9:
            fs.delete(product.product_img9.name)
        if product.product_img10:
            fs.delete(product.product_img10.name)
        product.delete()
        messages.success(request, "Product has been deleted!")
        return redirect('productList', pk=product_cat)
    except:
        messages.warning(request, "Product can't be deleted!")
        return redirect('productList', pk=product_cat)

    return redirect('productList', pk=product_cat_id)
