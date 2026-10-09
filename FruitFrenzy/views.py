from django.urls import reverse
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic import ListView
from .models import Product, Reviews
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import CartItem, Reviews, Order, Allergen, Product
from django.http import JsonResponse
from .forms import ReviewForm, ProductForm
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from decimal import Decimal


def index(request):
    return render(request, 'FruitFrenzy/index.html')


# class ProductListView(generic.ListView):
#    model = Product


def ProductListView(request):
    products = Product.objects.all()
    allergen_list = Allergen.objects.all()

    # Apply filters
    ingredients = request.GET.get('ingredients')
    price = request.GET.get('price')
    allergen = request.GET.get('allergen')
    search_query = request.GET.get('search')
    products = Product.objects.all()

    if ingredients:
        products = products.filter(product_ingredients__icontains=ingredients)

    if price:
        products = products.filter(product_price__lte=price)

    if allergen:
        products = products.filter(allergen_id=allergen)

    if search_query:
        products = products.filter(Q(product_name__icontains=search_query))

    context = {
        'products': products,
        'allergen_list': allergen_list,
    }

    return render(request, 'FruitFrenzy/product_list.html', context)


def ProductDetailView(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        price = float(product.product_price)
        cart_item = CartItem(user=request.user, product=product, quantity=quantity, price=price)
        cart_item.save()

        messages.success(request, f"{quantity} {product.product_name}(s) added to cart.")
        return redirect('mycart')

    context = {
        'product': product,
    }

    return render(request, 'FruitFrenzy/product_detail.html', context)


class ProductCreate(CreateView):
    model = Product
    fields = ['product_name', 'product_price', 'product_description', 'product_ingredients', 'product_image',
              'allergen']

    def get_initial(self):
        initial = super().get_initial()
        initial['allergen'] = 'non-allergen'
        return initial


class ProductUpdate(UpdateView):
    model = Product
    fields = ['product_name', 'product_price', 'product_description', 'product_ingredients', 'product_image',
              'allergen']


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        product.delete()

    except:
        messages.success(request, (product.product_name + ' cannot be deleted'))
    return redirect('product_list')


class AllergenDetailView(generic.DetailView):
    model = Allergen


class AllergenListView(generic.ListView):
    model = Allergen


class AllergenCreate(CreateView):
    model = Allergen
    fields = ['allergen_name']
    success_url = reverse_lazy('allergen_list')


class AllergenUpdate(UpdateView):
    model = Allergen
    fields = ['allergen_name']
    success_url = reverse_lazy('allergen_list')


def allergen_delete(request, pk):
    allergen = get_object_or_404(Allergen, pk=pk)
    try:
        allergen.delete()
        messages.success(request, (allergen.allergen_name + " has been deleted"))
    except:
        messages.success(request, (allergen.allergen_name + ' cannot be deleted'))
    return redirect('allergen_list')


class ReviewsView(TemplateView):
    template_name = 'FruitFrenzy/review_create.html'


def mycart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.price_tax() for item in cart_items)
    total_count = sum(item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_count': total_count
    }

    return render(request, 'FruitFrenzy/mycart.html', context)


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Product removed from cart.')

    return redirect('mycart')


@login_required()
def get_cart_item_count(request):
    cart_item_count = CartItem.objects.filter(user=request.user).count()
    data = {
        'cart_item_count': cart_item_count
    }
    return JsonResponse(data)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Reviews
    form_class = ReviewForm
    template_name = 'FruitFrenzy/review_create.html'
    success_url = '/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewListView(ListView):
    model = Reviews
    template_name = 'FruitFrenzy/review_list.html'
    context_object_name = 'reviews'
    ordering = ['-id']


class ReviewDeleteView(View):
    def post(self, request, pk):
        review = get_object_or_404(Reviews, pk=pk)
        review.delete()
        return redirect('review_list')


def place_your_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            order = Order.objects.create(
                user=request.user,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price,

            )
            order.save()

        # Clear the cart
        cart_items.delete()
        return redirect('myorder')


def get_order_item_count(request):
    order_item_count = Order.objects.filter(user=request.user).count()
    data = {
        'order_item_count': order_item_count
    }
    return JsonResponse(data)


def myorder(request):
    order_items = Order.objects.filter(user=request.user)
    total_price = sum(item.price_tax() for item in order_items)
    total_count = sum(item.quantity for item in order_items)

    context = {
        'order_items': order_items,
        'total_price': total_price,
        'total_count': total_count
    }

    return render(request, 'FruitFrenzy/my_orders.html', context)


def remove_order(request, item_id):
    item = get_object_or_404(Order, id=item_id, user=request.user)
    item.delete()

    return redirect('myorder')


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'FruitFrenzy/order_list.html', {'orders': orders})


def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


@login_required
def send_order_email(request):
    user = request.user
    order_items = Order.objects.filter(user=user)
    total_price = sum(item.price_tax() for item in order_items)
    total_count = sum(item.quantity for item in order_items)

    email_subject = 'Order placed Successfully'
    email_html_template = 'email/order_details.html'
    email_plain_text_template = 'email/order_details.txt'

    context = {
        'user': user,
        'order_items': order_items,
        'total_price': total_price,
        'total_count': total_count,

    }

    html_message = render_to_string(email_html_template, context)
    plain_text_message = strip_tags(render_to_string(email_plain_text_template, context))
    from_email = f'FruitFrenzy <settings.DEFAULT_FROM_EMAIL>'

    send_mail(
        email_subject,
        plain_text_message,
        from_email,
        [user.email],
        html_message=html_message,
    )
    messages.success(request, "Order summary sent to your email successfully.")

    return redirect('myorder')


def email_success(request):
    return render(request, 'FruitFrenzy/email_success.html')
