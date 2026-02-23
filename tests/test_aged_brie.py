# -*- coding: utf-8 -*-
"""
Tests parametrizados para Aged Brie
"""
import pytest
from gilded_rose import Item, GildedRose


@pytest.mark.aged_brie
@pytest.mark.quality
class TestAgedBrie:
    """Tests para Aged Brie - mejora con el tiempo"""
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (0, 1, 1),    # From zero
        (10, 1, 11),  # Normal increase
        (10, 5, 15),  # Multiple days
        (48, 2, 50),  # Near cap
        (49, 1, 50),  # At cap
        (50, 1, 50),  # Already at cap
    ])
    def test_quality_increases_before_sell_date(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Aged Brie aumenta 1 punto por día antes de expirar"""
        item = Item("Aged Brie", sell_in=days + 5, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (0, 1, 2),    # From zero after expiry
        (10, 1, 12),  # Double increase
        (10, 3, 16),  # Multiple days
        (47, 2, 50),  # Near cap
        (48, 1, 50),  # At cap
        (50, 1, 50),  # Already at cap
    ])
    def test_quality_increases_twice_after_sell_date(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Aged Brie aumenta 2 puntos por día después de expirar"""
        item = Item("Aged Brie", sell_in=0, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.edge_case
    def test_quality_never_exceeds_50(self, gilded_rose):
        """La calidad nunca supera 50"""
        item = Item("Aged Brie", sell_in=10, quality=50)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 50
    
    @pytest.mark.edge_case
    def test_quality_caps_at_50_after_expiry(self, gilded_rose):
        """La calidad se mantiene en 50 incluso después de expirar"""
        item = Item("Aged Brie", sell_in=0, quality=49)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 50
        
        # Try again, should stay at 50
        gr.update_quality()
        assert item.quality == 50
    
    @pytest.mark.sell_in
    def test_sell_in_decreases_normally(self, gilded_rose):
        """El sell_in de Aged Brie decrece normalmente"""
        item = Item("Aged Brie", sell_in=10, quality=20)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.sell_in == 9
