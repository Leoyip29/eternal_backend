from django.core.management.base import BaseCommand
from portfolio.models import OurWorkPage, WorkCategory, WorkItem


class Command(BaseCommand):
    help = "Seed Phase 4 Our Work Portfolio data with multilingual support"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing data.")

    def handle(self, *args, **kwargs):
        force = kwargs["force"]
        self.seed_page(force)
        categories = self.seed_categories(force)
        self.seed_work_items(force, categories)
        self.stdout.write(self.style.SUCCESS("\nPhase 4 Our Work Portfolio data seeded successfully."))

    # ── Page Header ───────────────────────────────────────────────────────────

    def seed_page(self, force):
        if OurWorkPage.objects.exists() and not force:
            self.stdout.write("  OurWorkPage exists — skipping.")
            return
        OurWorkPage.objects.all().delete()
        OurWorkPage.objects.create(
            title={
                "en":      "Our Work",
                "zh_hans": "我们的作品",
                "zh_hant": "我們的作品",
            },
            subtitle={
                "en":      "Our Collection of Blessed Memorials",
                "zh_hans": "我们的神圣纪念作品集",
                "zh_hant": "我們的神聖紀念作品集",
            },
        )
        self.stdout.write(self.style.SUCCESS("  ✓ OurWorkPage created."))

    # ── Work Categories ───────────────────────────────────────────────────────

    def seed_categories(self, force):
        if WorkCategory.objects.exists() and not force:
            self.stdout.write("  WorkCategories exist — skipping.")
            return {c.slug: c for c in WorkCategory.objects.all()}

        WorkCategory.objects.all().delete()
        data = [
            {
                "slug": "christian-companion", "order": 1,
                "name": {
                    "en":      "Christian Companion",
                    "zh_hans": "基督教伴侣墓",
                    "zh_hant": "基督教伴侶墓",
                },
            },
            {
                "slug": "jewish-companion", "order": 2,
                "name": {
                    "en":      "Jewish Companion",
                    "zh_hans": "犹太教伴侣墓",
                    "zh_hant": "猶太教伴侶墓",
                },
            },
            {
                "slug": "asian-chinese-grave", "order": 3,
                "name": {
                    "en":      "Asian / Chinese Grave",
                    "zh_hans": "亚洲 / 中式墓地",
                    "zh_hant": "亞洲 / 中式墓地",
                },
            },
            {
                "slug": "italian-grave", "order": 4,
                "name": {
                    "en":      "Italian Grave",
                    "zh_hans": "意大利式墓地",
                    "zh_hant": "意大利式墓地",
                },
            },
        ]
        categories = {}
        for d in data:
            c = WorkCategory.objects.create(**d)
            categories[c.slug] = c
        self.stdout.write(self.style.SUCCESS(f"  ✓ {len(data)} WorkCategories created."))
        return categories

    # ── Work Items ────────────────────────────────────────────────────────────

    def seed_work_items(self, force, categories):
        if WorkItem.objects.exists() and not force:
            self.stdout.write("  WorkItems exist — skipping.")
            return

        WorkItem.objects.all().delete()

        items_data = [

            # ── Christian Companion ───────────────────────────────────────────
            {
                "category": "christian-companion", "order": 1,
                "title": {
                    "en":      "Classic Cross Heritage Stone",
                    "zh_hans": "经典十字架传承墓石",
                    "zh_hant": "經典十字架傳承墓石",
                },
                "description": {
                    "en":      "A polished black granite companion gravestone featuring a hand-carved raised cross and personalised inscription panels on both sides.",
                    "zh_hans": "抛光黑色花岗岩伴侣墓碑，配有手工雕刻凸起十字架及双面个性化铭文面板。",
                    "zh_hant": "拋光黑色花崗岩伴侶墓碑，配有手工雕刻凸起十字架及雙面個人化銘文面板。",
                },
            },
            {
                "category": "christian-companion", "order": 2,
                "title": {
                    "en":      "Garden Cross Companion Memorial",
                    "zh_hans": "花园十字架伴侣纪念碑",
                    "zh_hant": "花園十字架伴侶紀念碑",
                },
                "description": {
                    "en":      "A garden-style companion memorial in grey granite with a decorative floral cross motif and dual name panels surrounded by natural stone landscaping.",
                    "zh_hans": "灰色花岗岩花园风格伴侣纪念碑，配有装饰性花卉十字架图案及双名铭文面板，周围以天然石材景观衬托。",
                    "zh_hant": "灰色花崗岩花園風格伴侶紀念碑，配有裝飾性花卉十字架圖案及雙名銘文面板，周圍以天然石材景觀襯托。",
                },
            },
            {
                "category": "christian-companion", "order": 3,
                "title": {
                    "en":      "White Marble Arch Companion",
                    "zh_hans": "白色大理石拱形伴侣墓碑",
                    "zh_hant": "白色大理石拱形伴侶墓碑",
                },
                "description": {
                    "en":      "An elegant arched white marble companion gravestone with gold-leaf letter engraving and a carved dove motif above the inscription.",
                    "zh_hans": "典雅的拱形白色大理石伴侣墓碑，配有金叶文字雕刻及铭文上方的鸽子图案。",
                    "zh_hant": "典雅的拱形白色大理石伴侶墓碑，配有金葉文字雕刻及銘文上方的鴿子圖案。",
                },
            },
            {
                "category": "christian-companion", "order": 4,
                "title": {
                    "en":      "Dark Granite Pillar Companion",
                    "zh_hans": "深色花岗岩柱形伴侣墓碑",
                    "zh_hant": "深色花崗岩柱形伴侶墓碑",
                },
                "description": {
                    "en":      "A tall pillar-style companion memorial in dark grey granite with twin portrait medallions and intertwined vine border engraving.",
                    "zh_hans": "深灰色花岗岩高柱形伴侣纪念碑，配有双人肖像圆形浮雕及交织藤蔓边框雕刻。",
                    "zh_hant": "深灰色花崗岩高柱形伴侶紀念碑，配有雙人肖像圓形浮雕及交織藤蔓邊框雕刻。",
                },
            },

            # ── Jewish Companion ──────────────────────────────────────────────
            {
                "category": "jewish-companion", "order": 1,
                "title": {
                    "en":      "Star of David Black Granite Companion",
                    "zh_hans": "大卫之星黑色花岗岩伴侣墓碑",
                    "zh_hant": "大衛之星黑色花崗岩伴侶墓碑",
                },
                "description": {
                    "en":      "A dignified black granite companion gravestone with a polished Star of David relief and Hebrew and English bilingual inscription panels.",
                    "zh_hans": "庄重的黑色花岗岩伴侣墓碑，配有抛光大卫之星浮雕及希伯来文与英文双语铭文面板。",
                    "zh_hant": "莊重的黑色花崗岩伴侶墓碑，配有拋光大衛之星浮雕及希伯來文與英文雙語銘文面板。",
                },
            },
            {
                "category": "jewish-companion", "order": 2,
                "title": {
                    "en":      "Hebrew Script Memorial Companion",
                    "zh_hans": "希伯来文字纪念伴侣墓碑",
                    "zh_hant": "希伯來文字紀念伴侶墓碑",
                },
                "description": {
                    "en":      "A refined companion gravestone featuring full Hebrew script engraving, a traditional Menorah motif, and a sandblasted geometric border pattern.",
                    "zh_hans": "精致的伴侣墓碑，配有完整的希伯来文字雕刻、传统灯台图案及喷砂几何边框图案。",
                    "zh_hant": "精緻的伴侶墓碑，配有完整的希伯來文字雕刻、傳統燈台圖案及噴砂幾何邊框圖案。",
                },
            },

            # ── Asian / Chinese Grave ─────────────────────────────────────────
            {
                "category": "asian-chinese-grave", "order": 1,
                "title": {
                    "en":      "Traditional Chinese Family Grave",
                    "zh_hans": "传统中式家族墓地",
                    "zh_hant": "傳統中式家族墓地",
                },
                "description": {
                    "en":      "A traditional Chinese-style family grave with red and black granite tiers, gold-inlaid Chinese calligraphy, and a curved ceremonial platform base.",
                    "zh_hans": "传统中式家族墓地，以红黑花岗岩层级为特色，配有金色镶嵌中文书法及弧形礼仪平台底座。",
                    "zh_hant": "傳統中式家族墓地，以紅黑花崗岩層級為特色，配有金色鑲嵌中文書法及弧形禮儀平台底座。",
                },
            },
            {
                "category": "asian-chinese-grave", "order": 2,
                "title": {
                    "en":      "Contemporary Asian Memorial Garden",
                    "zh_hans": "现代亚洲纪念花园",
                    "zh_hant": "現代亞洲紀念花園",
                },
                "description": {
                    "en":      "A contemporary memorial garden design combining a polished black granite headstone with a Chinese landscape relief carving and surrounding granite paving.",
                    "zh_hans": "现代纪念花园设计，融合抛光黑色花岗岩墓碑、中国山水浮雕及周围花岗岩铺装。",
                    "zh_hant": "現代紀念花園設計，融合拋光黑色花崗岩墓碑、中國山水浮雕及周圍花崗岩鋪裝。",
                },
            },
            {
                "category": "asian-chinese-grave", "order": 3,
                "title": {
                    "en":      "Red Granite Ancestral Shrine Grave",
                    "zh_hans": "红色花岗岩祖先神祠墓地",
                    "zh_hant": "紅色花崗岩祖先神祠墓地",
                },
                "description": {
                    "en":      "An elaborate ancestral shrine grave in deep red and black granite featuring traditional dragon motifs, gold-leaf inscriptions, and a multi-tiered altar base.",
                    "zh_hans": "以深红色和黑色花岗岩精制的精美祖先神祠墓地，配有传统龙纹图案、金叶铭文及多层坛台底座。",
                    "zh_hant": "以深紅色和黑色花崗岩精製的精美祖先神祠墓地，配有傳統龍紋圖案、金葉銘文及多層壇台底座。",
                },
            },
            {
                "category": "asian-chinese-grave", "order": 4,
                "title": {
                    "en":      "Minimalist Chinese Companion Stone",
                    "zh_hans": "极简中式伴侣墓石",
                    "zh_hant": "極簡中式伴侶墓石",
                },
                "description": {
                    "en":      "A clean minimalist companion gravestone with simplified Chinese characters etched in a modern sans-serif style, framed by a subtle lotus border.",
                    "zh_hans": "简洁极简主义伴侣墓碑，以现代无衬线风格蚀刻简体中文字符，以精致莲花边框点缀。",
                    "zh_hant": "簡潔極簡主義伴侶墓碑，以現代無襯線風格蝕刻簡體中文字符，以精緻蓮花邊框點綴。",
                },
            },

            # ── Italian Grave ─────────────────────────────────────────────────
            {
                "category": "italian-grave", "order": 1,
                "title": {
                    "en":      "Carrara Marble Italian Companion",
                    "zh_hans": "卡拉拉大理石意大利伴侣墓碑",
                    "zh_hant": "卡拉拉大理石意大利伴侶墓碑",
                },
                "description": {
                    "en":      "A classical Italian-style companion gravestone hewn from Carrara white marble, featuring a carved Madonna relief, Italian script, and gold-leaf accents.",
                    "zh_hans": "以卡拉拉白色大理石雕刻的经典意大利式伴侣墓碑，配有圣母玛利亚浮雕、意大利文字及金叶点缀。",
                    "zh_hant": "以卡拉拉白色大理石雕刻的經典意大利式伴侶墓碑，配有聖母瑪利亞浮雕、意大利文字及金葉點綴。",
                },
            },
            {
                "category": "italian-grave", "order": 2,
                "title": {
                    "en":      "Baroque Style Black Granite Tomb",
                    "zh_hans": "巴洛克风格黑色花岗岩墓碑",
                    "zh_hant": "巴洛克風格黑色花崗岩墓碑",
                },
                "description": {
                    "en":      "An ornate baroque-style tomb in polished black granite with hand-carved acanthus scrollwork, twin angel figures, and a gilded oval portrait frame.",
                    "zh_hans": "抛光黑色花岗岩华丽巴洛克风格墓碑，配有手工雕刻茛苕叶涡纹、双天使雕像及镀金椭圆肖像框架。",
                    "zh_hant": "拋光黑色花崗岩華麗巴洛克風格墓碑，配有手工雕刻茛苕葉渦紋、雙天使雕像及鍍金橢圓肖像框架。",
                },
            },
        ]

        count = 0
        for d in items_data:
            cat_slug = d.pop("category")
            WorkItem.objects.create(category=categories[cat_slug], **d)
            count += 1

        self.stdout.write(self.style.SUCCESS(f"  ✓ {count} WorkItems created across {len(categories)} categories."))