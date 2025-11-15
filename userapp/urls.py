# urls.py
from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .import views
from .views import *

from userapp.views import ChatbotAPIView, ProductByCategory, ProductDetailView,RegisterViewSet, login_view,CycleInputViewSet,get_cycle_inputs_by_user,chatbot_view,UserViewBook,UserViewProduct,UserViewCategory   

schema_view = get_schema_view(
   openapi.Info(
      title="Hertime App API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Define the router and register the viewset
router = DefaultRouter()
router.register(r'register',RegisterViewSet,basename='register')
router.register(r'cycle-inputs', CycleInputViewSet, basename='cycle-input')




urlpatterns = [
   path('', include(router.urls)),  # Now /api/register/ will work
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
   path("chatbot/", ChatbotAPIView.as_view(), name="chatbot_api"),
   path("login/", login_view, name="login"),
   path("cycle-inputs/user/<int:user_id>/", get_cycle_inputs_by_user, name="cycle_inputs_by_user"),
   path('chatbot_view/', chatbot_view, name='chatbot_view'),
   path("user_view_book/", UserViewBook.as_view(), name="user_view_book"),
   path('user_view_category/',UserViewCategory.as_view(),name='user_view_category'),
   path("user_view_product/", UserViewProduct.as_view(), name="user_view_product"),
   path("products/category/<int:category_id>/", ProductByCategory.as_view(), name="products_by_category"),
   path("product/<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
   path('product-booking/', ProductBookingView.as_view(),name='product_booking'),
   path('product-booking/payment/', BookingPaymentView.as_view(),name='booking_payment'),
   path('cart/add/<int:product_id>/', CartCreateView.as_view(),name='add_to_cart'),
   path('cart/update/', UpdateCartQuantity.as_view(), name='update_cart_quantity'),
   path('cart/remove/<int:cart_id>/', RemoveCartItem.as_view(), name='remove_cart_item'),

   path('cart/<int:user_id>/', ViewCart.as_view(),name='view_cart'),
   path('cart/payment/', CartPaymentView.as_view(),name='cart_payment'),
   path('my-orders/<int:user_id>/', MyOrdersView.as_view(),name='my_orders'),

]


















# http://127.0.0.1:8002/medico/chat_download_pdf/2/1/