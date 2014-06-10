from django.contrib import admin

# Register your models here.
from .models import Order

class OrderAdmin(admin.ModelAdmin):
	class Meta:
		model = Order

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['order_id']
		return self.get_readonly_fields

	def has_delete_permission(self, request, obj=None):
		return False


admin.site.register(Order, OrderAdmin)