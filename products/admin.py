from django.contrib import admin
from .models import Product, Review
from django.utils import timezone
class ReviewInline(admin.TabularInline):  # StackedInline farklı bir görünüm aynı iş
    '''Tabular Inline View for '''
    model = Review
    extra = 1
    classes = ('collapse',)
    # min_num = 3
    # max_num = 20
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "create_date", "is_in_stock", "update_date","added_days_ago")
    list_editable = ( "is_in_stock", )
    # list_display_links = ("create_date", ) #? can't add items in list_editable to here
    list_filter = ("is_in_stock", "create_date")
    ordering = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {'slug' : ('name',)}   #? when adding product in admin site
    list_per_page = 15
    date_hierarchy = "update_date"
    inlines = (ReviewInline,)
    # fields = (('name', 'slug'), 'description', "is_in_stock") #!when we use "fieldset" 👇 we can't use this

    fieldsets = (
        ('General', {
            "fields": (
                ('name', 'slug'), "is_in_stock" #? to display multiple fields on the same line, wrap those fields in their own tuple
            ),
            # 'classes': ('wide', 'extrapretty'), wide or collapse
        }),
        ('Optionals Settings', {
            "classes" : ("collapse", ),
            "fields" : ("description",),
            'description' : "You can use this section for optionals settings"
        })
    )

    actions = ("is_in_stock", )

    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} assorted products added to stock")
    is_in_stock.short_description = 'Update the stock status of marked products'

    def added_days_ago(self, product):
       difference = timezone.now() - product.create_date
       return difference.days

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    raw_id_fields = ('product',)



admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.site_title = "Clarusway Title"
admin.site.site_header = "Clarusway Admin Portal"
admin.site.index_title = "Welcome to Clarusway Admin Portal"