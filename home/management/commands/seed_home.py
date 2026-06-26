from django.core.management.base import BaseCommand
from home.models import (
    HeroSection, ProductsSectionHeading, FeaturedProduct,
    ServicesSectionHeading, ServiceStep,
    HowItWorksHeading, HowItWorksStep,
    StoneGallerySection, AboutUsSection,
    FAQSection, FAQ, TestimonialsSection, Testimonial,
)


class Command(BaseCommand):
    help = "Seed Phase 2 home page content with multilingual support"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing data.")

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_hero(force)
        self.seed_products_heading(force)
        self.seed_featured_products(force)
        self.seed_services(force)
        self.seed_how_it_works(force)
        self.seed_stone_gallery(force)
        self.seed_about_us(force)
        self.seed_faq(force)
        self.seed_testimonials(force)
        self.stdout.write(self.style.SUCCESS("\nPhase 2 home page data seeded successfully."))

    def seed_hero(self, force):
        if HeroSection.objects.exists() and not force:
            self.stdout.write("  HeroSection exists — skipping.")
            return
        HeroSection.objects.all().delete()
        HeroSection.objects.create(
            headline={
                "en":      "Honor Your Loved One with a Lasting Memorial.",
                "zh_hans": "以永恒的纪念，缅怀您挚爱的人。",
                "zh_hant": "以永恆的紀念，緬懷您摯愛的人。",
            },
            subtext={
                "en":      "Every life is a unique story that deserves to be remembered. A dedicated memorial is more than a marker — it is a sacred space for reflection and a permanent testament to a life beautifully lived.",
                "zh_hans": "每一段生命都是独一无二的故事，值得被永远铭记。一座专属的纪念碑不仅是标志，更是一处神圣的沉思之地，是对美好人生的永恒见证。",
                "zh_hant": "每一段生命都是獨一無二的故事，值得被永遠銘記。一座專屬的紀念碑不僅是標誌，更是一處神聖的沉思之地，是對美好人生的永恆見證。",
            },
            cta1_label={
                "en":      "Explore Our Stones",
                "zh_hans": "探索我们的石材",
                "zh_hant": "探索我們的石材",
            },
            cta1_url="/stone-catalogue",
            cta2_label={
                "en":      "Speak with Consultant",
                "zh_hans": "与顾问交谈",
                "zh_hant": "與顧問交談",
            },
            cta2_url="/booking",
        )
        self.stdout.write(self.style.SUCCESS("  ✓ HeroSection created."))

    def seed_products_heading(self, force):
        if ProductsSectionHeading.objects.exists() and not force:
            self.stdout.write("  ProductsSectionHeading exists — skipping.")
            return
        ProductsSectionHeading.objects.all().delete()
        ProductsSectionHeading.objects.create(
            headline={"en": "Our Products",               "zh_hans": "我们的产品",       "zh_hant": "我們的產品"},
            subtext= {"en": "A Selection of Recent Memorials", "zh_hans": "精选近期纪念品", "zh_hant": "精選近期紀念品"},
        )
        self.stdout.write(self.style.SUCCESS("  ✓ ProductsSectionHeading created."))

    def seed_featured_products(self, force):
        if FeaturedProduct.objects.exists() and not force:
            self.stdout.write("  FeaturedProducts exist — skipping.")
            return
        FeaturedProduct.objects.all().delete()
        products = [
            {
                "name":        {"en": "URN",                                          "zh_hans": "骨灰罐",              "zh_hant": "骨灰罈"},
                "description": {"en": "Exquisite urns with world-renowned engraving options, available in sleek onyx and porcelain.", "zh_hans": "精致骨灰罐，提供享誉世界的雕刻选项，有黑玉及瓷器款式可供选择。", "zh_hant": "精緻骨灰罈，提供享譽世界的雕刻選項，有黑玉及瓷器款式可供選擇。"},
                "order": 1,
            },
            {
                "name":        {"en": "Niche Stone Tablet",                           "zh_hans": "壁龛石碑",            "zh_hant": "壁龕石碑"},
                "description": {"en": "Timeless niche stone tablets with personalised custom-made designs crafted for the family directory.", "zh_hans": "永恒的壁龛石碑，为家族目录量身定制个性化设计。", "zh_hant": "永恆的壁龕石碑，為家族名錄量身定制個人化設計。"},
                "order": 2,
            },
            {
                "name":        {"en": "Special Colored Porcelain & Pictorial Tablets","zh_hans": "特色彩色瓷器及图案石碑","zh_hant": "特色彩色瓷器及圖案石碑"},
                "description": {"en": "Vivid personalised custom-made memorial options available in distinctive memorial designs.", "zh_hans": "生动的个性化定制纪念选项，提供独特的纪念设计。", "zh_hant": "生動的個人化訂製紀念選項，提供獨特的紀念設計。"},
                "order": 3,
            },
            {
                "name":        {"en": "Cemetery Gravestone / Burial Gravestone",      "zh_hans": "墓地墓碑 / 土葬墓碑", "zh_hant": "墓地墓碑 / 土葬墓碑"},
                "description": {"en": "Crafted for timeless permanence and refined elegance that define a traditional memorial headstone.", "zh_hans": "工艺精湛，历久弥新，优雅精致，彰显传统墓碑的经典风范。", "zh_hant": "工藝精湛，歷久彌新，優雅精緻，彰顯傳統墓碑的經典風範。"},
                "order": 4,
            },
            {
                "name":        {"en": "Huayong Family Columbarium",                  "zh_hans": "华雍家族纳骨塔",       "zh_hant": "華雍家族納骨塔"},
                "description": {"en": "Elegant family columbarium available in marble and granite, designed for private and shared use.", "zh_hans": "典雅的家族纳骨塔，以大理石及花岗岩制成，适合私人及共用用途。", "zh_hant": "典雅的家族納骨塔，以大理石及花崗岩製成，適合私人及共用用途。"},
                "order": 5,
            },
            {
                "name":        {"en": "Ash Scattering Memorial Monuments",            "zh_hans": "骨灰撒放纪念碑",       "zh_hant": "骨灰撒放紀念碑"},
                "description": {"en": "Beautifully designed and personalised ash scattering monuments with commemorative inscription.", "zh_hans": "设计精美的个性化骨灰撒放纪念碑，配有纪念铭文。", "zh_hant": "設計精美的個人化骨灰撒放紀念碑，配有紀念銘文。"},
                "order": 6,
            },
        ]
        for p in products:
            FeaturedProduct.objects.create(**p)
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(products)} FeaturedProducts created."))

    def seed_services(self, force):
        if ServicesSectionHeading.objects.exists() and not force:
            self.stdout.write("  ServicesSection exists — skipping.")
            return
        ServicesSectionHeading.objects.all().delete()
        heading = ServicesSectionHeading.objects.create(
            headline={"en": "Our Services",                                          "zh_hans": "我们的服务",          "zh_hant": "我們的服務"},
            subtext= {"en": "A Considered Path, From First Thought to Final Stone",  "zh_hans": "从最初构想到最终石材的周全历程", "zh_hant": "從最初構想到最終石材的周全歷程"},
        )
        steps = [
            {
                "title":       {"en": "Design a Gravestone",   "zh_hans": "设计墓碑",    "zh_hant": "設計墓碑"},
                "description": {"en": "Choose from our curated library of designs or let us craft a bespoke tribute that reflects a unique life.", "zh_hans": "从我们精心策划的设计库中选择，或让我们为您打造专属纪念碑，彰显独特的人生。", "zh_hant": "從我們精心策劃的設計庫中選擇，或讓我們為您打造專屬紀念碑，彰顯獨特的人生。"},
                "order": 1,
            },
            {
                "title":       {"en": "Choose Your Material",  "zh_hans": "选择材质",    "zh_hant": "選擇材質"},
                "description": {"en": "Select from premium granite, marble, and porcelain — each chosen for its beauty, durability, and meaning.", "zh_hans": "从优质花岗岩、大理石及瓷器中选择——每种材质均以其美观、耐用及含义而精选。", "zh_hant": "從優質花崗岩、大理石及瓷器中選擇——每種材質均以其美觀、耐用及含義而精選。"},
                "order": 2,
            },
            {
                "title":       {"en": "Add Engraving",         "zh_hans": "添加雕刻",    "zh_hant": "添加雕刻"},
                "description": {"en": "Personalise with inscriptions, portraits, and symbolic engravings in English, Chinese, or other scripts.", "zh_hans": "以英文、中文或其他文字，个性化添加铭文、肖像及象征性雕刻。", "zh_hant": "以英文、中文或其他文字，個人化添加銘文、肖像及象徵性雕刻。"},
                "order": 3,
            },
            {
                "title":       {"en": "Order Online",          "zh_hans": "网上订购",    "zh_hant": "網上訂購"},
                "description": {"en": "Submit your order securely and track production — we handle every detail with the utmost care and respect.", "zh_hans": "安全提交订单并追踪生产进度——我们以最高度的用心与尊重处理每一个细节。", "zh_hant": "安全提交訂單並追蹤生產進度——我們以最高度的用心與尊重處理每一個細節。"},
                "order": 4,
            },
        ]
        for s in steps:
            ServiceStep.objects.create(section=heading, **s)
        self.stdout.write(self.style.SUCCESS(f"  ✓ ServicesSection + {len(steps)} ServiceSteps created."))

    def seed_how_it_works(self, force):
        if HowItWorksHeading.objects.exists() and not force:
            self.stdout.write("  HowItWorksHeading exists — skipping.")
            return
        HowItWorksHeading.objects.all().delete()
        heading = HowItWorksHeading.objects.create(
            headline={"en": "How It Works",                        "zh_hans": "运作方式",          "zh_hant": "運作方式"},
            subtext= {"en": "Four Gentle Steps, Guided With Care", "zh_hans": "四个温柔步骤，贴心引导", "zh_hant": "四個溫柔步驟，貼心引導"},
        )
        steps = [
            {
                "step_number": 1,
                "title":       {"en": "Browse Stones",     "zh_hans": "浏览石材",   "zh_hant": "瀏覽石材"},
                "description": {"en": "Explore our curated range of memorial stones, urns, tablets, and columbarium options.", "zh_hans": "探索我们精心策划的纪念石材、骨灰罐、石碑及纳骨塔系列。", "zh_hant": "探索我們精心策劃的紀念石材、骨灰罈、石碑及納骨塔系列。"},
            },
            {
                "step_number": 2,
                "title":       {"en": "Customise Details", "zh_hans": "定制细节",   "zh_hant": "訂製細節"},
                "description": {"en": "Select your material, size, engraving text, portrait, and any special finishing details.", "zh_hans": "选择材质、尺寸、雕刻文字、肖像及任何特殊修饰细节。", "zh_hant": "選擇材質、尺寸、雕刻文字、肖像及任何特殊修飾細節。"},
            },
            {
                "step_number": 3,
                "title":       {"en": "Submit Order",      "zh_hans": "提交订单",   "zh_hant": "提交訂單"},
                "description": {"en": "Confirm your personalised order securely online — we'll review everything with you before production.", "zh_hans": "安全在线确认您的个性化订单——生产前我们将与您共同审核所有细节。", "zh_hant": "安全在線確認您的個人化訂單——生產前我們將與您共同審核所有細節。"},
            },
            {
                "step_number": 4,
                "title":       {"en": "Confirm & Deliver", "zh_hans": "确认并送达", "zh_hant": "確認並送達"},
                "description": {"en": "Once approved, we craft and deliver your memorial with full installation support where needed.", "zh_hans": "批准后，我们将精心制作并交付您的纪念碑，并在需要时提供全面的安装支持。", "zh_hant": "批准後，我們將精心製作並交付您的紀念碑，並在需要時提供全面的安裝支援。"},
            },
        ]
        for s in steps:
            HowItWorksStep.objects.create(section=heading, **s)
        self.stdout.write(self.style.SUCCESS(f"  ✓ HowItWorksHeading + {len(steps)} steps created."))

    def seed_stone_gallery(self, force):
        if StoneGallerySection.objects.exists() and not force:
            self.stdout.write("  StoneGallerySection exists — skipping.")
            return
        StoneGallerySection.objects.all().delete()
        StoneGallerySection.objects.create(
            headline=          {"en": "Our Stone Gallery",  "zh_hans": "石材展廊",  "zh_hant": "石材展廊"},
            subtext=           {"en": "A Selection of Recent Memorials", "zh_hans": "精选近期纪念作品", "zh_hant": "精選近期紀念作品"},
            explore_more_label={"en": "Explore More",       "zh_hans": "探索更多",  "zh_hant": "探索更多"},
            explore_more_url="/stone-catalogue",
        )
        self.stdout.write(self.style.SUCCESS("  ✓ StoneGallerySection created."))

    def seed_about_us(self, force):
        if AboutUsSection.objects.exists() and not force:
            self.stdout.write("  AboutUsSection exists — skipping.")
            return
        AboutUsSection.objects.all().delete()
        AboutUsSection.objects.create(
            headline={
                "en":      "About Us",
                "zh_hans": "关于我们",
                "zh_hant": "關於我們",
            },
            body_text={
                "en":      "At Stone Factory, We Specialise In Crafting Premium-Quality Unique Stone Products With Precision, Artistry, And Pride Of Design. With Years Of Experience In Stone Manufacturing, We Provide Custom Granite Solutions For A Wide Range Of Applications, Including Funeral Monuments, Landscaping, Interior Architecture, Decorative, And Constructions Applications.",
                "zh_hans": "在石材工厂，我们专注于以精准工艺、艺术匠心和设计自豪感，精心打造高品质独特石材产品。凭借多年的石材制造经验，我们为多种应用场景提供定制花岗岩解决方案，包括丧葬纪念碑、园林景观、室内建筑、装饰及建筑工程。",
                "zh_hant": "在石材工廠，我們專注於以精準工藝、藝術匠心和設計自豪感，精心打造高品質獨特石材產品。憑藉多年的石材製造經驗，我們為多種應用場景提供訂製花崗岩解決方案，包括喪葬紀念碑、園林景觀、室內建築、裝飾及建築工程。",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ AboutUsSection created."))

    def seed_faq(self, force):
        if FAQSection.objects.exists() and not force:
            self.stdout.write("  FAQSection exists — skipping.")
            return
        FAQSection.objects.all().delete()
        section = FAQSection.objects.create(
            headline={"en": "Frequently Asked Questions", "zh_hans": "常见问题", "zh_hant": "常見問題"}
        )
        faqs = [
            {
                "question": {"en": "What Types Of Granite Products Do You Manufacture?",   "zh_hans": "你们生产哪些类型的花岗岩产品？",   "zh_hant": "你們生產哪些類型的花崗岩產品？"},
                "answer":   {"en": "We manufacture a full range of granite memorial products including Gravestones, Burial Headstones, Niche Tablets, Landscaping, Wall Finishing, and Custom Designs.", "zh_hans": "我们生产各类花岗岩纪念产品，包括墓碑、土葬墓碑、壁龛石碑、园林景观、墙面装饰及定制设计。", "zh_hant": "我們生產各類花崗岩紀念產品，包括墓碑、土葬墓碑、壁龕石碑、園林景觀、牆面裝飾及訂製設計。"},
                "order": 1,
            },
            {
                "question": {"en": "Do You Offer Custom Stone Designs?",                   "zh_hans": "你们提供定制石材设计吗？",           "zh_hant": "你們提供訂製石材設計嗎？"},
                "answer":   {"en": "Yes. Every memorial can be fully customised — from the shape and material to the engraving, portrait etching, and finishing style.", "zh_hans": "是的。每件纪念品均可全面定制——从形状、材质到雕刻、肖像蚀刻及表面处理风格。", "zh_hant": "是的。每件紀念品均可全面訂製——從形狀、材質到雕刻、肖像蝕刻及表面處理風格。"},
                "order": 2,
            },
            {
                "question": {"en": "What Materials Do You Use?",                           "zh_hans": "你们使用哪些材料？",                 "zh_hant": "你們使用哪些材料？"},
                "answer":   {"en": "We work with premium granite, marble, porcelain, and specialist coloured stones, selected for durability, beauty, and suitability.", "zh_hans": "我们使用优质花岗岩、大理石、瓷器及特种彩色石材，以耐用性、美观性及适用性为选材标准。", "zh_hant": "我們使用優質花崗岩、大理石、瓷器及特種彩色石材，以耐用性、美觀性及適用性為選材標準。"},
                "order": 3,
            },
            {
                "question": {"en": "What Granite Finishes Are Available?",                 "zh_hans": "有哪些花岗岩表面处理选项？",          "zh_hant": "有哪些花崗岩表面處理選項？"},
                "answer":   {"en": "We offer polished, honed, flamed, sandblasted, and brushed finishes. Our team can guide you on what suits your memorial best.", "zh_hans": "我们提供抛光、研磨、火烧、喷砂及拉丝等表面处理。我们的团队将为您推荐最适合的处理方式。", "zh_hant": "我們提供拋光、研磨、火燒、噴砂及拉絲等表面處理。我們的團隊將為您推薦最適合的處理方式。"},
                "order": 4,
            },
            {
                "question": {"en": "How Durable Is Granite Stone?",                       "zh_hans": "花岗岩石材有多耐用？",               "zh_hant": "花崗岩石材有多耐用？"},
                "answer":   {"en": "Granite is one of the hardest natural stones, rated 6–7 on the Mohs scale. It is weather-resistant, UV-stable, and built to last generations.", "zh_hans": "花岗岩是最坚硬的天然石材之一，莫氏硬度为6至7。它具有耐候性、抗紫外线特性，经久耐用。", "zh_hant": "花崗岩是最堅硬的天然石材之一，莫氏硬度為6至7。它具有耐候性、抗紫外線特性，經久耐用。"},
                "order": 5,
            },
            {
                "question": {"en": "Do You Handle Bulk Or Commercial Orders?",             "zh_hans": "你们接受批量或商业订单吗？",          "zh_hant": "你們接受批量或商業訂單嗎？"},
                "answer":   {"en": "Yes. We welcome bulk orders for cemeteries, religious organisations, and memorial parks. Please contact us directly to discuss your requirements.", "zh_hans": "是的。我们欢迎墓地、宗教机构及纪念公园的批量订单。请直接联系我们，讨论您的具体需求。", "zh_hant": "是的。我們歡迎墓地、宗教機構及紀念公園的批量訂單。請直接聯繫我們，討論您的具體需求。"},
                "order": 6,
            },
        ]
        for f in faqs:
            FAQ.objects.create(section=section, **f)
        self.stdout.write(self.style.SUCCESS(f"  ✓ FAQSection + {len(faqs)} FAQs created."))

    def seed_testimonials(self, force):
        if TestimonialsSection.objects.exists() and not force:
            self.stdout.write("  TestimonialsSection exists — skipping.")
            return
        TestimonialsSection.objects.all().delete()
        section = TestimonialsSection.objects.create(
            headline={"en": "What Our Customers are saying?", "zh_hans": "客户怎么说？", "zh_hant": "客戶怎麼說？"},
            subtext= {"en": "",                               "zh_hans": "",             "zh_hant": ""},
        )
        testimonials = [
            {
                "customer_name": "Michael Thompson",
                "review_text": {
                    "en":      "The Craftsmanship And Detailing On The Granite Memorial Stone Exceeded Our Expectations. The Team Was Compassionate, Professional, And Delivered Exactly What We Envisioned.",
                    "zh_hans": "花岗岩纪念碑的工艺与细节超出了我们的期望。团队富有同情心、专业负责，完全实现了我们的设想。",
                    "zh_hant": "花崗岩紀念碑的工藝與細節超出了我們的期望。團隊富有同情心、專業負責，完全實現了我們的設想。",
                },
                "star_rating": 5, "order": 1,
            },
            {
                "customer_name": "Sarah Chen",
                "review_text": {
                    "en":      "From design to delivery, the entire process was smooth and respectful. The engraving detail on the niche tablet is absolutely beautiful.",
                    "zh_hans": "从设计到交付，整个过程顺畅而充满尊重。壁龛石碑上的雕刻细节美不胜收。",
                    "zh_hant": "從設計到交付，整個過程順暢而充滿尊重。壁龕石碑上的雕刻細節美不勝收。",
                },
                "star_rating": 5, "order": 2,
            },
            {
                "customer_name": "James O'Brien",
                "review_text": {
                    "en":      "Outstanding quality and a truly personalised service. The team guided us through every step with patience and professionalism.",
                    "zh_hans": "卓越的品质与真正个性化的服务。团队以耐心和专业精神引导我们走过每一步。",
                    "zh_hant": "卓越的品質與真正個人化的服務。團隊以耐心和專業精神引導我們走過每一步。",
                },
                "star_rating": 5, "order": 3,
            },
        ]
        for t in testimonials:
            Testimonial.objects.create(section=section, **t)
        self.stdout.write(self.style.SUCCESS(f"  ✓ TestimonialsSection + {len(testimonials)} Testimonials created."))