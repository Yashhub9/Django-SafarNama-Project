from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from safarnama_app.models import product,cart, orders,Booking
from .models import Review
from django.db.models import Q
from .models import product
from django.core.mail import send_mail
from django.conf import settings
from safarnama_app.models import PasswordResetOTP
from django.contrib import messages
import string
import random
from .models import Payment
from .models import Contact


from .models import product, Booking
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    p=product.objects.filter(is_active=True)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def home(request):
    p=product.objects.filter(is_active=True)
    context={}
    context['products']=p
    return render(request,'home.html',context)

def aboutus(request):
    return render(request,"projaboutus.html")

def contactus(request):
    return render(request,'contactus.html')

def register(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        ucpass=request.POST["ucpass"]
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'register.html')
        elif upass!=ucpass:
            context['errmsg']="password and confirm password not match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['sucess']="user created sucessfully..."
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="user name already exist"
    else:
        return render(request,'register.html')
    
def user_login(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Field cannot be empty"
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
    return render(request,'login.html')

def productdetails(request,pid):
    p=product.objects.filter(id=pid)
    print(p)
    context={}
    context['products']=p
    return render(request,'productdetails.html',context)


def user_logout(request):
    logout(request)
    return redirect('/')


def sort(request,sv):
    if sv=='0':
        col='price'  #sort by price asc order
    else:
        col="-price"                #sort by price desc order
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    #select * from products where price<=5000 and price>50000 and is_status=True
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)


def search_products(request):
    query = request.GET.get('q')  # Get the query parameter
    if query:
        # Use the correct field name from your model (e.g., name)
        products = product.objects.filter(name__icontains=query)
        if not products.exists():  # If no product matched
            messages.warning(request, "No product found!")
            return redirect('/index')
    else:
        products = product.objects.none()  # Return an empty queryset if no query
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'search_results.html', context)



def booking_view(request, product_id):
    product = get_object_or_404(product, id=product_id)
    passenger_count = 0
    total_price = 0
    passenger_details = []

    if request.method == 'POST':
        passenger_count = int(request.POST.get('no_of_passengers', 0))
        total_price = passenger_count * product.price

        if 'submit_booking' in request.POST:
            for i in range(1, passenger_count + 1):
                passenger_details.append({
                    "name": request.POST.get(f'passenger_{i}_name'),
                    "age": request.POST.get(f'passenger_{i}_age'),
                    "gender": request.POST.get(f'passenger_{i}_gender'),
                    "mobile": request.POST.get(f'passenger_{i}_mobile'),
                })

            booking = Booking.objects.create(
                product=product,
                passenger_count=passenger_count,
                total_price=total_price,
            )
            for passenger in passenger_details:
                Passenger.objects.create(
                    booking=booking,
                    name=passenger["name"],
                    age=passenger["age"],
                    gender=passenger["gender"],
                    mobile=passenger["mobile"],
                )

            return redirect('payment_gateway', booking_id=booking.id)

    passenger_range = range(1, passenger_count + 1)
    return render(request, 'booking.html', {
        'product': product,
        'passenger_count': passenger_count,
        'passenger_range': passenger_range,
        'passenger_details': passenger_details,
    })
    
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No account found with that email.")
            return render(request, "forgot_password.html")

        for user in users:
            # Generate an OTP
            otp = ''.join(random.choices(string.digits, k=6))
            PasswordResetOTP.objects.update_or_create(user=user, defaults={"otp": otp}) 

    # Send the OTP via email
            send_mail(
                "Password Reset OTP",
                f"Hello {user.username},\n\nYour OTP for resetting the password is: {otp}.\n\nUse this to reset your password.",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        messages.success(request, "An OTP has been sent to your email.")
        return redirect('enter_otp')  # Redirect to the OTP entry page
    return render(request,"forgot_password.html") 

def enter_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")

        try:
            reset_entry = PasswordResetOTP.objects.get(otp=otp)
            # Save the user ID in session to use it in the reset password view
            request.session['reset_user_id'] = reset_entry.user.id
            return redirect('reset_password')
        except PasswordResetOTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
            return render(request, "enter_otp.html")

    return render(request, "enter_otp.html")


def reset_password(request):
        user_id = request.session.get('reset_user_id')

        if not user_id:
            messages.error(request, "Unauthorized access. Please restart the process.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(id=user_id)

            if request.method == 'POST':
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                else:
                    user.set_password(password)
                    user.save()
                    del request.session['reset_user_id']  # Clear session after password reset
                    messages.success(request, "Your password has been reset successfully. You can now log in.")
                    return redirect('/login')
        except User.DoesNotExist:
            messages.error(request, "Invalid user.")
            return redirect('forgot_password')

        return render(request, 'reset_password.html')

@login_required
def booking_page(request, product_id):
    import razorpay

    product_obj = get_object_or_404(product, id=product_id)
    if request.method == 'POST':
        # Razorpay integration
        razorpay_client = razorpay.Client(auth=("rzp_test_xdN7uS1MwW4CAK", "Rx2nr5hml4BdAnOExD5S4JTJ"))
        total_price = float(request.POST['total_price']) * 100  # Convert to paisa (₹1 = 100 paisa)
        
        payment = razorpay_client.order.create({
            "amount": total_price,
            "currency": "INR",
            "payment_capture": "1"
        })
        
        # Save booking details
        booking = Booking.objects.create(
            product=product_obj,
            passenger_count=request.POST['passenger_count'],
            total_price=total_price / 100,
        )

        context = {
            'product': product_obj,
            'payment': payment,
            'booking': booking,
            'razorpay_key': settings.RAZORPAY_KEY_ID
        }
        return render(request, 'booking_payment.html', context)

    return render(request, 'booking_page.html', {'product': product_obj})



def make_payment(request):
    import razorpay

    if request.method == 'POST':
        # Get customer names as a comma-separated string
        customer_names = request.POST.get('customers')  
        customer_count = len(customer_names.split(','))  # Count the number of customers

        # Amount calculation
        amount_per_customer = 500.00  # Example price per customer
        total_amount = amount_per_customer * customer_count  # Calculate the total amount

        # Create Razorpay payment
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_in_paise = int(total_amount * 100)  # Convert amount to paise
        payment = client.order.create({'amount': amount_in_paise, 'currency': 'INR', 'payment_capture': '1'})

        # Save payment details in the database
        payment_obj = Payment(
            user=request.user,
            customers=customer_names,
            customer_count=customer_count,
            amount_per_customer=amount_per_customer,
            total_amount=total_amount,
            payment_id=payment['id']
        )
        payment_obj.save()

        context = {
            'payment': payment,
            'customer_names': customer_names,
            'total_amount': total_amount,
        }
        return render(request, 'payment.html', context)

    return render(request, 'make_payment.html')



def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save the details to the database
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Redirect to a contact page or wherever you want
    return render(request, 'contactus.html')
