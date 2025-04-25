from django.contrib import admin
from .models import PlantSale, Purchase

class PlantSaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_available', 'seller', 'is_sold', 'date_listed')
    list_filter = ('is_sold', 'date_listed')
    search_fields = ('name', 'description', 'seller__username')
    readonly_fields = ('total_sold',)

    def total_sold(self, obj):
        return obj.total_sold
    total_sold.short_description = 'Total Units Sold'

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('plant', 'buyer', 'quantity', 'get_total_price', 'purchase_date', 'status')
    list_filter = ('status', 'purchase_date')
    search_fields = ('plant__name', 'buyer__username')

    def get_total_price(self, obj):
        return f"₹{obj.total_price}"
    get_total_price.short_description = 'Total Price'

admin.site.register(PlantSale, PlantSaleAdmin)
admin.site.register(Purchase, PurchaseAdmin)
