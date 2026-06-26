from django.core.management.base import BaseCommand
from cms.models import SiteSettings, SocialLink, FooterColumn, FooterLink, NewsletterSection


class Command(BaseCommand):
    help = "Seed Phase 1 CMS data with multilingual support"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing data.")

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_site_settings(force)
        self.seed_social_links(force)
        self.seed_footer(force)
        self.seed_newsletter_section(force)
        self.stdout.write(self.style.SUCCESS("\nPhase 1 CMS data seeded successfully."))

    def seed_site_settings(self, force):
        if SiteSettings.objects.exists() and not force:
            self.stdout.write("  SiteSettings exists — skipping.")
            return
        SiteSettings.objects.all().delete()
        SiteSettings.objects.create(
            site_name="Gravestone Memorials",
            phone="+852 0000 0000",
            email="info@gravestonememorials.com",
            whatsapp_number="+852 0000 0000",
            address="Hong Kong",
            copyright_text={
                "en":      "© 2025 Gravestone Memorials. All rights reserved.",
                "zh_hans": "© 2025 墓碑纪念馆。保留所有权利。",
                "zh_hant": "© 2025 墓碑紀念館。保留所有權利。",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ SiteSettings created."))

    def seed_social_links(self, force):
        if SocialLink.objects.exists() and not force:
            self.stdout.write("  SocialLinks exist — skipping.")
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

    def seed_footer(self, force):
        if FooterColumn.objects.exists() and not force:
            self.stdout.write("  Footer exists — skipping.")
            return
        FooterColumn.objects.all().delete()
        footer_data = [
            {
                "title": {"en": "Gravestone Memorials", "zh_hans": "墓碑纪念馆", "zh_hant": "墓碑紀念館"},
                "order": 1,
                "links": [
                    {"label": {"en": "Register No: 12345678", "zh_hans": "注册号: 12345678", "zh_hant": "登記號: 12345678"}, "url": "#",                          "order": 1},
                    {"label": {"en": "Hong Kong",             "zh_hans": "香港",               "zh_hant": "香港"},              "url": "#",                          "order": 2},
                    {"label": {"en": "+852 0000 0000",        "zh_hans": "+852 0000 0000",     "zh_hant": "+852 0000 0000"},    "url": "tel:+85200000000",           "order": 3},
                ],
            },
            {
                "title": {"en": "Navigate", "zh_hans": "导航", "zh_hant": "導航"},
                "order": 2,
                "links": [
                    {"label": {"en": "Home",            "zh_hans": "首页",   "zh_hant": "首頁"},   "url": "/",                "order": 1},
                    {"label": {"en": "Stone Catalogue", "zh_hans": "石材目录", "zh_hant": "石材目錄"}, "url": "/stone-catalogue", "order": 2},
                    {"label": {"en": "Our Work",        "zh_hans": "我们的作品", "zh_hant": "我們的作品"}, "url": "/our-work",   "order": 3},
                    {"label": {"en": "Booking",         "zh_hans": "预订",   "zh_hant": "預訂"},   "url": "/booking",         "order": 4},
                ],
            },
            {
                "title": {"en": "Contact", "zh_hans": "联系我们", "zh_hant": "聯絡我們"},
                "order": 3,
                "links": [
                    {"label": {"en": "info@gravestonememorials.com", "zh_hans": "info@gravestonememorials.com", "zh_hant": "info@gravestonememorials.com"}, "url": "mailto:info@gravestonememorials.com", "order": 1},
                    {"label": {"en": "+852 0000 0000",               "zh_hans": "+852 0000 0000",               "zh_hant": "+852 0000 0000"},               "url": "tel:+85200000000",                   "order": 2},
                    {"label": {"en": "WhatsApp Us",                  "zh_hans": "WhatsApp 联系",                 "zh_hant": "WhatsApp 聯絡"},                 "url": "https://wa.me/85200000000",          "order": 3},
                ],
            },
            {
                "title": {"en": "Accompaniments", "zh_hans": "附加服务", "zh_hant": "附加服務"},
                "order": 4,
                "links": [
                    {"label": {"en": "Privacy Policy", "zh_hans": "隐私政策", "zh_hant": "私隱政策"}, "url": "/privacy-policy", "order": 1},
                    {"label": {"en": "Terms of Use",   "zh_hans": "使用条款", "zh_hant": "使用條款"}, "url": "/terms",          "order": 2},
                    {"label": {"en": "Sitemap",        "zh_hans": "网站地图", "zh_hant": "網站地圖"}, "url": "/sitemap",        "order": 3},
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
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(footer_data)} FooterColumns and {total_links} FooterLinks created."))

    def seed_newsletter_section(self, force):
        if NewsletterSection.objects.exists() and not force:
            self.stdout.write("  NewsletterSection exists — skipping.")
            return
        NewsletterSection.objects.all().delete()
        NewsletterSection.objects.create(
            headline={
                "en":      "Join Our Newsletter Stay Up To Date",
                "zh_hans": "订阅我们的通讯，保持最新资讯",
                "zh_hant": "訂閱我們的通訊，保持最新資訊",
            },
            subtext={
                "en":      "Subscribe to our newsletter and stay updated on the latest collections, memorial design inspiration, and personalised stone crafting services. Respectfully honouring your loved ones, every step of the way.",
                "zh_hans": "订阅我们的通讯，了解最新系列、纪念设计灵感及个性化石材定制服务。我们以尊重的态度，陪伴您走过每一步，缅怀您挚爱的人。",
                "zh_hant": "訂閱我們的通訊，了解最新系列、紀念設計靈感及個人化石材訂製服務。我們以尊重的態度，陪伴您走過每一步，緬懷您摯愛的人。",
            },
            button_label={
                "en":      "Subscribe",
                "zh_hans": "订阅",
                "zh_hant": "訂閱",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ NewsletterSection created."))