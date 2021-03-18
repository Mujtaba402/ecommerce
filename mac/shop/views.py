from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json


# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    print(query)
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    if len(allProds) == 0 or len(query) < 4:
        messages.error(request, "Please make sure to enter relevent query")
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        if name == "" or email == "" or phone == "" or desc == "":
            messages.error(request, "Please fill out the form correctly")
        else:
            contact.save()
            messages.success(request, "You have successfully submitted your message")
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        print(email)

        try:
            order = Orders.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})

                    response = json.dumps({"status": "success", "updates": updates, "itemJson": order[0].items_json},
                                          default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        addressline = request.POST.get('addressline', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        if name == "" or email == "" or address == "" or city == "" or state == "" or zip_code == "" or phone == "":
            messages.error(request, "Please fill out the form correctly")
        else:

            order = Orders(items_json=items_json, name=name, email=email, address=address, addressline=addressline,
                           city=city, state=state,
                           zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()

            messages.success(request, "Thanks for ordering with us.Your order id is :")
            id = order.order_id
            msg = "Use it to track your order our order tracker"
            return render(request, 'shop/checkout.html', {'msg': msg, 'id': id})
    return render(request, 'shop/checkout.html')


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    # comments = Comments.objects.filter(prod=product)

    return render(request, 'shop/productview.html', {'product': product[0]})


def handleSignUp(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 8 or username == "":
            messages.error(request, "User can enter username under 8 character and user can not be empty")
            return redirect('ShopHome')
        if fname == "" or lname == "":
            messages.error(request, "First name and Last name cannot be empty")
            return redirect('ShopHome')
        if pass1 == "" or pass2 == "":
            messages.error(request, "Password cannot be empty")
            return redirect('ShopHome')
        if pass1 != pass2:
            messages.error(request, "Password should not be matched")
            return redirect('ShopHome')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, " Your account has been created successfully")
        return redirect('ShopHome')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully loggedin")
            return redirect('ShopHome')
        else:
            messages.error(request, "Invalid Credentials Please try again")
            return redirect('ShopHome')

    return HttpResponse('404-not found')


def handleLogout(request):
    logout(request)
    messages.success(request, "You have successfully logout")
    return redirect('ShopHome')
