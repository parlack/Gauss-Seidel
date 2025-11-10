# 🌱 Predictor de Crecimiento de Plantas

## Aplicación Real del Método de Interpolación de Lagrange

Esta aplicación permite predecir la altura de tus plantas en cualquier día, basándose en mediciones reales que hayas tomado previamente. Es una herramienta práctica y educativa que demuestra cómo las matemáticas pueden resolver problemas cotidianos.

---

## 🎯 ¿Para qué sirve?

Imagina que tienes una planta en casa y quieres saber:
- ¿Qué altura tendrá mi planta el próximo lunes?
- ¿Cuánto creció mi planta entre dos mediciones?
- ¿Cuándo alcanzará cierta altura?

Con esta aplicación, solo necesitas:
1. Medir tu planta varios días (por ejemplo: día 0, 7, 14, 21)
2. Anotar el día y la altura en centímetros
3. La aplicación predice la altura en cualquier día que desees

---

## 🌿 ¿Cómo funciona?

Utiliza el **Método de Interpolación de Lagrange**, una técnica matemática que construye una curva que pasa exactamente por todos los puntos que mediste. Esta curva te permite predecir valores intermedios o cercanos.

### Ventajas del método:
- ✅ **Preciso**: Pasa exactamente por todos tus puntos medidos
- ✅ **Flexible**: Funciona con cualquier número de mediciones
- ✅ **Visual**: Muestra todo el proceso paso a paso
- ✅ **Educativo**: Aprende matemáticas de forma práctica

---

## 📊 Ejemplos Incluidos

La aplicación incluye ejemplos reales de diferentes plantas:

### 🍅 Tomate Cherry
- Mediciones durante 4 semanas
- Crecimiento moderado y constante
- Ideal para huertos caseros

### 🌻 Girasol
- Crecimiento rápido y espectacular
- Perfecto para ver cambios dramáticos
- Crece hasta 115 cm en 25 días

### 🌵 Suculenta
- Crecimiento muy lento
- Mediciones mensuales
- Ideal para plantas de interior

### 🫘 Frijol
- Desde la germinación
- Crecimiento inicial rápido
- Excelente para proyectos escolares

---

## 🚀 Cómo usar la aplicación

### Paso 1: Ingresa tus mediciones
1. Abre la pestaña "📝 Mis Mediciones"
2. Define cuántas mediciones tienes
3. Ingresa el día y la altura en cm de cada medición

**Ejemplo:**
```
Día 0:  5 cm
Día 7:  12 cm
Día 14: 22 cm
Día 21: 35 cm
```

### Paso 2: Valida tus datos
- Presiona el botón "Validar"
- La aplicación verificará que tus datos sean correctos
- Te mostrará un resumen de tus mediciones

### Paso 3: Haz una predicción
1. En el panel "🔮 Hacer Predicción"
2. Escribe el día que quieres predecir (ej: día 10)
3. Presiona "🌿 Predecir Altura"

### Paso 4: Ve los resultados
- La aplicación cambiará a la pestaña "📈 Predicción y Análisis"
- Verás el proceso matemático completo paso a paso
- Al final obtendrás la altura predicha

---

## 💡 Casos de Uso Reales

### Para Estudiantes
- Proyecto de ciencias sobre crecimiento de plantas
- Aprender interpolación de forma práctica
- Comparar diferentes tipos de plantas

### Para Jardineros Aficionados
- Monitorear el crecimiento de tus plantas
- Predecir cuándo trasplantar
- Comparar el efecto de diferentes fertilizantes

### Para Educadores
- Enseñar matemáticas con ejemplos reales
- Demostrar interpolación polinómica
- Proyecto interdisciplinario (matemáticas + biología)

### Para Curiosos
- Experimentar con el método de Lagrange
- Ver cómo las matemáticas modelan la naturaleza
- Entender predicciones matemáticas

---

## ⚠️ Limitaciones y Consejos

### ✅ Funciona mejor cuando:
- Tienes al menos 3-4 mediciones
- Las mediciones están espaciadas uniformemente
- Predices dentro del rango de días medidos
- El crecimiento es relativamente uniforme

### ⚠️ Ten cuidado con:
- **Extrapolación**: Predecir fuera del rango medido puede ser impreciso
- **Cambios bruscos**: Si la planta tuvo un cambio repentino (poda, enfermedad)
- **Demasiadas mediciones**: Más de 10 puntos puede crear curvas extrañas
- **Mediciones incorrectas**: Un dato malo afecta toda la predicción

### 💡 Consejos prácticos:
- Mide siempre a la misma hora del día
- Usa la misma técnica de medición
- Mide desde la base del suelo hasta el punto más alto
- Anota las condiciones (riego, luz, temperatura)

---

## 🔬 El Método de Lagrange Explicado

### ¿Qué hace?
Construye un polinomio (una fórmula matemática) que pasa exactamente por todos tus puntos medidos.

### Fórmula:
```
P(x) = Σ [y_j × L_j(x)]
```

Donde:
- `P(x)` es la altura predicha en el día x
- `y_j` son las alturas que mediste
- `L_j(x)` son los polinomios base de Lagrange

### ¿Por qué funciona?
Cada punto medido contribuye a la predicción final. Los puntos más cercanos al día que quieres predecir tienen mayor influencia.

---

## 🛠️ Requisitos Técnicos

### Para ejecutar la aplicación:
```bash
pip install -r requirements.txt
python main.py
```

### Dependencias:
- Python 3.8+
- customtkinter
- numpy

---

## 📚 Aprende Más

### Conceptos Matemáticos:
- Interpolación polinómica
- Polinomios de Lagrange
- Extrapolación vs Interpolación

### Aplicaciones Similares:
- Predicción de temperaturas
- Análisis de datos financieros
- Gráficos por computadora
- Procesamiento de señales

---

## 🎓 Proyecto Educativo

Este proyecto demuestra cómo un concepto matemático avanzado puede aplicarse a algo tan simple como observar crecer una planta. Es perfecto para:

- Ferias de ciencias
- Proyectos escolares
- Aprendizaje autodidacta
- Enseñanza de matemáticas aplicadas

---

## 🌟 Características de la Interfaz

- ✨ **Interfaz moderna y amigable**
- 📊 **Visualización paso a paso del proceso**
- 🎨 **Tema claro y colores agradables**
- 🔄 **Navegación intuitiva entre pasos**
- 📈 **Gráficos y explicaciones detalladas**
- 💾 **Ejemplos precargados para probar**

---

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:
- Agregar más ejemplos de plantas
- Mejorar la interfaz
- Añadir gráficas visuales
- Traducir a otros idiomas

---

## 📝 Notas Finales

Esta aplicación convierte un método matemático en algo tangible y útil. Cada vez que mides tu planta y haces una predicción, estás usando las mismas técnicas que se emplean en:
- Animación por computadora
- Análisis de datos científicos
- Predicción meteorológica
- Diseño de gráficos

**¡Las matemáticas están en todas partes, incluso en tu jardín! 🌱**

---

## 📞 Soporte

Si tienes dudas sobre cómo usar la aplicación:
1. Prueba los ejemplos incluidos
2. Lee la sección "ℹ️ Información" en la aplicación
3. Experimenta con diferentes valores

**¡Feliz jardinería matemática! 🌿📐**



