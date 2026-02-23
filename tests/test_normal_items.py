# -*- coding: utf-8 -*-
"""
Tests parametrizados para items normales
"""
import pytest
from gilded_rose import Item, GildedRose


@pytest.mark.normal
@pytest.mark.quality
class TestNormalItems:
    """Tests para items normales estándar"""
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (20, 1, 19),  # Normal degradation
        (20, 5, 15),  # Multiple days
        (10, 10, 0),  # Degrade to zero
        (1, 1, 0),    # Almost zero
        (0, 1, 0),    # Already zero
    ])
    def test_quality_degradation_before_sell_date(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Items normales degradan 1 punto por día antes de expirar"""
        item = Item("Normal Item", sell_in=days + 5, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("initial_quality,days,expected_quality", [
        (20, 1, 18),  # First day after expiry
        (20, 2, 16),  # Two days after
        (10, 5, 0),   # Degrade to zero
        (3, 2, 0),    # Almost zero
        (1, 1, 0),    # One point left
    ])
    def test_quality_degradation_after_sell_date(
        self, gilded_rose, initial_quality, days, expected_quality
    ):
        """Items normales degradan 2 puntos por día después de expirar"""
        item = Item("Normal Item", sell_in=0, quality=initial_quality)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == expected_quality
    
    @pytest.mark.parametrize("sell_in,days,expected_sell_in", [
        (10, 1, 9),
        (10, 5, 5),
        (5, 10, -5),
        (0, 1, -1),
        (-1, 1, -2),
    ])
    @pytest.mark.sell_in
    def test_sell_in_decreases(self, gilded_rose, sell_in, days, expected_sell_in):
        """El sell_in decrece cada día"""
        item = Item("Normal Item", sell_in=sell_in, quality=20)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.sell_in == expected_sell_in
    
    @pytest.mark.edge_case
    def test_quality_never_negative(self, gilded_rose):
        """La calidad nunca puede ser negativa"""
        item = Item("Normal Item", sell_in=5, quality=0)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality >= 0


@pytest.mark.normal
@pytest.mark.quality
class TestNormalItemsEdgeCases:
    """Tests de casos límite para items normales"""
    
    @pytest.mark.edge_case
    @pytest.mark.parametrize("name", [
        "+5 Dexterity Vest",
        "Elixir of the Mongoose",
        "Random Item",
        "Some Other Item"
    ])
    def test_different_normal_item_names(self, gilded_rose, name):
        """Diferentes nombres de items normales se comportan igual"""
        item = Item(name, sell_in=10, quality=20)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == 19
        assert item.sell_in == 9
