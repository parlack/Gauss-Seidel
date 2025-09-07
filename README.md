# 🔢 Resolver Sistemas de Ecuaciones - Método de Gauss-Seidel

Una aplicación Python con interfaz gráfica moderna para resolver sistemas de ecuaciones lineales usando el método iterativo de Gauss-Seidel, con visualización paso a paso del proceso de solución.

## ✨ Características

- **🎨 Interfaz Visual Moderna**: Diseño limpio y moderno usando CustomTkinter
- **🔬 Visualización Paso a Paso Mejorada**: 
  - Cards visuales para cada iteración (sin formato de terminal)
  - Barra de progreso animada
  - Comparación visual entre iteraciones
  - Navegación avanzada (Primera/Anterior/Siguiente/Última)
- **📊 Dashboard Interactivo**: 
  - Métricas en tiempo real
  - Gráficos de convergencia mejorados
  - Indicadores visuales de cambio
- **🎯 Sistemas Dinámicos y Responsivos**: 
  - Resuelve sistemas de 2×2 hasta 10×10 ecuaciones
  - **Layout de 2 columnas optimizado**: Términos independientes + Configuración del solver
  - Auto-redimensionado inteligente de ventana según tamaño del sistema
  - Scroll automático para sistemas grandes
  - Campos responsivos que se ajustan al tamaño disponible
- **📈 Análisis de Convergencia**: Visualiza cómo converge la solución con gráficos profesionales
- **✅ Validación Inteligente**: 
  - Verifica la validez de los datos de entrada
  - **🔧 Auto-optimización de matrices**: Detecta automáticamente si se puede hacer diagonalmente dominante
  - **↕️ Reordenamiento inteligente**: Intercambia filas automáticamente para garantizar convergencia
  - **⚠️ Advertencias claras**: Informa cuando no es posible optimizar el sistema
- **⚙️ Configuración Flexible**: Ajusta tolerancia y máximo de iteraciones
- **🏆 Resultado Visual**: Solución mostrada en tarjetas coloridas organizadas

## 📋 Requisitos

- Python 3.7 o superior
- Las dependencias listadas en `requirements.txt`

## 🚀 Instalación y Uso

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git:
   git clone [URL_DEL_REPOSITORIO]
   cd gauss-seidel
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```
   
   O ejecuta la **demostración mejorada** con instrucciones:
   ```bash
   python demo.py
   ```
   
   Para **probar sistemas grandes** y responsividad:
   ```bash
   python test_large_systems.py
   ```
   
   Para **demostrar la dominancia diagonal automática**:
   ```bash
   python demo_diagonal_dominance.py
   ```

## 🎯 Cómo Usar

### 1. Entrada de Datos
- **Tamaño del Sistema**: Selecciona entre 2×2 y 10×10 ecuaciones
- **Matriz de Coeficientes**: Ingresa los coeficientes del sistema Ax = b
- **Términos Independientes**: Ingresa el vector b
- **Configuración**: Ajusta tolerancia y máximo de iteraciones

### 2. Botones de Control
- **🧹 Limpiar Todo**: Borra todas las entradas
- **📋 Ejemplo**: Carga un sistema de ejemplo
- **✅ Validar**: Verifica que los datos sean correctos
- **🚀 RESOLVER SISTEMA**: Inicia el proceso de solución

### 3. Visualización de Resultados (🆕 MEJORADO)
- **📊 Vista Iterativa**: 
  - Cards visuales para cada iteración
  - Comparación con iteración anterior
  - Cálculos mostrados de forma gráfica
  - Navegación fluida entre pasos
- **📈 Convergencia**: 
  - Gráfico profesional de convergencia
  - Métricas en tiempo real
  - Indicadores de progreso
- **✅ Resultado Final**: 
  - Solución en tarjetas organizadas
  - Estadísticas visuales del proceso
  - Estado de convergencia claro

## 🔬 Método de Gauss-Seidel

El método de Gauss-Seidel es un algoritmo iterativo para resolver sistemas de ecuaciones lineales de la forma Ax = b. La fórmula iterativa es:

```
x_i^(k+1) = (b_i - Σ(a_ij * x_j^(k+1)) - Σ(a_ij * x_j^(k))) / a_ii
```

### Convergencia y Auto-Optimización 🔧

#### ✅ Dominancia Diagonal Automática (NUEVA FUNCIONALIDAD)
- **Detección automática**: La aplicación detecta si la matriz puede hacerse diagonalmente dominante
- **Reordenamiento inteligente**: Intercambia filas automáticamente para optimizar la convergencia
- **Garantía de convergencia**: Si se logra hacer diagonalmente dominante, la convergencia está asegurada

#### 🔍 Criterio de Convergencia
- Una matriz es **diagonalmente dominante** si: |a_ii| > Σ|a_ij| para toda fila i
- **Ejemplo**: En la fila [10, -1, 2], el elemento diagonal |10| > |-1| + |2| = 3 ✅

#### 🚨 Casos Especiales
- **Optimizable**: Si se puede reordenar → Se hace automáticamente con notificación
- **No optimizable**: Si no se puede → Advertencia clara y opción de continuar
- **Ya optimizada**: Si ya es dominante → Continúa sin cambios

## 📁 Estructura del Proyecto

```
gauss-seidel/
├── main.py                 # Archivo principal para ejecutar
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal
│   └── components.py      # Componentes de la interfaz
├── solver/
│   ├── __init__.py
│   └── gauss_seidel.py    # Algoritmo de Gauss-Seidel
└── utils/
    ├── __init__.py
    └── validators.py      # Validación de entrada
```

## 🛠️ Dependencias

- **customtkinter**: Interfaz gráfica moderna
- **numpy**: Cálculos matemáticos y arrays
- **matplotlib**: Gráficos y visualizaciones
- **tkinter**: Biblioteca GUI base (incluida en Python)

## 💡 Ejemplos de Uso

### Sistema 3×3 (Diagonalmente Dominante)
```
10x₁ -  1x₂ + 2x₃ =  6
-1x₁ + 11x₂ - 1x₃ = 25
 2x₁ -  1x₂ +10x₃ = -11
```

Solución: x₁ = 1, x₂ = 2, x₃ = -1

### Sistema 2×2
```
4x₁ + 1x₂ =  1
2x₁ + 3x₂ = 11
```

Solución: x₁ = -1, x₂ = 5

### 🔧 Ejemplo de Auto-Optimización (NUEVO)

#### Sistema que requiere reordenamiento:
```
Matriz Original:          Matriz Optimizada:
[1   8   2 ] [11]         [15  -1   2 ] [16]  ← Fila 3 → Fila 1
[2   1   9 ] [12]   →     [1    8   2 ] [11]  ← Fila 1 → Fila 2  
[15 -1   2 ] [16]         [2    1   9 ] [12]  ← Fila 2 → Fila 3

❌ Original NO dominante   ✅ Optimizada SÍ dominante
```

**Proceso automático:**
1. 🔍 Se detecta que la matriz NO es diagonalmente dominante
2. 🔧 Se analiza si puede optimizarse intercambiando filas
3. ↕️ Se realizan los intercambios necesarios automáticamente
4. ✅ Se muestra el resultado: "Matriz hecha diagonalmente dominante intercambiando 2 fila(s)"
5. 🚀 El sistema ahora converge garantizadamente

## 🎨 Mejoras Visuales (NUEVA VERSIÓN)

### 🔄 Visualización de Iteraciones
- **Sin Formato de Terminal**: Eliminado completamente el texto plano
- **Cards Interactivas**: Cada iteración se muestra en tarjetas visuales modernas
- **Comparación Visual**: Ver cambios entre iteraciones con iconos y colores
- **Fórmulas Amigables**: Cálculos mostrados de forma fácil de entender

### 📊 Dashboard de Progreso
- **Barra de Progreso**: Visualiza el avance del algoritmo
- **Métricas en Vivo**: Error actual, tasa de convergencia, iteraciones
- **Navegación Avanzada**: Botones Primera/Anterior/Siguiente/Última
- **Indicadores de Estado**: Colores y iconos para mostrar convergencia

### 🎯 Resultado Profesional
- **Solución en Grid**: Variables organizadas en tarjetas coloridas
- **Estadísticas Visuales**: Métricas del proceso en formato gráfico
- **Estado Claro**: Indicadores visuales de éxito/advertencia

## ⚡ Características Técnicas

- **Validación en Tiempo Real**: Verifica entrada mientras escribes
- **Manejo de Errores**: Mensajes claros para problemas comunes
- **Interfaz Responsive**: Se adapta a diferentes tamaños de ventana
- **Navegación Intuitiva**: Botones para navegar entre iteraciones
- **Temas Personalizables**: Interfaz moderna y limpia
- **Renderizado Optimizado**: Actualización eficiente de componentes visuales

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.7+ esté instalado
- Instala las dependencias: `pip install -r requirements.txt`

### El método no converge
- Verifica que la matriz sea diagonalmente dominante
- Aumenta el número máximo de iteraciones
- Reduce la tolerancia si es necesario

### Errores de entrada
- Usa números decimales (ej: 1.5, -2.0)
- No dejes celdas vacías
- Verifica que no haya ceros en la diagonal principal

## 🧪 Probando las Mejoras Visuales

Para experimentar completamente las **nuevas características visuales**:

1. **Ejecuta la demo**:
   ```bash
   python demo.py
   ```

2. **Carga el ejemplo recomendado** (3x3):
   - Usa el botón "📋 Ejemplo" en la aplicación
   - O ingresa manualmente:
     - Matriz A: `10, -1, 2` / `-1, 11, -1` / `2, -1, 10`
     - Vector b: `6, 25, -11`

3. **Resuelve y explora**:
   - Presiona "🚀 RESOLVER SISTEMA"
   - Ve a "📊 Vista Iterativa" para ver las cards visuales
   - Navega con los botones mejorados
   - Revisa "📈 Convergencia" para métricas en tiempo real
   - Checa "✅ Resultado Final" para la solución visual

4. **Compara iteraciones**:
   - Usa los botones de navegación avanzados
   - Observa los indicadores de cambio con colores
   - Ve la barra de progreso animada

## 🔧 Probando la Auto-Optimización (NUEVO)

Para experimentar la **nueva funcionalidad de dominancia diagonal**:

1. **Ejecuta la demo específica**:
   ```bash
   python demo_diagonal_dominance.py
   ```

2. **Prueba los ejemplos interactivos**:
   - **Ejemplo 1**: Sistema que SE PUEDE optimizar
   - **Ejemplo 2**: Sistema que NO se puede optimizar
   - **Ejemplo 3**: Sistema YA optimizado

3. **Observa el comportamiento automático**:
   - Al presionar "✅ Validar" verás la optimización en acción
   - Los intercambios de filas se muestran claramente
   - Se actualiza la matriz en tiempo real

4. **Prueba desde la app principal**:
   - Usa "📋 Ejemplo" y elige "SÍ" para sistemas que requieren reordenamiento
   - Observa cómo se optimiza automáticamente al resolver

## 🤝 Contribuciones

Este proyecto fue desarrollado como una herramienta educativa para visualizar el método de Gauss-Seidel. Las mejoras y sugerencias son bienvenidas.

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
1. Verifica la sección de solución de problemas
2. Asegúrate de que todas las dependencias estén instaladas
3. Revisa que los datos de entrada sean válidos

---

**¡Disfruta resolviendo sistemas de ecuaciones! 🚀**
