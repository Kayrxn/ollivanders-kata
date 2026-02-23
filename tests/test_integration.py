# -*- coding: utf-8 -*-
"""
Tests de integración para múltiples tipos de items
"""
import pytest
from gilded_rose import Item, GildedRose


@pytest.mark.integration
class TestIntegration:
    """Tests de integración con múltiples tipos de items"""
    
    def test_multiple_items_update_independently(self, gilded_rose):
        """Múltiples items se actualizan de forma independiente"""
        items = [
            Item("+5 Dexterity Vest", sell_in=10, quality=20),
            Item("Aged Brie", sell_in=2, quality=0),
            Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item("Conjured Mana Cake", sell_in=3, quality=6)
        ]
        gr = gilded_rose(items)
        gr.update_quality()
        
        # Normal item: -1 quality
        assert items[0].quality == 19
        assert items[0].sell_in == 9
        
        # Aged Brie: +1 quality
        assert items[1].quality == 1
        assert items[1].sell_in == 1
        
        # Sulfuras: no change
        assert items[2].quality == 80
        assert items[2].sell_in == 0
        
        # Backstage pass: +1 quality (>10 days)
        assert items[3].quality == 21
        assert items[3].sell_in == 14
        
        # Conjured: -2 quality
        assert items[4].quality == 4
        assert items[4].sell_in == 2
    
    def test_full_simulation_30_days(self, gilded_rose):
        """Simulación completa de 30 días como en texttest_fixture"""
        items = [
            Item("+5 Dexterity Vest", sell_in=10, quality=20),
            Item("Aged Brie", sell_in=2, quality=0),
            Item("Elixir of the Mongoose", sell_in=5, quality=7),
            Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item("Conjured Mana Cake", sell_in=3, quality=6),
        ]
        gr = gilded_rose(items)
        
        # Run for 30 days
        for day in range(30):
            gr.update_quality()
        
        # Verify final states
        assert items[0].quality == 0  # Normal item degraded
        assert items[1].quality == 50  # Aged Brie at max
        assert items[2].quality == 0  # Elixir degraded
        assert items[3].quality == 80  # Sulfuras unchanged
        assert items[4].quality == 0  # Backstage pass expired
        assert items[5].quality == 0  # Conjured degraded
    
    @pytest.mark.parametrize("days", [1, 5, 10, 20, 30])
    def test_simulation_consistency(self, gilded_rose, days):
        """Verificar consistencia en simulaciones de diferentes duraciones"""
        items = [
            Item("Normal Item", sell_in=10, quality=20),
            Item("Aged Brie", sell_in=10, quality=10),
        ]
        gr = gilded_rose(items)
        
        for _ in range(days):
            gr.update_quality()
        
        # All items should have valid states
        for item in items:
            assert 0 <= item.quality <= 50
            assert item.sell_in == 10 - days
    
    def test_mixed_items_at_different_stages(self, gilded_rose):
        """Items en diferentes etapas de su ciclo de vida"""
        items = [
            Item("Fresh Item", sell_in=10, quality=50),
            Item("About to Expire", sell_in=1, quality=10),
            Item("Expired Item", sell_in=0, quality=10),
            Item("Long Expired", sell_in=-5, quality=10),
        ]
        gr = gilded_rose(items)
        gr.update_quality()
        
        assert items[0].quality == 49  # Normal degradation
        assert items[1].quality == 9   # Normal degradation
        assert items[2].quality == 8   # Double degradation
        assert items[3].quality == 8   # Double degradation
    
    def test_no_items(self, gilded_rose):
        """Sistema funciona con lista vacía de items"""
        items = []
        gr = gilded_rose(items)
        gr.update_quality()  # Should not crash
        
        assert len(items) == 0
    
    def test_single_item_of_each_type(self, gilded_rose):
        """Un item de cada tipo se maneja correctamente"""
        items = [
            Item("Normal", sell_in=5, quality=10),
            Item("Aged Brie", sell_in=5, quality=10),
            Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10),
            Item("Conjured Item", sell_in=5, quality=10),
        ]
        
        expected_qualities_after_1_day = [9, 11, 80, 13, 8]
        
        gr = gilded_rose(items)
        gr.update_quality()
        
        for i, expected in enumerate(expected_qualities_after_1_day):
            assert items[i].quality == expected, f"Item {i} ({items[i].name}) quality mismatch"


@pytest.mark.integration
@pytest.mark.regression
class TestRegressionScenarios:
    """Tests de regresión para escenarios específicos"""
    
    def test_backstage_pass_and_aged_brie_both_respect_quality_cap(self, gilded_rose):
        """Tanto Backstage passes como Aged Brie respetan el límite de 50"""
        items = [
            Item("Aged Brie", sell_in=1, quality=49),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        ]
        gr = gilded_rose(items)
        gr.update_quality()
        
        assert items[0].quality == 50
        assert items[1].quality == 50
    
    def test_all_items_with_zero_quality_stay_at_zero(self, gilded_rose):
        """Items con calidad 0 no van a negativo"""
        items = [
            Item("Normal", sell_in=5, quality=0),
            Item("Conjured Item", sell_in=5, quality=0),
            Item("Normal Expired", sell_in=-1, quality=0),
            Item("Conjured Expired", sell_in=-1, quality=0),
        ]
        gr = gilded_rose(items)
        gr.update_quality()
        
        for item in items:
            assert item.quality == 0
    
    def test_backstage_pass_progression_near_concert(self, gilded_rose):
        """Backstage pass progression detallada cerca del concierto"""
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20)
        gr = gilded_rose([item])
        
        # Day 1: 11 days left -> +1
        gr.update_quality()
        assert item.quality == 21
        assert item.sell_in == 10
        
        # Day 2: 10 days left -> +2
        gr.update_quality()
        assert item.quality == 23
        assert item.sell_in == 9
        
        # Continue until 6 days left
        for _ in range(4):
            gr.update_quality()
        assert item.quality == 31  # 23 + (4 * 2)
        assert item.sell_in == 5
        
        # Day: 5 days left -> +3
        gr.update_quality()
        assert item.quality == 34
        assert item.sell_in == 4
