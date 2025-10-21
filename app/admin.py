from django.contrib import admin
from .models import Student, Sponsor, Sponsor_of_Student, University


class SponsorStudentTabularInline(admin.TabularInline):
    extra = 1
    model = Sponsor_of_Student

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("id", "university_name")
    search_fields = ("university_name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [SponsorStudentTabularInline, ]
    list_display = ("id", "full_name","contract_sum")
    list_display_links = ('id', "full_name")
    
    @admin.display(description="University")
    def get_university_name(self, obj):
        return obj.university.university_name if obj.university else "-"


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone_number", "payment_amount", "sponsor_status", "created_at")
    search_fields = ("full_name", "phone_number")
    list_filter = ("sponsor_status",)
    ordering = ("-created_at",)


@admin.register(Sponsor_of_Student)
class SponsorOfStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "sponsor", "student", "get_amount")
    search_fields = ("sponsor__full_name", "student__full_name")
    ordering = ("id",)

    @admin.display(description="Amount")
    def get_amount(self, obj):
        return getattr(obj, "amount", "—")
