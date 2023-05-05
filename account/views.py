from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from order.models import Orders, Work,Feedback
from .models import Car

from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
import datetime

# Create your views here.

def logoutView(request):
    logout(request)
    return redirect('login')


def check_car_data(car_data):
    def check_car_number(number):
        number = number.replace(' ', '')
        region = ['10','20','30','40','50','60','70','75','80','01','90']
        
        if len(Car.objects.filter(car_number=number)) >0:
            return False
        elif number[:2] in region:
            if len(number[2:]) == 6:
                l = 0
                for i in number[2:]:
                    if i in '0123456789':
                        l+=1
                if l == 3:
                    return True
        else:
            return False
    
    data = {
        'car_number' : car_data['car_number'],
        'car_type' : car_data['car_type'],
        'status' : 0
    }
    username = car_data['username']
    if len(username) == 9:
        username = '+998' + username

    if len(data['car_type'])< 3:
        return (False, 4, username, car_data['first_name'], car_data['last_name'], car_data['password'], car_data['car_type'], car_data['car_number'])
    elif not(check_car_number(data['car_number'])):
        return (False, 5, username, car_data['first_name'], car_data['last_name'], car_data['password'], car_data['car_type'], car_data['car_number'])
    
    return (True, 5, username, car_data['first_name'], car_data['last_name'], car_data['password'], car_data['car_type'], car_data['car_number'])
    
        

def loginView(request):
    if request.method == "GET":
        return render(request, "auth/login.html")
    elif request.method == "POST":
        username = request.POST['username']
        if username[:4] != '+998':
            username = '+998'+username
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            if len(Car.objects.filter(user = request.user)) > 0:
                return redirect('driver_home')
            else:
                return redirect('user_home')
        else:   
            data = {
                    'status' : 0,
                    'username': username,
                    'password': password
                }
            return render(request, 'auth/login.html', context={'data': data})


def check_signup(user_data, driver=False):
    data = ()    
    if 'username' in user_data:
        if not ( len(user_data['username'])==9 or len(user_data['username'])==13 and user_data['username'][0]=='+' ):
            data= (False, 0, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])
    else:
        data= (False, 0, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])
    
    if len(User.objects.filter(username=user_data['username']))>0 or len(User.objects.filter(username='+998'+user_data['username']))>0:
        data= (False, -1, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])

    if not('first_name' in user_data and len(user_data['first_name'])>= 3):
        data= (False, 1, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])
    
    if not('last_name' in user_data and len(user_data['last_name'])>= 3):
        data= (False, 2, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])

    if not('password' in user_data and len(user_data['password'])>= 8):
        data= (False, 3, user_data['username'], user_data['first_name'], user_data['last_name'], user_data['password'])
    
    if len(data) > 0:
        if driver:
            data+=(user_data['car_type'], user_data['car_number'])
        return data
    username = user_data['username']
    if len(username) == 9:
        username = '+998' + username

    first_name = user_data['first_name']
    last_name = user_data['last_name']
    password = user_data['password']
    if not(driver):
        return (True, 0, username, first_name, last_name, password)
    else:
        return check_car_data(user_data)




def signupView(request):
    if request.method == "GET":
        return render(request, 'auth/signup.html')
    elif request.method == "POST":
        answer = check_signup(request.POST)
        if answer[0]:
            user = User.objects.create_user(username = answer[2], first_name = answer[3], last_name = answer[4], password = answer[5])
            user.save()
            login(request, user)
            return redirect('user_home')
        else:
            data = {
                'status': answer[0],
                'error_status': answer[1],
                'username': answer[2],
                'first_name': answer[3],
                'last_name': answer[4],
                'password': answer[5],
            }
            return render(request = request, template_name ='auth/signup.html', context={'data': data})

    return render(request, 'not_found_page.html')


def driver_signupView(request):
    if request.method == "GET":
        return render(request, 'auth/signup-driver.html')
    elif request.method == "POST":
        answer = check_signup(request.POST, True)
        if answer[0]:
            user = User.objects.create_user(username = answer[2], first_name = answer[3], last_name = answer[4], password = answer[5])
            
            car = Car.objects.create(car_number=answer[7], car_type=answer[6], user = user)
            user.save()
            car.save()
            login(request, user)
            return redirect('driver_home')
        else:
            data = {
                'status': answer[0],
                'error_status': answer[1],
                'username': answer[2],
                'first_name': answer[3],
                'last_name': answer[4],
                'car_type': answer[6],
                'car_number': answer[7],
                'password': answer[5],
                
            }
            return render(request = request, template_name ='auth/signup-driver.html', context={'data': data})

    return render(request, 'not_found_page.html')


def homeView(request):
    return render(request, 'home.html')


def chooseView(request):
    if request.method == "GET":
        return render(request, "choose.html")
    elif request.method == "POST":
        data = check_car_data(request.POST)
        if data['status'] == 0:
            # Mashina ma`lumotlarini databasega qo`shish kere sheyda
            Car.objects.create(car_type=data['car_type'], car_number=data['car_number'], user = request.user).save()
            return redirect('driver_home')
        return render(request, "choose.html", context={'data' : data })

def check_order(order_data):
    
    order = {
    'order_type' : order_data['type'],
    'weight' : order_data['weight'],
    'start_location' : order_data['start_location'],
    'finished_location' : order_data['finished_location'],
    # 'price' : order_data['price'],
    # 'period' : order_data['period'],
    'status': 0,
    'error_status': 0,
    }

    if len(order['order_type']) < 3:
        order['error_status'] = 1
    elif len(order['weight']) < 1:
        order['error_status'] = 2
    elif len(order['start_location']) < 5:
        order['error_status'] = 3
    elif len(order['finished_location']) < 5:
        order['error_status'] = 4
    # elif len(order['price']) < 1:
    #     order['error_status'] = 5
    # elif len(order['period']) < 1:
    #     order['error_status'] = 6
    else:
        order['error_status'] = 0

        
    return order

def userhomeView(request,pk=(-1), id=(-1)):
    if pk != -1 and id != -1:
        a = Orders.objects.filter(id = pk)[0]
        if id == 1:
            a.status = 2
        else: 
            a.status = 0
            Work.objects.filter(order = pk).delete()
        a.save()
    if request.method == 'GET':
        work = Work.objects.filter(order_id__user = request.user)
        if request.GET.get('order_feedback'):
            order_id = request.GET.get('order_id')
            feedback= request.GET.get('order_feedback')
            driver_id = request.GET.get('driver_id')
            driver = User.objects.filter(id = driver_id)[0]
            order = Orders.objects.filter(id = order_id)
            if len(order)> 0:
                order = order[0]
                order.delivery_fee = ''
                order.period = ''
                order.status = 0
                order.save()
                x = Feedback.objects.create(user = driver, order = order, feedback = feedback)
                x.save()
        
      # orders = Orders.objects.filter( ~Q(status=0)  &  Q( work__driver_id = request.user) | Q(status=0)   ).order_by('-date')
        orders = Orders.objects.filter(user=request.user).order_by('-date')
        
        return render(request, 'user_home.html', context={'work':work, 'orders': orders})
    elif request.method == 'POST':
        
        order = check_order(request.POST)
        if order['error_status'] == 0:
            # Agar xatosiz kelgan bo`lsa shu yerda database ga qo`shishi kere bo`ladi
            
            new_order = Orders.objects.create(
                order_type=order['order_type'],
                order_weight = order['weight'],
                start_location = order['start_location'],
                finished_location = order['finished_location'],
                # delivery_fee = order['price'],
                # period=order['period'],
                status=0,
                user=request.user,
                date=datetime.datetime.now(),
            )
            new_order.save()     
            
        return render(request, 'user_home.html', context={'data': order, 'orders': Orders.objects.filter(user=request.user)})

def detailuserhomeView(request, pk, id):

    order = check_order(request.POST)
    return render(request, 'user_home.html', context={'data': order, 'orders': Orders.objects.filter(user=request.user)})
    
    # return render(request, 'user_home.html', context={'orders': Orders.objects.filter(user=request.user)})

        

def driverhomeView(request):
    
    orders = Orders.objects.filter( ~Q(status=0)  &  Q( work__driver_id = request.user) | Q(status=0)   ).order_by('-date')
    return render(request, 'driver_home.html', context = {'data': orders, 'status':False})

def eachdriverhomeView(request, pk):
    if request.method == 'POST':
        if 'url' in request.POST:
            a = Orders.objects.filter(pk = request.POST['url'])[0]
            if a.status == 0:
                a.delivery_fee = request.POST['price']
                a.period = request.POST['period']
                Work(order=a, driver=request.user).save()
                a.status = 1
                a.save()
        elif 'url1' in request.POST:
            a = Orders.objects.filter(pk = request.POST['url1'])[0]
            if a.status == 2:
                my_work = Work.objects.filter(order = a)[0]

                my_work.start_time = datetime.datetime.now()
                
                my_work.save()

                a.status = 3
                a.save()

        elif 'finish' in request.POST:
            a = Orders.objects.filter(pk = request.POST['finish'])[0]
            if a.status == 3:
                my_work = Work.objects.filter(order = a)[0]
                
                my_work.finish_time = datetime.datetime.now()
                my_work.save()
                my_work1 = Work.objects.filter(order = a)[0]

                future_time = my_work1.finish_time
                current_time = my_work1.start_time

                period = my_work1.order.period 
                time_diff = future_time - current_time
                minutes_diff = int(time_diff.total_seconds() / 60)

                diff = minutes_diff
                if diff<0:
                    my_work1.fine =  abs(diff)*5000
                    c = Orders.objects.filter(id = a.id)[0]
                    if my_work1.fine < 0:
                        c.delivery_fee = 0
                    else:
                        c.delivery_fee -= my_work1.fine
                    c.save()

                my_work1.diff_times  = minutes_diff
                my_work1.save()
                a.status = 4
                a.save()
    
    
    orders = Orders.objects.filter( ~Q(status=0)  &  Q( work__driver_id = request.user) | Q(status=0)   ).order_by('-date')
    order = Orders.objects.filter(id = pk)[0]
    # driver = request.user, order__status = 4, 
    works = Work.objects.filter(order__id = pk)
    if len(works)>0:
        works = works[0]
    feedback_text = Feedback.objects.filter(user = request.user.id, order = order)
    if len(feedback_text) > 0:
        feed = feedback_text[0].feedback
    else:
        feed = ''
    return render(request, 'driver_home.html', context = {'data': orders, 'feedback': feed, 'order': order, 'work':works, 'status':True, 'order_id':order.id})