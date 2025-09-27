# 🔢 Método de Gauss-Seidel - Resolución de Sistemas de Ecuaciones Lineales

Una aplicación Python con interfaz gráfica moderna que implementa el **método iterativo de Gauss-Seidel** para resolver sistemas de ecuaciones lineales de la forma **Ax = b**, con visualización paso a paso del proceso iterativo completo y optimización automática de matrices.

**Desarrollado por:**
- **Andrés Monsivais Salazar**
- **Luis Andrés Salinas Lozano**

## ✨ Características

- **🎨 Interfaz Visual Moderna**: Diseño limpio usando CustomTkinter
- **🔬 Visualización Paso a Paso**: 
  - Cards visuales para cada iteración
  - Navegación entre iteraciones (Primera/Anterior/Siguiente/Última)
  - Comparación visual entre iteraciones consecutivas
  - Barra de progreso del proceso
- **📊 Análisis Detallado**: 
  - Vista iterativa con cálculos detallados
  - Resultado final con verificación por sustitución
  - Métricas del proceso (iteraciones, error final)
- **🎯 Sistemas Dinámicos**: 
  - Resuelve sistemas de 2×2 hasta 50×50 ecuaciones
  - Layout responsive que se adapta al tamaño del sistema
  - Auto-redimensionado inteligente de ventana
- **✅ Validación Inteligente**: 
  - Verifica automáticamente la validez de los datos
  - **🔧 Auto-optimización**: Detecta y reordena automáticamente matrices para hacerlas diagonalmente dominantes
  - **⚠️ Advertencias claras**: Informa cuando la convergencia no está garantizada
- **⚙️ Configuración Flexible**: 
  - Tolerancia ajustable (default: 0.000001)
  - Máximo de iteraciones configurable (default: 100)
- **🏆 Resultado Visual**: Solución mostrada en tarjetas organizadas con verificación

## 📋 Requisitos

- Python 3.7 o superior
- Las dependencias listadas en `requirements.txt`

## 🚀 Instalación y Uso

1. **Clonar o descargar el proyecto**
   ```bash
   # Si tienes git:
   git clone [URL_DEL_REPOSITORIO]
   cd Gauss-Seidel
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## 🎯 Cómo Usar

### 1. Configuración del Sistema
- **Tamaño del Sistema**: Selecciona entre 2×2 y 50×50 ecuaciones usando el campo numérico y presiona ✓
- **Auto-redimensionado**: La ventana se ajusta automáticamente según el tamaño del sistema

### 2. Entrada de Datos
- **Matriz de Coeficientes**: Ingresa los coeficientes del sistema Ax = b en la grilla izquierda
- **Términos Independientes**: Ingresa el vector b en la columna derecha
- **Configuración del Solver**: 
  - Ajusta la tolerancia (precisión deseada)
  - Configura el máximo de iteraciones

### 3. Botones de Control
- **🧹 Limpiar Todo**: Borra todas las entradas
- **📋 Ejemplo**: Carga un sistema de ejemplo (con opción de reordenamiento automático)
- **✅ Validar**: Verifica que los datos sean correctos y optimiza la matriz automáticamente
- **🚀 Resolver Sistema**: Inicia el proceso de solución

### 4. Visualización de Resultados
- **📊 Vista Iterativa**: 
  - Cards visuales modernas para cada iteración
  - Cálculos detallados paso a paso
  - Comparación con iteración anterior
  - Navegación fluida entre pasos
- **🎯 Resultado Final**: 
  - Solución en formato visual organizado
  - Verificación por sustitución en el sistema original
  - Estadísticas del proceso de convergencia

## 🔬 Método de Gauss-Seidel

El método de Gauss-Seidel es un algoritmo iterativo para resolver sistemas de ecuaciones lineales de la forma **Ax = b**. La fórmula iterativa es:

```
x_i^(k+1) = (b_i - Σ(a_ij * x_j^(k+1)) - Σ(a_ij * x_j^(k))) / a_ii
```

### Convergencia y Auto-Optimización 🔧

#### ✅ Dominancia Diagonal Automática
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
Gauss-Seidel/
├── main.py                 # Archivo principal con verificación de dependencias
├── requirements.txt        # Dependencias de Python
├── README.md              # Este archivo
├── gui/
│   ├── main_window.py     # Ventana principal de la aplicación
│   └── components.py      # Componentes personalizados de la interfaz
├── solver/
│   └── gauss_seidel.py    # Algoritmo de Gauss-Seidel con visualización
└── utils/
    └── validators.py      # Validación y optimización de matrices
```

## 🛠️ Dependencias

- **customtkinter**: Interfaz gráfica moderna y componentes visuales
- **numpy**: Cálculos matemáticos eficientes y manipulación de matrices
- **tkinter**: Biblioteca GUI base (incluida en Python estándar)

## 💡 Ejemplos de Uso

### Sistema 3×3 Diagonalmente Dominante
```
10x₁ -  1x₂ + 2x₃ =  6
-1x₁ + 11x₂ - 1x₃ = 25
 2x₁ -  1x₂ +10x₃ = -11
```
**Solución**: x₁ = 1, x₂ = 2, x₃ = -1

### Sistema 2×2 Simple
```
4x₁ + 1x₂ =  1
2x₁ + 3x₂ = 11
```
**Solución**: x₁ = -1, x₂ = 5

### 🔧 Ejemplo de Auto-Optimización

**Sistema que requiere reordenamiento:**
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

## 🎨 Funcionalidades de la Interfaz

### 🔄 Navegación Avanzada
- **Botones de navegación**: Primera, Anterior, Siguiente, Última iteración
- **Barra de progreso**: Visualización del avance del algoritmo
- **Información en tiempo real**: Iteración actual, error, estado de convergencia

### 📊 Visualización Profesional
- **Cards de iteraciones**: Cada paso mostrado en tarjetas visuales modernas
- **Cálculos detallados**: Fórmulas y sustituciones paso a paso
- **Comparación visual**: Indicadores de cambio entre iteraciones
- **Resultado organizado**: Solución final en formato grid visual

### ⚙️ Configuración Inteligente
- **Sistemas adaptativos**: Layout responsive para cualquier tamaño de sistema
- **Redimensionado automático**: La ventana se ajusta según el tamaño del problema
- **Validación en tiempo real**: Retroalimentación inmediata sobre la entrada de datos

## ⚡ Características Técnicas

- **Manejo robusto de errores**: Mensajes claros para problemas comunes
- **Validación exhaustiva**: Verifica matrices, vectores y configuraciones
- **Algoritmo optimizado**: Implementación eficiente del método iterativo
- **Interfaz responsive**: Se adapta a diferentes tamaños de sistema
- **Memoria eficiente**: Manejo optimizado de sistemas grandes

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que Python 3.7+ esté instalado: `python --version`
- Instala las dependencias: `pip install -r requirements.txt`
- Si faltan dependencias, aparecerá un mensaje de error explicativo

### El método no converge
- La aplicación automáticamente intenta optimizar la matriz
- Si no es posible, aparecerá una advertencia clara
- Puedes:
  - Aumentar el número máximo de iteraciones
  - Reducir la tolerancia si es necesario
  - Verificar que los datos del sistema sean correctos

### Errores de entrada
- **Números**: Usa formato decimal (ej: 1.5, -2.0, 3)
- **Celdas vacías**: No dejes campos sin completar
- **Diagonal principal**: No puede contener ceros
- La validación automática te guiará en caso de errores

### Sistemas grandes son lentos
- Sistemas > 15×15 pueden tardar más en procesar
- La aplicación automáticamente maximiza la ventana para sistemas grandes
- Considera reducir la tolerancia para convergencia más rápida

## 💻 Prueba la Aplicación

1. **Carga un ejemplo básico**:
   - Presiona "📋 Ejemplo"
   - Elige "❌ NO" para un sistema ya optimizado
   - Presiona "🚀 Resolver Sistema"

2. **Experimenta con la optimización**:
   - Presiona "📋 Ejemplo"
   - Elige "✅ SÍ" para un sistema que necesita reordenamiento
   - Observa cómo se optimiza automáticamente

3. **Explora la visualización**:
   - Ve a "Proceso de Solución" después de resolver
   - Navega por las iteraciones usando los botones
   - Revisa la verificación por sustitución en "Resultado Final"

## 🤝 Contribuciones

Este proyecto fue desarrollado como una herramienta educativa para visualizar el método de Gauss-Seidel. Las mejoras y sugerencias son bienvenidas.

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que todas las dependencias estén instaladas correctamente
2. Asegúrate de que los datos de entrada sean válidos (números reales, sin celdas vacías)
3. Revisa que el sistema tenga una solución única
4. Para sistemas grandes, ten paciencia durante el procesamiento

---

## 🔧 Actualizaciones Recientes

### Versión Actual - Septiembre 2025
- **✅ Corrección de errores críticos** en la visualización
- **🎨 Mejora de la interfaz** con mejor manejo de errores
- **📊 Optimización de performance** para sistemas grandes
- **🛡️ Validación robusta** mejorada
- **📚 Documentación completamente actualizada**

---

**¡Explora el método de Gauss-Seidel de manera visual, interactiva y educativa! 🚀**

*Desarrollado con ❤️ para la educación en métodos numéricos*

**Última actualización: Septiembre 2025**