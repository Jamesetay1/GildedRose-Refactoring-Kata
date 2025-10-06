class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """
        Update quality and sell_in for all items in inventory.
        Dispatches to the correct update logic based on item name.
        """
        for item in self.items:
            if item.name == "Aged Brie":
                self._update_aged_brie(item)
            elif item.name == "Sulfuras, Hand of Ragnaros":
                self._update_sulfuras(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self._update_backstage_pass(item)
            elif "Conjured" in item.name:
                self._update_conjured(item)
            else:
                self._update_normal(item)

    def _update_normal(self, item):
        """
        Normal items degrade in quality by 1 each day.
        After the sell by date, degrade by 2 per day.
        Quality never goes below 0.
        """
        if item.quality > 0:
            item.quality -= 1
        item.sell_in -= 1
        if item.sell_in < 0 and item.quality > 0:
            item.quality -= 1

    def _update_aged_brie(self, item):
        """
        Aged Brie increases in quality as it ages.
        Quality increases by 1 per day, and by 2 after sell by date.
        Quality never exceeds 50.
        """
        if item.quality < 50:
            item.quality += 1
        item.sell_in -= 1
        if item.sell_in < 0 and item.quality < 50:
            item.quality += 1

    def _update_sulfuras(self, item):
        """
        Sulfuras is legendary: quality always 80, never sold or changes.
        """
        item.quality = 80 
        
    def _update_backstage_pass(self, item):
        """
        Backstage passes increase in quality as the concert approaches:
        - +1 when >10 days
        - +2 when 10 days or less
        - +3 when 5 days or less
        - Quality drops to 0 after concert
        Quality never exceeds 50.
        """
        if item.quality < 50:
            item.quality += 1
            if item.sell_in < 11 and item.quality < 50:
                item.quality += 1
            if item.sell_in < 6 and item.quality < 50:
                item.quality += 1
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = 0

    def _update_conjured(self, item):
        """
        Conjured items degrade in quality twice as fast as normal items:
        -2 per day before sell by date, -4 per day after.
        Quality never goes below 0.
        """
        degrade = 2
        if item.sell_in <= 0:
            degrade *= 2
        item.quality = max(0, item.quality - degrade)
        item.sell_in -= 1

        
    def update_quality_markedup(self):
        for item in self.items: # For each item (each day)
            # ORIGINAL DECAY LOGIC
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert": # Normal items
                if item.quality > 0: # Quality is still positive (it may not be negative)
                    if item.name != "Sulfuras, Hand of Ragnaros": # Does not degrade and never needs updated
                        # Conjured items degrade twice as fast
                        if "Conjured" in item.name:
                            if item.sell_in > 0:
                                item.quality = max(0, item.quality - 2)
                            else:
                                item.quality = max(0, item.quality - 4)
                        else:
                            item.quality = item.quality - 1 # Decrease quality by 1
            else: # Aged Brie or Backstage passes
                if item.quality < 50: # Quality may not go above 50
                    item.quality = item.quality + 1 # Aging :)
                    if item.name == "Backstage passes to a TAFKAL80ETC concert": # Special case for Backstage passes
                        if item.sell_in < 11: # Increases by 2 when 10 days or less
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6: # Increases by 3 when 5 days or less
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name == "Sulfuras, Hand of Ragnaros":
                item.quality = 80
            else:
                item.sell_in = item.sell_in - 1
                
            # ADDITIONAL AFTER SELL BY DATE DECAY LOGICAL
            if item.sell_in < 0: # After the sell by date
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert": 
                        if item.quality > 0: # Normal items with some quality left
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                # Conjured items already handled above
                                if "Conjured" not in item.name:
                                    item.quality = item.quality - 1
                    else: 
                        item.quality = item.quality - item.quality # Backstage passes after concert are worthless
                else: 
                    if item.quality < 50: # Aged Brie increases up to 50
                        item.quality = item.quality + 1


class Item: # Do not change or the Goblin will shoot!
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
