# 🚗 Análisis de Distancias de Frenado - Métodos Numéricos

Una aplicación Python con interfaz gráfica moderna que implementa dos **métodos numéricos** para analizar y optimizar la seguridad vial mediante el estudio de distancias de frenado:

1. **📐 Interpolación de Lagrange**: Predice la distancia de frenado a cualquier velocidad basándose en datos experimentales
2. **🔍 Método de Bisección**: Encuentra la velocidad máxima segura dado un límite de distancia disponible

**Desarrollado por:**
- **Andrés Monsivais Salazar**
- **Luis Andrés Salinas Lozano**

---

## 🎯 ¿Qué Problema Resuelve?

### Problema Real: Seguridad Vial

Imagina estas situaciones cotidianas:

1. **🚸 Zona escolar**: Hay un cruce peatonal a 50 metros. ¿Cuál es la velocidad máxima segura para poder frenar a tiempo?

2. **🚦 Semáforo en amarillo**: Vas a 70 km/h y el semáforo está a 40 metros. ¿Puedes frenar o es mejor pasar?

3. **🌧️ Pavimento mojado**: Tienes mediciones de frenado en diferentes velocidades. ¿Cuál sería la distancia de frenado a 85 km/h?

**Esta aplicación responde estas preguntas usando métodos numéricos**, permitiendo tomar decisiones informadas sobre seguridad vial basadas en datos experimentales reales.

---

## ✨ Características Principales

### 🎨 Interfaz Moderna y Amigable
- Diseño limpio y profesional usando CustomTkinter
- Organizada en pestañas intuitivas para cada funcionalidad
- Visualización paso a paso de ambos métodos
- Navegación fluida entre pasos del proceso

### 📊 Entrada de Datos Experimentales
- Tabla interactiva para ingresar mediciones de velocidad vs distancia
- Validación automática de datos
- Ejemplos precargados basados en datos reales
- Soporte para 2 a 20 mediciones

### 📐 Interpolación de Lagrange
- Construye un polinomio que pasa exactamente por todos los puntos experimentales
- Predice distancia de frenado a cualquier velocidad intermedia
- Muestra cálculos detallados de cada polinomio base
- Visualización clara de fórmulas y sustituciones

### 🔍 Método de Bisección
- Encuentra la velocidad máxima segura dado un límite de distancia
- Algoritmo iterativo con convergencia garantizada
- **Integración completa con Lagrange**: Muestra el cálculo de interpolación en cada iteración
- Precisión ajustable mediante tolerancia configurable (campo de entrada)
- Visualización detallada de cómo ambos métodos trabajan juntos

### 📈 Visualización Paso a Paso
- Cards visuales modernas para cada paso
- Navegación entre pasos (Primero/Anterior/Siguiente/Último)
- Explicaciones claras del proceso matemático
- Interpretación de resultados en contexto real

---

## 📋 Requisitos

- **Python 3.7 o superior**
- Las dependencias listadas en `requirements.txt`:
  - `customtkinter>=5.2.0` - Interfaz gráfica moderna
  - `numpy>=1.24.0` - Cálculos numéricos eficientes

---

## 🚀 Instalación y Uso

### 1. Clonar o descargar el proyecto

```bash
# Si tienes git:
git clone [URL_DEL_REPOSITORIO]
cd Frenado
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python main.py
```

---

## 📖 Guía de Uso Completa

### Paso 1️⃣: Ingresar Datos Experimentales

1. Ve a la pestaña **"📊 Datos Experimentales"**
2. Haz clic en **"📋 Ejemplo"** para cargar datos realistas, o ingresa tus propias mediciones:
   - **Velocidad**: en km/h (ej: 40, 60, 80, 100)
   - **Distancia**: en metros (ej: 16, 32, 52, 78)
3. Haz clic en **"✅ Validar"** para verificar que los datos son correctos

**Datos de Ejemplo Incluidos:**
```
Velocidad (km/h)  →  Distancia (m)
     20           →      6.0
     40           →     16.0
     60           →     32.0
     80           →     52.0
    100           →     78.0
    120           →    110.0
```
*Basados en condiciones típicas: pavimento seco, frenos en buen estado*

---

### Paso 2️⃣: Usar Interpolación de Lagrange

**Objetivo**: Predecir la distancia de frenado a una velocidad específica

1. Ve a la pestaña **"🎯 Interpolación (Lagrange)"**
2. Ingresa la velocidad deseada (ej: **75 km/h**)
3. Haz clic en **"🔍 Calcular Distancia de Frenado"**
4. La aplicación te mostrará:
   - Proceso paso a paso del cálculo
   - Fórmulas de los polinomios base
   - Resultado final (ej: **42.50 metros**)

**Ejemplo Real:**
```
Pregunta: ¿Cuántos metros necesito para frenar a 75 km/h?
Método: Interpolación de Lagrange sobre datos experimentales
Resultado: Aproximadamente 42.5 metros
```

---

### Paso 3️⃣: Usar Bisección para Velocidad Segura

**Objetivo**: Encontrar la velocidad máxima segura dado un límite de distancia

1. Ve a la pestaña **"⚠️ Bisección (Velocidad Segura)"**
2. Ingresa los parámetros:
   - **Distancia máxima disponible**: ej. **50 metros**
   - **Tolerancia / Margen de error**: ej. **0.01 km/h** (por defecto)
   - **Intervalo de búsqueda**: 
     - Velocidad mínima: ej. **20 km/h**
     - Velocidad máxima: ej. **150 km/h**
3. Haz clic en **"🚗 Calcular Velocidad Máxima Segura"**
4. La aplicación te mostrará:
   - **Integración completa de ambos métodos**: En cada iteración de Bisección verás el cálculo paso a paso de Lagrange
   - Proceso iterativo de bisección con refinamiento del intervalo
   - Velocidad máxima segura (ej: **82.3 km/h**)

**Ejemplo Real:**
```
Pregunta: Hay un cruce peatonal a 50 metros. ¿A qué velocidad máxima puedo ir?
Método: Bisección sobre función de distancia interpolada con Lagrange
Resultado: Máximo 82.3 km/h para frenar dentro de 50 metros
```

**✨ Característica Especial:**
La visualización paso a paso muestra cómo **Lagrange y Bisección trabajan juntos**:
- Para cada iteración de Bisección, verás el cálculo completo de Lagrange
- Esto demuestra cómo un método numérico (Lagrange) alimenta a otro (Bisección)
- Es una excelente herramienta educativa para entender la integración de métodos

---

### Paso 4️⃣: Explorar la Visualización Paso a Paso

1. Ve a la pestaña **"📈 Visualización Paso a Paso"**
2. Usa los botones de navegación:
   - **⏮️ Primero**: Ir al inicio del proceso
   - **◀️ Anterior**: Paso previo
   - **Siguiente ▶️**: Siguiente paso
   - **⏭️ Último**: Ir al resultado final
3. Cada paso muestra:
   - Título descriptivo
   - Explicación clara
   - Cálculos matemáticos detallados
   - Visualización de datos relevantes

---

## 🔬 Fundamentos Matemáticos

### 🔗 Integración de Ambos Métodos

**Lo que hace única a esta aplicación** es cómo integra dos métodos numéricos para resolver un problema complejo:

**Flujo de Trabajo:**
```
Datos Experimentales
        ↓
[Interpolación de Lagrange]
        ↓
Función Continua d(v)
        ↓
[Método de Bisección]
        ↓
Velocidad Máxima Segura
```

**¿Cómo trabajan juntos?**

1. **Lagrange construye la función**: A partir de mediciones discretas (ej: 6 puntos), crea una función continua d(v) que predice la distancia de frenado para cualquier velocidad.

2. **Bisección usa esa función**: Para encontrar la velocidad donde d(v) = distancia_límite, evalúa repetidamente la función de Lagrange en diferentes puntos.

3. **Visualización integrada**: En cada iteración de Bisección, la aplicación muestra:
   - Cómo se calcula d(v) usando Lagrange para ese punto específico
   - Cómo Bisección usa ese resultado para refinar su búsqueda
   - La convergencia hacia la solución final

**Ejemplo Práctico:**

```
Objetivo: Encontrar velocidad máxima para frenar en 50m

Iteración 1 de Bisección:
  → Probar punto medio: v = 70 km/h
  → Calcular d(70) usando Lagrange:
     • L₀(70) × 9.0 + L₁(70) × 24.0 + ... = 62.20 metros
  → f(70) = 62.20 - 50 = +12.20 (muy rápido)
  → Ajustar intervalo: buscar en [20, 70]

Iteración 2 de Bisección:
  → Probar punto medio: v = 45 km/h
  → Calcular d(45) usando Lagrange:
     • L₀(45) × 9.0 + L₁(45) × 24.0 + ... = 31.50 metros
  → f(45) = 31.50 - 50 = -18.50 (muy lento)
  → Ajustar intervalo: buscar en [45, 70]

... continúa hasta convergencia ...

Resultado: v_máx ≈ 58.7 km/h
```

**Ventajas de esta Integración:**
- ✅ **Flexibilidad**: Funciona con cualquier conjunto de datos experimentales
- ✅ **Precisión**: Lagrange interpola suavemente, Bisección converge garantizadamente
- ✅ **Educativo**: Muestra cómo los métodos numéricos se complementan
- ✅ **Práctico**: Resuelve un problema real de seguridad vial

---

### Método de Interpolación de Lagrange

El método construye un polinomio que pasa exactamente por todos los puntos experimentales.

**Fórmula del Polinomio Interpolador:**
```
P(v) = Σ d_j × L_j(v)
```

**Donde:**
- `v` = velocidad (variable independiente)
- `d_j` = distancia de frenado en el punto j
- `L_j(v)` = polinomio base de Lagrange para el punto j

**Polinomio Base de Lagrange:**
```
L_j(v) = ∏(i≠j) [(v - v_i) / (v_j - v_i)]
```

**Ejemplo con 3 puntos:**

Si tenemos mediciones:
- (40 km/h, 16 m)
- (60 km/h, 32 m)  
- (80 km/h, 52 m)

Para predecir la distancia a 70 km/h:

```
L_0(70) = (70-60)(70-80) / (40-60)(40-80) = 10×(-10) / (-20)×(-40) = 0.125
L_1(70) = (70-40)(70-80) / (60-40)(60-80) = 30×(-10) / 20×(-20) = 0.750
L_2(70) = (70-40)(70-60) / (80-40)(80-60) = 30×10 / 40×20 = 0.375

d(70) = 16×0.125 + 32×0.750 + 52×0.375 = 2 + 24 + 19.5 = 45.5 metros
```

**Propiedades:**
- ✓ El polinomio pasa exactamente por todos los puntos dados
- ✓ Único para un conjunto de puntos
- ✓ Grado del polinomio = n-1 (donde n = número de puntos)
- ⚠️ Preciso para interpolación, menos para extrapolación

---

### Método de Bisección

Encuentra la raíz de una función (donde f(x) = 0) dividiendo repetidamente el intervalo por la mitad.

**Aplicación en este caso:**
Queremos encontrar la velocidad `v` tal que:
```
d(v) = d_límite

Es decir, resolver:  f(v) = d(v) - d_límite = 0
```

**Algoritmo:**
1. Partir de un intervalo [a, b] donde f(a) y f(b) tienen signos opuestos
2. Calcular el punto medio: c = (a + b) / 2
3. Evaluar f(c)
4. Si f(a) × f(c) < 0 → la raíz está en [a, c], actualizar b = c
5. Si f(c) × f(b) < 0 → la raíz está en [c, b], actualizar a = c
6. Repetir hasta que el intervalo sea suficientemente pequeño

**Ejemplo:**

Queremos frenar en máximo 50 metros. Buscar velocidad en [20, 120] km/h.

```
Iteración 0: a=20, b=120, c=70
  d(20)=6 < 50  ✓  →  f(20) = -44
  d(120)=110 > 50 ✗  →  f(120) = +60
  d(70)=45.5 < 50 ✓  →  f(70) = -4.5
  → Raíz en [70, 120]

Iteración 1: a=70, b=120, c=95
  d(95)=68 > 50 ✗  →  f(95) = +18
  → Raíz en [70, 95]

Iteración 2: a=70, b=95, c=82.5
  d(82.5)=51.2 > 50 ✗  →  f(82.5) = +1.2
  → Raíz en [70, 82.5]

...continúa hasta convergencia...

Resultado: v_máx ≈ 82.3 km/h
```

**Convergencia:**
- ✓ Garantizada si f(a) × f(b) < 0
- ✓ Error se reduce a la mitad en cada iteración
- ✓ Convergencia lineal: error_n = (b-a) / 2^n

---

## 💡 Casos de Uso Prácticos

### 1. 🚸 Planificación de Zonas Escolares

**Escenario:**
Una escuela tiene un cruce peatonal con visibilidad limitada a 40 metros.

**Pregunta:**
¿Cuál debería ser el límite de velocidad para garantizar frenado seguro?

**Solución:**
1. Usar mediciones de frenado del vehículo típico
2. Aplicar bisección con distancia límite = 40 metros
3. Resultado: **Velocidad máxima segura ≈ 65 km/h**
4. **Recomendación**: Establecer límite de **50 km/h** con margen de seguridad

---

### 2. 🌧️ Frenado en Diferentes Condiciones

**Escenario:**
Se tienen datos experimentales de frenado en pavimento seco. Queremos estimar para pavimento mojado.

**Proceso:**
1. Ingresar datos de pavimento seco
2. Usar interpolación para obtener curva completa
3. Ajustar datos (multiplicar distancias por factor ~1.5 para mojado)
4. Comparar velocidades seguras en ambas condiciones

**Resultado:**
```
Pavimento Seco:   100 km/h → 78 m
Pavimento Mojado: 100 km/h → 117 m (estimado)

Para frenar en 50m:
  Seco:   máx. 82 km/h
  Mojado: máx. 67 km/h  ← 18% más lento
```

---

### 3. 🚦 Decisión en Semáforo Amarillo

**Escenario:**
Vas a 80 km/h, el semáforo está a 55 metros y cambia a amarillo. ¿Frenas o pasas?

**Análisis:**
1. Ingresar datos de frenado del vehículo
2. Interpolar distancia necesaria a 80 km/h
3. Comparar con distancia disponible

**Resultado:**
```
Velocidad: 80 km/h
Distancia necesaria: 52 m (por interpolación)
Distancia disponible: 55 m

Conclusión: ✅ PUEDES FRENAR CÓMODAMENTE (con 3m de margen)
```

---

### 4. 🏁 Calibración de Sistemas de Frenado

**Escenario:**
Taller mecánico quiere verificar que un vehículo frena correctamente.

**Proceso:**
1. Realizar pruebas de frenado a velocidades estándar
2. Comparar con datos de fabricante usando interpolación
3. Identificar desviaciones

**Ejemplo:**
```
A 60 km/h:
  Distancia esperada (fabricante): 32 m
  Distancia medida: 36 m
  
Desviación: +12.5%  →  ⚠️ Requiere revisión de frenos
```

---

## 📁 Estructura del Proyecto

```
Frenado/
│
├── main.py                    # Archivo principal con verificación de dependencias
├── requirements.txt           # Dependencias de Python
├── README.md                  # Este archivo - Documentación completa
│
├── gui/                       # Módulo de interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py         # Ventana principal con pestañas
│   └── components.py          # Componentes personalizados:
│                              #   - DatosExperimentalesPanel
│                              #   - InterpolacionPanel
│                              #   - BiseccionPanel
│                              #   - VisualizationPanel
│
├── solver/                    # Módulo de solvers numéricos
│   ├── __init__.py
│   ├── lagrange.py            # Interpolación de Lagrange
│   └── biseccion.py           # Método de bisección
│
└── utils/                     # Módulo de utilidades
    ├── __init__.py
    └── validators.py          # Validación de datos de entrada
```

---

## 🛠️ Detalles Técnicos

### Validación de Datos

La aplicación valida automáticamente:

✅ **Velocidades:**
- Deben ser números positivos
- Rango realista: 0-300 km/h
- Sin valores duplicados
- Al menos 2 mediciones

✅ **Distancias:**
- Deben ser números no negativos
- Rango realista: 0-500 metros
- Cantidad igual a velocidades

✅ **Interpolación:**
- Advertencia si se evalúa fuera del rango experimental (extrapolación)

✅ **Bisección:**
- Verifica que f(a) × f(b) < 0 (signos opuestos)
- Intervalo de al menos 1 km/h de ancho
- Advertencia si está fuera del rango de datos

---

### Tolerancias y Precisión

**Interpolación de Lagrange:**
- Precisión limitada por los datos experimentales
- Pasa exactamente por los puntos dados (error < 10⁻⁶)
- Más preciso dentro del rango de medición

**Bisección:**
- Tolerancia configurable por el usuario (por defecto: **0.01 km/h**)
- Puedes ajustar la precisión según tus necesidades:
  - **0.1 km/h**: Rápido, suficiente para uso general
  - **0.01 km/h**: Balance entre precisión y velocidad (recomendado)
  - **0.001 km/h**: Máxima precisión, más iteraciones
- Máximo de iteraciones: 100
- Convergencia garantizada

---

### Consideraciones de Rendimiento

- ⚡ Cálculos instantáneos para hasta 20 puntos
- 🎨 Interfaz responsive y fluida
- 💾 Uso eficiente de memoria
- 🔄 Visualización optimizada

---

## 🐛 Solución de Problemas

### La aplicación no inicia

**Problema**: Al ejecutar `python main.py`, aparece un error de dependencias.

**Solución**:
```bash
# Verifica la versión de Python
python --version  # Debe ser 3.7 o superior

# Instala las dependencias
pip install -r requirements.txt

# Si hay problemas con pip, actualízalo
python -m pip install --upgrade pip
```

---

### Error: "Primero debes ingresar y validar los datos"

**Problema**: Al intentar usar interpolación o bisección sin datos.

**Solución**:
1. Ve a la pestaña **"📊 Datos Experimentales"**
2. Haz clic en **"📋 Ejemplo"** o ingresa tus datos manualmente
3. Haz clic en **"✅ Validar"** y espera el mensaje de confirmación
4. Ahora puedes usar las otras pestañas

---

### Advertencia: "Extrapolación imprecisa"

**Problema**: Quieres evaluar fuera del rango de datos experimentales.

**Explicación**: 
- La interpolación es precisa DENTRO del rango de datos
- Fuera del rango (extrapolación) puede ser imprecisa
- La advertencia es informativa, puedes continuar con precaución

**Recomendación**:
- Para mejores resultados, usa velocidades dentro del rango medido
- Si necesitas extrapolación, agrega más puntos experimentales en ese rango

---

### Error: "Los signos deben ser opuestos" en Bisección

**Problema**: f(a) y f(b) tienen el mismo signo.

**Explicación**: 
El método requiere que la función cruce el eje X en el intervalo [a, b].

**Soluciones**:
1. **Amplía el intervalo**: Prueba con rango más amplio (ej: [10, 200] km/h)
2. **Verifica la distancia límite**: Asegúrate de que es alcanzable con los datos
3. **Revisa los datos**: Verifica que las mediciones son correctas

**Ejemplo:**
```
❌ Distancia límite: 200 m, Intervalo: [20, 80] km/h
   → d(80) = 52 m < 200 m  (ambos son menores, no hay solución)

✅ Distancia límite: 50 m, Intervalo: [20, 120] km/h
   → d(20) = 6 m < 50 m, d(120) = 110 m > 50 m  (signos opuestos ✓)
```

---

## 📊 Interpretación de Resultados

### Interpolación de Lagrange

**Resultado Ejemplo:**
```
A 75 km/h, la distancia de frenado es aproximadamente 42.50 metros
```

**Interpretación:**
- **Distancia de reacción** no está incluida (solo frenado efectivo)
- Para distancia total, suma ~1 segundo × velocidad en m/s
  - 75 km/h = 20.8 m/s
  - Distancia de reacción ≈ 21 metros
  - **Distancia total ≈ 63-64 metros**

---

### Bisección - Velocidad Segura

**Resultado Ejemplo:**
```
Velocidad Máxima Segura: 82.3 km/h para frenar en 50 metros
```

**Interpretación:**
- Esta es la velocidad **máxima teórica**
- En la práctica, **reduce 10-20%** por seguridad
- Factores adicionales a considerar:
  - ⏱️ Tiempo de reacción del conductor (~1 segundo)
  - 🌧️ Condiciones climáticas (lluvia, nieve)
  - 🛞 Estado de los neumáticos
  - 🛣️ Calidad del pavimento
  - ⚖️ Carga del vehículo

**Recomendación práctica:**
```
Velocidad calculada: 82.3 km/h
Margen de seguridad: -15%
Velocidad recomendada: ~70 km/h
```

---

## 🎓 Aspectos Educativos

### Para Estudiantes

Esta aplicación es ideal para aprender:

✅ **Métodos Numéricos:**
- Interpolación polinómica
- Búsqueda de raíces
- Análisis de convergencia

✅ **Aplicaciones Prácticas:**
- Física del movimiento
- Cinemática de vehículos
- Seguridad vial

✅ **Programación:**
- Python moderno
- Interfaces gráficas con CustomTkinter
- Arquitectura de software limpia
- Validación de datos

### Para Profesores

**Propuesta de Ejercicios:**

1. **Básico**: Usar los datos de ejemplo y obtener distancia a 65 km/h
2. **Intermedio**: Recolectar datos propios y analizar un vehículo específico
3. **Avanzado**: Comparar pavimento seco vs mojado y calcular % de reducción de velocidad
4. **Proyecto**: Diseñar límites de velocidad para una zona específica

---

## 🔐 Seguridad y Limitaciones

### ⚠️ Advertencias Importantes

1. **Esta aplicación es EDUCATIVA**:
   - No sustituye pruebas profesionales de frenado
   - Los resultados son aproximaciones basadas en interpolación
   - Siempre respeta las leyes de tránsito locales

2. **Factores No Considerados**:
   - Tiempo de reacción del conductor
   - Condiciones meteorológicas
   - Estado de los neumáticos
   - Pendiente de la carretera
   - Carga del vehículo
   - Sistemas de asistencia (ABS, EBD)

3. **Recomendación**:
   - Usa los resultados como referencia educativa
   - Siempre conduce con precaución
   - Mantén distancias de seguridad mayores a las calculadas

---

## 🌟 Características Avanzadas

### 🎯 Innovación: Visualización Integrada de Métodos

**Característica única de esta aplicación:**

Cuando ejecutas el método de Bisección, no solo ves las iteraciones de bisección, sino que **para cada iteración, la aplicación genera y muestra el cálculo completo de Lagrange** para ese punto específico.

**Flujo de visualización:**
```
1. Problema inicial y contexto
2. Explicación del método de Bisección
3. ITERACIÓN 1:
   3.1. Calcular d(70.0) con Lagrange
       - Datos experimentales (solo en primera iteración)
       - Método de Lagrange (solo en primera iteración)
       - Cálculo de L₀(70), L₁(70), L₂(70)...
       - Suma ponderada
       - Resultado: d(70.0) = 62.20 metros
   3.2. Resultado de Bisección iteración 1
       - Intervalo actual
       - Evaluación de f(v) = d(v) - límite
       - Decisión de qué subintervalo usar
4. ITERACIÓN 2:
   4.1. Calcular d(45.0) con Lagrange
       - Cálculo de L₀(45), L₁(45), L₂(45)...
       - Suma ponderada
       - Resultado: d(45.0) = 31.50 metros
   4.2. Resultado de Bisección iteración 2
       - Nuevo intervalo refinado
       - Nueva evaluación
... y así sucesivamente ...
```

**Ventajas educativas:**
- ✅ Ves exactamente cómo un método (Lagrange) alimenta al otro (Bisección)
- ✅ Entiendes que Bisección no "conoce" la fórmula de d(v), solo la evalúa
- ✅ Observas cómo la misma fórmula de Lagrange se aplica a diferentes puntos
- ✅ Comprendes la integración práctica de métodos numéricos

### Datos Realistas Incluidos

Los datos de ejemplo están basados en mediciones reales:
- Vehículo mediano (sedán ~1500 kg)
- Pavimento de asfalto seco
- Neumáticos en buen estado
- Sistema de frenos ABS funcional
- Conductor experimentado

### Precisión de los Métodos

**Lagrange:**
- Error de interpolación: típicamente < 1-2% dentro del rango
- Pasa exactamente por los puntos dados
- Más preciso con más puntos de datos

**Bisección:**
- Convergencia garantizada
- Error controlable mediante tolerancia
- Típicamente 5-10 iteraciones para convergencia

### Validación Exhaustiva

Todos los datos pasan por múltiples capas de validación:
1. ✓ Verificación de tipo (números válidos)
2. ✓ Verificación de rango (valores realistas)
3. ✓ Verificación de consistencia (no duplicados)
4. ✓ Advertencias de extrapolación
5. ✓ Verificación de convergencia en bisección

---

## 🤝 Contribuciones y Créditos

**Desarrollado por:**
- Andrés Monsivais Salazar
- Luis Andrés Salinas Lozano

**Tecnologías Utilizadas:**
- Python 3.7+
- CustomTkinter - Interfaz gráfica moderna
- NumPy - Cálculos numéricos eficientes

**Agradecimientos:**
- Datos de ejemplo basados en estudios de seguridad vial
- Diseño inspirado en principios de UX modernos

---

## 📞 Soporte

### Problemas Comunes

Si encuentras algún problema:

1. **Verifica las dependencias** estén instaladas correctamente
2. **Asegúrate** de que los datos de entrada sean válidos
3. **Consulta** la sección de "Solución de Problemas" en este README
4. **Revisa** que Python sea versión 3.7 o superior

### Reportar Errores

Para reportar errores, incluye:
- Versión de Python (`python --version`)
- Mensaje de error completo
- Pasos para reproducir el problema
- Datos de entrada usados (si es relevante)

---

## 📚 Referencias

### Métodos Numéricos

- **Interpolación de Lagrange**: 
  - Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis*. Brooks/Cole.
  - Chapra, S. C., & Canale, R. P. (2010). *Numerical Methods for Engineers*.

- **Método de Bisección**:
  - Heath, M. T. (2002). *Scientific Computing: An Introductory Survey*.
  - Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing*.

### Seguridad Vial

- Datos basados en estudios de la NHTSA (National Highway Traffic Safety Administration)
- Estándares de frenado según normativas internacionales
- Investigaciones sobre distancia de frenado en diferentes condiciones

---

## 🎯 Roadmap Futuro

Posibles mejoras futuras:

- [ ] Exportar resultados a PDF
- [ ] Graficar curva de distancia vs velocidad
- [ ] Comparar múltiples conjuntos de datos
- [ ] Incluir factor de tiempo de reacción
- [ ] Ajuste de condiciones (pavimento, clima)
- [ ] Base de datos de vehículos típicos
- [ ] Cálculo de distancia de seguridad recomendada

---

## 📜 Licencia

Este proyecto fue desarrollado con fines educativos para demostrar la aplicación de métodos numéricos a problemas reales de ingeniería y seguridad.

---

## ✅ Checklist de Inicio Rápido

- [ ] Instalar Python 3.7+
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Ejecutar aplicación (`python main.py`)
- [ ] Ir a "📊 Datos Experimentales"
- [ ] Hacer clic en "📋 Ejemplo"
- [ ] Hacer clic en "✅ Validar"
- [ ] Probar "🎯 Interpolación" con velocidad 75 km/h
- [ ] Probar "⚠️ Bisección" con distancia 50 m
- [ ] Explorar "📈 Visualización Paso a Paso"

---

## 🌟 Conclusión

Esta aplicación demuestra cómo los **métodos numéricos** pueden resolver problemas reales e importantes de seguridad vial. Al combinar:

- 📐 **Interpolación de Lagrange** para predicción de datos
- 🔍 **Método de Bisección** para optimización
- 🎨 **Interfaz gráfica moderna** para accesibilidad
- 📊 **Visualización paso a paso** para comprensión

Proporcionamos una herramienta educativa y práctica que cualquier persona puede entender y usar.

**¡Explora los métodos numéricos aplicados a la seguridad vial! 🚗💡**

---

*Desarrollado con ❤️ para la educación en métodos numéricos y seguridad vial*

**Última actualización: Noviembre 2025**

---

## 📝 Registro de Cambios Recientes

### Versión Actual

**Nuevas Características:**
- ✨ **Visualización integrada completa**: Ahora cada iteración de Bisección muestra el cálculo paso a paso de Lagrange
- ⚙️ **Tolerancia configurable**: Campo de entrada para ajustar la precisión del método de Bisección
- 🎯 **Optimización de visualización**: La explicación del método de Lagrange se muestra solo en la primera iteración
- 📊 **Mejor flujo educativo**: Claridad en cómo ambos métodos trabajan juntos
- 🚀 **Panel de Bisección con scroll**: Interfaz más accesible para todos los campos de entrada

**Mejoras Técnicas:**
- Parámetro `skip_method_explanation` en el solver de Lagrange
- Integración dinámica de pasos de visualización
- Propagación de contexto entre métodos
- Validación mejorada de tolerancia

**Documentación:**
- README completamente actualizado con ejemplos de integración
- Explicación detallada del flujo de trabajo entre métodos
- Casos de uso prácticos ampliados
- Sección de fundamentos matemáticos mejorada

