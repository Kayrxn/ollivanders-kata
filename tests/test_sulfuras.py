# -*- coding: utf-8 -*-
"""
Tests parametrizados para Sulfuras (item legendario)
"""
import pytest
from src.gilded_rose import Item, GildedRose


@pytest.mark.sulfuras
class TestSulfuras:
    """Tests para Sulfuras - item legendario inmutable"""
    
    @pytest.mark.quality
    @pytest.mark.parametrize("sell_in,days", [
        (10, 1),
        (0, 1),
        (-1, 1),
        (10, 5),
        (0, 10),
    ])
    def test_quality_never_changes(self, gilded_rose, sell_in, days):
        """La calidad de Sulfuras nunca cambia"""
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=sell_in, quality=80)
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.quality == 80
    
    @pytest.mark.sell_in
    @pytest.mark.parametrize("sell_in,days", [
        (10, 1),
        (0, 1),
        (-1, 1),
        (5, 10),
    ])
    def test_sell_in_never_changes(self, gilded_rose, sell_in, days):
        """El sell_in de Sulfuras nunca cambia"""
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=sell_in, quality=80)
        initial_sell_in = item.sell_in
        gr = gilded_rose([item])
        
        for _ in range(days):
            gr.update_quality()
        
        assert item.sell_in == initial_sell_in
    
    @pytest.mark.edge_case
    @pytest.mark.parametrize("quality", [80, 50, 100])
    def test_legendary_quality_preserved(self, gilded_rose, quality):
        """Sulfuras mantiene cualquier calidad inicial (típicamente 80)"""
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=quality)
        gr = gilded_rose([item])
        gr.update_quality()
        
        assert item.quality == quality
