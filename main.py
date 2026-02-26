"""
Main execution file for the Gilded Rose inventory system.
Simulates the passage of days and shows how item quality and sell_in values change.
"""

from src.gilded_rose import GildedRose, Item


def print_inventory(items, day):
    """Prints the current state of the inventory"""
    print(f"\n{'='*80}")
    print(f"Dia {day}")
    print(f"{'='*80}")
    print(f"{'Articulo':<50} {'Caducidad':>12} {'Calidad':>10}")
    print(f"{'-'*80}")
    
    for item in items:
        print(f"{item.name:<50} {item.sell_in:>12} {item.quality:>10}")


def main():
    """Main execution function"""
    
    # Crear inventario con diferentes tipos de articulos
    items = [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),
    ]
    
    # Número de días a simular
    days = 11
    
    # Crear instancia de GildedRose
    gilded_rose = GildedRose(items)
    
    # Mostrar inventario inicial
    print("\n" + "="*80)
    print("INVENTARIO - OLLIVANDERS - SISTEMA GILDED ROSE")
    print("="*80)
    
    # Mostrar estado inicial (día 0)
    print_inventory(items, 0)
    
    # Simular el paso de los días
    for day in range(1, days):
        gilded_rose.update_quality()
        print_inventory(items, day)
    
    # Resumen final
    print(f"\n{'='*80}")
    print("LEYENDA:")
    print(f"{'-'*80}")
    print("Articulos normales: Pierden 1 de calidad por dia (2 despues de caducar)")
    print("Aged Brie: Aumenta calidad con el tiempo")
    print("Backstage passes: Aumentan calidad segun proximidad al evento (0 despues)")
    print("Sulfuras: Legendario, nunca cambia")
    print("Conjured: Pierden 2 de calidad por dia (4 despues de caducar)")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
