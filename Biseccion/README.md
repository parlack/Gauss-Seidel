# Método de Bisección - Resolución de Ecuaciones No Lineales

## Descripción

Esta aplicación implementa el **método de bisección** para encontrar raíces de ecuaciones no lineales de la forma f(x) = 0. El método utiliza el teorema del valor intermedio para encontrar aproximaciones de las raíces mediante la división sucesiva de intervalos.

## Características

- ✅ **Interfaz gráfica moderna** con CustomTkinter
- 🔄 **Visualización paso a paso** del proceso iterativo
- 📊 **Validación automática** de funciones e intervalos
- 🎯 **Múltiples tipos de funciones** soportadas
- 📈 **Navegación entre iteraciones** con controles intuitivos
- 🔍 **Verificación de resultados** con sustitución automática

## Funciones Soportadas

### Operadores Básicos
- `+`, `-`, `*`, `/` (operaciones aritméticas)
- `**` o `^` (potenciación)
- `()` (paréntesis para agrupación)

### Funciones Matemáticas
- `sin(x)`, `cos(x)`, `tan(x)` (trigonométricas)
- `exp(x)` (exponencial)
- `log(x)` (logaritmo natural)
- `log10(x)` (logaritmo base 10)
- `sqrt(x)` (raíz cuadrada)
- `abs(x)` (valor absoluto)

### Constantes
- `pi` (π = 3.14159...)
- `e` (e = 2.71828...)

## Ejemplos de Funciones

```python
# Polinomios
x**3 - 2*x - 5
x**2 - 4

# Exponenciales
exp(-x) - x
2**x - 3

# Trigonométricas
cos(x) - x
sin(x) - 0.5

# Logarítmicas
log(x) - 1
log10(x) + 2

# Combinadas
x**2 + sin(x) - 1
exp(x) - 2*cos(x)
```

## Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias
```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- `customtkinter>=5.2.0` (interfaz gráfica moderna)
- `numpy>=1.21.0` (cálculos numéricos)

## Uso

### Ejecutar la Aplicación
```bash
python main.py
```

### Pasos para Resolver una Ecuación

1. **Ingresar la función**: Escriba f(x) en el campo correspondiente
   - Ejemplo: `x**3 - 2*x - 5`

2. **Definir el intervalo**: Ingrese xl (límite inferior) y xu (límite superior)
   - Asegúrese de que f(xl) y f(xu) tengan signos opuestos

3. **Configurar parámetros** (opcional):
   - Tolerancia: criterio de convergencia (default: 0.000001%)
   - Máximo de iteraciones: límite de iteraciones (default: 100)

4. **Validar**: Use el botón "Validar" para verificar la función e intervalo

5. **Resolver**: Presione "Resolver Ecuación" para iniciar el proceso

6. **Explorar resultados**: Use los controles de navegación para revisar cada iteración

### Ejemplos Predefinidos

La aplicación incluye ejemplos predefinidos que puede cargar usando el botón "Ejemplo":

- **Polinomio Cúbico**: f(x) = x³ - 2x - 5
- **Exponencial**: f(x) = e^(-x) - x  
- **Trigonométrica**: f(x) = cos(x) - x

## Algoritmo del Método de Bisección

### Teoría

El método de bisección se basa en el **teorema del valor intermedio**:

Si f(x) es continua en [a,b] y f(a) × f(b) < 0, entonces existe al menos un valor c ∈ (a,b) tal que f(c) = 0.

### Proceso Iterativo

1. **Verificar condiciones iniciales**: f(xl) × f(xu) < 0
2. **Calcular punto medio**: xr = (xl + xu) / 2
3. **Evaluar función**: f(xr)
4. **Seleccionar nuevo intervalo**:
   - Si f(xl) × f(xr) < 0 → Nueva interval: [xl, xr]
   - Si f(xl) × f(xr) > 0 → Nuevo interval: [xr, xu]
5. **Calcular error relativo**: εa = |((xr_nuevo - xr_anterior) / xr_nuevo)| × 100%
6. **Verificar convergencia**: εa < tolerancia
7. **Repetir** hasta converger o alcanzar máximo de iteraciones

### Visualización del Proceso

La aplicación muestra para cada iteración:

- **Valores del intervalo**: xl, xr, xu
- **Evaluaciones de la función**: f(xl), f(xr), f(xu)  
- **Criterio de decisión**: f(xl) × f(xr)
- **Nuevo intervalo**: basado en el signo del producto
- **Error relativo**: porcentaje de cambio entre iteraciones
- **Estado de convergencia**: si se alcanzó la tolerancia

## Estructura del Proyecto

```
Biseccion/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── gui/                   # Interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal
│   └── components.py      # Componentes de UI
├── solver/                # Motor de cálculo
│   ├── __init__.py
│   └── biseccion.py       # Implementación del método
├── utils/                 # Utilidades
│   ├── __init__.py
│   └── validators.py      # Validadores de entrada
└── tests/                 # Pruebas unitarias
    ├── __init__.py
    └── test_solver.py     # Tests del solver
```

## Pruebas

### Ejecutar Tests
```bash
# Todos los tests
python -m pytest tests/ -v

# Solo tests del solver
python -m pytest tests/test_solver.py -v

# Test específico
python -m pytest tests/test_solver.py::TestBiseccionSolver::test_polynomial_function -v
```

### Cobertura de Tests

Los tests incluyen:
- ✅ Funciones polinomiales, exponenciales, trigonométricas
- ✅ Validación de intervalos y condiciones iniciales
- ✅ Manejo de errores y casos límite
- ✅ Convergencia con diferentes tolerancias
- ✅ Creación de funciones desde expresiones string
- ✅ Generación del proceso paso a paso

## Ventajas del Método de Bisección

### Pros ✅
- **Garantía de convergencia** (si existen las condiciones iniciales)
- **Simplicidad conceptual** y de implementación
- **Estabilidad numérica** robusta
- **Convergencia predecible** (error se reduce a la mitad cada iteración)

### Contras ❌
- **Convergencia lenta** (lineal, no cuadrática)
- **Requiere intervalo inicial** con cambio de signo
- **Solo encuentra una raíz** por ejecución
- **No funciona con raíces múltiples** o tangencias

## Casos de Uso Ideales

- 🎯 **Ecuaciones transcendentales** complejas
- 📊 **Funciones con múltiples discontinuidades**
- 🔧 **Cuando se requiere garantía de convergencia**
- 📈 **Análisis de comportamiento** de funciones no lineales

## Limitaciones

- No encuentra raíces complejas
- Requiere continuidad de la función
- No detecta raíces múltiples automáticamente
- Necesita intervalo inicial apropiado

## Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## Licencia

Este proyecto es de uso educativo. Desarrollado como parte del material de estudio de métodos numéricos.

## Autores

- **Andres Monsivais Salazar**
- **Luis Andres Salinas Lozano**

---

**Nota**: Este proyecto forma parte de una serie de implementaciones de métodos numéricos que incluye también Gauss-Seidel y otros algoritmos de análisis numérico.
