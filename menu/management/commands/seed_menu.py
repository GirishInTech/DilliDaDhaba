"""
Management command: seed_menu

Usage:
    python manage.py seed_menu          # wipe + seed
    python manage.py seed_menu --dry-run # count-only preview, no DB writes

Wipes ALL existing Category and MenuItem rows, then inserts the
complete Dilli Da Dhaba menu exactly as photographed.

Rules applied:
  * veg / non-veg auto-detected from category + item name
  * Items explicitly flagged needs_verification=True where data
    was ambiguous on the source menu card
  * Prices follow the Half / Full convention used in the category;
    standalone items use price_regular
  * Mineral Water: "20 / 10" stored as price_half=20 / price_full=10
    with needs_verification=True — exact values to be confirmed on-site
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from menu.models import Category, MenuItem

# ---------------------------------------------------------------------------
# Dataset
# Each tuple: (category_name, display_order, [ item_dicts, ... ])
#
# Item dict keys:
#   name, veg, price_regular, price_half, price_full, needs_verification
#   All prices are Decimal or None.
# ---------------------------------------------------------------------------

D = Decimal  # shorthand


def _item(
    name,
    *,
    veg=True,
    price_regular=None,
    price_half=None,
    price_full=None,
    needs_verification=False,
):
    return dict(
        name=name,
        veg=veg,
        price_regular=D(str(price_regular)) if price_regular is not None else None,
        price_half=D(str(price_half)) if price_half is not None else None,
        price_full=D(str(price_full)) if price_full is not None else None,
        needs_verification=needs_verification,
    )


MENU_DATA = [
    # ------------------------------------------------------------------ #
    # 1. SPECIAL APPETIZERS VEG
    # ------------------------------------------------------------------ #
    (
        "Special Appetizers Veg",
        1,
        [
            _item("Cheese Garlic Paneer",        veg=True,  price_regular=179),
            _item("Burnt Garlic Cheese Paneer",  veg=True,  price_regular=189),
            _item("Paneer Satay",                veg=True,  price_regular=199),
            _item("Paneer Banjara Kabab",        veg=True,  price_regular=230),
            _item("Paneer Angara Tikka",         veg=True,  price_regular=230),
            _item("Paneer Pahadi Tikka",         veg=True,  price_regular=230),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 2. SPECIAL APPETIZERS NON-VEG
    # ------------------------------------------------------------------ #
    (
        "Special Appetizers Non-Veg",
        2,
        [
            _item("Cheese Garlic Chicken (Bone/BL)", veg=False, price_regular=199),
            _item("Chicken Banjara Kabab",            veg=False, price_regular=220),
            _item("Tandoori Lollipop (8 pcs)",        veg=False, price_regular=220),
            _item("Chicken Angara Kabab",             veg=False, price_regular=249),
            _item("Chicken Pahadi Tikka",             veg=False, price_regular=239),
            _item("Chicken Reshmi Kabab",             veg=False, price_regular=269),
            _item("Burnt Garlic Cheese Chicken",      veg=False, price_regular=229),
            _item("Chicken Satay",                    veg=False, price_regular=199),
            _item("Mohini Fish Tikka",                veg=False, price_regular=259),
            # "Cheese Girlk Prawn" — exact name preserved; likely "Garlic" typo
            _item("Cheese Girlk Prawn",               veg=False, price_regular=249,
                  needs_verification=True),
            _item("Spicy Chicken Pepper Wings",       veg=False, price_regular=199),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 3. SPECIAL PANEER MAIN COURSE  (half / full)
    # ------------------------------------------------------------------ #
    (
        "Special Paneer Main Course",
        3,
        [
            _item("Paneer Majedar",          veg=True, price_half=179, price_full=249),
            _item("Paneer Lababdar",         veg=True, price_half=179, price_full=249),
            _item("Paneer Chatpata",         veg=True, price_half=179, price_full=249),
            _item("Pind Da Paneer",          veg=True, price_half=179, price_full=249),
            _item("Paneer Patiyala",         veg=True, price_half=179, price_full=249),
            _item("Paneer Chingari",         veg=True, price_half=179, price_full=249),
            _item("Paneer Tufani",           veg=True, price_half=179, price_full=249),
            _item("Dum Handi Paneer",        veg=True, price_half=189, price_full=259),
            _item("Lasooni Paneer Masala",   veg=True, price_half=189, price_full=259),
            _item("Paneer Lahore",           veg=True, price_half=189, price_full=259),
            _item("Paneer Malai Masala",     veg=True, price_half=199, price_full=259),
            _item("Paneer Hariyali Masala",  veg=True, price_half=179, price_full=259),
            # Half price (179) is higher than a comparable full (239) —
            # exact values preserved, flagged for verification
            _item("Paneer Maharaja",         veg=True, price_half=179, price_full=239,
                  needs_verification=True),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 4. SPECIAL CHICKEN MAIN COURSE  (half / full)
    # ------------------------------------------------------------------ #
    (
        "Special Chicken Main Course",
        4,
        [
            _item("Chicken Lababdar",          veg=False, price_half=179, price_full=249),
            _item("Chicken Majeedar",          veg=False, price_half=179, price_full=249),
            _item("Chicken Rara",              veg=False, price_half=189, price_full=269),
            _item("Chicken Keema",             veg=False, price_half=179, price_full=249),
            _item("Chicken Chatpata",          veg=False, price_half=179, price_full=249),
            _item("Murgh Musallam",            veg=False, price_half=249, price_full=429),
            _item("Chicken Lazeez",            veg=False, price_half=179, price_full=249),
            _item("Pind Da Chicken",           veg=False, price_half=199, price_full=269),
            _item("Chicken Chingari",          veg=False, price_half=199, price_full=269),
            _item("Chicken Tufani",            veg=False, price_half=199, price_full=269),
            _item("Chicken Leg Piece Masala",  veg=False, price_half=180, price_full=240),
            _item("Chicken Kalmi Kosha",       veg=False, price_half=180, price_full=249),
            _item("Chicken Afghani",           veg=False, price_half=170, price_full=249),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 5. SPECIAL VEG MAIN COURSE  (half / full)
    # ------------------------------------------------------------------ #
    (
        "Special Veg Main Course",
        5,
        [
            _item("Matka Sabzi",           veg=True, price_half=159, price_full=199),
            _item("Veg Chilli Milli",      veg=True, price_half=149, price_full=199),
            _item("Veg Lajawab",           veg=True, price_half=149, price_full=199),
            _item("Rajasthani Sabzi",      veg=True, price_half=149, price_full=199),
            _item("Veg Patiyala",          veg=True, price_half=149, price_full=199),
            _item("Veg Tufani",            veg=True, price_half=149, price_full=199),
            _item("Veg Majedaar",          veg=True, price_half=149, price_full=199),
            _item("Veg Hariyali Masala",   veg=True, price_half=149, price_full=199),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 6. SPECIAL RICE
    # ------------------------------------------------------------------ #
    (
        "Special Rice",
        6,
        [
            _item("Veg Yakni Pulao",                  veg=True,  price_regular=149),
            _item("Nasi Goreng Chicken Fried Rice",   veg=False, price_regular=189),
            _item("Chicken Yakhni Pulao",             veg=False, price_regular=189),
            _item("Mutton Yakhni Pulao",              veg=False, price_regular=250),
            # "Domli Masala Papad" — unusual for a rice section; verified as-is
            _item("Domli Masala Papad",               veg=True,  price_regular=149,
                  needs_verification=True),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 7. PASTA
    # ------------------------------------------------------------------ #
    (
        "Pasta",
        7,
        [
            _item("Veg Penne Arrabita",            veg=True,  price_regular=180),
            _item("Veg Penne with Cream Sauce",    veg=True,  price_regular=180),
            _item("Chicken Penne Arrabita",        veg=False, price_regular=220),
            _item("Chicken Penne with Cream Sauce",veg=False, price_regular=220),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 8. SNACKS
    # ------------------------------------------------------------------ #
    (
        "Snacks",
        8,
        [
            _item("Puri Sabbi (5 pcs)",    veg=True, price_regular=110),
            _item("Plain Kachori (5 pcs)", veg=True, price_regular=110),
            _item("Chola Bhatura (5 pcs)", veg=True, price_regular=130),
            _item("Extra Pav",             veg=True, price_regular=15),
            _item("Per Pc Puri",           veg=True, price_regular=20),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 9. ROLLS
    # ------------------------------------------------------------------ #
    (
        "Rolls",
        9,
        [
            _item("Veg Roll",                    veg=True,  price_regular=60),
            _item("Veg Cheese Roll",             veg=True,  price_regular=70),
            _item("Paneer Roll",                 veg=True,  price_regular=80),
            _item("Paneer Cheese Roll",          veg=True,  price_regular=90),
            _item("Paneer Tikka Roll",           veg=True,  price_regular=100),
            _item("Egg Roll",                    veg=False, price_regular=70),
            _item("Egg Cheese Roll",             veg=False, price_regular=80),
            _item("Double Egg Roll",             veg=False, price_regular=90),
            _item("Double Egg Cheese Roll",      veg=False, price_regular=100),
            _item("Chicken Roll",                veg=False, price_regular=90),
            _item("Chicken Egg Roll",            veg=False, price_regular=100),
            _item("Chicken Cheese Roll",         veg=False, price_regular=110),
            _item("Chicken Tikka Roll",          veg=False, price_regular=110),
            _item("Chicken Tikka Cheese Roll",   veg=False, price_regular=120),
            _item("Chicken Tikka Egg Cheese Roll", veg=False, price_regular=130),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 10. SIZZLER
    # ------------------------------------------------------------------ #
    (
        "Sizzler",
        10,
        [
            _item("Veg Grill Sizzler",          veg=True,  price_regular=210),
            _item("Veg Cheese Sizzler",         veg=True,  price_regular=250),
            _item("Paneer Sizzler",             veg=True,  price_regular=250),
            _item("Chicken Grill Sizzler",      veg=False, price_regular=250),
            _item("Chicken Cheese Grill Sizzler",veg=False, price_regular=250),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 11. MAGGIE
    # ------------------------------------------------------------------ #
    (
        "Maggie",
        11,
        [
            _item("Plain Maggie",             veg=True,  price_regular=60),
            _item("Veg Maggie",               veg=True,  price_regular=70),
            _item("Cheese Maggie",            veg=True,  price_regular=80),
            _item("Egg Maggie",               veg=False, price_regular=100),
            _item("Double Egg Cheese Maggie", veg=False, price_regular=120),
            _item("Chicken Maggie",           veg=False, price_regular=120),
            _item("Chicken Cheese Maggie",    veg=False, price_regular=130),
        ],
    ),
    # ------------------------------------------------------------------ #
    # 12. BEVERAGES | DESSERTS | JUICE
    # ------------------------------------------------------------------ #
    (
        "Beverages | Desserts | Juice",
        12,
        [
            _item("Butter Milk",           veg=True, price_regular=40),
            _item("Lassi",                 veg=True, price_regular=50),
            _item("Nimboo Pani",           veg=True, price_regular=30),
            _item("Masala Cold Drinks",    veg=True, price_regular=40),
            _item("Virgin Mojito Lemon",   veg=True, price_regular=70),
            # "20 / 10" — exact source values stored as half/full;
            # interpretation (bottle sizes) to be confirmed on-site
            _item("Mineral Water",         veg=True,
                  price_half=20, price_full=10,
                  needs_verification=True),
            _item("Cold Drinks",           veg=True, price_regular=20),
            _item("Gulab Jamun (1 pc)",    veg=True, price_regular=20),
            _item("Lime Soda",             veg=True, price_regular=50),
            _item("Watermelon Juice",      veg=True, price_regular=89),
            _item("Mosambi Juice",         veg=True, price_regular=69),
            _item("Apple Juice",           veg=True, price_regular=99),
            _item("Pineapple Juice",       veg=True, price_regular=69),
            _item("Mango Juice",           veg=True, price_regular=99),
            _item("Pomegranate Juice",     veg=True, price_regular=99),
            _item("Chocolate Milk Shake",  veg=True, price_regular=99),
            # "Chikku Milk Shake" — spelling preserved from source menu
            _item("Chikku Milk Shake",     veg=True, price_regular=119,
                  needs_verification=True),
        ],
    ),
]

# Expected totals — used as post-seed verification
EXPECTED_CATEGORIES = 12
EXPECTED_ITEMS = sum(len(items) for _, _, items in MENU_DATA)


class Command(BaseCommand):
    help = (
        "Wipe all Category / MenuItem rows and seed from the "
        "Dilli Da Dhaba photographed menu dataset."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print summary counts only; make no DB changes.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        if dry_run:
            self._print_preview()
            return

        with transaction.atomic():
            self._wipe_existing()
            cat_count, item_count = self._insert_menu()
            self._verify_counts(cat_count, item_count)

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅  Seed complete — {cat_count} categories, "
                f"{item_count} menu items inserted."
            )
        )

    # ------------------------------------------------------------------
    def _print_preview(self):
        self.stdout.write("\n--- DRY RUN (no DB changes) ---\n")
        for cat_name, order, items in MENU_DATA:
            self.stdout.write(
                f"  [{order:>2}] {cat_name}  ({len(items)} items)"
            )
        self.stdout.write(
            f"\n  Categories : {EXPECTED_CATEGORIES}"
            f"\n  Menu items : {EXPECTED_ITEMS}\n"
        )

    def _wipe_existing(self):
        deleted_items, _ = MenuItem.objects.all().delete()
        deleted_cats, _  = Category.objects.all().delete()
        self.stdout.write(
            f"  🗑  Deleted {deleted_items} menu items "
            f"and {deleted_cats} categories."
        )

    def _insert_menu(self):
        cat_count  = 0
        item_count = 0

        for cat_name, display_order, items in MENU_DATA:
            category = Category.objects.create(
                name=cat_name,
                display_order=display_order,
            )
            cat_count += 1

            menu_items = [
                MenuItem(
                    category=category,
                    name=item["name"],
                    veg=item["veg"],
                    price_regular=item["price_regular"],
                    price_half=item["price_half"],
                    price_full=item["price_full"],
                    needs_verification=item["needs_verification"],
                    is_available=True,
                    featured=False,
                )
                for item in items
            ]
            MenuItem.objects.bulk_create(menu_items)
            item_count += len(menu_items)

            self.stdout.write(
                f"  ✔  {cat_name:<40} {len(menu_items):>3} items"
            )

        return cat_count, item_count

    def _verify_counts(self, cat_count, item_count):
        db_cats  = Category.objects.count()
        db_items = MenuItem.objects.count()

        errors = []
        if db_cats != EXPECTED_CATEGORIES:
            errors.append(
                f"Category count mismatch: expected {EXPECTED_CATEGORIES}, "
                f"got {db_cats}"
            )
        if db_items != EXPECTED_ITEMS:
            errors.append(
                f"MenuItem count mismatch: expected {EXPECTED_ITEMS}, "
                f"got {db_items}"
            )

        if errors:
            for err in errors:
                self.stderr.write(self.style.ERROR(f"  ❌  {err}"))
            raise SystemExit(1)

        self.stdout.write(
            f"\n  ✔  Verified: {db_cats} categories, {db_items} items in DB."
        )
