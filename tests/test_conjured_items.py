# -*- coding: utf-8 -*-
"""
Tests parametrizados para items Conjured
"""
import pytest
from gilded_rose import Item, GildedRose


@pytest.mark.conjured
@pytest.mark.quality
class TestConjuredItems:
    """Tests para items Conjured - degradan el doble de rápido"""
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (20, 1, 18),   # Normal degradation (2x)
        (20, 5, 10),   # Multiple days
        (10, 5, 0),    # Degrade to zero
        (5, 3, 0),     # Almost zero
        (1, 1, 0),     # One point left
        (0, 1, 0),     # Already zero
    ])
    def test_quality_degrades_twice_as_fast(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Items Conjured degradan 2 puntos por día antes de expirar"""
        item = Item("Conjured Mana Cake", sell_in=days + 5, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (20, 1, 16),   # First day after expiry (4x)
        (20, 2, 12),   # Two days after
        (20, 5, 0),    # Degrade to zero
        (10, 3, 0),    # Almost zero
        (3, 1, 0),     # Small value
        (1, 1, 0),     # One point left
    ])
    def test_quality_degrades_four_times_after_sell_date(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Items Conjured degradan 4 puntos por día después de expirar"""
        item = Item("Conjured Sword", sell_in=0, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.edge_case
    @pytest.mark.parametrize("initial_quality", [0, 1, 2, 3])
    def test_quality_never_negative(self, gilded_rose, initial_quality):
        """La calidad nunca puede ser negativa"""
        item = Item("Conjured Item", sell_in=5, quality=initial_quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality >= 0
    
    @pytest.mark.parametrize("name", [
        "Conjured Mana Cake",
        "Conjured Sword",
        "Conjured Elixir",
        "Conjured Health Potion",
    ])
    def test_different_conjured_item_names(self, gilded_rose, name):
        """Diferentes items con 'Conjured' en el nombre se comportan igual"""
        item = Item(name, sell_in=10, quality=20)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 18  # -2
        assert item.sell_in == 9
    
    @pytest.mark.sell_in
    def test_sell_in_decreases_normally(self, gilded_rose):
        """El sell_in de items Conjured decrece normalmente"""
        item = Item("Conjured Mana Cake", sell_in=10, quality=20)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.sell_in == 9
    
    @pytest.mark.integration
    def test_comparison_with_normal_item(self, gilded_rose):
        """Items Conjured degradan exactamente el doble que items normales"""
        normal = Item("Normal Item", sell_in=10, quality=20)
        conjured = Item("Conjured Item", sell_in=10, quality=20)
        gr = gilded_rose([normal, conjured])
        
        gr.update_quality()
        
        assert normal.quality == 19    # -1
        assert conjured.quality == 18  # -2 (double)
        
        # After sell date
        normal.sell_in = -1
        conjured.sell_in = -1
        gr.update_quality()
        
        assert normal.quality == 17    # -2
        assert conjured.quality == 14  # -4 (double)


@pytest.mark.conjured
@pytest.mark.regression
class TestConjuredEdgeCases:
    """Tests de regresión y casos límite para items Conjured"""
    
    @pytest.mark.edge_case
    def test_conjured_with_low_quality_before_expiry(self, gilded_rose):
        """Conjured con calidad baja antes de expirar"""
        item = Item("Conjured Potion", sell_in=5, quality=1)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 0
    
    @pytest.mark.edge_case
    def test_conjured_with_low_quality_after_expiry(self, gilded_rose):
        """Conjured con calidad baja después de expirar"""
        item = Item("Conjured Elixir", sell_in=0, quality=2)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 0
    
    @pytest.mark.integration
    def test_conjured_full_lifecycle(self, gilded_rose):
        """Test del ciclo completo de un item Conjured"""
        item = Item("Conjured Magic Item", sell_in=3, quality=20)
        gr = gilded_rose([item])
        
        # Day 1: sell_in=2, quality=18
        gr.update_quality()
        assert item.quality == 18
        assert item.sell_in == 2
        
        # Day 2: sell_in=1, quality=16
        gr.update_quality()
        assert item.quality == 16
        assert item.sell_in == 1
        
        # Day 3: sell_in=0, quality=14
        gr.update_quality()
        assert item.quality == 14
        assert item.sell_in == 0
        
        # Day 4: sell_in=-1, quality=10 (now degrades 4/day)
        gr.update_quality()
        assert item.quality == 10
        assert item.sell_in == -1
        
        # Day 5: sell_in=-2, quality=6
        gr.update_quality()
        assert item.quality == 6
