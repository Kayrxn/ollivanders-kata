class ItemUpdater:
    """Clase base para actualizar items"""
    
    def update(self, item):
        """Actualiza la calidad y sell_in del item"""
        self._update_quality_before_sell_in(item)
        self._update_sell_in(item)
        self._update_quality_after_sell_in(item)
    
    def _update_quality_before_sell_in(self, item):
        """Actualiza la calidad antes de decrementar sell_in"""
        pass
    
    def _update_sell_in(self, item):
        """Actualiza el sell_in del item"""
        item.sell_in -= 1
    
    def _update_quality_after_sell_in(self, item):
        """Actualiza la calidad después de decrementar sell_in si ha expirado"""
        pass
    
    def _increase_quality(self, item, amount=1):
        """Incrementa la calidad sin exceder 50"""
        item.quality = min(50, item.quality + amount)
    
    def _decrease_quality(self, item, amount=1):
        """Decrementa la calidad sin bajar de 0"""
        item.quality = max(0, item.quality - amount)


class NormalItemUpdater(ItemUpdater):
    """Actualiza items normales"""
    
    def _update_quality_before_sell_in(self, item):
        self._decrease_quality(item, 1)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._decrease_quality(item, 1)


class AgedBrieUpdater(ItemUpdater):
    """Actualiza Aged Brie - aumenta su calidad con el tiempo"""
    
    def _update_quality_before_sell_in(self, item):
        self._increase_quality(item, 1)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._increase_quality(item, 1)


class BackstagePassUpdater(ItemUpdater):
    """Actualiza Backstage passes - aumenta calidad según proximidad al evento"""
    
    def _update_quality_before_sell_in(self, item):
        self._increase_quality(item, 1)
        
        if item.sell_in < 11:
            self._increase_quality(item, 1)
        
        if item.sell_in < 6:
            self._increase_quality(item, 1)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            item.quality = 0


class SulfurasUpdater(ItemUpdater):
    """Actualiza Sulfuras - item legendario que nunca cambia"""
    
    def _update_sell_in(self, item):
        # Sulfuras no cambia su sell_in
        pass


class ConjuredItemUpdater(ItemUpdater):
    """Actualiza items conjurados - degradan el doble de rápido"""
    
    def _update_quality_before_sell_in(self, item):
        self._decrease_quality(item, 2)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._decrease_quality(item, 2)


class UpdaterFactory:
    """Factory para crear el updater apropiado según el tipo de item"""
    
    _updaters = {
        "Aged Brie": AgedBrieUpdater(),
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater(),
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater(),
    }
    
    @classmethod
    def get_updater(cls, item):
        """Retorna el updater apropiado para el item"""
        # Verificar si el item es conjurado
        if item.name.startswith("Conjured"):
            return ConjuredItemUpdater()
        
        # Retornar el updater específico o el normal por defecto
        return cls._updaters.get(item.name, NormalItemUpdater())


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = UpdaterFactory.get_updater(item)
            updater.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
