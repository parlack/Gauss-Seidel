# Guía de Solución de Problemas - Método de Bisección

## Errores Comunes y Soluciones

### ❌ Error: "unsupported operand type(s) for '*': 'NoneType' and 'float'"

**Causa**: La función no se puede evaluar correctamente en algún punto del intervalo.

**Soluciones**:
1. **Verificar la función**:
   - ✅ Correcto: `x**2 - 4`
   - ❌ Incorrecto: `1/(x-2)` (división por cero en x=2)
   - ❌ Incorrecto: `log(x)` con intervalo [-1, 1] (logaritmo de negativo)

2. **Verificar el intervalo**:
   - Asegúrate de que la función esté definida en todo el intervalo [xl, xu]
   - Evita puntos donde la función no existe

### ❌ Error: "f(xl) y f(xu) deben tener signos opuestos"

**Causa**: El método de bisección requiere que f(xl) × f(xu) < 0.

**Soluciones**:
1. **Buscar un intervalo válido**:
   ```
   Para f(x) = x² - 4:
   ✅ Usar [-3, -1] (f(-3) = 5 > 0, f(-1) = -3 < 0)
   ✅ Usar [1, 3] (f(1) = -3 < 0, f(3) = 5 > 0)
   ❌ No usar [2, 4] (ambos positivos)
   ```

2. **Graficar mentalmente la función** para encontrar cambios de signo

### ❌ Error: "La función no está definida en..."

**Causa**: División por cero, logaritmo de negativo, raíz de negativo, etc.

**Soluciones comunes**:

#### División por Cero
```
❌ f(x) = 1/(x-2) con intervalo [1, 3]
✅ f(x) = 1/(x-2) con intervalo [2.1, 3]
```

#### Logaritmo de Negativo
```
❌ f(x) = log(x) con intervalo [-1, 1]
✅ f(x) = log(x) con intervalo [0.1, 2]
```

#### Raíz Cuadrada de Negativo
```
❌ f(x) = sqrt(x-5) con intervalo [1, 4]
✅ f(x) = sqrt(x-5) con intervalo [5.1, 7]
```

## Funciones Problemáticas Comunes

### 1. Funciones Racionales
```python
# Problema: f(x) = (x-1)/(x-2)
# División por cero en x=2

# Solución: Usar intervalos que eviten x=2
# Intervalo válido: [-1, 1.5] o [2.5, 4]
```

### 2. Funciones Logarítmicas
```python
# Problema: f(x) = log(x) - 1
# Logaritmo no definido para x ≤ 0

# Solución: Usar solo x > 0
# Intervalo válido: [0.1, 5]
```

### 3. Funciones Trigonométricas con Transformaciones
```python
# Problema: f(x) = 1/sin(x)
# División por cero cuando sin(x) = 0

# Solución: Evitar múltiplos de π
# Intervalo válido: [0.1, 3] (evita π ≈ 3.14)
```

## Consejos para Funciones Exitosas

### ✅ Funciones Recomendadas para Empezar
1. **Polinomios**: `x**3 - 2*x - 5`
2. **Exponenciales simples**: `exp(-x) - x`
3. **Trigonométricas básicas**: `cos(x) - x`

### ✅ Intervalos Típicos que Funcionan Bien
- **Para polinomios cúbicos**: [-5, 5]
- **Para exp(-x) - x**: [0, 1]
- **Para cos(x) - x**: [0, 1]
- **Para sin(x) - 0.5**: [0, π]

### ✅ Estrategias para Encontrar Intervalos

1. **Método de prueba y error**:
   ```python
   # Evaluar la función en varios puntos
   f(-2) = ?
   f(-1) = ?
   f(0) = ?
   f(1) = ?
   f(2) = ?
   
   # Buscar cambios de signo
   ```

2. **Usar el botón "Ejemplo"**:
   - Carga ejemplos predefinidos que funcionan
   - Modifica gradualmente para aprender

3. **Validar antes de resolver**:
   - Siempre usar el botón "Validar" primero
   - Lee los mensajes de error cuidadosamente

## Ejemplos Paso a Paso

### Ejemplo 1: Función Polinomial
```
Función: x**3 - 2*x - 5
Intervalo inicial: [1, 3]

Verificación:
f(1) = 1 - 2 - 5 = -6 < 0
f(3) = 27 - 6 - 5 = 16 > 0
f(1) × f(3) = (-6) × (16) < 0 ✅
```

### Ejemplo 2: Función Exponencial
```
Función: exp(-x) - x
Intervalo inicial: [0, 1]

Verificación:
f(0) = e⁰ - 0 = 1 - 0 = 1 > 0
f(1) = e⁻¹ - 1 ≈ 0.368 - 1 = -0.632 < 0
f(0) × f(1) = (1) × (-0.632) < 0 ✅
```

### Ejemplo 3: Función Trigonométrica
```
Función: cos(x) - x
Intervalo inicial: [0, 1]

Verificación:
f(0) = cos(0) - 0 = 1 - 0 = 1 > 0
f(1) = cos(1) - 1 ≈ 0.540 - 1 = -0.460 < 0
f(0) × f(1) = (1) × (-0.460) < 0 ✅
```

## Mensajes de Error y Significados

| Error | Significado | Solución |
|-------|-------------|----------|
| "NoneType and float" | Función retorna None | Revisar definición de función |
| "signos opuestos" | Mismo signo en extremos | Cambiar intervalo |
| "no está definida" | Función indefinida en punto | Ajustar intervalo |
| "división por cero" | División por cero | Evitar punto problemático |
| "logaritmo de negativo" | log(x) con x ≤ 0 | Usar solo x > 0 |

## Parámetros Recomendados

### Tolerancia
- **Para aprendizaje**: 0.01% (rápido)
- **Para precisión**: 0.000001% (predeterminado)
- **Para alta precisión**: 0.0000001%

### Máximo de Iteraciones
- **Funciones simples**: 50
- **Uso normal**: 100 (predeterminado)
- **Funciones complejas**: 200

## Contacto y Soporte

Si encuentras un problema no listado aquí, verifica:

1. ✅ **Función bien escrita**: Sin caracteres extraños
2. ✅ **Intervalo válido**: f(xl) × f(xu) < 0
3. ✅ **Función definida**: En todo el intervalo
4. ✅ **Parámetros razonables**: Tolerancia y iteraciones

**¡Usa el botón "Ejemplo" para ver casos que funcionan garantizados!**
