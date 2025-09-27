# Método de Bisección - Resolver Ecuaciones No Lineales

## Descripción

Este proyecto implementa el método numérico de **bisección** para encontrar raíces de ecuaciones no lineales. Incluye una interfaz gráfica moderna y fácil de usar que permite visualizar paso a paso el proceso iterativo del algoritmo.

## Características

### 🎯 Funcionalidades Principales
- **Resolución de ecuaciones no lineales** usando el método de bisección
- **Interfaz gráfica intuitiva** con pestañas organizadas
- **Visualización paso a paso** del proceso iterativo
- **Validación automática** de funciones e intervalos
- **Navegación interactiva** entre iteraciones
- **Ejemplos predefinidos** para aprendizaje rápido

### 📊 Método de Bisección
El método de bisección es un algoritmo numérico robusto que:
- Encuentra raíces de funciones continuas
- Requiere un intervalo [a,b] donde f(a) × f(b) < 0
- Divide sucesivamente el intervalo por la mitad
- Converge siempre (aunque puede ser lento)
- Es numéricamente estable

### 🔧 Funciones Matemáticas Soportadas
- **Básicas**: x, +, -, *, /, **
- **Trigonométricas**: sin(x), cos(x), tan(x), asin(x), acos(x), atan(x)
- **Hiperbólicas**: sinh(x), cosh(x), tanh(x)
- **Logarítmicas**: log(x), ln(x), log10(x)
- **Exponenciales**: exp(x), e**x
- **Otras**: sqrt(x), abs(x), pi, e

## Instalación

### Requisitos del Sistema
- Python 3.7 o superior
- Pip (administrador de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd Biseccion/
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## Uso de la Aplicación

### 1. Entrada de Datos
- **Función Matemática**: Ingresa la función f(x) que quieres resolver
  - Ejemplo: `x**2 - 4` (encuentra las raíces x = ±2)
  - Ejemplo: `sin(x)` (encuentra x = 0, π, 2π, etc.)
  - Ejemplo: `exp(x) - 2` (encuentra x = ln(2))

- **Intervalo [a,b]**: Define el intervalo donde buscar la raíz
  - Debe cumplir: f(a) × f(b) < 0 (cambio de signo)
  - Ejemplo: Para x² - 4, usar intervalo [1, 3] para encontrar x = 2

- **Parámetros de Configuración**:
  - **Tolerancia**: Precisión deseada (default: 0.000001)
  - **Max. Iteraciones**: Máximo número de iteraciones (default: 100)

### 2. Validación
- Haz clic en **"✅ Validar"** para verificar tu entrada
- La aplicación verificará:
  - Sintaxis de la función
  - Existencia de cambio de signo en el intervalo
  - Evaluabilidad de la función en el intervalo

### 3. Resolución
- Haz clic en **"🚀 Resolver Ecuación"**
- La aplicación cambiará automáticamente a la pestaña "Proceso de Solución"

### 4. Visualización del Proceso
- **Vista Iterativa**: Navega entre las iteraciones para ver cada paso
- **Resultado Final**: Resumen completo con la raíz encontrada
- **Controles de Navegación**: ⏮ Primero, ⏪ Anterior, Siguiente ⏩, Último ⏭

## Ejemplos de Uso

### Ejemplo 1: Función Cuadrática
```
Función: x**2 - 4
Intervalo: [1, 3]
Raíz esperada: x = 2
```

### Ejemplo 2: Función Trigonométrica  
```
Función: sin(x)
Intervalo: [3, 4] 
Raíz esperada: x = π ≈ 3.14159
```

### Ejemplo 3: Función Exponencial
```
Función: exp(x) - 2
Intervalo: [0, 1]
Raíz esperada: x = ln(2) ≈ 0.69314
```

### Ejemplo 4: Función Logarítmica
```
Función: log(x) - 1
Intervalo: [1, 5]
Raíz esperada: x = e ≈ 2.71828
```

## Estructura del Proyecto

```
Biseccion/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── solver/
│   └── biseccion.py       # Algoritmo de bisección
├── gui/
│   ├── main_window.py     # Ventana principal
│   └── components.py      # Componentes de interfaz
├── utils/
│   └── validators.py      # Validadores de entrada
└── tests/
    └── test_*.py          # Tests unitarios
```

## Algoritmo Implementado

### Pseudocódigo del Método de Bisección

```
1. Verificar que f(a) × f(b) < 0
2. Para i = 1, 2, ..., max_iteraciones:
   a. xr = (a + b) / 2
   b. Calcular f(xr)
   c. Si |f(xr)| < tolerancia: ¡raíz encontrada!
   d. Si f(a) × f(xr) < 0: b = xr
   e. Si no: a = xr
   f. Calcular error relativo
   g. Si error < tolerancia: ¡convergencia!
3. Retornar xr como aproximación de la raíz
```

### Ventajas del Método
- **Siempre converge** si hay cambio de signo
- **Numéricamente estable**
- **Fácil de implementar**
- **No requiere derivadas**

### Limitaciones
- **Convergencia lenta** (lineal)
- **Requiere cambio de signo**
- **Una raíz por intervalo**
- **No encuentra raíces múltiples**

## Solución de Problemas

### Error: "No hay cambio de signo"
- **Causa**: f(a) × f(b) ≥ 0
- **Solución**: Cambia el intervalo [a,b] hasta que f(a) y f(b) tengan signos opuestos
- **Tip**: Usa la función "Validar" para obtener sugerencias de intervalos

### Error: "División por cero"
- **Causa**: La función no está definida en algún punto del intervalo
- **Solución**: Evita puntos donde la función es indefinida (ej: log(0), 1/x donde x=0)

### Error: "Función no evaluable"
- **Causa**: Sintaxis incorrecta o funciones no soportadas
- **Solución**: Verifica la sintaxis y usa solo funciones soportadas

### Convergencia Lenta
- **Causa**: El método de bisección siempre converge linealmente
- **Solución**: Aumenta el máximo de iteraciones o reduce la tolerancia

## Contribuciones

Este proyecto fue desarrollado como material educativo para el aprendizaje de métodos numéricos.

### Autores
- Andrés Monsivais Salazar
- Luis Andrés Salinas Lozano

## Licencia

Proyecto educativo - Uso libre para fines académicos.
