# Especificaciones de la Rosa Dorada (Gilded Rose) - Sistema Refactorizado

Bienvenido al equipo **Gilded Rose**.
Como sabrás, somos una pequeña posada ubicada estratégicamente en una prestigiosa ciudad, atendida por la amable Allison. También compramos y vendemos mercadería de alta calidad. Por desgracia, nuestra mercadería va bajando de calidad (`Quality`) a medida que se aproxima la fecha de venta.

Tenemos un sistema instalado que actualiza automáticamente nuestro inventario. Este sistema fue originalmente desarrollado por un tipo serio y práctico llamado Leeroy, que ahora se encuentra en otras aventuras. **Este sistema ha sido completamente refactorizado para mejorar su mantenibilidad y escalabilidad.**

## 📋 Especificaciones de Negocio

### Propiedades de los artículos

- Todos los artículos (`Item`) tienen una propiedad `sell_in` que denota el número de días que tenemos para venderlo
- Todos los artículos (`Item`) tienen una propiedad `quality` que denota cuán valioso es el artículo
- Al final de cada día, nuestro sistema actualiza ambos valores para cada artículo

### Reglas de actualización

- Una vez que ha pasado la fecha recomendada de venta (`sell_in < 0`), la calidad (`quality`) se degrada al **doble de velocidad**
- La `calidad` de un artículo **nunca es negativa** (mínimo 0)
- La calidad de un artículo **no puede superar 50** (excepto Sulfuras)

### Tipos de artículos especiales

#### 🧀 Aged Brie (Queso Brie Envejecido)
- **Comportamiento:** Incrementa su calidad con el tiempo (envejece bien)
- **Antes de expiración:** Calidad aumenta `+1` por día
- **Después de expiración:** Calidad aumenta `+2` por día
- **Límite máximo:** 50

#### ⚔️ Sulfuras (Legendario)
- **Comportamiento:** Objeto legendario e inmutable
- `sell_in` nunca cambia
- `quality` nunca cambia (siempre 80)
- No envejece ni se degrada

#### 🎫 Backstage Passes (Entradas al Concierto)
- **Comportamiento:** Aumenta valor conforme se acerca el evento
- **Más de 10 días:** `+1` quality por día
- **Entre 10 y 6 días:** `+2` quality por día
- **Entre 5 y 1 días:** `+3` quality por día
- **Después del evento:** Cae a `0` quality
- **Límite máximo:** 50

#### 🪄 Conjured Items (Artículos Conjurados)
- **Comportamiento:** Degradación rápida por naturaleza mágica
- **Antes de expiración:** Calidad disminuye `-2` por día
- **Después de expiración:** Calidad disminuye `-4` por día
- **Límite mínimo:** 0

#### 📦 Items Normales
- **Comportamiento:** Degradación estándar
- **Antes de expiración:** Calidad disminuye `-1` por día
- **Después de expiración:** Calidad disminuye `-2` por día
- **Límite:** 0-50

---

## 🏗️ Arquitectura y Refactorización

### El Problema Original: El Gran If/Else

El código original contenía un **único método `updateQuality()` monolítico** con una cadena masiva de condicionales `if/else`:

```python
# ANTES (Código acoplado y difícil de mantener):
if item.name == "Aged Brie":
    # ... lógica para Aged Brie
elif item.name == "Backstage passes...":
    # ... lógica para Backstage
elif item.name == "Sulfuras...":
    # ... lógica para Sulfuras
elif item.name.startswith("Conjured"):
    # ... lógica para Conjured
else:
    # ... lógica normal
```

### Problemas de este enfoque:

1. **Alto acoplamiento:** Todo estaba entrelazado en un único método
2. **Difícil de mantener:** Cambiar un tipo de item requería modificar el método principal
3. **Violación del Principio de Responsabilidad Única:** Un método hacía todo
4. **Difícil de testear:** Los tests tenían que verificar toda la lógica mezclada
5. **Escalabilidad:** Añadir nuevos tipos de items requería modificar el método principal
6. **Riesgo de regresiones:** Cambios en un tipo afectaban potencialmente a otros

### ✨ La Solución: Patrón Strategy + Factory

Se implementó una arquitectura limpia basada en dos patrones de diseño:

1. **Strategy Pattern:** Cada tipo de item tiene su propia clase de actualización
2. **Factory Pattern:** Una factory decide qué actualizer usar según el tipo de item

**Ventajas:**

- ✅ Código desacoplado y modular
- ✅ Cada clase tiene una única responsabilidad
- ✅ Fácil de extender 
- ✅ Tests unitarios por tipo de item
- ✅ Bajo acoplamiento entre componentes

---

## 📚 Descripción de las clases

### Clase `Item`

```python
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name          # Nombre del artículo
        self.sell_in = sell_in    # Días para vender
        self.quality = quality    # Valor del artículo
```

**Responsabilidad:** Representa un artículo del inventario.
- Propiedades básicas del item
- No contiene lógica de actualización (separación de responsabilidades)
- Esta clase no debe ser modificada por restricción del kata

---

### Clase `ItemUpdater` (Clase Base)

```python
class ItemUpdater:
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
```

**Responsabilidad:** Clase base abstracta que define la estructura común para actualizar items.

**Métodos principales:**

- `update(item)` - Orquesta el proceso de actualización en 3 fases
- `_update_quality_before_sell_in(item)` - Hook para cambios antes de expiración
- `_update_sell_in(item)` - Decrementa `sell_in` (sobrescribible)
- `_update_quality_after_sell_in(item)` - Hook para cambios después de expiración
- `_increase_quality(item, amount)` - Aumenta calidad respetando máximo de 50
- `_decrease_quality(item, amount)` - Disminuye calidad respetando mínimo de 0

**Flujo de ejecución normal:**
1. Se actualiza calidad antes de expiración
2. Se decrementa `sell_in`
3. Se actualiza calidad después de expiración (si `sell_in` es negativo)

---

### Clase `NormalItemUpdater`

```python
class NormalItemUpdater(ItemUpdater):
    """Actualiza items normales"""
    
    def _update_quality_before_sell_in(self, item):
        self._decrease_quality(item, 1)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._decrease_quality(item, 1)
```

**Responsabilidad:** Actualiza artículos normales (los que no tienen comportamiento especial).

**Comportamiento:**
- Decrementa calidad `-1` mientras `sell_in >= 0`
- Decrementa calidad `-1` adicional más cuando `sell_in < 0`
- Total de degradación después de expiración: `-2` por día

---

### Clase `AgedBrieUpdater`

```python
class AgedBrieUpdater(ItemUpdater):
    """Actualiza Aged Brie - aumenta su calidad con el tiempo"""
    
    def _update_quality_before_sell_in(self, item):
        self._increase_quality(item, 1)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._increase_quality(item, 1)
```

**Responsabilidad:** Actualiza Aged Brie con su comportamiento especial de envejecimiento.

**Comportamiento:**
- Aumenta calidad `+1` mientras `sell_in >= 0`
- Aumenta calidad `+1` adicional cuando `sell_in < 0`
- Total de aumento después de expiración: `+2` por día
- Respeta máximo de 50

---

### Clase `BackstagePassUpdater`

```python
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
```

**Responsabilidad:** Actualiza entradas al backstage con bonificación según proximidad del evento.

**Comportamiento:**
- Base: `+1` quality siempre
- Entre 10 y 6 días: `+1` additional = `+2` total
- Entre 5 y 1 días: `+1` additional = `+3` total
- Después del evento: `quality = 0` (pierde todo valor)
- Respeta máximo de 50 antes de expiración

---

### Clase `SulfurasUpdater`

```python
class SulfurasUpdater(ItemUpdater):
    """Actualiza Sulfuras - item legendario que nunca cambia"""
    
    def _update_sell_in(self, item):
        # Sulfuras no cambia su sell_in
        pass
```

**Responsabilidad:** Actualiza Sulfuras (que en realidad no hace nada).

**Comportamiento:**
- Sobrescribe `_update_sell_in()` para no cambiar nada
- `sell_in` permanece constante
- `quality` permanece constante en 80
- Item legendario e inmutable

---

### Clase `ConjuredItemUpdater`

```python
class ConjuredItemUpdater(ItemUpdater):
    """Actualiza items conjurados - degradan el doble de rápido"""
    
    def _update_quality_before_sell_in(self, item):
        self._decrease_quality(item, 2)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._decrease_quality(item, 2)
```

**Responsabilidad:** Actualiza artículos conjurados con degradación acelerada.

**Comportamiento:**
- Decrementa calidad `-2` mientras `sell_in >= 0`
- Decrementa calidad `-2` adicional cuando `sell_in < 0`
- Total de degradación después de expiración: `-4` por día
- Degrada el doble de rápido que items normales

---

### Clase `UpdaterFactory`

```python
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
        if item.name.startswith("Conjured"):
            return ConjuredItemUpdater()
        
        return cls._updaters.get(item.name, NormalItemUpdater())
```

**Responsabilidad:** Factory que decide qué updater usar basándose en el tipo de item.

**Métodos:**

- `get_updater(item)` - Retorna la instancia correcta del updater
  - Busca items especiales por nombre exacto (Aged Brie, Backstage, Sulfuras)
  - Detecta items conjurados por prefijo "Conjured"
  - Por defecto retorna NormalItemUpdater para items desconocidos

**Ventajas del Factory Pattern:**
- Punto centralizado de decisión
- Fácil agregar nuevos tipos de items
- Desacoplamiento entre GildedRose y los updaters específicos

---

### Clase `GildedRose`

```python
class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = UpdaterFactory.get_updater(item)
            updater.update(item)
```

**Responsabilidad:** Orquestador principal del sistema. Responsable por actualizar todo el inventario.

**Métodos:**

- `__init__(items)` - Inicializa con la lista de items
- `update_quality()` - Actualiza la calidad y sell_in de todos los items
  - Itera sobre cada item
  - Obtiene el updater correcto del factory
  - Ejecuta el update del item

**Beneficio de esta refactorización:**
El método `update_quality()` es ahora **muy simple y legible** - solo 4 líneas de código que delegan la responsabilidad a los especializadores.

---

## 🧪 Estructura de Tests

El proyecto incluye tests exhaustivos organizados por tipo de item:

- `test_normal_items.py` - Tests para items normales
- `test_aged_brie.py` - Tests para Aged Brie
- `test_backstage_passes.py` - Tests para Backstage Passes
- `test_sulfuras.py` - Tests para Sulfuras
- `test_conjured_items.py` - Tests para Items Conjurados
- `test_integration.py` - Tests de integración del sistema completo

---

## 📊 Diagrama de clases

```
┌─────────────────────────────┐
│         Item                │
├─────────────────────────────┤
│ - name: str                 │
│ - sell_in: int              │
│ - quality: int              │
└─────────────────────────────┘
           ▲
           │ contiene
           │
┌─────────────────────────────┐
│      GildedRose             │
├─────────────────────────────┤
│ + update_quality()          │
└─────────────────────────────┘
           │ usa
           ▼
┌─────────────────────────────┐
│    UpdaterFactory           │
├─────────────────────────────┤
│ + get_updater(item): Updater│
└─────────────────────────────┘
           │ retorna
           ▼
     ┌─────────────────────────────────────────────────────┐
     │           ItemUpdater (Base)                        │
     ├─────────────────────────────────────────────────────┤
     │ + update(item)                                      │
     │ # _update_quality_before_sell_in(item)             │
     │ # _update_sell_in(item)                            │
     │ # _update_quality_after_sell_in(item)              │
     │ # _increase_quality(item, amount)                  │
     │ # _decrease_quality(item, amount)                  │
     └─────────────────────────────────────────────────────┘
                    ▲
        ┌───────────┼───────────┬────────────┬─────────────┐
        │           │           │            │             │
   ┌────┴───┐ ┌────┴────┐ ┌───┴─────┐ ┌────┴────┐ ┌──────┴───┐
   │ Normal │ │AgedBrie │ │Backstage│ │Conjured │ │Sulfuras  │
   │Updater │ │ Updater │ │ Updater │ │ Updater │ │ Updater  │
   └────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘
```

---

## 🚀 Cómo usar el sistema

### Crear un inventario y actualizar

```python
from src.gilded_rose import GildedRose, Item

# Crear items
items = [
    Item("+5 Dexterity Vest", sell_in=10, quality=20),
    Item("Aged Brie", sell_in=2, quality=0),
    Item("Conjured Mana Cake", sell_in=3, quality=6),
]

# Crear instancia de GildedRose
gilded_rose = GildedRose(items)

# Actualizar cada día
gilded_rose.update_quality()
```

### Agregar un nuevo tipo de item

1. Crear una clase que extienda `ItemUpdater`
2. Implementar métodos `_update_quality_before_sell_in()` y `_update_quality_after_sell_in()`
3. Registrar en `UpdaterFactory._updaters` o agregar lógica en `get_updater()`

Ejemplo:

```python
class MagicStaffUpdater(ItemUpdater):
    """Actualiza Magic Staff - aumenta el doble que Aged Brie"""
    
    def _update_quality_before_sell_in(self, item):
        self._increase_quality(item, 2)
    
    def _update_quality_after_sell_in(self, item):
        if item.sell_in < 0:
            self._increase_quality(item, 2)

# Registrar en factory
UpdaterFactory._updaters["Mystical Staff"] = MagicStaffUpdater()
```

---

## 📝 Notas Importantes

- Un artículo nunca puede tener una calidad superior a `50` (excepto Sulfuras)
- Sulfuras posee una calidad inmutable de `80`
- La cantidad de calidad nunca puede ser negativa (mínimo 0)
- La clase `Item` **no debe ser modificada** (restricción del kata)