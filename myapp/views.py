from django.shortcuts import render,get_object_or_404,reverse,redirect
from .models import Product,OrderDetail
from django.http import HttpResponseNotFound,JsonResponse
from django.conf import settings
import stripe,json
from .forms import ProductForm,UserRegistrationForm
 
from django.views.decorators.csrf import csrf_exempt


def index(request):
    products=Product.objects.all()
    return render(request,'myapp/index.html',{'products':products})

def detail(request,id):
    product=Product.objects.get(id=id)
    stripe_publishable_key=settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'myapp/detail.html',{'product':product,'stripe_publishable_key': stripe_publishable_key})


@csrf_exempt
def create_checkout_session(request,id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types = ['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price * 100)
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
        
    )
 
    order=OrderDetail()                             
    order.customer_email=request_data['email']
    order.product=product
    order.stripe_payment_intent=checkout_session['id']
    order.amount=int(product.price)
    order.save()
    return JsonResponse({'sessionId':checkout_session.id})


 

def payment_success_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail,stripe_payment_intent= session.id)
    order.stripe_payment_intent=session['payment_intent']
    order.has_paid=True
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount = product.total_sales_amount + int(product.price)
    product.total_sales = product.total_sales + 1
    product.save()
    order.save()

    return render(request,'myapp/payment_success.html',{'order':order})
    
def payment_failed_view(request):
    return render(request,'myapp/failed.html')  

def  create_product(request):
    product_form=ProductForm()
    if request.method=='POST':
        product_form=ProductForm(request.POST,request.FILES)
        if product_form.is_valid:
            new_product=product_form.save(commit=False)
            new_product.seller=request.user
            new_product.save()
            return redirect('index')
    return render(request,'myapp/create_product.html',{'product_form':product_form})

def Product_edit(request,id):
    product=Product.objects.get(id=id)
    if product.seller!=request.user:
        return redirect('invalid')
    product_form=ProductForm(request.POST or None,request.FILES or None,instance=product)
    if request.method=='POST':
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    
    return render(request,'myapp/product_edit.html',{'product_form':product_form,'product':product})

def Product_delete(request,id):
    product=Product.objects.get(id=id)
    if product.seller!=request.user:
        return redirect('invalid')
    if request.method=='POST':
        product.delete()
        return redirect('index')
    return render(request,'myapp/delete.html',{'product':product})

def register(request):
    
    if request.method=='POST':

        user_form=UserRegistrationForm(request.POST)
        new_user=user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form=UserRegistrationForm()

    return render(request,'myapp/register.html',{'user_form':user_form})

def invalid(request):
    return render(request,'myapp/invalid.html')

def my_purchases(request):
    orders=OrderDetail.objects.filter(customer_email=request.user.email)
    return render(request,'myapp/purchases.html',{'orders':orders})

def dashboard(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'myapp/dashboard.html',{'products':products})

def prelogout(request):
    return render(request,'myapp/prelogout.html')
