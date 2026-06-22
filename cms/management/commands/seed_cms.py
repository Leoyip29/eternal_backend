from django.core.management.base import BaseCommand
from cms.models import SiteSettings, SocialLink, FooterColumn, FooterLink, NewsletterSection


class Command(BaseCommand):
    help = "Seed Phase 1 CMS data: SiteSettings, SocialLinks, Footer, NewsletterSection"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing data with fresh seed values.",
        )

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_site_settings(force)
        self.seed_social_links(force)
        self.seed_footer(force)
        self.seed_newsletter_section(force)
        self.stdout.write(self.style.SUCCESS("\nPhase 1 CMS data seeded successfully."))

    # ------------------------------------------------------------------
    def seed_site_settings(self, force):
        if SiteSettings.objects.exists() and not force:
            self.stdout.write("  SiteSettings already exists — skipping. (use --force to overwrite)")
            return

        SiteSettings.objects.all().delete()
        SiteSettings.objects.create(
            site_name="Gravestone Memorials",
            phone="+852 0000 0000",
            email="info@gravestonememorials.com",
            whatsapp_number="+852 0000 0000",
            address="Hong Kong",
            copyright_text="© 2025 Gravestone Memorials. All rights reserved.",
        )
        self.stdout.write(self.style.SUCCESS("  ✓ SiteSettings created."))

    # ------------------------------------------------------------------
    def seed_social_links(self, force):
        if SocialLink.objects.exists() and not force:
            self.stdout.write("  SocialLinks already exist — skipping. (use --force to overwrite)")
            return

        SocialLink.objects.all().delete()
        links = [
            {"platform": "instagram", "url": "https://instagram.com/gravestonememorials", "order": 1},
            {"platform": "facebook",  "url": "https://facebook.com/gravestonememorials",  "order": 2},
            {"platform": "youtube",   "url": "https://youtube.com/@gravestonememorials",  "order": 3},
            {"platform": "tiktok",    "url": "https://tiktok.com/@gravestonememorials",   "order": 4},
        ]
        for data in links:
            SocialLink.objects.create(**data)
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(links)} SocialLinks created."))

    # ------------------------------------------------------------------
    def seed_footer(self, force):
        if FooterColumn.objects.exists() and not force:
            self.stdout.write("  Footer already exists — skipping. (use --force to overwrite)")
            return

        FooterColumn.objects.all().delete()

        footer_data = [
            {
                "title": "Gravestone Memorials",
                "order": 1,
                "links": [
                    {"label": "Register No: 12345678", "url": "#",                          "order": 1},
                    {"label": "Hong Kong",             "url": "#",                          "order": 2},
                    {"label": "+852 0000 0000",        "url": "tel:+85200000000",           "order": 3},
                ],
            },
            {
                "title": "Navigate",
                "order": 2,
                "links": [
                    {"label": "Home",            "url": "/",                "order": 1},
                    {"label": "Stone Catalogue", "url": "/stone-catalogue", "order": 2},
                    {"label": "Our Work",        "url": "/our-work",        "order": 3},
                    {"label": "Booking",         "url": "/booking",         "order": 4},
                ],
            },
            {
                "title": "Contact",
                "order": 3,
                "links": [
                    {"label": "info@gravestonememorials.com", "url": "mailto:info@gravestonememorials.com", "order": 1},
                    {"label": "+852 0000 0000",               "url": "tel:+85200000000",                   "order": 2},
                    {"label": "WhatsApp Us",                  "url": "https://wa.me/85200000000",          "order": 3},
                ],
            },
            {
                "title": "Accompaniments",
                "order": 4,
                "links": [
                    {"label": "Privacy Policy", "url": "/privacy-policy", "order": 1},
                    {"label": "Terms of Use",   "url": "/terms",          "order": 2},
                    {"label": "Sitemap",        "url": "/sitemap",        "order": 3},
                ],
            },
        ]

        total_links = 0
        for col_data in footer_data:
            links = col_data.pop("links")
            column = FooterColumn.objects.create(**col_data)
            for link_data in links:
                FooterLink.objects.create(column=column, **link_data)
                total_links += 1

        self.stdout.write(self.style.SUCCESS(
            f"  ✓ {len(footer_data)} FooterColumns and {total_links} FooterLinks created."
        ))

    # ------------------------------------------------------------------
    def seed_newsletter_section(self, force):
        if NewsletterSection.objects.exists() and not force:
            self.stdout.write("  NewsletterSection already exists — skipping. (use --force to overwrite)")
            return

        NewsletterSection.objects.all().delete()
        NewsletterSection.objects.create(
            headline="Join Our Newsletter Stay Up To Date",
            subtext=(
                "Subscribe to our newsletter and stay updated on the latest collections, "
                "memorial design inspiration, and personalised stone crafting services. "
                "Respectfully honouring your loved ones, every step of the way."
            ),
            button_label="Subscribe",
        )
        self.stdout.write(self.style.SUCCESS("  ✓ NewsletterSection created."))