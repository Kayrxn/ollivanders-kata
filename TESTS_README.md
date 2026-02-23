# Guía de Tests - Gilded Rose Kata

## 📊 Suite de Tests Profesional con Pytest

Se han creado **108 tests parametrizados** organizados por tipo de item con markers para ejecución selectiva.

## 🚀 Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidas
├── test_normal_items.py     # Tests para items normales (18 tests)
├── test_aged_brie.py        # Tests para Aged Brie (15 tests)
├── test_sulfuras.py         # Tests para Sulfuras (11 tests)
├── test_backstage_passes.py # Tests para Backstage passes (22 tests)
├── test_conjured_items.py   # Tests para items Conjured (25 tests)
└── test_integration.py      # Tests de integración (17 tests)
```

## 🏃 Ejecutar Tests

### Todos los tests
```powershell
.\venv\Scripts\Activate.ps1
pytest tests/ -v
```

### Por markers (categorías)

```powershell
# Tests de items normales
pytest tests/ -m normal -v

# Tests de Aged Brie
pytest tests/ -m aged_brie -v

# Tests de Sulfuras
pytest tests/ -m sulfuras -v

# Tests de Backstage passes
pytest tests/ -m backstage -v

# Tests de items Conjured (nueva funcionalidad)
pytest tests/ -m conjured -v

# Tests de integración
pytest tests/ -m integration -v

# Tests de casos límite
pytest tests/ -m edge_case -v

# Tests de regresión
pytest tests/ -m regression -v

# Tests relacionados con calidad
pytest tests/ -m quality -v

# Tests relacionados con sell_in
pytest tests/ -m sell_in -v
```

### Combinar markers

```powershell
# Tests de conjured Y edge cases
pytest tests/ -m "conjured and edge_case" -v

# Tests de calidad O sell_in
pytest tests/ -m "quality or sell_in" -v

# Excluir tests lentos de integración
pytest tests/ -m "not integration" -v
```

### Por archivo específico

```powershell
# Solo tests de Conjured
pytest tests/test_conjured_items.py -v

# Solo tests de integración
pytest tests/test_integration.py -v
```

### Con cobertura

```powershell
pytest tests/ --cov=gilded_rose --cov-report=html
```

## 📝 Markers Disponibles

| Marker | Descripción |
|--------|-------------|
| `normal` | Tests para items normales |
| `aged_brie` | Tests para Aged Brie |
| `sulfuras` | Tests para Sulfuras (legendario) |
| `backstage` | Tests para Backstage passes |
| `conjured` | Tests para items Conjured |
| `quality` | Tests relacionados con calidad |
| `sell_in` | Tests relacionados con sell_in |
| `integration` | Tests de integración con múltiples items |
| `edge_case` | Tests de casos límite |
| `regression` | Tests de regresión |

## 🎯 Características de los Tests

### ✨ Tests Parametrizados
Los tests usan `@pytest.mark.parametrize` para probar múltiples casos con el mismo código:

```python
@pytest.mark.parametrize("initial_quality,days,expected_quality", [
    (20, 1, 18),   # Caso 1
    (20, 5, 10),   # Caso 2
    (10, 5, 0),    # Caso 3
])
def test_quality_degrades_twice_as_fast(self, gilded_rose, initial_quality, days, expected_quality):
    # Un solo test, múltiples casos
```

### 🔧 Fixtures Reutilizables
Fixtures definidas en `conftest.py` para crear items fácilmente:

```python
def test_example(aged_brie, gilded_rose):
    gr = gilded_rose([aged_brie])
    gr.update_quality()
    assert aged_brie.quality == 21
```

### 📊 Organización por Clases
Tests agrupados en clases para mejor organización:

```python
class TestConjuredItems:
    """Tests para items Conjured - degradan el doble de rápido"""
    
    def test_quality_degrades_twice_as_fast(self, ...):
        ...
    
    def test_quality_degrades_four_times_after_sell_date(self, ...):
        ...
```

## 📈 Resultados

```
============================= 108 passed in 0.29s =============================
```

✅ **100% de tests pasando**
- 18 tests para items normales
- 15 tests para Aged Brie  
- 11 tests para Sulfuras
- 22 tests para Backstage passes
- 25 tests para items Conjured (nueva funcionalidad)
- 17 tests de integración y regresión

## 🎓 Ejemplos de Uso

### Desarrollo de nueva funcionalidad
```powershell
# Solo ejecutar tests relevantes durante desarrollo
pytest tests/test_conjured_items.py -v
```

### Verificación rápida
```powershell
# Tests de integración + edge cases
pytest tests/ -m "integration or edge_case" -v
```

### CI/CD
```powershell
# Todos los tests con output detallado
pytest tests/ -v --tb=short --strict-markers
```

## 🛠️ Configuración

La configuración está en [pytest.ini](pytest.ini):
- Output verbose por defecto
- Strict markers (no permite markers no definidos)
- Traceback corto para errores
- Resumen de todos los tests

## 📚 Cobertura de Tests

Los tests cubren:
- ✅ Degradación normal de calidad
- ✅ Degradación doble después de expirar
- ✅ Calidad nunca negativa
- ✅ Calidad nunca mayor a 50
- ✅ Items legendarios inmutables
- ✅ Backstage passes con incrementos progresivos
- ✅ Items Conjured con degradación doble
- ✅ Casos límite (valores 0, 50, negativos)
- ✅ Múltiples items simultáneos
- ✅ Simulaciones de largo plazo
