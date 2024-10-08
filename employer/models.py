from django.db import models
from django.utils import timezone
from account.models import Employer, EmployerProfile
import uuid


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


def populate_categories():
    categories = [
        "Engineering", "Information Technology", "Marketing", "Sales",
        "Human Resources", "Finance", "Healthcare", "Education",
        "Customer Service", "Legal", "Administration", "Manufacturing",
        "Logistics & Supply Chain", "Consulting", "Construction",
        "Creative & Design", "Research & Development", "Public Relations",
        "Project Management", "Operations", "Software Development",
        "Frontend Development", "Backend Development", "Data Science",
        "DevOps", "UI/UX Design", "Mobile Development", "Cybersecurity",
        "Quality Assurance", "Business Analysis", "Product Management",
        "Technical Support", "Content Creation", "Digital Marketing"
    ]
    

    for category in categories:
        Category.objects.get_or_create(name=category)


# Job Model
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("REMOTE", "Remote"),
        ("HYBRID", "Hybrid"),
        ("ONSITE", "Onsite"),
    ]

    SCHEDULE_CHOICES = [
        ("FULL_TIME", "Full Time"),
        ("PART_TIME", "Part Time"),
    ]

    CAREER_LEVEL_CHOICES = [
        ("ENTRY_LEVEL", "Entry Level"),
        ("EXPERIENCED", "Experienced"),
        ("PROFESSIONAL", "Professional"),
        ("MANAGER", "Manager"),
        ("SENIOR_MANAGER", "Senior Level Manager"),
    ]

    # id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    company = models.ForeignKey(
        EmployerProfile, on_delete=models.CASCADE, related_name="jobs"
    )
    company_awards_recognitions = models.TextField(blank=True, null=True)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES)
    career_level = models.CharField(max_length=50, choices=CAREER_LEVEL_CHOICES)
    education_level = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="jobs"
    )
    description = models.TextField()
    time_posted = models.DateTimeField(default=timezone.now)
    time_updated = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return self.title
