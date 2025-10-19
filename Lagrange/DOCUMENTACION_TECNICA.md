# Documentación Técnica - Interpolación de Lagrange

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Módulo Solver](#módulo-solver)
4. [Módulo GUI](#módulo-gui)
5. [Módulo Utils](#módulo-utils)
6. [Flujo de Ejecución](#flujo-de-ejecución)
7. [Algoritmos Implementados](#algoritmos-implementados)
8. [Optimizaciones](#optimizaciones)

---

## Introducción

Este proyecto implementa el método de interpolación polinómica de Lagrange con una interfaz gráfica moderna. El código está organizado en módulos separados siguiendo el patrón de arquitectura MVC (Modelo-Vista-Controlador).

### Objetivo

Proporcionar una herramienta educativa que permita:
- Ingresar puntos de interpolación de forma intuitiva
- Visualizar el proceso de cálculo completo
- Mostrar las fracciones en notación matemática estándar
- Evaluar el polinomio interpolador en cualquier punto

---

## Arquitectura del Proyecto

```
Lagrange/
│
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias
│
├── solver/                    # Lógica matemática
│   └── lagrange.py           # Implementación del método
│
├── gui/                       # Interfaz gráfica
│   ├── main_window.py        # Ventana principal
│   └── components.py         # Componentes personalizados
│
└── utils/                     # Utilidades
    └── validators.py         # Validación de datos
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una función específica
2. **Reutilización**: Componentes diseñados para ser reutilizables
3. **Extensibilidad**: Fácil agregar nuevas funcionalidades
4. **Mantenibilidad**: Código limpio y bien documentado

---

## Módulo Solver

### Archivo: `solver/lagrange.py`

Este módulo contiene la implementación matemática del método de Lagrange.

#### Clase: `LagrangeSolver`

```python
class LagrangeSolver:
    """
    Implementa el método de interpolación de Lagrange.
    
    Atributos:
        points (List[Tuple[float, float]]): Lista de puntos (x, y)
    """
```

##### Constructor

```python
def __init__(self):
    """Inicializa el solver sin puntos."""
    self.points = []
```

**Funcionamiento:**
- Crea una instancia vacía del solver
- Inicializa la lista de puntos como vacía

##### Método: `set_points`

```python
def set_points(self, points: List[Tuple[float, float]]) -> None:
    """
    Establece los puntos de interpolación.
    
    Args:
        points: Lista de tuplas (x, y)
    
    Raises:
        ValueError: Si hay menos de 2 puntos o valores x duplicados
    """
```

**Funcionamiento:**
1. Valida que haya al menos 2 puntos
2. Verifica que no haya valores x duplicados
3. Ordena los puntos por valor de x
4. Almacena los puntos en `self.points`

**Ejemplo:**
```python
solver = LagrangeSolver()
solver.set_points([(1, 7), (2, 8), (9, 5)])
```

##### Método: `calculate_basis_polynomial`

```python
def calculate_basis_polynomial(self, j: int, x: float) -> float:
    """
    Calcula el j-ésimo polinomio base de Lagrange L_j(x).
    
    Fórmula:
    L_j(x) = ∏(i≠j) (x - x_i) / (x_j - x_i)
    
    Args:
        j: Índice del polinomio base (0 a n-1)
        x: Valor donde evaluar el polinomio
    
    Returns:
        Valor de L_j(x)
    """
```

**Funcionamiento:**
1. Inicializa el resultado en 1.0
2. Para cada punto i (excepto j):
   - Calcula el término: (x - x_i) / (x_j - x_i)
   - Multiplica el resultado por este término
3. Retorna el producto final

**Ejemplo matemático:**
Para puntos (1, 7), (2, 8), (9, 5) y j=0, x=2.7:

```
L_0(2.7) = [(2.7 - 2) / (1 - 2)] × [(2.7 - 9) / (1 - 9)]
         = [0.7 / -1] × [-6.3 / -8]
         = -0.7 × 0.7875
         = -0.551250
```

**Código:**
```python
def calculate_basis_polynomial(self, j: int, x: float) -> float:
    result = 1.0
    x_j = self.points[j][0]
    
    for i in range(len(self.points)):
        if i != j:
            x_i = self.points[i][0]
            result *= (x - x_i) / (x_j - x_i)
    
    return result
```

##### Método: `interpolate`

```python
def interpolate(self, x: float) -> float:
    """
    Calcula P(x) usando interpolación de Lagrange.
    
    Fórmula:
    P(x) = Σ(j=0 to n-1) y_j × L_j(x)
    
    Args:
        x: Valor donde evaluar el polinomio
    
    Returns:
        Valor interpolado P(x)
    
    Raises:
        ValueError: Si no hay puntos establecidos
    """
```

**Funcionamiento:**
1. Verifica que haya puntos establecidos
2. Inicializa el resultado en 0.0
3. Para cada punto j:
   - Calcula L_j(x) usando `calculate_basis_polynomial`
   - Multiplica por y_j
   - Suma al resultado
4. Retorna la suma total

**Ejemplo matemático:**
Para puntos (1, 7), (2, 8), (9, 5) y x=2.7:

```
P(2.7) = 7 × L_0(2.7) + 8 × L_1(2.7) + 5 × L_2(2.7)
       = 7 × (-0.551250) + 8 × (1.530000) + 5 × (0.021250)
       = -3.858750 + 12.240000 + 0.106250
       = 8.487500
```

##### Método: `generate_step_by_step`

```python
def generate_step_by_step(self, x_eval: float) -> List[Dict]:
    """
    Genera la visualización paso a paso del proceso.
    
    Args:
        x_eval: Valor de x donde evaluar
    
    Returns:
        Lista de diccionarios con información de cada paso
    """
```

**Funcionamiento:**
1. **Paso 1 - Puntos de Interpolación:**
   - Crea un diccionario con la lista de puntos
   - Indica el valor de x a evaluar

2. **Paso 2 - Cálculos Detallados:**
   - Para cada punto j:
     - Construye la fórmula simbólica del numerador y denominador
     - Calcula los valores evaluados
     - Calcula los productos
     - Almacena toda la información
   - Calcula el resultado final

3. **Paso 3 - Resultado:**
   - Muestra el valor final de P(x)

**Estructura de datos retornada:**
```python
[
    {
        'type': 'points',
        'points': [(1, 7), (2, 8), (9, 5)],
        'x_eval': 2.7
    },
    {
        'type': 'calculations',
        'x_eval': 2.7,
        'basis_details': [
            {
                'j': 0,
                'x_j': 1,
                'y_j': 7,
                'L_j': -0.551250,
                'contribution': -3.858750,
                'numerator_formula': '(x - 2) × (x - 9)',
                'denominator_formula': '(1 - 2) × (1 - 9)',
                'numerator_eval': '0.7 × -6.3',
                'denominator_eval': '-1 × -8',
                'numerator_product': -4.41,
                'denominator_product': 8.0
            },
            # ... más detalles para j=1, j=2, etc.
        ],
        'result': 8.487500
    },
    {
        'type': 'result',
        'x_eval': 2.7,
        'result': 8.487500
    }
]
```

---

## Módulo GUI

### Archivo: `gui/components.py`

Este módulo contiene todos los componentes personalizados de la interfaz.

#### Clase: `ModernButton`

```python
class ModernButton(ctk.CTkButton):
    """Botón con estilo moderno y consistente."""
```

**Características:**
- Bordes redondeados (corner_radius=8)
- Altura fija de 40px
- Fuente de tamaño 14
- Colores personalizables

**Uso:**
```python
button = ModernButton(
    parent=frame,
    text="Calcular",
    command=self.calculate
)
```

#### Clase: `ModernEntry`

```python
class ModernEntry(ctk.CTkEntry):
    """Campo de entrada con estilo moderno."""
```

**Características:**
- Bordes redondeados (corner_radius=8)
- Altura de 40px
- Fuente de tamaño 13
- Placeholder text opcional

#### Clase: `PointsTableInput`

```python
class PointsTableInput(ctk.CTkFrame):
    """Tabla interactiva para ingresar puntos (x, y)."""
```

**Funcionamiento:**

1. **Inicialización:**
   ```python
   def __init__(self, parent, on_validate=None):
       # Crea el frame principal
       # Inicializa variables
       # Crea el panel de control
   ```

2. **Método: `create_table`**
   - Destruye la tabla anterior si existe
   - Crea encabezados (Índice, X, Y)
   - Crea filas con campos de entrada
   - Cada fila tiene:
     - Label con el número de índice
     - Entry para valor X
     - Entry para valor Y

3. **Método: `get_points`**
   ```python
   def get_points(self) -> List[Tuple[float, float]]:
       """Obtiene los puntos ingresados en la tabla."""
   ```
   - Lee cada fila de la tabla
   - Convierte los valores a float
   - Retorna lista de tuplas (x, y)
   - Maneja errores de conversión

4. **Método: `set_points`**
   ```python
   def set_points(self, points: List[Tuple[float, float]]):
       """Establece valores en la tabla."""
   ```
   - Limpia la tabla actual
   - Crea nueva tabla con el número correcto de filas
   - Llena los campos con los valores proporcionados

**Ejemplo de uso:**
```python
table = PointsTableInput(parent=frame, on_validate=self.validate_data)
table.pack(fill="both", expand=True)

# Obtener puntos
points = table.get_points()  # [(1.0, 7.0), (2.0, 8.0), ...]

# Establecer puntos
table.set_points([(1, 7), (2, 8), (9, 5)])
```

#### Clase: `EvaluationPanel`

```python
class EvaluationPanel(ctk.CTkFrame):
    """Panel para evaluar el polinomio en un punto específico."""
```

**Componentes:**
- Campo de entrada para el valor de x
- Botón "Evaluar P(x)"
- Label para mostrar el resultado
- Advertencia de extrapolación (si aplica)

**Método: `set_result`**
```python
def set_result(self, result: float, x_value: float, x_range: Tuple[float, float]):
    """
    Muestra el resultado de la evaluación.
    
    Args:
        result: Valor de P(x)
        x_value: Valor de x evaluado
        x_range: Rango (min, max) de los puntos
    """
```

**Funcionamiento:**
1. Muestra el resultado con formato: "P(x) = valor"
2. Verifica si x está fuera del rango de puntos
3. Si está extrapolando, muestra advertencia en amarillo

#### Clase: `VisualizationPanel`

```python
class VisualizationPanel(ctk.CTkScrollableFrame):
    """Panel para visualizar el proceso paso a paso."""
```

Esta es la clase más compleja del proyecto. Maneja toda la visualización del proceso.

##### Método: `display_steps`

```python
def display_steps(self, steps: List[Dict]):
    """
    Muestra los pasos del proceso de interpolación.
    
    Args:
        steps: Lista de diccionarios con información de cada paso
    """
```

**Funcionamiento:**
1. Limpia el contenido anterior
2. Almacena los pasos
3. Muestra el primer paso automáticamente
4. Llama a `show_step(0)` para renderizar

##### Método: `show_step`

```python
def show_step(self, step_index: int):
    """Muestra un paso específico."""
```

**Funcionamiento:**
1. Limpia el frame actual
2. Obtiene el paso correspondiente
3. Determina el tipo de paso
4. Llama al método correspondiente:
   - `create_points_card()` para tipo 'points'
   - `create_calculations_card()` para tipo 'calculations'
   - `create_result_card()` para tipo 'result'

##### Método: `create_calculations_card`

Este es el método más importante y complejo. Muestra todo el proceso de cálculo.

```python
def create_calculations_card(self, step):
    """Crea tarjeta para mostrar todos los cálculos en una sola página."""
```

**Estructura:**

1. **Título y Información:**
   ```python
   ctk.CTkLabel(
       self.current_step_frame,
       text="Cálculos del Polinomio de Lagrange",
       font=ctk.CTkFont(size=16, weight="bold")
   ).pack(pady=(0, 10))
   ```

2. **Fórmula del Polinomio Interpolador:**
   - Crea un frame para la fórmula
   - Muestra "y(x) = " como etiqueta inicial
   - Para cada punto j:
     - Muestra el signo (+ o -)
     - Muestra el coeficiente y_j
     - Crea una fracción vertical con:
       - Numerador: (x - x₀)(x - x₁)...
       - Línea horizontal: ─────────
       - Denominador: (xⱼ - x₀)(xⱼ - x₁)...

3. **Sustitución con x evaluado:**
   - Similar a la fórmula, pero con valores numéricos
   - Muestra "y(2.7) = " 
   - Fracciones con valores sustituidos

4. **Resultados numéricos:**
   - Muestra los productos del numerador y denominador
   - Formato: numerador_producto / denominador_producto

5. **Suma de contribuciones:**
   - Muestra la suma: valor₁ + valor₂ + valor₃ = resultado

6. **Resultado final:**
   - Muestra P(x) = resultado en grande

**Implementación de fracciones verticales:**

```python
# Frame horizontal para todas las fracciones
horizontal_frame = ctk.CTkFrame(fractions_container)
horizontal_frame.pack(anchor="w", pady=5)

for i, detail in enumerate(step['basis_details']):
    # Signo
    if i > 0:
        sign_text = " + " if detail['y_j'] >= 0 else " - "
        ctk.CTkLabel(horizontal_frame, text=sign_text).pack(side="left")
    
    # Coeficiente
    coef_text = f"{abs(detail['y_j']):.3g} × "
    ctk.CTkLabel(horizontal_frame, text=coef_text).pack(side="left")
    
    # Fracción vertical
    vert_frac = ctk.CTkFrame(horizontal_frame)
    vert_frac.pack(side="left", padx=3)
    
    # Numerador
    ctk.CTkLabel(vert_frac, text=numerador).pack()
    
    # Línea horizontal
    line = "─" * max_width
    ctk.CTkLabel(vert_frac, text=line).pack()
    
    # Denominador
    ctk.CTkLabel(vert_frac, text=denominador).pack()
```

**Clave del diseño:**
- `pack(side="left")`: Coloca elementos horizontalmente
- `pack()` sin side: Coloca elementos verticalmente
- Frames anidados permiten la estructura vertical dentro de horizontal

---

### Archivo: `gui/main_window.py`

Contiene la ventana principal de la aplicación.

#### Clase: `MainWindow`

```python
class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación."""
```

##### Constructor

```python
def __init__(self):
    """Inicializa la ventana principal."""
```

**Funcionamiento:**
1. Llama al constructor de CTk
2. Configura la ventana:
   - Título: "Interpolación de Lagrange"
   - Tamaño: 1400x900
   - Centrado en pantalla
3. Crea el solver: `self.solver = LagrangeSolver()`
4. Crea la interfaz: `self.create_widgets()`

##### Método: `create_widgets`

```python
def create_widgets(self):
    """Crea todos los widgets de la interfaz."""
```

**Estructura de layout:**

```
┌─────────────────────────────────────────────────────┐
│                    TÍTULO                            │
├──────────────────┬──────────────────────────────────┤
│                  │                                   │
│   Panel Izq.     │      Panel Derecho               │
│   (40%)          │      (60%)                       │
│                  │                                   │
│  ┌────────────┐  │  ┌──────────────────────────┐   │
│  │  Tabla     │  │  │  Visualización           │   │
│  │  Puntos    │  │  │  Paso a Paso             │   │
│  └────────────┘  │  │                          │   │
│                  │  │                          │   │
│  ┌────────────┐  │  │                          │   │
│  │ Evaluación │  │  │                          │   │
│  └────────────┘  │  └──────────────────────────┘   │
│                  │                                   │
│  ┌────────────┐  │                                   │
│  │  Ejemplos  │  │                                   │
│  └────────────┘  │                                   │
└──────────────────┴──────────────────────────────────┘
```

**Código:**
```python
def create_widgets(self):
    # Título
    title = ctk.CTkLabel(
        self,
        text="Interpolación de Lagrange",
        font=ctk.CTkFont(size=28, weight="bold")
    )
    title.pack(pady=20)
    
    # Container principal
    main_container = ctk.CTkFrame(self)
    main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Panel izquierdo (40%)
    left_panel = ctk.CTkFrame(main_container)
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    # Panel derecho (60%)
    right_panel = ctk.CTkFrame(main_container)
    right_panel.pack(side="right", fill="both", expand=True)
```

##### Método: `validate_and_interpolate`

```python
def validate_and_interpolate(self):
    """Valida los datos y realiza la interpolación."""
```

**Flujo de ejecución:**

1. **Obtener puntos de la tabla:**
   ```python
   points = self.points_table.get_points()
   ```

2. **Validar puntos:**
   ```python
   is_valid, message = validate_points(points)
   if not is_valid:
       messagebox.showerror("Error de Validación", message)
       return
   ```

3. **Establecer puntos en el solver:**
   ```python
   self.solver.set_points(points)
   ```

4. **Obtener valor de x a evaluar:**
   ```python
   x_value = self.eval_panel.get_x_value()
   ```

5. **Calcular resultado:**
   ```python
   result = self.solver.interpolate(x_value)
   ```

6. **Generar visualización paso a paso:**
   ```python
   steps = self.solver.generate_step_by_step(x_value)
   ```

7. **Mostrar resultado y pasos:**
   ```python
   self.eval_panel.set_result(result, x_value, x_range)
   self.viz_panel.display_steps(steps)
   ```

8. **Manejo de errores:**
   ```python
   except ValueError as e:
       messagebox.showerror("Error", str(e))
   except Exception as e:
       messagebox.showerror("Error Inesperado", str(e))
   ```

##### Método: `load_example`

```python
def load_example(self, example_num: int):
    """Carga un ejemplo predefinido."""
```

**Ejemplos disponibles:**

```python
examples = {
    1: [(1, 7), (2, 8), (9, 5)],
    2: [(0, 1), (1, 3), (2, 9)],
    3: [(-1, 2), (1, 1), (2, 1)]
}
```

**Funcionamiento:**
1. Obtiene los puntos del ejemplo
2. Establece los puntos en la tabla: `self.points_table.set_points(points)`
3. Limpia el panel de evaluación
4. Muestra mensaje de éxito

---

## Módulo Utils

### Archivo: `utils/validators.py`

Contiene funciones de validación de datos.

#### Función: `validate_points`

```python
def validate_points(points: List[Tuple[float, float]]) -> Tuple[bool, str]:
    """
    Valida que los puntos sean correctos para interpolación.
    
    Args:
        points: Lista de tuplas (x, y)
    
    Returns:
        (es_válido, mensaje)
    """
```

**Validaciones realizadas:**

1. **Cantidad mínima:**
   ```python
   if len(points) < 2:
       return False, "Se necesitan al menos 2 puntos"
   ```

2. **Valores finitos:**
   ```python
   for x, y in points:
       if not (math.isfinite(x) and math.isfinite(y)):
           return False, f"Valor no finito detectado: ({x}, {y})"
   ```

3. **Valores x únicos:**
   ```python
   x_values = [x for x, y in points]
   if len(x_values) != len(set(x_values)):
       return False, "Los valores de x deben ser únicos"
   ```

4. **Éxito:**
   ```python
   return True, "Validación exitosa"
   ```

#### Función: `is_extrapolating`

```python
def is_extrapolating(x: float, x_range: Tuple[float, float]) -> bool:
    """
    Verifica si x está fuera del rango de interpolación.
    
    Args:
        x: Valor a verificar
        x_range: (x_min, x_max) del rango de puntos
    
    Returns:
        True si está extrapolando
    """
```

**Implementación:**
```python
def is_extrapolating(x: float, x_range: Tuple[float, float]) -> bool:
    x_min, x_max = x_range
    return x < x_min or x > x_max
```

---

## Flujo de Ejecución

### 1. Inicio de la Aplicación

```python
# main.py
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
```

**Secuencia:**
1. Se crea instancia de `MainWindow`
2. Se ejecuta `__init__()`:
   - Configura ventana
   - Crea solver
   - Crea widgets
3. Se inicia el loop de eventos de tkinter

### 2. Ingreso de Datos

**Usuario:**
1. Especifica número de puntos
2. Ingresa valores en la tabla
3. Hace clic en "Validar"

**Sistema:**
```python
validate_and_interpolate()
├── points_table.get_points()
├── validate_points(points)
├── solver.set_points(points)
└── Muestra mensaje de éxito
```

### 3. Evaluación

**Usuario:**
1. Ingresa valor de x
2. Hace clic en "Evaluar P(x)"

**Sistema:**
```python
validate_and_interpolate()
├── eval_panel.get_x_value()
├── solver.interpolate(x_value)
│   └── Para cada punto j:
│       ├── calculate_basis_polynomial(j, x)
│       │   └── Calcula L_j(x)
│       └── Suma y_j × L_j(x)
├── solver.generate_step_by_step(x_value)
│   └── Para cada punto j:
│       ├── Construye fórmulas simbólicas
│       ├── Calcula valores evaluados
│       └── Calcula productos
├── eval_panel.set_result(result, x_value, x_range)
└── viz_panel.display_steps(steps)
    └── show_step(0)
        └── create_calculations_card(step)
            ├── Muestra fórmula del polinomio
            ├── Muestra sustitución
            ├── Muestra resultados numéricos
            └── Muestra suma y resultado
```

### 4. Visualización

**Sistema:**
```python
viz_panel.display_steps(steps)
└── Para cada paso:
    ├── Determina tipo de paso
    └── Crea tarjeta correspondiente:
        ├── create_points_card()
        ├── create_calculations_card()
        └── create_result_card()
```

---

## Algoritmos Implementados

### Algoritmo de Lagrange

**Complejidad temporal:** O(n²) donde n es el número de puntos

**Pseudocódigo:**

```
FUNCIÓN interpolate(x):
    resultado = 0
    
    PARA j = 0 HASTA n-1:
        L_j = 1
        
        PARA i = 0 HASTA n-1:
            SI i ≠ j:
                L_j = L_j × (x - x_i) / (x_j - x_i)
        
        resultado = resultado + y_j × L_j
    
    RETORNAR resultado
```

**Análisis:**
- Loop externo: n iteraciones
- Loop interno: n-1 iteraciones
- Total: n × (n-1) = O(n²) operaciones

### Construcción de Fórmulas

**Complejidad temporal:** O(n²)

**Pseudocódigo:**

```
FUNCIÓN generate_step_by_step(x_eval):
    basis_details = []
    
    PARA j = 0 HASTA n-1:
        numerator_terms = []
        denominator_terms = []
        
        PARA i = 0 HASTA n-1:
            SI i ≠ j:
                numerator_terms.agregar("(x - " + x_i + ")")
                denominator_terms.agregar("(" + x_j + " - " + x_i + ")")
        
        numerator_formula = unir(numerator_terms, " × ")
        denominator_formula = unir(denominator_terms, " × ")
        
        basis_details.agregar({
            'numerator_formula': numerator_formula,
            'denominator_formula': denominator_formula,
            ...
        })
    
    RETORNAR basis_details
```

---

## Optimizaciones

### 1. Visualización en Una Sola Página

**Antes:**
- Múltiples pasos de navegación
- Un polinomio base por página
- Requería muchos clics

**Después:**
- Todo en una sola vista
- Scroll vertical para ver todo
- Experiencia más fluida

**Implementación:**
```python
# Todas las fracciones en un solo frame horizontal
horizontal_frame = ctk.CTkFrame(container)
horizontal_frame.pack(anchor="w")

for detail in basis_details:
    # Cada fracción se agrega con side="left"
    frac_frame = ctk.CTkFrame(horizontal_frame)
    frac_frame.pack(side="left", padx=3)
```

### 2. Fracciones con Línea Horizontal

**Antes:**
```
(x - 2)(x - 9) / (1 - 2)(1 - 9)
```

**Después:**
```
(x - 2)(x - 9)
──────────────
(1 - 2)(1 - 9)
```

**Implementación:**
```python
# Calcular ancho máximo
max_width = max(len(numerador), len(denominador))

# Crear línea con caracteres Unicode
line = "─" * max_width

# Crear estructura vertical
ctk.CTkLabel(frame, text=numerador).pack()
ctk.CTkLabel(frame, text=line).pack()
ctk.CTkLabel(frame, text=denominador).pack()
```

**Ventaja:**
- Más legible
- Más cercano a notación matemática
- Mejor para educación

### 3. Caché de Cálculos

Aunque no está implementado actualmente, se podría optimizar:

```python
# Idea para futuro
class LagrangeSolver:
    def __init__(self):
        self.points = []
        self._basis_cache = {}  # Cache de polinomios base
    
    def calculate_basis_polynomial(self, j: int, x: float) -> float:
        cache_key = (j, x)
        if cache_key in self._basis_cache:
            return self._basis_cache[cache_key]
        
        result = # ... cálculo ...
        self._basis_cache[cache_key] = result
        return result
```

### 4. Validación Temprana

```python
def set_points(self, points: List[Tuple[float, float]]) -> None:
    # Validar ANTES de procesar
    if len(points) < 2:
        raise ValueError("Se necesitan al menos 2 puntos")
    
    x_values = [x for x, y in points]
    if len(x_values) != len(set(x_values)):
        raise ValueError("Los valores de x deben ser únicos")
    
    # Ahora sí procesar
    self.points = sorted(points, key=lambda p: p[0])
```

**Ventaja:**
- Falla rápido si hay error
- No desperdicia recursos
- Mensajes de error claros

---

## Consideraciones de Rendimiento

### Complejidad Espacial

- **Almacenamiento de puntos:** O(n)
- **Generación de pasos:** O(n²) por las fórmulas de cada polinomio
- **Interfaz gráfica:** O(n) widgets por punto

### Límites Prácticos

**Número de puntos recomendado:** 3-10

**Razones:**
1. **Fenómeno de Runge:** Oscilaciones con muchos puntos
2. **Rendimiento visual:** Muchas fracciones no caben en pantalla
3. **Precisión numérica:** Errores de redondeo con muchos términos

### Mejoras Futuras

1. **Virtualización de tabla:** Para muchos puntos
2. **Cálculo en thread separado:** Para no bloquear UI
3. **Exportación a PDF:** Del proceso completo
4. **Gráfica del polinomio:** Visualización gráfica

---

## Manejo de Errores

### Errores Capturados

1. **ValueError:**
   - Puntos insuficientes
   - Valores x duplicados
   - Valores no numéricos

2. **TypeError:**
   - Tipos de datos incorrectos

3. **Exception genérica:**
   - Errores inesperados

### Estrategia de Manejo

```python
try:
    # Operación riesgosa
    result = self.solver.interpolate(x_value)
except ValueError as e:
    # Error esperado y manejable
    messagebox.showerror("Error de Validación", str(e))
except Exception as e:
    # Error inesperado
    messagebox.showerror("Error Inesperado", 
                        f"Ocurrió un error: {str(e)}")
    # En producción, aquí se registraría en log
```

---

## Conclusión

Este proyecto implementa el método de interpolación de Lagrange con:

✅ **Código modular y mantenible**
✅ **Interfaz gráfica intuitiva**
✅ **Visualización educativa completa**
✅ **Validación robusta de datos**
✅ **Manejo apropiado de errores**
✅ **Documentación completa**

La arquitectura permite fácil extensión y mantenimiento, mientras que la interfaz proporciona una experiencia educativa excelente.

---

**Versión:** 3.0  
**Fecha:** Octubre 2025  
**Autores:** Andres Monsivais Salazar, Luis Andres Salinas Lozano

