# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        self.update_quality_markedup()
        
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
