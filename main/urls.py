from django.urls import path
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import show_main, create_product, show_product
from main.views import edit_product
from main.views import delete_product
from main.views import get_products_json, get_product_json, add_product_entry_ajax, edit_product_ajax, delete_product_ajax, login_ajax, register_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete', delete_product, name='delete_product'),
    # AJAX URLs
    path('get-products/', get_products_json, name='get_products_json'),
    path('get-product/<uuid:id>/', get_product_json, name='get_product_json'),
    path('add-product-entry-ajax/', add_product_entry_ajax, name='add_product_entry_ajax'),
    path('edit-product/<uuid:id>/ajax/', edit_product_ajax, name='edit_product_ajax'),
    path('delete-product/<uuid:id>/ajax/', delete_product_ajax, name='delete_product_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
]