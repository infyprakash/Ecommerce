"""ecomstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog import views as catalog_views
from cart import views as cart_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',catalog_views.home,name='home'),
    path('category/<int:id>/', catalog_views.category_detail, name='category_detail'),
    path('product/<int:id>/', catalog_views.product_detail, name='product_detail'),
    path('add/to/cart/<int:id>/',cart_views.add_to_cart,name='add_to_cart'),
    path('show/cart/',cart_views.show_cart,name='show_cart'),
    path('create/user/',catalog_views.create_user,name="createuser"),
    path('login/',catalog_views.login_page,name="logingin"),
    path('logout/',catalog_views.logout_page,name="logingout"),
    path('checkout/',cart_views.checkout,name="checkout"),
    path('get/address/',catalog_views.show_address,name='show_address'),
    # path('set/session/',cart_views.set_session,name='set_session'),
    # path('get/session/',cart_views.get_session,name='get_session'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
