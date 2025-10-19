# Interpolación Polinómica - Método de Lagrange

## Descripción

Aplicación de escritorio para realizar interpolación polinómica usando el método de Lagrange. Permite ingresar puntos en formato de tabla y visualizar el proceso de cálculo paso a paso.

## Características

- ✅ **Interfaz de tabla intuitiva**: Ingresa puntos (x, y) en formato de tabla
- ✅ **Número variable de puntos**: Especifica cuántos puntos deseas usar
- ✅ **Validación automática**: Verifica que los datos sean válidos antes de interpolar
- ✅ **Visualización optimizada**: Muestra todo el proceso en una sola página con fracciones matemáticas
- ✅ **Fracciones con notación matemática**: Las fracciones se muestran con línea horizontal (─) en lugar de /
- ✅ **Disposición horizontal**: Todas las operaciones se muestran en una sola línea horizontal
- ✅ **Evaluación en cualquier punto**: Calcula P(x) para cualquier valor de x
- ✅ **Advertencias de extrapolación**: Alerta cuando evalúas fuera del rango de datos
- ✅ **Ejemplos predefinidos**: Carga ejemplos para aprender el método

## Método de Lagrange

El método de interpolación de Lagrange construye un polinomio único de grado n-1 que pasa exactamente por n puntos dados.

### Fórmula

El polinomio interpolador se expresa como:

```
P(x) = Σ(j=0 to n-1) y_j × L_j(x)
```

donde L_j(x) son los polinomios base de Lagrange:

```
L_j(x) = ∏(i≠j) (x - x_i) / (x_j - x_i)
```

### Propiedades

- El polinomio resultante tiene grado máximo n-1 (donde n es el número de puntos)
- Pasa exactamente por todos los puntos dados
- Es único (existe un solo polinomio de grado ≤ n-1 que pasa por n puntos)
- No requiere resolver sistemas de ecuaciones lineales

## Requisitos

- Python 3.8 o superior
- customtkinter 5.2.0
- numpy 1.24.3

## Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Pasos para interpolar

1. **Especifica el número de puntos**: En la tabla, ingresa cuántos puntos deseas usar y presiona ✓

2. **Ingresa los puntos**: Completa la tabla con los valores de x e y
   - Los valores de x deben ser únicos (no duplicados)
   - Se necesitan al menos 2 puntos

3. **Valida los datos**: Haz clic en "Validar" para verificar que los datos sean correctos

4. **Evalúa el polinomio**: Ingresa un valor de x en el panel de evaluación y haz clic en "Evaluar P(x)"

5. **Visualiza el proceso**: La aplicación mostrará de forma concisa en una sola página:
   - Los puntos de interpolación
   - Fórmula del polinomio interpolador con fracciones matemáticas
   - Sustitución del valor de x en las fracciones
   - Resultados numéricos de cada fracción
   - La suma de contribuciones y el resultado final P(x)

### Ejemplos de uso

#### Ejemplo 1: Interpolación simple con 3 puntos
```
Puntos: (1, 7), (2, 8), (9, 5)
Evaluar en: x = 2.7
```

**Visualización del proceso:**

La aplicación mostrará:

1. **Fórmula del Polinomio Interpolador** (todas las fracciones en una línea):
   ```
   y(x) = 7 × (x - 2)(x - 9)     + 8 × (x - 1)(x - 9)     + 5 × (x - 1)(x - 2)
              ─────────────           ─────────────           ─────────────
              (1 - 2)(1 - 9)          (2 - 1)(2 - 9)          (9 - 1)(9 - 2)
   ```

2. **Sustituyendo x = 2.7** (todas las fracciones en una línea):
   ```
   y(2.7) = 7 × (0.7)(-6.3)     + 8 × (1.7)(-6.3)     + 5 × (1.7)(0.7)
                ─────────           ─────────             ───────────
                (-1)(-8)            (1)(-7)               (8)(7)
   ```

3. **Resultados numéricos** (todas las fracciones en una línea):
   ```
   y(2.7) = 7 × -4.410000     + 8 × -10.710000     + 5 × 1.190000
                ────────           ─────────            ─────────
                8.000000           -7.000000            56.000000
   ```

4. **Suma y resultado final:**
   ```
   y(2.7) = -3.85875 + 12.24 + 0.10625 = 8.48750
   ```

#### Ejemplo 2: Polinomio cuadrático
```
Puntos: (0, 1), (1, 3), (2, 9)
Evaluar en: x = 1.5
Resultado: P(1.5) ≈ 5.25
```

## Estructura del Proyecto

```
Lagrange/
│
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
├── gui/                   # Interfaz gráfica
│   ├── main_window.py     # Ventana principal
│   └── components.py      # Componentes personalizados (tabla, botones, etc.)
│
├── solver/                # Lógica de interpolación
│   └── lagrange.py        # Implementación del método de Lagrange
│
└── utils/                 # Utilidades
    └── validators.py      # Validadores de entrada
```

## Características Técnicas

### Validaciones

- ✅ Verifica que los valores de x sean únicos
- ✅ Valida que todos los valores sean números finitos
- ✅ Requiere al menos 2 puntos para interpolar
- ✅ Detecta cuando se está extrapolando (fuera del rango de datos)

### Interfaz

- 🎨 Diseño moderno con customtkinter
- 📊 Tabla dinámica que se ajusta al número de puntos
- 📄 Proceso completo en una sola página (sin navegación entre pasos)
- 📈 Visualización clara con fracciones matemáticas en línea horizontal
- ➗ Fracciones con línea horizontal (─) para mejor legibilidad

## Mejoras de Visualización

Esta aplicación incluye mejoras significativas en la presentación del proceso de interpolación:

### Fracciones con Notación Matemática
Las fracciones se muestran con una línea horizontal (─) en lugar del símbolo de división (/), similar a como se escriben en matemáticas:

```
numerador
─────────
denominador
```

### Disposición Horizontal
Todas las operaciones se muestran en una sola línea horizontal, permitiendo ver toda la fórmula de una vez:

```
y(x) = 7 × fracción₁ + 8 × fracción₂ + 5 × fracción₃
```

### Proceso Completo en Una Página
Todo el proceso de cálculo se muestra en una sola vista sin necesidad de navegar entre múltiples pasos, incluyendo:
- Fórmula simbólica del polinomio
- Sustitución de valores
- Resultados numéricos
- Suma final

## Ventajas del Método de Lagrange

1. **Simplicidad conceptual**: Fácil de entender y programar
2. **No requiere resolver sistemas**: A diferencia de otros métodos
3. **Flexibilidad**: Fácil agregar o quitar puntos
4. **Precisión**: Pasa exactamente por todos los puntos

## Limitaciones

1. **Inestabilidad numérica**: Con muchos puntos puede haber errores de redondeo
2. **Oscilaciones**: El polinomio puede oscilar entre puntos (fenómeno de Runge)
3. **Costo computacional**: Para muchos puntos, el cálculo puede ser lento
4. **Extrapolación imprecisa**: Fuera del rango de datos, las predicciones pueden ser malas

## Recomendaciones

- Usa entre 3 y 10 puntos para mejores resultados
- Evita extrapolar demasiado lejos del rango de datos
- Si los puntos están muy espaciados, considera usar más puntos intermedios
- Para datos con ruido, considera métodos de aproximación en lugar de interpolación

## Autores

- Andres Monsivais Salazar
- Luis Andres Salinas Lozano

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## Soporte

Si encuentras algún error o tienes sugerencias, por favor reporta el problema.

---

**Nota**: Esta aplicación fue desarrollada con fines educativos para demostrar el método de interpolación de Lagrange de manera visual e interactiva.

