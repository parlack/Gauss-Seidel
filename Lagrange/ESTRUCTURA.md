# Estructura del Proyecto - Interpolación de Lagrange

## 📁 Estructura de Archivos

```
Lagrange/
│
├── 📄 main.py                    # Punto de entrada de la aplicación
├── 📄 requirements.txt           # Dependencias del proyecto
├── 📄 README.md                  # Documentación principal
├── 📄 EJEMPLOS.md                # Ejemplos de uso detallados
├── 📄 ESTRUCTURA.md              # Este archivo
│
├── 📁 gui/                       # Interfaz gráfica de usuario
│   ├── 📄 main_window.py         # Ventana principal de la aplicación
│   └── 📄 components.py          # Componentes personalizados
│
├── 📁 solver/                    # Lógica de interpolación
│   └── 📄 lagrange.py            # Implementación del método de Lagrange
│
└── 📁 utils/                     # Utilidades
    └── 📄 validators.py          # Validadores de entrada de datos
```

## 📋 Descripción de Archivos

### Archivos Principales

#### `main.py`
- **Propósito**: Punto de entrada de la aplicación
- **Funciones principales**:
  - `check_dependencies()`: Verifica que las dependencias estén instaladas
  - `run_application()`: Inicia la aplicación GUI
  - `setup_closing_protocol()`: Configura el cierre de la aplicación
- **Líneas de código**: ~100

#### `requirements.txt`
- **Propósito**: Lista de dependencias del proyecto
- **Dependencias**:
  - `customtkinter==5.2.0`: Framework para GUI moderna
  - `numpy==1.24.3`: Biblioteca para cálculos numéricos

---

### Carpeta `gui/`

#### `main_window.py`
- **Propósito**: Ventana principal de la aplicación
- **Clase principal**: `LagrangeApp(ctk.CTk)`
- **Componentes**:
  - Header con título e información
  - Notebook con 2 pestañas:
    1. "Entrada de Datos": Para ingresar puntos
    2. "Proceso de Interpolación": Para visualizar resultados
  - Barra de estado
- **Métodos principales**:
  - `setup_ui()`: Configura la interfaz
  - `validate_input()`: Valida los datos ingresados
  - `evaluate_polynomial()`: Evalúa el polinomio
  - `load_example()`: Carga ejemplos predefinidos
  - `clear_all_inputs()`: Limpia todos los campos
- **Líneas de código**: ~400

#### `components.py`
- **Propósito**: Componentes personalizados reutilizables
- **Clases**:
  1. **`ModernButton`**: Botón con estilo moderno
  2. **`ModernEntry`**: Campo de entrada con estilo moderno
  3. **`PointsTableInput`**: Tabla para ingresar puntos (x, y)
     - Permite especificar número de puntos
     - Validación en tiempo real
     - Scroll automático para muchos puntos
  4. **`EvaluationPanel`**: Panel para evaluar el polinomio
     - Campo para ingresar x
     - Botón para evaluar
  5. **`VisualizationPanel`**: Panel para visualizar el proceso
     - Navegación paso a paso
     - Barra de progreso
     - Visualización de cada paso del cálculo
- **Líneas de código**: ~900

---

### Carpeta `solver/`

#### `lagrange.py`
- **Propósito**: Implementación del método de interpolación de Lagrange
- **Clase principal**: `LagrangeSolver`
- **Atributos**:
  - `points`: Lista de puntos (x, y)
  - `basis_polynomials`: Polinomios base calculados
  - `evaluation_history`: Historial de evaluaciones
- **Métodos principales**:
  1. **`set_points(x_values, y_values)`**: Establece los puntos de interpolación
  2. **`calculate_basis_polynomial(j, x)`**: Calcula L_j(x)
     - Fórmula: L_j(x) = ∏(i≠j) (x - x_i) / (x_j - x_i)
  3. **`interpolate(x)`**: Evalúa el polinomio en x
     - Fórmula: P(x) = Σ y_j × L_j(x)
  4. **`generate_step_by_step(x_eval)`**: Genera explicación paso a paso
  5. **`verify_interpolation()`**: Verifica que el polinomio pase por todos los puntos
  6. **`get_polynomial_string()`**: Genera representación en string del polinomio
  7. **`evaluate_multiple_points(x_values)`**: Evalúa en múltiples puntos
- **Líneas de código**: ~350

---

### Carpeta `utils/`

#### `validators.py`
- **Propósito**: Validación de datos de entrada
- **Clase principal**: `DataValidator`
- **Métodos estáticos**:
  1. **`validate_point_data(x_values, y_values)`**: Valida puntos de interpolación
     - Verifica que no estén vacíos
     - Verifica misma longitud
     - Verifica al menos 2 puntos
     - Convierte a numpy arrays
     - Verifica valores finitos
     - Detecta x duplicados
  2. **`validate_evaluation_point(x)`**: Valida punto de evaluación
     - Verifica que no esté vacío
     - Convierte a float
     - Verifica que sea finito
  3. **`validate_number_of_points(n)`**: Valida número de puntos
     - Verifica que sea entero
     - Verifica rango válido (2-100)
  4. **`check_interpolation_range(x_eval, x_points)`**: Verifica si está en rango
     - Detecta extrapolación
     - Genera advertencias
  5. **`format_number(value, decimals)`**: Formatea números para mostrar
     - Usa notación científica para números muy grandes/pequeños
- **Líneas de código**: ~150

---

## 🔄 Flujo de Ejecución

### 1. Inicio de la Aplicación
```
main.py
  ↓
check_dependencies()
  ↓
run_application()
  ↓
LagrangeApp.__init__()
  ↓
setup_ui()
```

### 2. Ingreso de Datos
```
Usuario ingresa puntos en PointsTableInput
  ↓
Usuario hace clic en "Validar"
  ↓
validate_input()
  ↓
DataValidator.validate_point_data()
  ↓
LagrangeSolver.set_points()
```

### 3. Evaluación del Polinomio
```
Usuario ingresa x en EvaluationPanel
  ↓
Usuario hace clic en "Evaluar P(x)"
  ↓
evaluate_polynomial()
  ↓
DataValidator.validate_evaluation_point()
  ↓
LagrangeSolver.generate_step_by_step()
  ↓
VisualizationPanel.update_visualization()
```

### 4. Visualización de Resultados
```
VisualizationPanel muestra pasos:
  1. Puntos de interpolación
  2. Explicación del método
  3. Cálculo de cada L_j(x)
  4. Resultado final P(x)
```

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Total de archivos Python** | 5 |
| **Total de líneas de código** | ~1,900 |
| **Clases principales** | 7 |
| **Funciones/Métodos** | ~50 |
| **Archivos de documentación** | 3 |

---

## 🎨 Tecnologías Utilizadas

1. **Python 3.8+**: Lenguaje de programación principal
2. **customtkinter**: Framework para interfaz gráfica moderna
3. **numpy**: Biblioteca para cálculos numéricos eficientes
4. **tkinter**: Base para la interfaz gráfica (incluido en Python)

---

## 🔧 Características Técnicas

### Validaciones Implementadas
- ✅ Verificación de valores x únicos
- ✅ Validación de números finitos (no NaN, no infinito)
- ✅ Mínimo 2 puntos para interpolar
- ✅ Detección de extrapolación
- ✅ Manejo de errores robusto

### Interfaz de Usuario
- 🎨 Diseño moderno y limpio
- 📊 Tabla dinámica ajustable
- 🔄 Navegación paso a paso
- 📈 Visualización clara de cálculos
- 💡 Mensajes de ayuda contextuales
- ⚠️ Advertencias de extrapolación

### Algoritmo
- 📐 Implementación clásica de Lagrange
- ⚡ Cálculo eficiente con numpy
- 🎯 Precisión numérica alta
- 🔍 Verificación automática de resultados

---

## 🚀 Mejoras Futuras Posibles

1. **Gráficas**: Visualización gráfica del polinomio y los puntos
2. **Exportación**: Guardar resultados en archivo (CSV, PDF)
3. **Importación**: Cargar puntos desde archivo
4. **Comparación**: Comparar con otros métodos (Newton, Splines)
5. **Derivadas**: Calcular derivadas del polinomio
6. **Optimización**: Usar puntos de Chebyshev para evitar Runge
7. **Historial**: Guardar historial de interpolaciones
8. **Temas**: Modo oscuro/claro

---

## 📚 Referencias

- [Interpolación de Lagrange - Wikipedia](https://es.wikipedia.org/wiki/Interpolaci%C3%B3n_polin%C3%B3mica_de_Lagrange)
- [NumPy Documentation](https://numpy.org/doc/)
- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)

---

**Última actualización**: Octubre 2025
**Autores**: Andres Monsivais Salazar, Luis Andres Salinas Lozano

