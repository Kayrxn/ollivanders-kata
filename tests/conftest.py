# -*- coding: utf-8 -*-
"""
Fixtures y configuración compartida para tests de Gilded Rose
"""
import pytest
from src.gilded_rose import Item, GildedRose


@pytest.fixture
def gilded_rose():
    """Factory fixture para crear instancias de GildedRose"""
    def _make_gilded_rose(items):
        return GildedRose(items)
    return _make_gilded_rose


@pytest.fixture
def normal_item():
    """Fixture que retorna un item normal estándar"""
    return Item("+5 Dexterity Vest", sell_in=10, quality=20)


@pytest.fixture
def aged_brie():
    """Fixture que retorna Aged Brie"""
    return Item("Aged Brie", sell_in=10, quality=20)


@pytest.fixture
def sulfuras():
    """Fixture que retorna Sulfuras (item legendario)"""
    return Item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)


@pytest.fixture
def backstage_pass():
    """Fixture que retorna un backstage pass"""
    return Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)


@pytest.fixture
def conjured_item():
    """Fixture que retorna un item conjurado"""
    return Item("Conjured Mana Cake", sell_in=10, quality=20)


@pytest.fixture
def update_item(gilded_rose):
    """Helper fixture para actualizar un item n veces"""
    def _update(item, days=1):
        gr = gilded_rose([item])
        for _ in range(days):
            gr.update_quality()
        return item
    return _update
