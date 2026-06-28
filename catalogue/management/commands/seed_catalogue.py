from django.core.management.base import BaseCommand
from catalogue.models import (
    CataloguePage, Category, Material,
    Product, ProductSize, ProductColor, ProductReview,
)


class Command(BaseCommand):
    help = "Seed Phase 3 Stone Catalogue data with multilingual support"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing data.")

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_page(force)
        materials = self.seed_materials(force)
        categories = self.seed_categories(force)
        self.seed_products(force, categories, materials)
        self.stdout.write(self.style.SUCCESS("\nPhase 3 Stone Catalogue data seeded successfully."))

    # ── Catalogue Page ────────────────────────────────────────────────────────

    def seed_page(self, force):
        if CataloguePage.objects.exists() and not force:
            self.stdout.write("  CataloguePage exists — skipping.")
            return
        CataloguePage.objects.all().delete()
        CataloguePage.objects.create(
            hero_title={
                "en":      "Find the Perfect Memorial Stone for Your Loved One",
                "zh_hans": "为您挚爱的人找到完美的纪念石材",
                "zh_hant": "為您摯愛的人找到完美的紀念石材",
            },
            hero_subtitle={
                "en":      "Crafted with care. Designed to last a lifetime.",
                "zh_hans": "精心制作，历久弥新。",
                "zh_hant": "精心製作，歷久彌新。",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ CataloguePage created."))

    # ── Materials ─────────────────────────────────────────────────────────────

    def seed_materials(self, force):
        if Material.objects.exists() and not force:
            self.stdout.write("  Materials exist — skipping.")
            return {m.slug: m for m in Material.objects.all()}

        Material.objects.all().delete()
        data = [
            {"slug": "black-granite",  "name": {"en": "Black Granite",  "zh_hans": "黑色花岗岩", "zh_hant": "黑色花崗岩"}},
            {"slug": "grey-granite",   "name": {"en": "Grey Granite",   "zh_hans": "灰色花岗岩", "zh_hant": "灰色花崗岩"}},
            {"slug": "red-granite",    "name": {"en": "Red Granite",    "zh_hans": "红色花岗岩", "zh_hant": "紅色花崗岩"}},
            {"slug": "white-marble",   "name": {"en": "White Marble",   "zh_hans": "白色大理石", "zh_hant": "白色大理石"}},
            {"slug": "green-marble",   "name": {"en": "Green Marble",   "zh_hans": "绿色大理石", "zh_hant": "綠色大理石"}},
            {"slug": "porcelain",      "name": {"en": "Porcelain",      "zh_hans": "瓷器",      "zh_hant": "瓷器"}},
            {"slug": "mixed-granite",  "name": {"en": "Mixed Granite",  "zh_hans": "混合花岗岩", "zh_hant": "混合花崗岩"}},
        ]
        materials = {}
        for d in data:
            m = Material.objects.create(**d)
            materials[m.slug] = m
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(data)} Materials created."))
        return materials

    # ── Categories ────────────────────────────────────────────────────────────

    def seed_categories(self, force):
        if Category.objects.exists() and not force:
            self.stdout.write("  Categories exist — skipping.")
            return {c.slug: c for c in Category.objects.all()}

        Category.objects.all().delete()
        data = [
            {
                "slug": "grave-stones", "order": 1,
                "name":        {"en": "Grave Stones",                              "zh_hans": "墓碑",           "zh_hant": "墓碑"},
                "description": {"en": "Traditional and contemporary gravestones crafted from premium granite and marble.", "zh_hans": "以优质花岗岩和大理石打造的传统及现代墓碑。", "zh_hant": "以優質花崗岩和大理石打造的傳統及現代墓碑。"},
            },
            {
                "slug": "urn", "order": 2,
                "name":        {"en": "URN",                                       "zh_hans": "骨灰罐",          "zh_hant": "骨灰罈"},
                "description": {"en": "Exquisite urns in granite, marble, and porcelain — designed for dignified remembrance.", "zh_hans": "以花岗岩、大理石和瓷器制成的精致骨灰罐，专为庄重的缅怀而设计。", "zh_hant": "以花崗岩、大理石和瓷器製成的精緻骨灰罈，專為莊重的緬懷而設計。"},
            },
            {
                "slug": "niche-stone-tablet", "order": 3,
                "name":        {"en": "Niche Stone Tablet",                        "zh_hans": "壁龛石碑",        "zh_hant": "壁龕石碑"},
                "description": {"en": "Personalised niche tablets for columbarium walls, available in a wide range of custom designs.", "zh_hans": "适用于纳骨墙的个性化壁龛石碑，提供多种定制设计。", "zh_hant": "適用於納骨牆的個人化壁龕石碑，提供多種訂製設計。"},
            },
            {
                "slug": "special-colored-porcelain-pictorial-tablets", "order": 4,
                "name":        {"en": "Special Colored Porcelain & Pictorial Tablets", "zh_hans": "特色彩色瓷器及图案石碑", "zh_hant": "特色彩色瓷器及圖案石碑"},
                "description": {"en": "Vivid full-colour porcelain tablets with photo-realistic pictorial designs and custom inscriptions.", "zh_hans": "鲜艳的全彩瓷板，配有逼真的图案设计和定制铭文。", "zh_hant": "鮮艷的全彩瓷板，配有逼真的圖案設計和訂製銘文。"},
            },
            {
                "slug": "huayonghui-family-columbarium", "order": 5,
                "name":        {"en": "Huayonghui — Family Columbarium",           "zh_hans": "华雍会 — 家族纳骨塔", "zh_hant": "華雍會 — 家族納骨塔"},
                "description": {"en": "Premium family columbarium units in marble and granite, crafted for generations of remembrance.", "zh_hans": "以大理石和花岗岩精制的高级家族纳骨塔，为世代的缅怀而设计。", "zh_hant": "以大理石和花崗岩精製的高級家族納骨塔，為世代的緬懷而設計。"},
            },
            {
                "slug": "ash-monument", "order": 6,
                "name":        {"en": "Ash Monument",                              "zh_hans": "骨灰纪念碑",       "zh_hant": "骨灰紀念碑"},
                "description": {"en": "Dedicated ash scattering monuments and memorial stones for outdoor and garden settings.", "zh_hans": "适用于户外及花园场景的专用骨灰撒放纪念碑和纪念石。", "zh_hant": "適用於戶外及花園場景的專用骨灰撒放紀念碑和紀念石。"},
            },
        ]
        categories = {}
        for d in data:
            c = Category.objects.create(**d)
            categories[c.slug] = c
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(data)} Categories created."))
        return categories

    # ── Products ──────────────────────────────────────────────────────────────

    def seed_products(self, force, categories, materials):
        if Product.objects.exists() and not force:
            self.stdout.write("  Products exist — skipping.")
            return

        Product.objects.all().delete()

        shipping = {
            "en":      "Free shipping to Hong Kong. Estimated delivery: 4–6 weeks after order confirmation. Installation service available upon request.",
            "zh_hans": "香港免费送货。预计交货时间：订单确认后4至6周。可应要求提供安装服务。",
            "zh_hant": "香港免費送貨。預計交貨時間：訂單確認後4至6週。可應要求提供安裝服務。",
        }

        products_data = [

            # ── GRAVE STONES ──────────────────────────────────────────────────
            {
                "slug": "napoleon-minimum-estate-columbarium",
                "category": "grave-stones", "material": "black-granite",
                "price": 38000, "is_featured": True, "is_new": True,
                "name": {"en": "Napoleon Minimum Estate Columbarium",    "zh_hans": "拿破仑极简纳骨塔",   "zh_hant": "拿破崙極簡納骨塔"},
                "short_description": {"en": "A bold minimalist gravestone in polished black granite with classic engraving.",    "zh_hans": "以抛光黑色花岗岩制成的大胆极简主义墓碑，配有经典雕刻。", "zh_hant": "以拋光黑色花崗岩製成的大膽極簡主義墓碑，配有經典雕刻。"},
                "full_description":  {"en": "The Napoleon Minimum Estate Columbarium combines contemporary minimalism with the timeless gravitas of polished black granite. Its sleek form makes it suitable for both traditional cemetery settings and modern memorial gardens. Custom engraving available in English, Chinese, and Hebrew.", "zh_hans": "拿破仑极简纳骨塔将现代极简主义与抛光黑色花岗岩的永恒庄重感融为一体。其简洁的造型使其适用于传统墓地和现代纪念花园。可提供英文、中文和希伯来文的定制雕刻。", "zh_hant": "拿破崙極簡納骨塔將現代極簡主義與拋光黑色花崗岩的永恆莊重感融為一體。其簡潔的造型使其適用於傳統墓地和現代紀念花園。可提供英文、中文和希伯來文的訂製雕刻。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 100×50 cm", "zh_hans": "标准 / 100×50 厘米", "zh_hant": "標準 / 100×50 厘米"}, "dimensions": "100 x 50 cm", "price_modifier": 0,     "is_default": True,  "order": 1},
                    {"label": {"en": "Large / 150×60 cm",    "zh_hans": "大号 / 150×60 厘米",  "zh_hant": "大號 / 150×60 厘米"},  "dimensions": "150 x 60 cm", "price_modifier": 8000,  "is_default": False, "order": 2},
                    {"label": {"en": "XLarge / 200×70 cm",   "zh_hans": "加大 / 200×70 厘米",  "zh_hant": "加大 / 200×70 厘米"},  "dimensions": "200 x 70 cm", "price_modifier": 15000, "is_default": False, "order": 3},
                ],
                "colors": [
                    {"name": {"en": "Polished Black", "zh_hans": "抛光黑色", "zh_hant": "拋光黑色"}, "hex_code": "#1a1a1a", "is_default": True,  "order": 1},
                    {"name": {"en": "Honed Black",    "zh_hans": "研磨黑色", "zh_hant": "研磨黑色"}, "hex_code": "#2d2d2d", "is_default": False, "order": 2},
                ],
                "reviews": [
                    {"customer_name": "David Lam", "star_rating": 5, "review_text": {"en": "Exceptional quality. The engraving was precise and beautifully done.", "zh_hans": "品质卓越，雕刻精准美观。", "zh_hant": "品質卓越，雕刻精準美觀。"}},
                ],
            },
            {
                "slug": "imperishable-endure-ancestral-marker",
                "category": "grave-stones", "material": "red-granite",
                "price": 42000,
                "name": {"en": "Imperishable Endure Ancestral Marker",  "zh_hans": "永存先祖纪念碑",   "zh_hant": "永存先祖紀念碑"},
                "short_description": {"en": "A distinguished ancestral marker in deep red granite with traditional motifs.", "zh_hans": "以深红色花岗岩制成的杰出祖先纪念碑，配有传统图案。", "zh_hant": "以深紅色花崗岩製成的傑出祖先紀念碑，配有傳統圖案。"},
                "full_description":  {"en": "The Imperishable Endure Ancestral Marker is crafted from rare deep red granite, symbolising enduring love and familial respect. Traditional Chinese and Western motifs can be combined in the engraving design.", "zh_hans": "永存先祖纪念碑由罕见的深红色花岗岩精制而成，象征永恒的爱与家族的尊重。传统中西图案可融入雕刻设计之中。", "zh_hant": "永存先祖紀念碑由罕見的深紅色花崗岩精製而成，象徵永恆的愛與家族的尊重。傳統中西圖案可融入雕刻設計之中。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 120×55 cm", "zh_hans": "标准 / 120×55 厘米", "zh_hant": "標準 / 120×55 厘米"}, "dimensions": "120 x 55 cm", "price_modifier": 0,    "is_default": True,  "order": 1},
                    {"label": {"en": "Large / 160×65 cm",    "zh_hans": "大号 / 160×65 厘米",  "zh_hant": "大號 / 160×65 厘米"},  "dimensions": "160 x 65 cm", "price_modifier": 9000, "is_default": False, "order": 2},
                ],
                "colors": [
                    {"name": {"en": "Deep Red", "zh_hans": "深红色", "zh_hant": "深紅色"}, "hex_code": "#8B0000", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },
            {
                "slug": "serenity-granite-garden",
                "category": "grave-stones", "material": "grey-granite",
                "price": 29000, "is_new": True,
                "name": {"en": "Serenity Granite Garden",               "zh_hans": "宁静花岗岩花园",    "zh_hant": "寧靜花崗岩花園"},
                "short_description": {"en": "A serene garden-style gravestone in grey granite with floral relief carving.", "zh_hans": "以灰色花岗岩制成的宁静花园风格墓碑，配有花卉浮雕。", "zh_hant": "以灰色花崗岩製成的寧靜花園風格墓碑，配有花卉浮雕。"},
                "full_description":  {"en": "The Serenity Granite Garden gravestone brings a peaceful garden aesthetic to memorial commemoration. The delicate floral relief is hand-carved and can be customised with the flower of your choice.", "zh_hans": "宁静花岗岩花园墓碑为纪念活动带来宁静的花园美感。精致的花卉浮雕经手工雕刻，可根据您的选择定制花卉图案。", "zh_hant": "寧靜花崗岩花園墓碑為紀念活動帶來寧靜的花園美感。精緻的花卉浮雕經手工雕刻，可根據您的選擇訂製花卉圖案。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 90×45 cm", "zh_hans": "标准 / 90×45 厘米", "zh_hant": "標準 / 90×45 厘米"}, "dimensions": "90 x 45 cm", "price_modifier": 0, "is_default": True, "order": 1},
                ],
                "colors": [
                    {"name": {"en": "Pearl Grey", "zh_hans": "珍珠灰", "zh_hant": "珍珠灰"}, "hex_code": "#b0b0b0", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },

            # ── URN ───────────────────────────────────────────────────────────
            {
                "slug": "jade-moonstone-classique-urn",
                "category": "urn", "material": "green-marble",
                "price": 12000, "is_featured": True,
                "name": {"en": "Jade Moonstone Classique",              "zh_hans": "玉石月光经典骨灰罐",  "zh_hant": "玉石月光經典骨灰罈"},
                "short_description": {"en": "An elegant jade-toned urn with moonstone finish, ideal for columbarium niches.", "zh_hans": "优雅的玉色骨灰罐，配有月光石饰面，适合壁龛安放。", "zh_hant": "優雅的玉色骨灰罈，配有月光石飾面，適合壁龕安放。"},
                "full_description":  {"en": "The Jade Moonstone Classique urn is handcrafted from premium green marble with a lustrous moonstone surface treatment. Its timeless form is inspired by classical Chinese vessel design, blending heritage with modern refinement.", "zh_hans": "玉石月光经典骨灰罐由优质绿色大理石精制而成，表面经过光泽月光石处理。其永恒的造型灵感源自中国古典器皿设计，将传统与现代精致融为一体。", "zh_hant": "玉石月光經典骨灰罈由優質綠色大理石精製而成，表面經過光澤月光石處理。其永恆的造型靈感源自中國古典器皿設計，將傳統與現代精緻融為一體。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Small (up to 1L)",   "zh_hans": "小号（最多1升）",  "zh_hant": "小號（最多1升）"},  "dimensions": "15 x 10 cm", "price_modifier": 0,    "is_default": False, "order": 1},
                    {"label": {"en": "Standard (up to 3L)","zh_hans": "标准（最多3升）",  "zh_hant": "標準（最多3升）"},  "dimensions": "22 x 14 cm", "price_modifier": 2000,  "is_default": True,  "order": 2},
                    {"label": {"en": "Large (up to 5L)",   "zh_hans": "大号（最多5升）",  "zh_hant": "大號（最多5升）"},  "dimensions": "28 x 18 cm", "price_modifier": 4000,  "is_default": False, "order": 3},
                ],
                "colors": [
                    {"name": {"en": "Jade Green",   "zh_hans": "玉绿色", "zh_hant": "玉綠色"}, "hex_code": "#5a7a5a", "is_default": True,  "order": 1},
                    {"name": {"en": "Onyx Black",   "zh_hans": "缟玛瑙黑", "zh_hant": "縞瑪瑙黑"}, "hex_code": "#1c1c1c", "is_default": False, "order": 2},
                    {"name": {"en": "Ivory White",  "zh_hans": "象牙白", "zh_hant": "象牙白"},  "hex_code": "#f5f0e8", "is_default": False, "order": 3},
                ],
                "reviews": [
                    {"customer_name": "Agnes Yuen", "star_rating": 5, "review_text": {"en": "Beautiful craftsmanship. The jade finish is exactly as pictured.", "zh_hans": "工艺精美，玉石饰面与图片完全一致。", "zh_hant": "工藝精美，玉石飾面與圖片完全一致。"}},
                ],
            },
            {
                "slug": "golden-ember-fleur-urn",
                "category": "urn", "material": "mixed-granite",
                "price": 15500, "is_sale": True, "sale_price": 12800,
                "name": {"en": "Golden Ember Fleur Urn",                "zh_hans": "金色炽焰花卉骨灰罐", "zh_hant": "金色熾焰花卉骨灰罈"},
                "short_description": {"en": "A warm golden-toned urn with hand-carved floral motifs and a polished finish.", "zh_hans": "温暖金色调骨灰罐，配有手工雕刻花卉图案及抛光饰面。", "zh_hant": "溫暖金色調骨灰罈，配有手工雕刻花卉圖案及拋光飾面。"},
                "full_description":  {"en": "The Golden Ember Fleur Urn features intricate hand-carved floral reliefs set against a warm amber granite body. Available in three sizes, it is suitable for indoor display or columbarium placement.", "zh_hans": "金色炽焰花卉骨灰罐以精美的手工花卉浮雕为特色，衬托于温暖琥珀色花岗岩罐身上。提供三种尺寸，适用于室内展示或壁龛安放。", "zh_hant": "金色熾焰花卉骨灰罈以精美的手工花卉浮雕為特色，襯托於溫暖琥珀色花崗岩罈身上。提供三種尺寸，適用於室內展示或壁龕安放。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard (up to 3L)", "zh_hans": "标准（最多3升）", "zh_hant": "標準（最多3升）"}, "dimensions": "24 x 15 cm", "price_modifier": 0, "is_default": True, "order": 1},
                ],
                "colors": [
                    {"name": {"en": "Golden Amber", "zh_hans": "金色琥珀", "zh_hant": "金色琥珀"}, "hex_code": "#c8a96e", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },
            {
                "slug": "imperial-topaz-stone-jade-urn",
                "category": "urn", "material": "green-marble",
                "price": 18000,
                "name": {"en": "Imperial Topaz Stone Jade Urn",         "zh_hans": "帝王黄玉石骨灰罐",  "zh_hant": "帝王黃玉石骨灰罈"},
                "short_description": {"en": "A majestic imperial-style urn combining topaz stone and jade for regal tribute.", "zh_hans": "雄伟的帝王风格骨灰罐，融合黄玉石和玉石，打造尊贵的致敬。", "zh_hant": "雄偉的帝王風格骨灰罈，融合黃玉石和玉石，打造尊貴的致敬。"},
                "full_description":  {"en": "Inspired by imperial Chinese ceramics, the Imperial Topaz Stone Jade Urn combines natural topaz stone accents with a jade body. Each piece is individually crafted and no two are identical.", "zh_hans": "灵感源自中国皇家陶瓷，帝王黄玉石骨灰罐融合天然黄玉石点缀与玉石罐身。每件均为独立制作，独一无二。", "zh_hant": "靈感源自中國皇家陶瓷，帝王黃玉石骨灰罈融合天然黃玉石點綴與玉石罈身。每件均為獨立製作，獨一無二。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard (up to 3L)", "zh_hans": "标准（最多3升）", "zh_hant": "標準（最多3升）"}, "dimensions": "25 x 16 cm", "price_modifier": 0, "is_default": True, "order": 1},
                ],
                "colors": [
                    {"name": {"en": "Topaz & Jade", "zh_hans": "黄玉与玉石", "zh_hant": "黃玉與玉石"}, "hex_code": "#8B7355", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },

            # ── NICHE STONE TABLET ────────────────────────────────────────────
            {
                "slug": "floral-serenity-memorial-tablet",
                "category": "niche-stone-tablet", "material": "white-marble",
                "price": 8800, "is_featured": True,
                "name": {"en": "Floral Serenity Memorial Tablet",       "zh_hans": "花卉宁静纪念石碑",  "zh_hant": "花卉寧靜紀念石碑"},
                "short_description": {"en": "A delicate white marble niche tablet with floral border engraving and portrait space.", "zh_hans": "精致的白色大理石壁龛石碑，配有花卉边框雕刻和肖像空间。", "zh_hant": "精緻的白色大理石壁龕石碑，配有花卉邊框雕刻和肖像空間。"},
                "full_description":  {"en": "The Floral Serenity Memorial Tablet is carved from premium white marble and features an ornate floral border surrounding a central portrait panel. Text engraving is available in English, Traditional Chinese, and Simplified Chinese.", "zh_hans": "花卉宁静纪念石碑由优质白色大理石雕刻而成，以华丽的花卉边框环绕中央肖像面板为特色。可提供英文、繁体中文和简体中文的文字雕刻。", "zh_hant": "花卉寧靜紀念石碑由優質白色大理石雕刻而成，以華麗的花卉邊框環繞中央肖像面板為特色。可提供英文、繁體中文和簡體中文的文字雕刻。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Small / 30×20 cm",   "zh_hans": "小号 / 30×20 厘米",  "zh_hant": "小號 / 30×20 厘米"},  "dimensions": "30 x 20 cm", "price_modifier": 0,    "is_default": False, "order": 1},
                    {"label": {"en": "Standard / 40×30 cm","zh_hans": "标准 / 40×30 厘米",  "zh_hant": "標準 / 40×30 厘米"},  "dimensions": "40 x 30 cm", "price_modifier": 1500,  "is_default": True,  "order": 2},
                    {"label": {"en": "Large / 50×40 cm",   "zh_hans": "大号 / 50×40 厘米",  "zh_hant": "大號 / 50×40 厘米"},  "dimensions": "50 x 40 cm", "price_modifier": 3000,  "is_default": False, "order": 3},
                ],
                "colors": [
                    {"name": {"en": "White Marble",  "zh_hans": "白色大理石", "zh_hant": "白色大理石"}, "hex_code": "#f5f5f0", "is_default": True,  "order": 1},
                    {"name": {"en": "Cream Marble",  "zh_hans": "奶油大理石", "zh_hant": "奶油大理石"}, "hex_code": "#f0ead2", "is_default": False, "order": 2},
                ],
                "reviews": [
                    {"customer_name": "Linda Ho", "star_rating": 5, "review_text": {"en": "The floral carving is exquisite. Exactly what we hoped for our mother.", "zh_hans": "花卉雕刻精美绝伦，正是我们为母亲所期望的。", "zh_hant": "花卉雕刻精美絕倫，正是我們為母親所期望的。"}},
                ],
            },
            {
                "slug": "stone-relief-monument-tablet",
                "category": "niche-stone-tablet", "material": "grey-granite",
                "price": 6500,
                "name": {"en": "Stone Relief Monument Tablet",          "zh_hans": "石材浮雕纪念石碑",  "zh_hant": "石材浮雕紀念石碑"},
                "short_description": {"en": "A classic granite niche tablet with raised stone relief design and text panel.", "zh_hans": "经典花岗岩壁龛石碑，配有凸起的石材浮雕设计和文字面板。", "zh_hant": "經典花崗岩壁龕石碑，配有凸起的石材浮雕設計和文字面板。"},
                "full_description":  {"en": "The Stone Relief Monument Tablet combines traditional memorial design with modern craftsmanship. The raised relief panel can feature religious symbols, landscapes, or portrait engravings.", "zh_hans": "石材浮雕纪念石碑将传统纪念设计与现代工艺相结合。凸起的浮雕面板可呈现宗教符号、风景或肖像雕刻。", "zh_hant": "石材浮雕紀念石碑將傳統紀念設計與現代工藝相結合。凸起的浮雕面板可呈現宗教符號、風景或肖像雕刻。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 40×30 cm", "zh_hans": "标准 / 40×30 厘米", "zh_hant": "標準 / 40×30 厘米"}, "dimensions": "40 x 30 cm", "price_modifier": 0, "is_default": True, "order": 1},
                ],
                "colors": [
                    {"name": {"en": "Charcoal Grey", "zh_hans": "木炭灰", "zh_hant": "木炭灰"}, "hex_code": "#555555", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },

            # ── SPECIAL COLORED PORCELAIN ─────────────────────────────────────
            {
                "slug": "huayongkai-special-coloured-porcelain-slate-classic",
                "category": "special-colored-porcelain-pictorial-tablets", "material": "porcelain",
                "price": 9500, "is_featured": True, "is_new": True,
                "name": {"en": "Huayongkai Special Coloured Porcelain Slate — Classic",  "zh_hans": "华雍楷特色彩色瓷板 — 经典款", "zh_hant": "華雍楷特色彩色瓷板 — 經典款"},
                "short_description": {"en": "Full-colour porcelain memorial slate with photographic portrait and custom Chinese calligraphy.", "zh_hans": "全彩瓷器纪念石板，配有摄影肖像和定制中文书法。", "zh_hant": "全彩瓷器紀念石板，配有攝影肖像和訂製中文書法。"},
                "full_description":  {"en": "The Huayongkai Special Coloured Porcelain Slate uses high-temperature kiln-fired porcelain with photographic-quality colour printing. The portrait and calligraphy are fired into the surface — completely weatherproof and fade-resistant for outdoor use.", "zh_hans": "华雍楷特色彩色瓷板采用高温窑烧瓷器，具有摄影级彩色印刷质量。肖像和书法烧制于表面——完全防风雨，户外使用不褪色。", "zh_hant": "華雍楷特色彩色瓷板採用高溫窯燒瓷器，具有攝影級彩色印刷質量。肖像和書法燒製於表面——完全防風雨，戶外使用不褪色。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 35×25 cm", "zh_hans": "标准 / 35×25 厘米", "zh_hant": "標準 / 35×25 厘米"}, "dimensions": "35 x 25 cm", "price_modifier": 0,    "is_default": True,  "order": 1},
                    {"label": {"en": "Large / 45×35 cm",    "zh_hans": "大号 / 45×35 厘米",  "zh_hant": "大號 / 45×35 厘米"},  "dimensions": "45 x 35 cm", "price_modifier": 2500,  "is_default": False, "order": 2},
                ],
                "colors": [
                    {"name": {"en": "Full Colour", "zh_hans": "全彩", "zh_hant": "全彩"}, "hex_code": "", "is_default": True, "order": 1},
                ],
                "reviews": [
                    {"customer_name": "Helen Ng", "star_rating": 5, "review_text": {"en": "The colours are vibrant and the portrait looks incredibly lifelike.", "zh_hans": "色彩鲜艳，肖像栩栩如生。", "zh_hant": "色彩鮮艷，肖像栩栩如生。"}},
                ],
            },

            # ── HUAYONGHUI FAMILY COLUMBARIUM ────────────────────────────────
            {
                "slug": "sapphire-shimmer-estate-columbarium",
                "category": "huayonghui-family-columbarium", "material": "black-granite",
                "price": 52000, "is_featured": True,
                "name": {"en": "Sapphire Shimmer Estate Columbarium",   "zh_hans": "蓝宝石光华庄园纳骨塔", "zh_hant": "藍寶石光華莊園納骨塔"},
                "short_description": {"en": "A premium family columbarium in polished black granite with sapphire-tone mosaic inlay.", "zh_hans": "以抛光黑色花岗岩制成的高级家族纳骨塔，配有蓝宝石色调马赛克镶嵌。", "zh_hant": "以拋光黑色花崗岩製成的高級家族納骨塔，配有藍寶石色調馬賽克鑲嵌。"},
                "full_description":  {"en": "The Sapphire Shimmer Estate Columbarium is a landmark family memorial piece, designed to hold multiple urns across generations. Its polished black granite body features hand-set sapphire-coloured glass mosaic panels. Available with 2, 4, or 6 niche compartments.", "zh_hans": "蓝宝石光华庄园纳骨塔是一件标志性的家族纪念作品，专为跨代安放多个骨灰罐而设计。其抛光黑色花岗岩罐身配有手工镶嵌的蓝宝石色玻璃马赛克面板。提供2个、4个或6个壁龛格。", "zh_hant": "藍寶石光華莊園納骨塔是一件標誌性的家族紀念作品，專為跨代安放多個骨灰罈而設計。其拋光黑色花崗岩罈身配有手工鑲嵌的藍寶石色玻璃馬賽克面板。提供2個、4個或6個壁龕格。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "2 Niches",  "zh_hans": "2个壁龛",  "zh_hant": "2個壁龕"},  "dimensions": "80 x 60 x 40 cm",  "price_modifier": 0,      "is_default": False, "order": 1},
                    {"label": {"en": "4 Niches",  "zh_hans": "4个壁龛",  "zh_hant": "4個壁龕"},  "dimensions": "120 x 80 x 40 cm", "price_modifier": 18000,  "is_default": True,  "order": 2},
                    {"label": {"en": "6 Niches",  "zh_hans": "6个壁龛",  "zh_hant": "6個壁龕"},  "dimensions": "160 x 90 x 40 cm", "price_modifier": 36000,  "is_default": False, "order": 3},
                ],
                "colors": [
                    {"name": {"en": "Sapphire Black", "zh_hans": "蓝宝石黑色", "zh_hant": "藍寶石黑色"}, "hex_code": "#0d1b2a", "is_default": True,  "order": 1},
                    {"name": {"en": "Emerald Black",  "zh_hans": "祖母绿黑色", "zh_hant": "祖母綠黑色"}, "hex_code": "#0d2a1b", "is_default": False, "order": 2},
                ],
                "reviews": [
                    {"customer_name": "Robert Chan", "star_rating": 5, "review_text": {"en": "A truly stunning piece. Our family is honoured to have this as our memorial centrepiece.", "zh_hans": "真是令人叹为观止的作品。我们家族以此作为纪念中心感到无比荣幸。", "zh_hant": "真是令人嘆為觀止的作品。我們家族以此作為紀念中心感到無比榮幸。"}},
                ],
            },

            # ── ASH MONUMENT ─────────────────────────────────────────────────
            {
                "slug": "huayongkai-ash-memorial-monument-classic",
                "category": "ash-monument", "material": "grey-granite",
                "price": 22000,
                "name": {"en": "Huayongkai Ash Memorial Monument — Classic",  "zh_hans": "华雍楷骨灰纪念碑 — 经典款", "zh_hant": "華雍楷骨灰紀念碑 — 經典款"},
                "short_description": {"en": "A solid granite ash monument with inscribed memorial plaque and garden placement base.", "zh_hans": "坚固的花岗岩骨灰纪念碑，配有铭文纪念牌匾和花园放置底座。", "zh_hant": "堅固的花崗岩骨灰紀念碑，配有銘文紀念牌匾和花園放置底座。"},
                "full_description":  {"en": "The Huayongkai Ash Memorial Monument is designed for garden or outdoor memorial settings. The polished grey granite column features a recessed bronze plaque mount and a wide stability base. Suitable for ash scattering ceremonies and permanent placement.", "zh_hans": "华雍楷骨灰纪念碑专为花园或户外纪念场所而设计。抛光灰色花岗岩柱体配有嵌入式青铜牌匾托架和宽大的稳固底座。适用于骨灰撒放仪式和永久安放。", "zh_hant": "華雍楷骨灰紀念碑專為花園或戶外紀念場所而設計。拋光灰色花崗岩柱體配有嵌入式青銅牌匾托架和寬大的穩固底座。適用於骨灰撒放儀式和永久安放。"},
                "shipping_info": shipping,
                "sizes": [
                    {"label": {"en": "Standard / 80 cm height", "zh_hans": "标准 / 高80厘米", "zh_hant": "標準 / 高80厘米"}, "dimensions": "80 x 30 x 30 cm",  "price_modifier": 0,    "is_default": True,  "order": 1},
                    {"label": {"en": "Tall / 120 cm height",    "zh_hans": "高款 / 高120厘米", "zh_hant": "高款 / 高120厘米"}, "dimensions": "120 x 35 x 35 cm", "price_modifier": 8000,  "is_default": False, "order": 2},
                ],
                "colors": [
                    {"name": {"en": "Polished Grey", "zh_hans": "抛光灰色", "zh_hant": "拋光灰色"}, "hex_code": "#888888", "is_default": True, "order": 1},
                ],
                "reviews": [],
            },
        ]

        count = 0
        for p in products_data:
            sizes_data = p.pop("sizes", [])
            colors_data = p.pop("colors", [])
            reviews_data = p.pop("reviews", [])
            cat_slug = p.pop("category")
            mat_slug = p.pop("material")

            product = Product.objects.create(
                category=categories[cat_slug],
                material=materials.get(mat_slug),
                **p,
            )
            for s in sizes_data:
                ProductSize.objects.create(product=product, **s)
            for c in colors_data:
                ProductColor.objects.create(product=product, **c)
            for r in reviews_data:
                ProductReview.objects.create(product=product, **r)
            count += 1

        self.stdout.write(self.style.SUCCESS(f"  ✓ {count} Products created with sizes, colors, and reviews."))