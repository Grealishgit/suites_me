from django.core.management.base import BaseCommand
from a_main.models import BlogTags
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Bulk add predefined blog tags to the database"

    def handle(self, *args, **kwargs):
        # List of predefined tags
        tags = [
            "Software Development", "Web Development", "Mobile App Development",
            "UI/UX Design", "Artificial Intelligence (AI)", "Cloud Computing",
            "E-Commerce Solutions", "DevOps", "Cybersecurity", 
            "Career in Tech", "Tech Tutorials", "Industry Trends"
        ]

        # Prepare BlogTags instances
        blog_tags = [BlogTags(name=tag, slug=slugify(tag)) for tag in tags]

        # Bulk create tags
        created_tags = BlogTags.objects.bulk_create(blog_tags, ignore_conflicts=True)

        # Feedback to the user
        if created_tags:
            self.stdout.write(self.style.SUCCESS(f"Successfully added {len(created_tags)} tags!"))
        else:
            self.stdout.write(self.style.WARNING("No new tags were added. All tags already exist."))
