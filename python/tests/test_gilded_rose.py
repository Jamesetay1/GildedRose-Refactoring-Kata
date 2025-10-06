# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    # Test that a normal item's quality and sell_in decrease by 1 before the sell date
    def test_normal_item_before_sell_date(self):
        items = [Item("normal item", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(19, items[0].quality)

    # Test that a normal item's quality decreases by 2 on the sell date
    def test_normal_item_on_sell_date(self):
        items = [Item("normal item", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(18, items[0].quality)

    # Test that a normal item's quality decreases by 2 after the sell date
    def test_normal_item_after_sell_date(self):
        items = [Item("normal item", -1, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-2, items[0].sell_in)
        self.assertEqual(18, items[0].quality)

    # Test that a normal item's quality never goes below 0
    def test_normal_item_quality_never_negative(self):
        items = [Item("normal item", 5, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    # Test that Aged Brie increases in quality as it gets older
    def test_aged_brie_increases_quality(self):
        items = [Item("Aged Brie", 2, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(1, items[0].quality)

    # Test that Aged Brie quality never exceeds 50
    def test_aged_brie_quality_max_50(self):
        items = [Item("Aged Brie", 2, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    # Test that Sulfuras never changes in quality or sell_in (sell_in = 0)
    def test_sulfuras_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    # Test that Sulfuras never changes in quality or sell_in (sell_in > 0)
    def test_sulfuras_never_changes_positive_sell_in(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(5, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    # Test that Sulfuras never changes in quality or sell_in (sell_in < 0)
    def test_sulfuras_never_changes_negative_sell_in(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    # Test that Sulfuras always has quality 80, even if initialized with a different value
    def test_sulfuras_quality_always_80(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 70)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)

    # Test that Backstage passes increase in quality as sell_in approaches
    def test_backstage_pass_increase_quality(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(14, items[0].sell_in)
        self.assertEqual(21, items[0].quality)

    # Test that Backstage passes increase in quality by 2 when 10 days or less
    def test_backstage_pass_10_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(22, items[0].quality)

    # Test that Backstage passes increase in quality by 3 when 5 days or less
    def test_backstage_pass_5_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(23, items[0].quality)

    # Test that Backstage passes quality never exceeds 50
    def test_backstage_pass_quality_max_50(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(50, items[0].quality)

    # Test that Backstage passes quality drops to 0 after the concert
    def test_backstage_pass_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    # Test that Conjured items degrade in quality twice as fast as normal items before sell date
    def test_conjured_items_degrade_twice_as_fast(self):
        items = [Item("Conjured Mana Cake", 3, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        # Should degrade by 2
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(4, items[0].quality)

    # Test that Conjured items degrade in quality twice as fast as normal items after sell date
    def test_conjured_items_degrade_twice_as_fast_after_sell_date(self):
        items = [Item("Conjured Mana Cake", 0, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        # Should degrade by 4
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(2, items[0].quality)

        
if __name__ == '__main__':
    unittest.main()
