from django.contrib import admin
from .models import Job, Category

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["title", "job_type", "company", "company_awards_recognitions", "schedule", "career_level", "education_level", "category"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
