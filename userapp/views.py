from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")

# Configure Gemini API
genai.configure(api_key=api_key)

# Create model instance
model = genai.GenerativeModel('gemini-2.5-flash')

# Period-related keywords
PERIOD_KEYWORDS = [
    "period", "menstrual", "menstruation", "pms", "cramps",
    "cycle", "bleeding", "ovulation", "menopause", "fertility",
    "flow", "spotting", "pads", "tampons", "menstrual cup",
    "dysmenorrhea", "amenorrhea", "menorrhagia", "endometriosis", "fibroids",
    "ovaries", "uterus", "hormones", "estrogen", "progesterone",
    "follicular phase", "luteal phase", "perimenopause", "pcos", "pmdd", "periods", "relief",
    "medication", "pain relief", "cramp relief", "medicines", "medicine", "book", "books","suggestions", "suggestion", "skin care"
]

# Greeting keywords
GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]

# def chatbot_view(request):
#     if request.method == "POST":
#         user_message = request.POST.get("message", "").lower().strip()

#         if not user_message:
#             return JsonResponse({"error": "Message is empty"}, status=400)

#         # Check for greetings
#         if any(greet in user_message for greet in GREETINGS):
#             return JsonResponse({
#                 "reply": "Hello! 😊 I'm Her Time, your menstrual health assistant. You can ask me about periods, ovulation, PMS, or cycle tracking."
#             })

#         # Check for period-related topics
#         if not any(keyword in user_message for keyword in PERIOD_KEYWORDS):
#             return JsonResponse({
#                 "reply": "I can only answer questions related to menstrual health, periods, ovulation, and PMS."
#             })

#         try:
#             # Keep Gemini focused on menstrual health
#             response = model.generate_content(
#                 f"You are a menstrual health assistant. Answer only about periods, cycles, ovulation, and PMS. Question: {user_message}"
#             )
#             return JsonResponse({"reply": response.text})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)

#     return render(request, "chatbot.html")

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
import os
from dotenv import load_dotenv
from django.conf import settings
# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file")

# Configure Gemini API
genai.configure(api_key=settings.OPENAI_API_KEY)

# Create model instance
model = genai.GenerativeModel('gemini-2.5-flash') 

# Period-related keywords
PERIOD_KEYWORDS = [
    "period", "menstrual", "menstruation", "pms", "cramps",
    "cycle", "bleeding", "ovulation", "menopause", "fertility",
    "flow", "spotting", "pads", "tampons", "menstrual cup",
    "dysmenorrhea", "amenorrhea", "menorrhagia", "endometriosis", "fibroids",
    "ovaries", "uterus", "hormones", "estrogen", "progesterone",
    "follicular phase", "luteal phase", "perimenopause", "pcos", "pmdd", "periods", "relief",
    "medication", "pain relief", "cramp relief", "medicines", "medicine", "book", "books",
    "suggestions", "suggestion", "skin care", "tips", "advice"
]

# Greeting keywords
GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]


class ChatbotAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "").lower().strip()

        if not user_message:
            return Response({
                "type": "error",
                "reply": "Message is empty"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for greetings
        if any(greet in user_message for greet in GREETINGS):
            return Response({
                "type": "greeting",
                "reply": "Hello! 😊 I'm Her Time, your menstrual health assistant. You can ask me about periods, ovulation, PMS, or cycle tracking."
            })

        # Check for period-related topics
        if not any(keyword in user_message for keyword in PERIOD_KEYWORDS):
            return Response({
                "type": "not_related",
                "reply": "I can only answer questions related to menstrual health, periods, ovulation, and PMS."
            })

        try:
            # Keep Gemini focused on menstrual health
            response = model.generate_content(
                f"You are a menstrual health assistant. Answer only about periods, cycles, ovulation, and PMS. Question: {user_message}"
            )
            return Response({
                "type": "period_info",
                "reply": response.text
            })
        except Exception as e:
            return Response({
                "type": "error",
                "reply": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

# from houseprojectapp.utils.material_budget import get_material_budget

from .models import  tbl_register

from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = tbl_register.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import tbl_register
from .serializers import LoginSerializer

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = tbl_register.objects.get(email=email, password=password)
            return Response({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "password": user.password  # ⚠️ Usually we should NOT send plain password, but you asked for it
            }, status=status.HTTP_200_OK)

        except tbl_register.DoesNotExist:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import viewsets
from .models import CycleInput
from .serializers import CycleInputSerializer

class CycleInputViewSet(viewsets.ModelViewSet):
    queryset = CycleInput.objects.all()
    serializer_class = CycleInputSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CycleInput
from .serializers import CycleInputSerializer,BookSerializer
from adminapp.models import Book

@api_view(["GET"])
def get_cycle_inputs_by_user(request, user_id):
    try:
        inputs = CycleInput.objects.filter(user_id=user_id).order_by("-created_at")
        serializer = CycleInputSerializer(inputs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CycleInput.DoesNotExist:
        return Response({"error": "No cycle inputs found for this user."}, status=status.HTTP_404_NOT_FOUND)



class UserViewBook(APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    
from adminapp.models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewCategory(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class UserViewProduct(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)



from rest_framework.views import APIView
from rest_framework.response import Response
from adminapp.models import Product
from .serializers import ProductSerializer

class ProductByCategory(APIView):
    def get(self, request, category_id, *args, **kwargs):
        products = Product.objects.filter(category_id=category_id)
        serializer = ProductSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import Product
from .serializers import ProductSerializer

class ProductDetailView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)



#product booking and cart purchase
from .serializers import *
class ProductBookingView(APIView):
    def post(self, request):
        serializer = ProductBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        total_price = serializer.validated_data['total_price']

        user = get_object_or_404(tbl_register, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        booking = ProductBooking.objects.create(
            user=user,
            product=product,
            category=product.category,
            quantity=quantity,
            total_price=total_price,
            status='completed'
        )

        return Response({
            "status": "success",
            "booking": ProductBookingSerializer(booking).data
        }, status=201)


class BookingPaymentView(APIView):
    def post(self, request):
        serializer = BookingPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(payment_choice="booking_payment")
        return Response({"status": "success", "payment": serializer.data}, status=201)
    
class CartCreateView(APIView):
    def post(self, request, product_id):
        user_id = request.data.get("user_id")
        quantity = int(request.data.get("quantity", 1))
        total_price = request.data.get("total_price")

        user = get_object_or_404(tbl_register, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        item = Cart.objects.create(
            user=user,
            product=product,
            category=product.category,
            quantity=quantity,
            total_price=total_price,
        )
        return Response({"status": "success", "cart": CartSerializer(item).data}, status=201)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart
from .serializers import CartSerializer

class UpdateCartQuantity(APIView):
    def patch(self, request):
        cart_id = request.data.get("cart_id")
        quantity = request.data.get("quantity")
        total_price = request.data.get("total_price")  # Flutter sends this

        if not cart_id or not quantity:
            return Response(
                {"error": "cart_id and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = get_object_or_404(Cart, id=cart_id)

        # Remove item if quantity is 0
        if int(quantity) <= 0:
            cart_item.delete()
            return Response(
                {"message": "Item removed from cart because quantity is 0."},
                status=status.HTTP_200_OK
            )

        cart_item.quantity = int(quantity)

        # Flutter calculates total price, so update only if sent
        if total_price is not None:
            cart_item.total_price = total_price

        cart_item.save()

        return Response({
            "message": "Cart quantity updated successfully.",
            "cart": CartSerializer(cart_item).data
        }, status=status.HTTP_200_OK)
class RemoveCartItem(APIView):
    def delete(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id)
        cart_item.delete()

        return Response(
            {"status": "success", "message": "Cart item removed"},
            status=200
        )


class ViewCart(APIView):
    def get(self, request, user_id):
        cart = Cart.objects.filter(user_id=user_id, status="pending")
        data = CartSerializer(cart, many=True, context={'request': request}).data
        return Response({"cart": data})
class CartPaymentView(APIView):
    def post(self, request):
        serializer = CartPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pay = serializer.save(payment_choice="cart_payment")

        # ✅ UPDATE CART STATUS AFTER SUCCESSFUL PAYMENT
        cart_ids = pay.cart_ids          # e.g., [1,2,3]
        Cart.objects.filter(id__in=cart_ids).update(status="completed")

        return Response({
            "status": "success",
            "message": "Payment successful and cart status updated",
            "payment": serializer.data
        }, status=201)

# class MyOrdersView(APIView):
#     def get(self, request, user_id):
#         orders = []

#         bookings = ProductBooking.objects.filter(user_id=user_id)
#         for b in bookings:
#             pay = getattr(b, 'payment', None)
#             orders.append({
#                 # "type": "single_product",
#                 "product": b.product.name,
#                 "quantity": b.quantity,
#                 "total_price": b.total_price,
#                 "product_image": product_image_url,
#                 "payment_type": pay.payment_type if pay else None,
#                 "payment_status": pay.status if pay else None,
#             })

#         carts = Cart.objects.filter(user_id=user_id)
#         for c in carts:
#             pay = CartPayment.objects.filter(user_id=user_id, cart_ids__contains=[c.id]).first()
#             orders.append({
#                 # "type": "cart_item",
#                 "product": c.product.name,
#                 "quantity": c.quantity,
#                 "total_price": c.total_price,
#                 "product_image": product_image_url,
#                 "payment_type": pay.payment_type if pay else None,
#                 "payment_status": pay.status if pay else None,
#             })

#         return Response({"orders": orders})

class MyOrdersView(APIView):
    def get(self, request, user_id):
        orders = []

        # ----------- PRODUCT BOOKINGS ----------
        bookings = ProductBooking.objects.filter(user_id=user_id)
        for b in bookings:

            # ✅ Only /media/... 
            product_image_url = b.product.image.url if b.product.image else None

            pay = getattr(b, 'payment', None)

            orders.append({
                "product": b.product.name,
                "quantity": b.quantity,
                "total_price": b.total_price,
                "product_image": product_image_url,
                "payment_type": pay.payment_type if pay else None,
                "payment_status": pay.status if pay else None,
            })

        # ----------- CART PURCHASES ----------
        carts = Cart.objects.filter(user_id=user_id)
        for c in carts:

            # ✅ Only /media/...
            product_image_url = c.product.image.url if c.product.image else None

            pay = CartPayment.objects.filter(
                user_id=user_id,
                cart_ids__contains=[c.id]
            ).first()

            orders.append({
                "product": c.product.name,
                "quantity": c.quantity,
                "total_price": c.total_price,
                "product_image": product_image_url,
                "payment_type": pay.payment_type if pay else None,
                "payment_status": pay.status if pay else None,
            })

        return Response({"orders": orders})
