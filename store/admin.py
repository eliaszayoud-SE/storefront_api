from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models import Count
from django.utils.html import format_html
from django.http import HttpRequest
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        products_count = collection.products_count
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode(
                {
                    'collection__id':collection.id
                }
            )
            )
        return format_html(f'<a href="{url}">{products_count}</a>')
        

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin) :
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_select_related = ['collection']
    list_per_page = 10
    inlines = [ProductImageInline]
    actions = ['clear_inventory']
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear inverntory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
        )

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory > 10:
            return 'Ok'
        return 'Low'
    
    class Media:
        css = {
            'all':['store/styles.css']
        }
    
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


admin.site.register(models.OrderItem)    

   

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    