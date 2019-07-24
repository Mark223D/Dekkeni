from django.contrib import admin
from .models import Product, Category#, Subcategory, Subsubcategory, TestCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'pk', '__str__', 'category','price','slug']
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_filter = ('category','featured','hot_deals', 'new_arrivals', 'title')
    list_display_links = ('__str__',)
    fieldsets = (
        (None, {'fields': ('category', 'title', 'slug', 'featured','hot_deals', 'new_arrivals', 'in_cart', 'image', 'description')}),
       # ('Full name', {'fields': ()}),
        # ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('category', 'title', 'featured','hot_deals', 'new_arrivals')}
        ),
    )
    search_fields = ('category', 'title', 'slug')
    ordering = ('category', 'title')
    filter_horizontal = ()

    class Meta:
        model = Product

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['__str__','slug']
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_filter = ('title',)
#     list_display_links = ('__str__',)

#     fieldsets = (
#         (None, {'fields': ('title',)}),
#        # ('Full name', {'fields': ()}),
#         # ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('title'),}
#         ),
#     )
#     search_fields = ('title','slug')
#     ordering = ('title',)
#     filter_horizontal = ()

#     class Meta:
#         model = Category

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category', '__str__','slug']
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_filter = ('category', 'title',)
#     list_display_links = ('__str__',)
#     fieldsets = (
#         (None, {'fields': ('category', 'title',)}),
#        # ('Full name', {'fields': ()}),
#         # ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('category', 'title',)}
#         ),
#     )
#     search_fields = ('category', 'title','slug')
#     ordering = ('category', 'title',)
#     filter_horizontal = ()
#     class Meta:
#         model = Subcategory

# class SubsubCategoryAdmin(admin.ModelAdmin):
#     list_display = ['subcategory', '__str__', 'slug']
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_filter = ('subcategory', )
#     list_display_links = ('__str__',)
#     fieldsets = (
#         (None, {'fields': ('subcategory',)}),
#        # ('Full name', {'fields': ()}),
#         # ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('subcategory'),}
#         ),
#     )
#     search_fields = ('subcategory',)
#     ordering = ('subcategory',)
#     filter_horizontal = ()
#     class Meta:
#         model = Subsubcategory

# admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
# admin.site.register(Subcategory, SubCategoryAdmin)
# admin.site.register(Subsubcategory, SubsubCategoryAdmin)
