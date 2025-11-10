# 📚 Ejemplos Prácticos - Análisis de Distancias de Frenado

**Desarrollado por:**
- Andrés Monsivais Salazar
- Luis Andrés Salinas Lozano

---

## 📋 Tabla de Contenidos

1. [Ejemplo Básico: Primera Vez](#ejemplo-básico-primera-vez)
2. [Ejemplo 1: Zona Escolar](#ejemplo-1-zona-escolar)
3. [Ejemplo 2: Pavimento Mojado](#ejemplo-2-pavimento-mojado)
4. [Ejemplo 3: Comparación de Condiciones](#ejemplo-3-comparación-de-condiciones)
5. [Ejemplo 4: Decisión en Semáforo](#ejemplo-4-decisión-en-semáforo)
6. [Ejemplo 5: Calibración de Vehículo](#ejemplo-5-calibración-de-vehículo)
7. [Ejercicios Propuestos](#ejercicios-propuestos)

---

## 🎯 Ejemplo Básico: Primera Vez

### Objetivo
Familiarizarse con la aplicación usando datos de ejemplo.

### Pasos Detallados

#### 1. Iniciar la Aplicación

```bash
cd Frenado
python main.py
```

Verás la ventana principal con 4 pestañas.

#### 2. Cargar Datos de Ejemplo

1. Estás en la pestaña **"Datos Experimentales"** por defecto
2. Haz clic en el botón **"Ejemplo 1"**
3. Verás que se llenan automáticamente 6 mediciones:

```
Velocidad (km/h)  →  Distancia (m)
     20           →      6.0
     40           →     16.0
     60           →     32.0
     80           →     52.0
    100           →     78.0
    120           →    110.0
```

4. Haz clic en **"Validar"**
5. Verás un mensaje: "Datos experimentales válidos"

#### 3. Probar Interpolación

1. Ve a la pestaña **"Interpolacion (Lagrange)"**
2. Ingresa velocidad: **75**
3. Haz clic en **"Calcular Distancia de Frenado"**
4. Automáticamente cambiará a **"Visualizacion Paso a Paso"**

#### 4. Explorar la Visualización

1. Usa los botones de navegación:
   - **Siguiente**: Ver cada paso del cálculo
   - **Anterior**: Volver atrás
   - **Último**: Ir al resultado final

2. Observarás:
   - Paso 1: Datos experimentales
   - Paso 2: Explicación del método de Lagrange
   - Pasos 3-8: Cálculo de cada polinomio base L₀, L₁, L₂...
   - Paso 9: Resultado final

**Resultado esperado:** ~42.50 metros

#### 5. Probar Bisección

1. Ve a la pestaña **"Biseccion (Velocidad Segura)"**
2. Ingresa:
   - Distancia máxima: **50**
   - Tolerancia: **0.01** (ya está por defecto)
   - Mínima: **20**
   - Máxima: **150**
3. Haz clic en **"Calcular Velocidad Maxima Segura"**

4. Observarás la integración de métodos:
   - Cada iteración muestra primero el cálculo de Lagrange
   - Luego el resultado de bisección para esa iteración
   - Convergencia hacia la solución

**Resultado esperado:** ~82.3 km/h

---

## 🚸 Ejemplo 1: Zona Escolar

### Escenario Real

Una escuela primaria está en una calle donde los vehículos circulan a diferentes velocidades. La dirección quiere establecer un límite de velocidad seguro.

**Datos del problema:**
- Cruce peatonal con visibilidad limitada a **40 metros**
- Se han medido distancias de frenado de vehículos típicos
- Necesitamos determinar la velocidad máxima segura

### Datos Experimentales

Mediciones en pavimento seco con vehículo mediano:

```
Velocidad (km/h)  →  Distancia (m)
     20           →      6.0
     30           →     11.0
     40           →     16.0
     50           →     23.0
     60           →     32.0
     70           →     42.0
     80           →     52.0
```

### Paso a Paso

#### 1. Ingresar Datos

1. Abre la aplicación
2. En **"Datos Experimentales"**, ingresa los 7 puntos manualmente
3. Haz clic en **"Validar"**

#### 2. Calcular Velocidad Máxima Segura

1. Ve a **"Biseccion (Velocidad Segura)"**
2. Ingresa:
   - **Distancia máxima disponible**: 40 metros
   - **Tolerancia**: 0.01 km/h
   - **Intervalo**: [20, 80] km/h
3. Haz clic en **"Calcular"**

#### 3. Interpretar Resultados

**Resultado obtenido:** ~69.8 km/h

**Análisis:**
- Velocidad máxima teórica: 69.8 km/h
- Considerando tiempo de reacción (~1 segundo):
  - A 69.8 km/h = 19.4 m/s
  - Distancia de reacción: ~19 metros
  - Distancia total: 40 + 19 = 59 metros

**Recomendación:**
- Aplicar margen de seguridad del 20%
- Velocidad recomendada: **55-60 km/h**
- Señalización sugerida: **Límite 50 km/h** (estándar para zonas escolares)

#### 4. Verificación

Verificar con interpolación:
1. Ve a **"Interpolacion (Lagrange)"**
2. Evalúa a 50 km/h
3. Resultado: ~23 metros
4. Confirma que 23m < 40m (seguro con margen)

### Conclusión

Para garantizar seguridad en la zona escolar:
- ✅ Establecer límite de **50 km/h**
- ✅ Instalar señalización visible
- ✅ Considerar reductores de velocidad
- ✅ Zona escolar claramente marcada

---

## 🌧️ Ejemplo 2: Pavimento Mojado

### Escenario Real

Un conductor quiere entender cómo cambia la distancia de frenado en condiciones de lluvia.

**Datos del problema:**
- Mismo vehículo, diferentes condiciones
- Comparar pavimento seco vs mojado
- Determinar velocidades seguras en cada caso

### Datos Experimentales

#### Pavimento Seco (Ejemplo 1)
```
Velocidad (km/h)  →  Distancia (m)
     20           →      6.0
     40           →     16.0
     60           →     32.0
     80           →     52.0
    100           →     78.0
```

#### Pavimento Mojado (Ejemplo 2)
```
Velocidad (km/h)  →  Distancia (m)
     20           →      9.0
     40           →     24.0
     60           →     48.0
     80           →     78.0
    100           →    117.0
```

### Análisis Comparativo

#### 1. Comparar Distancias a 70 km/h

**Pavimento Seco:**
1. Cargar Ejemplo 1
2. Validar datos
3. Interpolar a 70 km/h
4. **Resultado:** ~42.5 metros

**Pavimento Mojado:**
1. Limpiar datos (botón "Limpiar")
2. Cargar Ejemplo 2
3. Validar datos
4. Interpolar a 70 km/h
5. **Resultado:** ~62.2 metros

**Diferencia:** 62.2 - 42.5 = **19.7 metros más** (+46%)

#### 2. Velocidad Segura para 50 metros

**Pavimento Seco:**
1. Usar Ejemplo 1
2. Bisección con distancia límite = 50 metros
3. **Resultado:** ~82.3 km/h

**Pavimento Mojado:**
1. Usar Ejemplo 2
2. Bisección con distancia límite = 50 metros
3. **Resultado:** ~58.7 km/h

**Diferencia:** 82.3 - 58.7 = **23.6 km/h menos** (-29%)

### Tabla Comparativa

| Condición | Distancia a 70 km/h | Velocidad segura (50m) | Factor |
|-----------|---------------------|------------------------|--------|
| Seco      | 42.5 m              | 82.3 km/h              | 1.0x   |
| Mojado    | 62.2 m              | 58.7 km/h              | 1.46x  |

### Conclusiones Prácticas

1. **En lluvia, reduce tu velocidad al menos 30%**
   - Si normalmente vas a 80 km/h → reduce a 55 km/h

2. **Las distancias de frenado aumentan ~50%**
   - Mantén mayor distancia de seguimiento

3. **Anticipación es clave**
   - Frena antes y más suavemente
   - Mayor tiempo de reacción necesario

---

## 📊 Ejemplo 3: Comparación de Condiciones

### Escenario Real

Empresa de transporte quiere establecer protocolos de seguridad para diferentes condiciones climáticas.

### Metodología

Usar la aplicación para crear una tabla de velocidades seguras en diferentes escenarios.

### Datos para Diferentes Condiciones

#### Condición 1: Pavimento Seco, Frenos Buenos
```
20 → 6, 40 → 16, 60 → 32, 80 → 52, 100 → 78, 120 → 110
```

#### Condición 2: Pavimento Mojado
```
20 → 9, 40 → 24, 60 → 48, 80 → 78, 100 → 117
```

#### Condición 3: Pavimento con Hielo (Simulado)
```
20 → 15, 40 → 40, 60 → 80, 80 → 135
```

### Análisis: Velocidades Máximas Seguras

Para diferentes distancias disponibles:

| Distancia Disponible | Seco | Mojado | Hielo |
|---------------------|------|--------|-------|
| 30 metros           | 66.2 | 48.5   | 28.3  |
| 40 metros           | 75.8 | 55.2   | 32.1  |
| 50 metros           | 82.3 | 58.7   | 35.4  |
| 60 metros           | 87.9 | 62.8   | 38.2  |

### Protocolo Recomendado

**Distancia de seguimiento mínima: 50 metros**

| Condición | Velocidad Máxima | Reducción |
|-----------|------------------|-----------|
| Seco      | 80 km/h          | Base      |
| Mojado    | 55 km/h          | -31%      |
| Hielo     | 35 km/h          | -56%      |

---

## 🚦 Ejemplo 4: Decisión en Semáforo

### Escenario Real

Conductor se aproxima a un semáforo que cambia a amarillo. ¿Debe frenar o pasar?

**Datos del problema:**
- Velocidad actual: **70 km/h**
- Distancia al semáforo: **55 metros**
- Condición: Pavimento seco

### Análisis con la Aplicación

#### 1. Calcular Distancia de Frenado Necesaria

1. Cargar Ejemplo 1 (pavimento seco)
2. Validar datos
3. Interpolar a 70 km/h
4. **Resultado:** 42.5 metros de frenado

#### 2. Considerar Tiempo de Reacción

- Tiempo de reacción típico: 1 segundo
- A 70 km/h = 19.4 m/s
- Distancia de reacción: ~19 metros

#### 3. Distancia Total

```
Distancia total = Distancia de reacción + Distancia de frenado
Distancia total = 19 + 42.5 = 61.5 metros
```

#### 4. Comparar con Distancia Disponible

```
Distancia disponible: 55 metros
Distancia necesaria: 61.5 metros
Déficit: -6.5 metros ❌
```

### Decisión

**NO FRENAR - PASAR EL SEMÁFORO**

**Razones:**
1. No hay suficiente distancia para frenar completamente
2. Frenar bruscamente podría causar colisión trasera
3. Es más seguro pasar (si el tiempo amarillo lo permite)

### Caso Alternativo: 65 metros disponibles

```
Distancia disponible: 65 metros
Distancia necesaria: 61.5 metros
Margen: +3.5 metros ✅
```

**DECISIÓN: FRENAR**
- Hay suficiente distancia con margen
- Frenado controlado es posible

---

## 🔧 Ejemplo 5: Calibración de Vehículo

### Escenario Real

Taller mecánico quiere verificar el sistema de frenos de un vehículo.

**Datos del problema:**
- Vehículo: Sedán mediano
- Comparar con datos del fabricante
- Identificar si necesita mantenimiento

### Datos del Fabricante (Estándar)

```
Velocidad (km/h)  →  Distancia (m)
     40           →     16.0
     60           →     32.0
     80           →     52.0
    100           →     78.0
```

### Mediciones del Vehículo en Prueba

```
Velocidad (km/h)  →  Distancia (m)
     40           →     18.5
     60           →     36.0
     80           →     58.0
    100           →     87.0
```

### Análisis Comparativo

#### 1. Ingresar Datos del Fabricante

1. Ingresar los 4 puntos estándar
2. Validar
3. Interpolar a 70 km/h
4. **Resultado estándar:** 42.5 metros

#### 2. Ingresar Datos del Vehículo

1. Limpiar datos
2. Ingresar los 4 puntos medidos
3. Validar
4. Interpolar a 70 km/h
5. **Resultado medido:** 47.8 metros

#### 3. Calcular Desviación

```
Desviación = (Medido - Estándar) / Estándar × 100%
Desviación = (47.8 - 42.5) / 42.5 × 100% = +12.5%
```

### Interpretación

| Desviación | Estado | Acción |
|------------|--------|--------|
| 0-5%       | ✅ Excelente | Ninguna |
| 5-10%      | ⚠️ Aceptable | Monitorear |
| 10-15%     | ⚠️ Atención | Revisar frenos |
| >15%       | ❌ Crítico | Mantenimiento urgente |

**En este caso: 12.5% → REVISAR FRENOS**

### Posibles Causas

- Pastillas de freno desgastadas
- Líquido de frenos degradado
- Discos de freno con surcos
- Calibración de ABS necesaria

### Recomendación

1. ✅ Inspeccionar sistema de frenos
2. ✅ Reemplazar pastillas si es necesario
3. ✅ Verificar líquido de frenos
4. ✅ Probar nuevamente después del mantenimiento

---

## 📝 Ejercicios Propuestos

### Ejercicio 1: Básico

**Objetivo:** Familiarizarse con interpolación

**Datos:**
```
30 → 11, 50 → 23, 70 → 42, 90 → 67
```

**Tareas:**
1. Ingresar los datos
2. Validar
3. Calcular distancia a 60 km/h
4. Calcular distancia a 80 km/h
5. ¿Cuál es la diferencia?

**Respuesta esperada:**
- 60 km/h: ~32 metros
- 80 km/h: ~54 metros
- Diferencia: ~22 metros

---

### Ejercicio 2: Intermedio

**Objetivo:** Usar bisección para encontrar velocidad segura

**Datos:** Usar Ejemplo 1 (pavimento seco)

**Escenario:** Hay un obstáculo a 60 metros

**Tareas:**
1. Cargar Ejemplo 1
2. Usar bisección con distancia límite = 60 metros
3. ¿Cuál es la velocidad máxima segura?
4. Verificar con interpolación que esa velocidad da ~60 metros

**Respuesta esperada:**
- Velocidad máxima: ~87.9 km/h
- Verificación: d(87.9) ≈ 60 metros

---

### Ejercicio 3: Avanzado

**Objetivo:** Comparar dos vehículos diferentes

**Vehículo A (Deportivo):**
```
40 → 14, 60 → 28, 80 → 46, 100 → 68, 120 → 95
```

**Vehículo B (SUV):**
```
40 → 18, 60 → 36, 80 → 58, 100 → 86, 120 → 120
```

**Tareas:**
1. Para cada vehículo, calcular velocidad segura para 50 metros
2. ¿Cuál vehículo frena mejor?
3. ¿Cuál es la diferencia porcentual?
4. A 90 km/h, ¿cuál necesita más distancia y cuánto más?

**Respuestas esperadas:**
- Vehículo A: ~88 km/h (mejor frenado)
- Vehículo B: ~78 km/h
- Diferencia: ~11% más lento
- A 90 km/h: A necesita ~57m, B necesita ~72m (+26%)

---

### Ejercicio 4: Proyecto

**Objetivo:** Diseñar límites de velocidad para una zona

**Escenario:**
Eres ingeniero de tránsito y debes establecer límites de velocidad para una avenida con las siguientes características:

- Tramo 1: Zona comercial, visibilidad 40m
- Tramo 2: Zona residencial, visibilidad 50m
- Tramo 3: Vía rápida, visibilidad 80m

**Condiciones:**
- Pavimento seco (usar Ejemplo 1)
- Margen de seguridad: 20%

**Tareas:**
1. Calcular velocidad máxima teórica para cada tramo
2. Aplicar margen de seguridad del 20%
3. Redondear a múltiplos de 10 km/h (estándar de señalización)
4. Crear tabla de velocidades recomendadas
5. Justificar cada decisión

**Solución sugerida:**

| Tramo | Visibilidad | V. Teórica | Con Margen | Recomendado |
|-------|-------------|------------|------------|-------------|
| 1     | 40m         | 75.8 km/h  | 60.6 km/h  | **60 km/h** |
| 2     | 50m         | 82.3 km/h  | 65.8 km/h  | **60 km/h** |
| 3     | 80m         | 100.5 km/h | 80.4 km/h  | **80 km/h** |

---

## 🎯 Tips y Trucos

### Tip 1: Usar Ejemplos como Base

No reinventes la rueda. Los ejemplos incluidos son buenos puntos de partida:
- Ejemplo 1: Pavimento seco, condiciones ideales
- Ejemplo 2: Pavimento mojado, condiciones adversas

### Tip 2: Validar Siempre

Antes de hacer cálculos complejos:
1. Ingresa datos
2. Haz clic en "Validar"
3. Espera confirmación
4. Procede con interpolación o bisección

### Tip 3: Verificación Cruzada

Para verificar resultados de bisección:
1. Obtén velocidad máxima (ej: 82.3 km/h)
2. Usa interpolación para calcular d(82.3)
3. Debe ser aproximadamente igual a tu distancia límite

### Tip 4: Navegación Eficiente

En visualización paso a paso:
- **Primero**: Ver contexto del problema
- **Último**: Ver resultado directo
- **Siguiente/Anterior**: Estudiar proceso detallado

### Tip 5: Tolerancia Adecuada

Para bisección:
- **0.1 km/h**: Rápido, suficiente para uso general
- **0.01 km/h**: Balance ideal (recomendado)
- **0.001 km/h**: Máxima precisión, más lento

---

## 📊 Plantilla de Reporte

Usa esta plantilla para documentar tus análisis:

```markdown
# Análisis de Frenado - [Nombre del Caso]

## Datos del Problema
- Fecha: [fecha]
- Vehículo: [descripción]
- Condiciones: [seco/mojado/etc]
- Objetivo: [qué quieres calcular]

## Datos Experimentales
| Velocidad (km/h) | Distancia (m) |
|------------------|---------------|
| [v1]             | [d1]          |
| [v2]             | [d2]          |
| ...              | ...           |

## Análisis Realizado

### Interpolación
- Velocidad evaluada: [v] km/h
- Distancia calculada: [d] metros
- Interpretación: [explicación]

### Bisección
- Distancia límite: [límite] metros
- Intervalo: [[a], [b]] km/h
- Tolerancia: [tol] km/h
- Velocidad máxima segura: [v_max] km/h

## Conclusiones
1. [Conclusión 1]
2. [Conclusión 2]
3. [Conclusión 3]

## Recomendaciones
- [Recomendación 1]
- [Recomendación 2]
```

---

## 🎓 Para Profesores

### Actividades Sugeridas

#### Actividad 1: Laboratorio Virtual (1 hora)
1. Explicar conceptos de interpolación y bisección (15 min)
2. Demostración con la aplicación (15 min)
3. Práctica guiada con Ejercicio 1 (15 min)
4. Práctica libre con Ejercicio 2 (15 min)

#### Actividad 2: Proyecto de Investigación (1 semana)
1. Recolectar datos reales de frenado (investigación)
2. Ingresar en la aplicación
3. Analizar diferentes escenarios
4. Presentar informe con recomendaciones

#### Actividad 3: Debate (45 min)
Tema: "¿Son suficientes los límites de velocidad actuales?"
- Usar la aplicación para calcular velocidades seguras
- Comparar con límites reales
- Discutir factores adicionales (tiempo de reacción, etc.)

### Rúbrica de Evaluación

| Criterio | Excelente (4) | Bueno (3) | Suficiente (2) | Insuficiente (1) |
|----------|---------------|-----------|----------------|------------------|
| Uso de la aplicación | Domina todas las funciones | Usa correctamente las principales | Uso básico con ayuda | No puede usar efectivamente |
| Interpretación de resultados | Análisis profundo y contextualizado | Interpretación correcta | Interpretación básica | No interpreta correctamente |
| Aplicación práctica | Propone soluciones innovadoras | Aplica a casos reales | Entiende aplicaciones | No ve aplicaciones |
| Documentación | Reporte completo y profesional | Reporte bien estructurado | Reporte básico | Documentación insuficiente |

---

## 🚀 Desafíos Avanzados

### Desafío 1: Optimización de Ruta

**Problema:** Tienes una ruta con 5 tramos de diferentes distancias y condiciones. Minimiza el tiempo total manteniendo seguridad.

### Desafío 2: Análisis de Accidente

**Problema:** Dado un accidente donde se conoce la distancia de frenado, determina la velocidad inicial del vehículo.

### Desafío 3: Diseño de Circuito

**Problema:** Diseña un circuito de pruebas con diferentes secciones de frenado y calcula velocidades máximas para cada una.

---

*¡Explora, experimenta y aprende sobre seguridad vial con métodos numéricos!*

**Última actualización: Noviembre 2025**

