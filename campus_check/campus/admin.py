from django.contrib import admin
from campus.models import Location, Degree, University, Course, User, Enrollment, Review

admin.site.register(Location)
admin.site.register(Degree)
admin.site.register(Enrollment)
admin.site.register(Review)

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
# Update the registration to include this customised interface
admin.site.register(University, CategoryAdmin)
admin.site.register(Course, CategoryAdmin)
