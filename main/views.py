import datetime
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from main.forms import ProductForm, RegisterForm
from main.models import Product
# Create your views here.

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    trending_product_list = Product.objects.filter(likes__gt=100)

    context = {
        'npm' : '2406402542',
        'name': request.user.username,
        'class': 'PBP F',
            'product_list': product_list,
            'trending_product_list' : trending_product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json_by_id(request, product_id):
   try:
       product_item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [product_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   
@csrf_exempt
def register(request):
    # Check if this is an API request (JSON) or web request (form)
    if request.content_type == 'application/json' or 'application/json' in request.META.get('CONTENT_TYPE', ''):
        # Handle JSON API request for Flutter
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password1 = data.get('password1')
                password2 = data.get('password2')

                # Check if the passwords match
                if password1 != password2:
                    return JsonResponse({
                        "status": False,
                        "message": "Passwords do not match."
                    }, status=400)

                # Check if the username is already taken
                if User.objects.filter(username=username).exists():
                    return JsonResponse({
                        "status": False,
                        "message": "Username already exists."
                    }, status=400)

                # Create the new user
                user = User.objects.create_user(username=username, password=password1)
                user.save()

                return JsonResponse({
                    "username": user.username,
                    "status": 'success',
                    "message": "User created successfully!"
                }, status=200)

            except json.JSONDecodeError:
                return JsonResponse({
                    "status": False,
                    "message": "Invalid JSON data."
                }, status=400)
            except KeyError as e:
                return JsonResponse({
                    "status": False,
                    "message": f"Missing field: {str(e)}"
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    "status": False,
                    "message": f"Registration failed: {str(e)}"
                }, status=500)

        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid request method."
            }, status=400)
    else:
        # Handle web form request
        form = RegisterForm()
        registration_success = False

        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                registration_success = True
                form = RegisterForm()  # Reset form
        context = {'form': form, 'registration_success': registration_success}
        return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            # Try to parse as JSON (for Flutter requests)
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except (json.JSONDecodeError, KeyError):
            # Fallback to form data (for web requests)
            username = request.POST.get('username')
            password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({
                "status": False,
                "message": "Username and password are required."
            }, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": "Login successful",
                    "user": {
                        "username": user.username,
                        "id": user.id
                    }
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Login failed, account is disabled."
                }, status=401)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, please check your username or password."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout_user(request):
    logout(request)
    # Check if this is a JSON API request
    if request.content_type == 'application/json' or request.method == 'POST':
        return JsonResponse({
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    else:
        # Web request - redirect
        response = HttpResponseRedirect(reverse('main:login'))
        response.delete_cookie('last_login')
        return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# AJAX Views
@csrf_exempt
def get_products_json(request):
    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": False,
            "message": "Authentication required."
        }, status=401)

    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    data = []
    for product in product_list:
        data.append({
            'product_id': str(product.product_id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'views': product.views,
            'likes': product.likes,
            'user': product.user.username if product.user else None,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def add_product_entry_ajax(request):
    if request.method == 'POST':
        # Check authentication
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": False,
                "message": "Authentication required."
            }, status=401)

        try:
            # Try to parse JSON first (for Flutter API requests)
            data = json.loads(request.body)
            name = strip_tags(data.get("name", ""))
            price = data.get("price", 0)
            description = strip_tags(data.get("description", ""))
            category = data.get("category", "")
            thumbnail = data.get("thumbnail", "")
            is_featured = data.get("is_featured", False)
        except json.JSONDecodeError:
            # Fallback to form data (for web requests)
            name = strip_tags(request.POST.get("name", ""))
            price = request.POST.get("price", 0)
            description = strip_tags(request.POST.get("description", ""))
            category = request.POST.get("category", "")
            thumbnail = request.POST.get("thumbnail", "")
            is_featured = request.POST.get("is_featured") == 'on'

        # Create product
        new_product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=request.user
        )
        new_product.save()

        return JsonResponse({
            "status": True,
            "message": "Product created successfully!",
            "product_id": str(new_product.product_id)
        }, status=201)

    return JsonResponse({'status': False, 'message': 'Invalid request'}, status=400)

@login_required(login_url='/login')
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Product updated successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required(login_url='/login')
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    product.delete()
    return JsonResponse({'success': True, 'message': 'Product deleted successfully!'})

def login_ajax(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = JsonResponse({'success': True, 'message': 'Login successful', 'username': user.username})
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def register_ajax(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Registration successful!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def get_product_json(request, id):
    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({
            "status": False,
            "message": "Authentication required."
        }, status=401)

    product = get_object_or_404(Product, pk=id)
    data = {
        'product_id': str(product.product_id),
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'thumbnail': product.thumbnail,
        'category': product.category,
        'is_featured': product.is_featured,
        'views': product.views,
        'likes': product.likes,
        'user': product.user.username if product.user else None,
    }
    return JsonResponse(data)

@csrf_exempt
def proxy_image(request):
    """Proxy external images to avoid CORS issues"""
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)

    try:
        # URL decode the image URL
        from urllib.parse import unquote
        decoded_url = unquote(image_url)
        print(f"Proxying image: {decoded_url}")

        # Fetch image from external source
        import requests
        response = requests.get(decoded_url, timeout=10, stream=True)
        response.raise_for_status()

        # Return the image with proper content type and CORS headers
        django_response = HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )

        # Add CORS headers
        django_response['Access-Control-Allow-Origin'] = '*'
        django_response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        django_response['Access-Control-Allow-Headers'] = '*'

        return django_response

    except requests.RequestException as e:
        print(f"Error fetching image {decoded_url}: {e}")
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    except Exception as e:
        print(f"Unexpected error proxying image: {e}")
        return HttpResponse(f'Unexpected error: {str(e)}', status=500)