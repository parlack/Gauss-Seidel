# 📘 Documentación Técnica - Análisis de Distancias de Frenado

**Desarrollado por:**
- Andrés Monsivais Salazar
- Luis Andrés Salinas Lozano

---

## 📋 Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Módulos y Componentes](#módulos-y-componentes)
3. [Flujo de Datos](#flujo-de-datos)
4. [Algoritmos Implementados](#algoritmos-implementados)
5. [Validación y Manejo de Errores](#validación-y-manejo-de-errores)
6. [Interfaz Gráfica](#interfaz-gráfica)
7. [Integración de Métodos](#integración-de-métodos)
8. [Optimizaciones](#optimizaciones)

---

## 🏗️ Arquitectura del Sistema

### Estructura General

```
Frenado/
│
├── main.py                 # Punto de entrada
│
├── gui/                    # Capa de presentación
│   ├── __init__.py
│   ├── main_window.py      # Ventana principal y lógica de UI
│   └── components.py       # Componentes reutilizables
│
├── solver/                 # Capa de lógica de negocio
│   ├── __init__.py
│   ├── lagrange.py         # Solver de interpolación
│   └── biseccion.py        # Solver de bisección
│
└── utils/                  # Capa de utilidades
    ├── __init__.py
    └── validators.py       # Validación de datos
```

### Patrón de Diseño

**Arquitectura en Capas (Layered Architecture)**

1. **Capa de Presentación** (`gui/`):
   - Maneja la interfaz de usuario
   - Captura eventos del usuario
   - Muestra resultados visuales

2. **Capa de Lógica** (`solver/`):
   - Implementa los algoritmos numéricos
   - Independiente de la UI
   - Reutilizable y testeable

3. **Capa de Utilidades** (`utils/`):
   - Funciones auxiliares
   - Validación de datos
   - Servicios compartidos

**Ventajas:**
- ✅ Separación de responsabilidades
- ✅ Fácil mantenimiento
- ✅ Testeable
- ✅ Escalable

---

## 🧩 Módulos y Componentes

### 1. `main.py`

**Responsabilidad**: Punto de entrada de la aplicación

```python
def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    
def main():
    """Función principal que inicia la aplicación"""
```

**Flujo:**
1. Verificar dependencias (customtkinter, numpy)
2. Configurar apariencia de CustomTkinter
3. Crear instancia de `FrenadoApp`
4. Iniciar loop de eventos

---

### 2. `solver/lagrange.py`

**Clase**: `LagrangeSolver`

**Atributos:**
```python
self.points = []                    # Lista de tuplas (x, y)
self.basis_polynomials = []         # Polinomios base calculados
self.coefficients = []              # Coeficientes del polinomio
self.evaluation_history = []        # Historial de evaluaciones
```

**Métodos Principales:**

#### `set_points(x_values, y_values)`
Establece los puntos de interpolación.

**Validaciones:**
- Longitudes iguales
- Mínimo 2 puntos
- Sin valores x duplicados

#### `calculate_basis_polynomial(j, x)`
Calcula el polinomio base de Lagrange L_j(x).

**Fórmula:**
```
L_j(x) = ∏(i≠j) [(x - x_i) / (x_j - x_i)]
```

**Complejidad**: O(n) donde n = número de puntos

#### `interpolate(x)`
Evalúa el polinomio interpolador en x.

**Fórmula:**
```
P(x) = Σ y_j × L_j(x)
```

**Complejidad**: O(n²)

#### `generate_step_by_step(x_eval, skip_method_explanation=False)`
Genera visualización paso a paso del proceso.

**Parámetros:**
- `x_eval`: Punto donde evaluar
- `skip_method_explanation`: Si True, omite pasos explicativos (útil para iteraciones repetidas)

**Retorna**: Lista de diccionarios con pasos de visualización

**Tipos de pasos:**
- `'points'`: Muestra datos experimentales
- `'method'`: Explica el método
- `'calculation'`: Muestra cálculo de un polinomio base
- `'result'`: Muestra resultado final

---

### 3. `solver/biseccion.py`

**Clase**: `BiseccionSolver`

**Atributos:**
```python
self.tolerance = 0.001              # Tolerancia de convergencia (configurable)
self.max_iterations = 100           # Máximo de iteraciones
self.iteration_history = []         # Historial de iteraciones
self.error_history = []             # Historial de errores
```

**Métodos Principales:**

#### `solve(func, a, b)`
Resuelve f(x) = 0 usando bisección.

**Algoritmo:**
```python
while |b - a| > tolerance and iter < max_iterations:
    c = (a + b) / 2
    fc = func(c)
    
    if func(a) * fc < 0:
        b = c  # Raíz en [a, c]
    else:
        a = c  # Raíz en [c, b]
```

**Complejidad**: O(log₂((b-a)/tol))

**Convergencia**: Garantizada si f(a) × f(b) < 0

#### `generate_step_by_step(func, a, b, func_name, context)`
Genera visualización paso a paso.

**Parámetros:**
- `func`: Función a evaluar
- `a, b`: Intervalo inicial
- `func_name`: Nombre para mostrar
- `context`: Contexto del problema (incluye `dist_limit` para visualización)

**Tipos de pasos:**
- `'context'`: Contexto del problema
- `'method'`: Explicación del método
- `'initial'`: Intervalo inicial
- `'iteration'`: Cada iteración
- `'result'`: Resultado final

---

### 4. `utils/validators.py`

**Clase**: `FrenadoValidator`

**Métodos estáticos:**

#### `validate_point_data(velocidades, distancias)`
Valida datos experimentales completos.

**Validaciones:**
- Tipos numéricos
- Valores positivos
- Rangos realistas (0-300 km/h, 0-500 m)
- Sin duplicados en velocidades
- Mínimo 2 puntos

**Retorna**: `(is_valid, message, vel_array, dist_array)`

#### `validate_velocity(v_str)`
Valida una velocidad individual.

**Retorna**: `(is_valid, message, v_value)`

#### `validate_distance(d_str)`
Valida una distancia límite.

**Retorna**: `(is_valid, message, d_value)`

#### `validate_interval(a_str, b_str)`
Valida intervalo de bisección.

**Validaciones adicionales:**
- a < b
- Ancho mínimo de 1 km/h

**Retorna**: `(is_valid, message, a_value, b_value)`

#### `check_interpolation_range(x, x_array)`
Verifica si x está dentro del rango de datos.

**Retorna**: `(in_range, message)`

---

### 5. `gui/components.py`

**Componentes Personalizados:**

#### `ModernEntry`
Entry personalizado con placeholder.

**Características:**
- Placeholder gris que desaparece al escribir
- Estilo moderno
- Validación visual

#### `ModernButton`
Botón con estilo consistente.

#### `DatosExperimentalesPanel`
Panel para ingresar datos experimentales.

**Características:**
- Tabla dinámica (2-20 filas)
- Botones para agregar/quitar filas
- Validación en tiempo real
- Callback `on_change`

**Métodos:**
- `get_values()`: Retorna (velocidades, distancias)
- `set_values(data)`: Establece valores desde lista de tuplas
- `clear_all()`: Limpia todos los campos
- `add_row()`: Agrega fila
- `remove_row()`: Elimina última fila

#### `InterpolacionPanel`
Panel para interpolación de Lagrange.

**Métodos:**
- `get_velocity()`: Obtiene velocidad ingresada
- `set_velocity(v)`: Establece velocidad
- `clear()`: Limpia campo

#### `BiseccionPanel`
Panel para método de bisección.

**Características:**
- `CTkScrollableFrame` para scroll automático
- Campos: distancia límite, tolerancia, intervalo [a, b]
- Valor por defecto de tolerancia: 0.01 km/h

**Métodos:**
- `get_values()`: Retorna (dist, a, b, tol)
- `set_values(dist, a, b, tol)`: Establece valores
- `clear()`: Limpia campos y restaura tolerancia por defecto

#### `VisualizationPanel`
Panel para visualización paso a paso.

**Características:**
- Navegación entre pasos
- Barra de progreso
- Cards dinámicas según tipo de paso

**Métodos:**
- `update_visualization(steps)`: Actualiza con nueva lista de pasos
- `show_step(index)`: Muestra paso específico
- `next_step()`, `prev_step()`: Navegación
- `first_step()`, `last_step()`: Ir a extremos

**Tipos de cards:**
- `create_context_card()`: Contexto del problema
- `create_method_card()`: Explicación del método
- `create_points_card()`: Tabla de datos
- `create_calculations_card()`: Cálculos de Lagrange
- `create_iteration_card()`: Iteración de bisección
- `create_result_card()`: Resultado final
- `create_error_card()`: Mensajes de error

---

### 6. `gui/main_window.py`

**Clase**: `FrenadoApp(ctk.CTk)`

**Atributos:**
```python
self.lagrange_solver = LagrangeSolver()
self.biseccion_solver = BiseccionSolver()
self.datos_panel = DatosExperimentalesPanel(...)
self.interpolacion_panel = InterpolacionPanel(...)
self.biseccion_panel = BiseccionPanel(...)
self.visualization_panel = VisualizationPanel(...)
```

**Métodos Principales:**

#### `setup_ui()`
Configura la interfaz completa.

**Estructura:**
1. Frame principal
2. Header con título
3. TabView con 4 pestañas:
   - Datos Experimentales
   - Interpolación (Lagrange)
   - Bisección (Velocidad Segura)
   - Visualización Paso a Paso

#### `validate_data()`
Valida datos experimentales.

**Flujo:**
1. Obtener valores del panel
2. Validar con `FrenadoValidator`
3. Configurar puntos en `lagrange_solver`
4. Verificar interpolación
5. Mostrar mensaje de confirmación

#### `evaluate_interpolation()`
Evalúa interpolación de Lagrange.

**Flujo:**
1. Verificar que hay datos
2. Obtener velocidad
3. Validar velocidad
4. Verificar rango (advertir si extrapolación)
5. Generar pasos con `lagrange_solver.generate_step_by_step()`
6. Actualizar visualización
7. Cambiar a pestaña de visualización

#### `solve_biseccion()`
Resuelve problema de bisección.

**Flujo complejo - Integración de métodos:**

```python
# 1. Validar datos y parámetros
dist_limit, a, b, tol = validar_entradas()

# 2. Configurar tolerancia
self.biseccion_solver.tolerance = tol

# 3. Definir función objetivo
def f(v):
    return self.lagrange_solver.interpolate(v) - dist_limit

# 4. Verificar signos opuestos
if f(a) * f(b) > 0:
    error()

# 5. Resolver bisección
result = self.biseccion_solver.solve(f, a, b)

# 6. INTEGRACIÓN: Generar pasos intercalados
all_steps = []
for iter_data in result['history']:
    # 6.1. Generar pasos de Lagrange para este punto
    lagrange_steps = self.lagrange_solver.generate_step_by_step(
        iter_data['c'],
        skip_method_explanation=(idx > 0)  # Solo primera vez
    )
    all_steps.extend(lagrange_steps)
    
    # 6.2. Agregar paso de bisección
    biseccion_step = crear_paso_biseccion(iter_data)
    all_steps.append(biseccion_step)

# 7. Visualizar todos los pasos
self.visualization_panel.update_visualization(all_steps)
```

**Características clave:**
- ✅ Integración completa de ambos métodos
- ✅ Visualización paso a paso intercalada
- ✅ Optimización: explicación solo en primera iteración
- ✅ Contexto propagado entre métodos

---

## 🔄 Flujo de Datos

### Caso 1: Interpolación de Lagrange

```
Usuario ingresa datos
        ↓
DatosExperimentalesPanel.get_values()
        ↓
FrenadoValidator.validate_point_data()
        ↓
LagrangeSolver.set_points()
        ↓
Usuario ingresa velocidad
        ↓
InterpolacionPanel.get_velocity()
        ↓
FrenadoValidator.validate_velocity()
        ↓
LagrangeSolver.generate_step_by_step()
        ↓
VisualizationPanel.update_visualization()
        ↓
Usuario navega por pasos
```

### Caso 2: Bisección (Integrado)

```
Usuario ingresa datos (igual que caso 1)
        ↓
Usuario ingresa parámetros de bisección
        ↓
BiseccionPanel.get_values()
        ↓
Validar distancia, intervalo, tolerancia
        ↓
BiseccionSolver.tolerance = tol
        ↓
Definir f(v) = Lagrange(v) - límite
        ↓
BiseccionSolver.solve(f, a, b)
        ↓
Para cada iteración:
    ├─→ LagrangeSolver.generate_step_by_step(c)
    └─→ Crear paso de bisección
        ↓
Combinar todos los pasos
        ↓
VisualizationPanel.update_visualization()
        ↓
Usuario navega por pasos integrados
```

---

## 🧮 Algoritmos Implementados

### Interpolación de Lagrange

**Complejidad Temporal:**
- Construcción: O(n²) donde n = número de puntos
- Evaluación: O(n²) por cada punto

**Complejidad Espacial:** O(n)

**Pseudocódigo:**

```
función interpolate(x, puntos):
    resultado = 0
    n = longitud(puntos)
    
    para j desde 0 hasta n-1:
        x_j, y_j = puntos[j]
        L_j = 1
        
        para i desde 0 hasta n-1:
            si i ≠ j:
                L_j *= (x - puntos[i].x) / (x_j - puntos[i].x)
        
        resultado += y_j * L_j
    
    retornar resultado
```

**Propiedades:**
- Pasa exactamente por todos los puntos
- Único para un conjunto de puntos
- Grado del polinomio = n-1
- Puede oscilar entre puntos (fenómeno de Runge)

---

### Método de Bisección

**Complejidad Temporal:** O(log₂((b-a)/ε)) donde ε = tolerancia

**Complejidad Espacial:** O(1) (sin contar historial)

**Pseudocódigo:**

```
función biseccion(f, a, b, tolerancia):
    si f(a) * f(b) > 0:
        error "Signos no opuestos"
    
    mientras |b - a| > tolerancia:
        c = (a + b) / 2
        fc = f(c)
        
        si f(a) * fc < 0:
            b = c
        sino:
            a = c
        
        guardar_iteracion(a, b, c, fc)
    
    retornar (a + b) / 2
```

**Propiedades:**
- Convergencia garantizada si f(a) × f(b) < 0
- Error se reduce a la mitad en cada iteración
- Convergencia lineal
- Robusto y simple

**Análisis de Convergencia:**

```
Error después de n iteraciones:
ε_n = (b - a) / 2^n

Número de iteraciones necesarias:
n = log₂((b - a) / ε)

Ejemplo:
Intervalo: [20, 120] km/h → ancho = 100
Tolerancia: 0.01 km/h
n = log₂(100 / 0.01) = log₂(10000) ≈ 13.3 → 14 iteraciones
```

---

## ✅ Validación y Manejo de Errores

### Estrategia de Validación

**Capas de validación:**

1. **Validación de UI** (components.py):
   - Verificación de campos vacíos
   - Formato de entrada

2. **Validación de Negocio** (validators.py):
   - Rangos válidos
   - Consistencia de datos
   - Restricciones del dominio

3. **Validación de Algoritmo** (solvers):
   - Precondiciones del método
   - Verificación de convergencia

### Manejo de Errores

**Tipos de errores:**

1. **Errores de Usuario**:
   - Campos vacíos → `messagebox.showerror()`
   - Valores fuera de rango → Advertencia con explicación
   - Datos inconsistentes → Mensaje descriptivo

2. **Advertencias**:
   - Extrapolación → `messagebox.askyesno()` para confirmar
   - Intervalo fuera de rango → Advertencia informativa

3. **Errores de Algoritmo**:
   - Signos no opuestos en bisección → Explicación y sugerencias
   - No convergencia → Mensaje con detalles

**Ejemplo de manejo robusto:**

```python
try:
    # Validar entrada
    is_valid, message, value = validator.validate_velocity(v_str)
    if not is_valid:
        messagebox.showerror("Error", message)
        return
    
    # Verificar rango
    in_range, range_msg = validator.check_interpolation_range(value, data)
    if not in_range:
        result = messagebox.askyesno("Advertencia", f"{range_msg}\n\n¿Continuar?")
        if not result:
            return
    
    # Ejecutar algoritmo
    result = solver.interpolate(value)
    
except Exception as e:
    # Error inesperado
    messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    traceback.print_exc()
```

---

## 🎨 Interfaz Gráfica

### Tecnología: CustomTkinter

**Ventajas:**
- ✅ Apariencia moderna
- ✅ Temas (claro/oscuro)
- ✅ Widgets personalizables
- ✅ Compatible con tkinter estándar

### Diseño Visual

**Paleta de colores:**
- Azul principal: `#1f538d` (modo claro), `#4a9eff` (modo oscuro)
- Naranja: `darkorange` (bisección)
- Verde: `green` (éxito)
- Rojo: `#d32f2f` (error/resultado)
- Gris: `gray60` (texto secundario)

**Tipografía:**
- Títulos: 18-26px, bold
- Subtítulos: 14-16px, bold
- Texto normal: 12-13px
- Texto secundario: 11px

### Responsividad

**Estrategias:**
- `pack(fill="both", expand=True)` para contenido principal
- `CTkScrollableFrame` para contenido largo
- Tamaño mínimo de ventana: 1200x700
- Tamaño inicial: 1400x800

### Accesibilidad

- ✅ Contraste adecuado de colores
- ✅ Tamaños de fuente legibles
- ✅ Mensajes de error descriptivos
- ✅ Navegación clara con pestañas
- ✅ Botones con texto descriptivo

---

## 🔗 Integración de Métodos

### Diseño de la Integración

**Problema a resolver:**
Mostrar cómo Bisección usa Lagrange en cada iteración.

**Solución implementada:**

1. **Separación de responsabilidades:**
   - `LagrangeSolver`: No sabe nada de Bisección
   - `BiseccionSolver`: No sabe nada de Lagrange
   - `FrenadoApp`: Orquesta la integración

2. **Generación de pasos:**
   ```python
   # En solve_biseccion():
   all_steps = []
   
   for iter_data in history:
       # Generar pasos de Lagrange
       lagrange_steps = self.lagrange_solver.generate_step_by_step(
           iter_data['c'],
           skip_method_explanation=(idx > 0)
       )
       all_steps.extend(lagrange_steps)
       
       # Agregar paso de bisección
       biseccion_step = {...}
       all_steps.append(biseccion_step)
   ```

3. **Optimización:**
   - Primera iteración: Muestra explicación completa de Lagrange
   - Iteraciones siguientes: Solo cálculos, sin explicación

4. **Propagación de contexto:**
   - `dist_limit` se pasa a cada paso de iteración
   - Permite calcular d(v) en la visualización

### Ventajas del Diseño

- ✅ **Modularidad**: Solvers independientes
- ✅ **Reutilizabilidad**: Cada solver funciona solo
- ✅ **Testabilidad**: Fácil de probar por separado
- ✅ **Extensibilidad**: Fácil agregar más métodos
- ✅ **Claridad**: Separación clara de responsabilidades

---

## ⚡ Optimizaciones

### Optimizaciones Implementadas

1. **Visualización:**
   - Explicación del método solo en primera iteración
   - Reduce pasos de ~200 a ~100 en 10 iteraciones
   - Mejora significativa en tiempo de generación

2. **Cálculo de Lagrange:**
   - Evaluación directa sin almacenar polinomio completo
   - Complejidad O(n²) inevitable, pero eficiente en práctica

3. **Validación:**
   - Validación temprana antes de cálculos pesados
   - Evita procesamiento innecesario

4. **Interfaz:**
   - `CTkScrollableFrame` solo donde es necesario
   - Actualización de UI solo cuando cambia el paso
   - Uso de `update_idletasks()` para responsividad

### Posibles Optimizaciones Futuras

1. **Caché de Lagrange:**
   ```python
   # Cachear polinomios base si se evalúan muchos puntos
   @lru_cache(maxsize=128)
   def calculate_basis_polynomial_cached(self, j, x):
       ...
   ```

2. **Paralelización:**
   - Cálculo de polinomios base en paralelo (para n grande)
   - Generación de pasos en background thread

3. **Interpolación más eficiente:**
   - Forma de Newton (más eficiente para múltiples evaluaciones)
   - Splines cúbicos (mejor comportamiento)

---

## 🧪 Testing

### Estrategia de Testing (Recomendada)

**Tests Unitarios:**

```python
# test_lagrange.py
def test_lagrange_two_points():
    solver = LagrangeSolver()
    solver.set_points([0, 1], [0, 1])
    assert abs(solver.interpolate(0.5) - 0.5) < 1e-6

def test_lagrange_exact_points():
    solver = LagrangeSolver()
    points = [(20, 6), (40, 16), (60, 32)]
    solver.set_points([p[0] for p in points], [p[1] for p in points])
    for x, y in points:
        assert abs(solver.interpolate(x) - y) < 1e-6

# test_biseccion.py
def test_biseccion_simple():
    solver = BiseccionSolver()
    result = solver.solve(lambda x: x - 5, 0, 10)
    assert abs(result['root'] - 5) < solver.tolerance

def test_biseccion_convergence():
    solver = BiseccionSolver()
    result = solver.solve(lambda x: x**2 - 4, 0, 3)
    assert result['converged'] == True
    assert abs(result['root'] - 2) < solver.tolerance
```

**Tests de Integración:**

```python
def test_integration_lagrange_biseccion():
    # Simular flujo completo
    lagrange = LagrangeSolver()
    biseccion = BiseccionSolver()
    
    # Datos de prueba
    lagrange.set_points([20, 40, 60], [6, 16, 32])
    
    # Función objetivo
    def f(v):
        return lagrange.interpolate(v) - 20
    
    # Resolver
    result = biseccion.solve(f, 20, 60)
    
    # Verificar
    assert result['success'] == True
    assert 20 < result['root'] < 60
```

---

## 📊 Métricas de Código

**Estadísticas aproximadas:**

- **Líneas de código total**: ~3500
  - `gui/components.py`: ~1160 líneas
  - `gui/main_window.py`: ~620 líneas
  - `solver/lagrange.py`: ~315 líneas
  - `solver/biseccion.py`: ~220 líneas
  - `utils/validators.py`: ~180 líneas

- **Complejidad ciclomática**: Baja-Media
  - Funciones bien estructuradas
  - Máximo ~15 por función compleja

- **Cobertura de validación**: Alta
  - Validación en múltiples capas
  - Manejo exhaustivo de errores

---

## 🔐 Seguridad

### Consideraciones de Seguridad

1. **Validación de Entrada:**
   - Todos los inputs son validados
   - Rangos realistas para prevenir overflow
   - Protección contra división por cero

2. **Límites de Recursos:**
   - Máximo 100 iteraciones en bisección
   - Máximo 20 puntos de datos
   - Previene consumo excesivo de memoria/CPU

3. **Manejo de Excepciones:**
   - Try-catch en todas las operaciones críticas
   - Mensajes de error sin información sensible
   - Logging de errores para debugging

---

## 📝 Convenciones de Código

### Estilo

- **PEP 8**: Estilo estándar de Python
- **Docstrings**: Formato Google
- **Type Hints**: Usados donde es apropiado
- **Nombres**: Descriptivos en español (contexto educativo)

### Ejemplo de Docstring:

```python
def interpolate(self, x: float) -> float:
    """
    Evalúa el polinomio interpolador en un punto específico.
    
    Args:
        x: Velocidad donde evaluar (km/h)
        
    Returns:
        Distancia de frenado interpolada (metros)
        
    Raises:
        ValueError: Si no hay puntos definidos
        
    Example:
        >>> solver = LagrangeSolver()
        >>> solver.set_points([20, 40], [6, 16])
        >>> solver.interpolate(30)
        11.0
    """
```

---

## 🚀 Deployment

### Requisitos del Sistema

**Mínimos:**
- Python 3.7+
- 100 MB de espacio en disco
- 512 MB de RAM
- Resolución mínima: 1200x700

**Recomendados:**
- Python 3.9+
- 200 MB de espacio
- 1 GB de RAM
- Resolución: 1920x1080

### Instalación

```bash
# 1. Clonar repositorio
git clone [URL]
cd Frenado

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

### Distribución

**Opción 1: PyInstaller**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="FrenadoAnalisis" main.py
```

**Opción 2: cx_Freeze**
```bash
pip install cx_Freeze
python setup.py build
```

---

## 📚 Referencias Técnicas

### Algoritmos

- Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis* (9th ed.). Brooks/Cole.
- Press, W. H., et al. (2007). *Numerical Recipes* (3rd ed.). Cambridge University Press.

### Python y GUI

- CustomTkinter Documentation: https://customtkinter.tomschimansky.com/
- NumPy Documentation: https://numpy.org/doc/

### Patrones de Diseño

- Gamma, E., et al. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*.
- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*.

---

## 🤝 Contribución

### Guía para Desarrolladores

**Para agregar un nuevo método numérico:**

1. Crear solver en `solver/nuevo_metodo.py`
2. Implementar clase con métodos estándar:
   - `solve()`: Algoritmo principal
   - `generate_step_by_step()`: Visualización
3. Agregar panel en `gui/components.py`
4. Integrar en `gui/main_window.py`
5. Actualizar documentación

**Ejemplo de estructura:**

```python
# solver/nuevo_metodo.py
class NuevoMetodoSolver:
    def __init__(self):
        self.parametros = {}
    
    def solve(self, ...):
        """Implementación del algoritmo"""
        pass
    
    def generate_step_by_step(self, ...):
        """Generación de pasos para visualización"""
        pass
```

---

## 📞 Soporte Técnico

### Debugging

**Habilitar modo debug:**

```python
# En main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Logs útiles:**
- Valores de entrada
- Resultados intermedios
- Errores de validación
- Tiempos de ejecución

### Problemas Comunes

1. **ImportError: No module named 'customtkinter'**
   - Solución: `pip install customtkinter`

2. **Ventana no se muestra**
   - Verificar que no hay errores en consola
   - Verificar versión de Python (>= 3.7)

3. **Cálculos incorrectos**
   - Verificar datos de entrada
   - Revisar validación de rangos
   - Comprobar convergencia

---

## 🎓 Conclusión Técnica

Este proyecto demuestra:

- ✅ **Arquitectura limpia** con separación de responsabilidades
- ✅ **Integración efectiva** de múltiples métodos numéricos
- ✅ **Interfaz moderna** y accesible
- ✅ **Código mantenible** y extensible
- ✅ **Validación robusta** y manejo de errores
- ✅ **Documentación completa** para usuarios y desarrolladores

**Ideal para:**
- Aprendizaje de métodos numéricos
- Ejemplo de arquitectura de software
- Base para proyectos similares
- Herramienta educativa práctica

---

*Documentación técnica completa - Noviembre 2025*

