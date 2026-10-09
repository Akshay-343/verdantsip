from django.contrib import admin
from .models import Product
from .models import Allergen
from .models import Reviews

# Register your models here.
admin.site.register(Product)
admin.site.register(Allergen)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review_title', 'review_content', 'review_rating', 'product_image']
    list_filter = ['review_rating']
    search_fields = ['user__username', 'review_title']
    actions = ['delete_selected']


admin.site.register(Reviews, ReviewAdmin)
