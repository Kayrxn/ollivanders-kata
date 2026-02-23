# -*- coding: utf-8 -*-
"""
Tests parametrizados para Backstage passes
"""
import pytest
from gilded_rose import Item, GildedRose


@pytest.mark.backstage
@pytest.mark.quality
class TestBackstagePasses:
    """Tests para Backstage passes - aumentan valor según proximidad al evento"""
    
    @pytest.mark.parametrize("sell_in,initial_quality,expected_quality", [
        (15, 20, 21),  # More than 10 days
        (11, 20, 21),  # Exactly 11 days
        (20, 10, 11),  # Long before event
        (12, 49, 50),  # Near cap
        (15, 50, 50),  # Already at cap
    ])
    def test_quality_increases_by_1_when_more_than_10_days(
        self, gilded_rose, sell_in, initial_quality, expected_quality
    ):
        """Backstage passes aumentan 1 cuando faltan más de 10 días"""
        item = Item("Backstage passes to a TAFKAL80ETC concert", 
                   sell_in=sell_in, quality=initial_quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("sell_in,initial_quality,expected_quality", [
        (10, 20, 22),  # Exactly 10 days
        (9, 20, 22),   # 9 days left
        (6, 20, 22),   # 6 days left
        (10, 48, 50),  # Near cap
        (10, 49, 50),  # One from cap
        (10, 50, 50),  # Already at cap
    ])
    def test_quality_increases_by_2_when_10_days_or_less(
        self, gilded_rose, sell_in, initial_quality, expected_quality
    ):
        """Backstage passes aumentan 2 cuando faltan 10 días o menos"""
        item = Item("Backstage passes to a TAFKAL80ETC concert",
                   sell_in=sell_in, quality=initial_quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("sell_in,initial_quality,expected_quality", [
        (5, 20, 23),   # Exactly 5 days
        (4, 20, 23),   # 4 days left
        (1, 20, 23),   # Last day
        (5, 47, 50),   # Near cap
        (5, 48, 50),   # Two from cap
        (5, 50, 50),   # Already at cap
    ])
    def test_quality_increases_by_3_when_5_days_or_less(
        self, gilded_rose, sell_in, initial_quality, expected_quality
    ):
        """Backstage passes aumentan 3 cuando faltan 5 días o menos"""
        item = Item("Backstage passes to a TAFKAL80ETC concert",
                   sell_in=sell_in, quality=initial_quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("sell_in,initial_quality", [
        (0, 20),
        (0, 50),
        (-1, 30),
        (-5, 40),
    ])
    def test_quality_drops_to_zero_after_concert(
        self, gilded_rose, sell_in, initial_quality
    ):
        """Backstage passes pierden todo su valor después del concierto"""
        item = Item("Backstage passes to a TAFKAL80ETC concert",
                   sell_in=sell_in, quality=initial_quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 0
    
    @pytest.mark.edge_case
    def test_quality_never_exceeds_50(self, gilded_rose):
        """La calidad nunca supera 50, incluso con increases múltiples"""
        item = Item("Backstage passes to a TAFKAL80ETC concert",
                   sell_in=5, quality=49)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 50
    
    @pytest.mark.integration
    def test_full_lifecycle(self, gilded_rose):
        """Test del ciclo completo de un backstage pass"""
        item = Item("Backstage passes to a TAFKAL80ETC concert",
                   sell_in=15, quality=20)
        gr = gilded_rose([item])
        
        # Days 15-11: +1 per day
        for _ in range(5):
            gr.update_quality()
        assert item.quality == 25
        assert item.sell_in == 10
        
        # Days 10-6: +2 per day
        for _ in range(5):
            gr.update_quality()
        assert item.quality == 35
        assert item.sell_in == 5
        
        # Days 5-1: +3 per day
        for _ in range(5):
            gr.update_quality()
        assert item.quality == 50  # Capped at 50
        assert item.sell_in == 0
        
        # After concert: drops to 0
        gr.update_quality()
        assert item.quality == 0
        assert item.sell_in == -1
