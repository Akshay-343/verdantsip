from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='create_review'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('product_list/', views.ProductListView, name='product_list'),
    path('product_detail/<int:pk>', views.ProductDetailView, name='product_detail'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('allergen_list/', views.AllergenListView.as_view(), name='allergen_list'),
    path('allergen/create/', views.AllergenCreate.as_view(), name='allergen_create'),
    path('allergen/<int:pk>/update/', views.AllergenUpdate.as_view(), name='allergen_update'),
    path('allergen/<int:pk>/delete/', views.allergen_delete, name='allergen_delete'),
    path('mycart/', views.mycart, name='mycart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart_item_count/', views.get_cart_item_count, name='cart_item_count'),
    path('order_item_count/', views.get_order_item_count, name='order_item_count'),
    path('myorder/', views.myorder, name='myorder'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('my-orders/', views.place_your_order, name='orders_btn'),
    path('remove_order/<int:item_id>/', views.remove_order, name='remove_order'),
    path('orders/', views.order_list, name='order_list'),
    path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('send_order_email/', views.send_order_email, name='send_order_email'),
    path('email_success/',views.email_success, name='email_success'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
