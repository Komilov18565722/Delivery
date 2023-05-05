from django.urls import path
from . views import loginView, logoutView, signupView, homeView, chooseView, driver_signupView, userhomeView, detailuserhomeView, driverhomeView, eachdriverhomeView

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('customer/signup/', signupView, name = 'user_signup'),
    path('driver/signup/', driver_signupView, name = 'driver_signup'),
    path('home/', homeView, name= 'home'),
    path('choose/', chooseView, name='choose'),
    path('user-home/', userhomeView, name = 'user_home'),
    path('user-home/<int:pk>/<int:id>', userhomeView, name = 'user_home1'),
    path('driver-home/', driverhomeView, name = 'driver_home'),
    path('driver-home/<int:pk>', eachdriverhomeView, name = 'driver_home_detail'),
    
    # path('agreement/<int:pk>', agreementView, name = 'agreement'),
    path('', loginView, name = 'login'),

    

]