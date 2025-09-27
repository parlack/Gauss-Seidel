# 📈 Método de Bisección - Resolución de Ecuaciones No Lineales

Una aplicación Python con interfaz gráfica moderna que implementa el **método de bisección** para encontrar raíces de ecuaciones no lineales de la forma f(x) = 0, con visualización paso a paso del proceso iterativo completo.

**Desarrollado por:**
- **Andrés Monsivais Salazar**
- **Luis Andrés Salinas Lozano**

---

## ✨ Características Principales

### 🎨 Interfaz Visual Moderna
- **🖥️ CustomTkinter**: Diseño limpio y profesional con tema claro
- **📱 Responsive Design**: Interfaz que se adapta al contenido
- **🎯 Navegación intuitiva**: Pestañas organizadas y controles claros
- **⚡ Feedback inmediato**: Validación en tiempo real

### 🔄 Visualización Paso a Paso
- **📊 Cards visuales**: Cada iteración en tarjetas organizadas  
- **🎮 Navegación completa**: Primera/Anterior/Siguiente/Última iteración
- **📈 Progreso visual**: Barra de progreso y contador de iteraciones
- **📋 Detalles completos**: Cálculos, decisiones y convergencia

### 🎯 Funciones Matemáticas Avanzadas
- **🔢 Polinomiales**: x², x³, x⁴, etc.
- **📈 Exponenciales**: eˣ, e⁻ˣ, 2ˣ, etc.
- **📐 Trigonométricas**: sin(x), cos(x), tan(x)
- **📊 Logarítmicas**: ln(x), log₁₀(x)
- **🔀 Combinadas**: Expresiones complejas mixtas

### ✅ Validación Inteligente
- **🔍 Auto-verificación**: Valida función e intervalo automáticamente
- **⚠️ Detección de errores**: Mensajes claros y soluciones sugeridas
- **🎯 Garantía de convergencia**: Verifica condiciones del teorema del valor intermedio
- **💡 Ejemplos integrados**: Sistemas predefinidos listos para usar

### ⚙️ Configuración Flexible
- **🎚️ Tolerancia ajustable**: Precisión configurable (default: 0.000001%)
- **🔄 Iteraciones máximas**: Límite configurable (default: 100)
- **🎨 Interface adaptativa**: Se ajusta al contenido y proceso

---

## 🚀 Instalación y Uso

### 📋 Requisitos
- **Python 3.8 o superior**
- **pip** (gestor de paquetes)

### 💾 Instalación
```bash
# 1. Navegar al directorio
cd Biseccion

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación
python main.py
```

### 📦 Dependencias
- `customtkinter>=5.2.0` - Interfaz gráfica moderna
- `numpy>=1.21.0` - Cálculos numéricos eficientes

---

## 🎯 Guía de Uso

### 1. 📝 Entrada de Datos

#### **Función f(x)**
Ingresa la función en el campo principal usando la sintaxis de Python:

**Ejemplos válidos:**
```python
# Polinomiales
x**3 - 2*x - 5
x**2 - 4
2*x**4 - x**2 + 1

# Exponenciales  
exp(-x) - x
2*exp(x) - 5
exp(x**2) - 3

# Trigonométricas
cos(x) - x  
sin(x) - 0.5
tan(x) - x

# Logarítmicas
log(x) - 1
log10(x) + 2
log(x**2) - 3

# Combinadas complejas
x**2 + sin(x) - 1
exp(x) - 2*cos(x)
log(x) + x**3 - 5
```

#### **Intervalo [xl, xu]**
- **xl**: Límite inferior donde buscar la raíz
- **xu**: Límite superior donde buscar la raíz
- **Condición**: f(xl) y f(xu) deben tener signos opuestos

#### **Configuración del Solver**
- **Tolerancia**: Criterio de parada (% de error relativo)
- **Máx. Iteraciones**: Límite de iteraciones para evitar bucles infinitos

### 2. 🔧 Controles Principales

#### **🧹 Limpiar Todo**
Borra todas las entradas y reinicia la aplicación

#### **📋 Ejemplo** 
Carga automáticamente uno de estos sistemas predefinidos:
- **Polinomio Cúbico**: f(x) = x³ - 2x - 5 en [1, 3]
- **Exponencial**: f(x) = e⁻ˣ - x en [0, 1]  
- **Trigonométrica**: f(x) = cos(x) - x en [0, 1]

#### **✅ Validar**
Verifica que:
- La función esté correctamente escrita
- El intervalo sea válido (xl < xu)
- f(xl) y f(xu) tengan signos opuestos
- Se garantice la existencia de al menos una raíz

#### **🚀 Resolver Ecuación**
Inicia el proceso de bisección con visualización completa

### 3. 📊 Visualización de Resultados

#### **🔄 Vista Iterativa**
Cada iteración muestra:

**📊 Valores del Intervalo:**
- xl, xr, xu (límites e punto medio)
- f(xl), f(xr), f(xu) (evaluaciones de función)
- Código de colores según signos

**🎯 Criterio de Decisión:**
- Producto f(xl) × f(xr)
- Selección del nuevo intervalo basado en signos
- Explicación clara del proceso

**📈 Convergencia:**
- Error relativo porcentual entre iteraciones
- Indicador visual de convergencia alcanzada
- Progreso hacia la solución

#### **🏆 Resultado Final**
- **Raíz aproximada**: Valor de x donde f(x) ≈ 0
- **Iteraciones totales**: Número de pasos necesarios
- **Error final**: Precisión alcanzada
- **Verificación**: f(raíz) para comprobar la solución

---

## 🔬 Método de Bisección - Teoría

### 📘 Fundamento Teórico

El método de bisección se basa en el **Teorema del Valor Intermedio**:

> **Si f(x) es continua en [a,b] y f(a) × f(b) < 0, entonces existe al menos un valor c ∈ (a,b) tal que f(c) = 0.**

### 🔄 Algoritmo Paso a Paso

1. **🔍 Verificar condiciones iniciales**
   - f(xl) × f(xu) < 0 (signos opuestos)
   - xl < xu (intervalo válido)

2. **📐 Calcular punto medio**
   ```
   xr = (xl + xu) / 2
   ```

3. **📊 Evaluar función**
   ```
   f(xr) = función evaluada en xr
   ```

4. **🎯 Seleccionar nuevo intervalo**
   - Si f(xl) × f(xr) < 0 → Raíz en [xl, xr] → xu = xr
   - Si f(xl) × f(xr) > 0 → Raíz en [xr, xu] → xl = xr
   - Si f(xr) = 0 → Raíz exacta encontrada

5. **📏 Calcular error relativo**
   ```
   εa = |((xr_nuevo - xr_anterior) / xr_nuevo)| × 100%
   ```

6. **✅ Verificar convergencia**
   - Si εa < tolerancia → ¡Convergencia alcanzada!
   - Si iteración ≥ máximo → Detener proceso

7. **🔄 Repetir** desde el paso 2 hasta convergencia

### 📈 Análisis de Convergencia

#### **✅ Ventajas**
- **🔒 Garantía de convergencia** (si se cumplen condiciones iniciales)
- **🧮 Simplicidad conceptual** y de implementación
- **💪 Estabilidad numérica** robusta contra errores de redondeo  
- **📊 Convergencia predecible** (error se reduce a la mitad cada iteración)
- **🎯 Funciona con cualquier función continua**

#### **❌ Limitaciones**  
- **🐌 Convergencia lenta** (lineal, no cuadrática como Newton-Raphson)
- **📐 Requiere intervalo inicial** con cambio de signo
- **🔍 Solo encuentra una raíz** por ejecución
- **❌ No funciona con raíces múltiples** o tangencias al eje X
- **📈 No aprovecha información de la derivada**

### 🎯 Casos de Uso Ideales

- **📊 Ecuaciones transcendentales complejas** (e^x + ln(x) = 0)
- **🔧 Funciones con múltiples discontinuidades**
- **✅ Cuando se requiere garantía absoluta de convergencia**
- **📈 Análisis de comportamiento de funciones no lineales**
- **🎓 Propósitos educativos y demostración de conceptos**

---

## 🧪 Ejemplos Detallados

### 📊 Ejemplo 1: Polinomio Cúbico
```python
f(x) = x³ - 2x - 5
Intervalo: [1, 3]

f(1) = 1 - 2 - 5 = -6
f(3) = 27 - 6 - 5 = 16
f(1) × f(3) = -96 < 0 ✅

Raíz esperada: x ≈ 2.094
```

### 📈 Ejemplo 2: Función Exponencial
```python
f(x) = e^(-x) - x  
Intervalo: [0, 1]

f(0) = 1 - 0 = 1
f(1) = 0.368 - 1 = -0.632
f(0) × f(1) = -0.632 < 0 ✅

Raíz esperada: x ≈ 0.567
```

### 📐 Ejemplo 3: Función Trigonométrica
```python
f(x) = cos(x) - x
Intervalo: [0, 1]

f(0) = 1 - 0 = 1  
f(1) = 0.540 - 1 = -0.460
f(0) × f(1) = -0.460 < 0 ✅

Raíz esperada: x ≈ 0.739
```

---

## 🛡️ Funciones Soportadas

### 🔢 Operadores Básicos
- `+`, `-`, `*`, `/` - Operaciones aritméticas
- `**` o `^` - Potenciación (x**2, x^3)
- `()` - Paréntesis para agrupación

### 📐 Funciones Matemáticas
- `sin(x)`, `cos(x)`, `tan(x)` - Trigonométricas básicas
- `asin(x)`, `acos(x)`, `atan(x)` - Trigonométricas inversas
- `sinh(x)`, `cosh(x)`, `tanh(x)` - Hiperbólicas
- `exp(x)` - Función exponencial e^x
- `log(x)` - Logaritmo natural (ln)
- `log10(x)` - Logaritmo base 10
- `sqrt(x)` - Raíz cuadrada
- `abs(x)` - Valor absoluto
- `pow(x, n)` - Potencia (alternativa a **)

### 📊 Constantes Matemáticas
- `pi` - π = 3.14159265...
- `e` - e = 2.71828182...

### ⚠️ Restricciones y Cuidados
- **División por cero**: Evitar términos como `1/(x-a)` cuando x puede ser a
- **Logaritmos**: log(x) requiere x > 0
- **Raíces pares**: sqrt(x) requiere x ≥ 0  
- **Dominios**: Verificar que la función esté definida en todo el intervalo

---

## 📁 Estructura del Proyecto

```
Biseccion/
├── 📄 README.md              # Esta documentación
├── 🚀 main.py                # Punto de entrada principal con manejo de errores
├── 📋 requirements.txt       # Dependencias del proyecto
├── 🔧 TROUBLESHOOTING.md     # Guía de solución de problemas
├── 🎨 gui/                   # Interfaz gráfica de usuario
│   ├── __init__.py
│   ├── main_window.py        # Ventana principal con pestañas
│   └── components.py         # Componentes personalizados (botones, entradas, visualización)
├── 📈 solver/                # Motor de cálculo numérico
│   ├── __init__.py
│   └── biseccion.py          # Implementación del método de bisección
├── 🛠️ utils/                 # Utilidades y herramientas auxiliares
│   ├── __init__.py
│   └── validators.py         # Validadores de funciones e intervalos
└── ✅ tests/                 # Suite de pruebas unitarias
    ├── __init__.py
    └── test_solver.py        # Tests del algoritmo de bisección
```

### 📋 Descripción de Módulos

#### **🚀 main.py**
- Verificación de dependencias al inicio
- Manejo de errores de importación  
- Configuración del protocolo de cierre
- Punto de entrada principal

#### **🎨 gui/main_window.py**
- Ventana principal con pestañas organizadas
- Manejo de eventos de interfaz
- Integración con el solver
- Gestión de estados de la aplicación

#### **🎨 gui/components.py**  
- Componentes personalizados (ModernButton, ModernEntry)
- Panel de entrada de funciones con ayuda
- Panel de configuración de intervalos
- Sistema completo de visualización paso a paso

#### **📈 solver/biseccion.py**
- Algoritmo completo de bisección
- Generación de funciones desde strings
- Validación de funciones e intervalos
- Sistema de paso a paso con historial

#### **🛠️ utils/validators.py**
- Validación de expresiones matemáticas
- Verificación de intervalos apropiados
- Sugerencias de intervalos alternativos
- Análisis de funciones para bisección

---

## ✅ Testing y Calidad

### 🧪 Ejecutar Tests
```bash
# Todos los tests
python -m pytest tests/ -v

# Solo tests del solver  
python -m pytest tests/test_solver.py -v

# Test específico con detalle
python -m pytest tests/test_solver.py::TestBiseccionSolver::test_polynomial_function -v

# Con cobertura
python -m pytest tests/ --cov=solver --cov-report=html
```

### 📊 Cobertura de Tests
Los tests incluyen verificación de:

**✅ Funcionalidad Core:**
- Algoritmo de bisección con diferentes funciones
- Convergencia con varias tolerancias  
- Manejo de casos límite y errores
- Generación paso a paso completa

**✅ Validación Robusta:**
- Funciones válidas e inválidas
- Intervalos apropiados e inapropiados
- Condiciones de convergencia
- Manejo de excepciones

**✅ Tipos de Funciones:**
- Polinomiales de diversos grados
- Exponenciales y logarítmicas  
- Trigonométricas básicas e inversas
- Combinaciones complejas

---

## 🚨 Solución de Problemas

### ❌ Errores Comunes

#### **"La aplicación no inicia"**
```bash
# Verificar versión de Python
python --version  # Debe ser 3.8+

# Reinstalar dependencias
pip uninstall customtkinter numpy
pip install -r requirements.txt

# Verificar instalación
python -c "import customtkinter, numpy; print('OK')"
```

#### **"Error inesperado: unsupported operand type(s)"**
Este error ha sido completamente corregido en la versión actual. Si aparece:
```bash
# Limpiar cache de Python
find . -name "__pycache__" -exec rm -rf {} +  # Linux/Mac
Get-ChildItem -Directory -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force  # Windows

# Relanzar aplicación
python main.py
```

#### **"La función no se puede evaluar"**
- Verifica la sintaxis: usa `**` en lugar de `^` para potencias
- Evita divisiones por cero: `1/(x-2)` falla si x=2 está en el intervalo
- Dominios restringidos: `log(x)` requiere x > 0, `sqrt(x)` requiere x ≥ 0

#### **"f(xl) y f(xu) deben tener signos opuestos"**
- Cambia el intervalo [xl, xu]
- Usa la función de sugerencia automática
- Verifica que la función tenga raíces en el rango esperado

### 🔧 Optimización de Performance

#### **Para funciones complejas:**
- Reduce la tolerancia si la convergencia es lenta  
- Aumenta el máximo de iteraciones para mayor precisión
- Usa intervalos más pequeños cuando sea posible

#### **Para sistemas lentos:**
- Cierra otras aplicaciones pesadas
- Usa tolerancias más relajadas (0.001% en lugar de 0.000001%)
- Considera simplificar la función si es muy compleja

---

## 🎓 Uso Educativo

### 👨‍🎓 Para Estudiantes
- **📚 Comprensión visual** del método paso a paso
- **🔬 Experimentación** con diferentes funciones y parámetros
- **✅ Verificación manual** de cálculos iterativos  
- **📈 Análisis de convergencia** en tiempo real

### 👨‍🏫 Para Profesores  
- **📊 Ejemplos listos** para clases teóricas
- **🎬 Demostración visual** del teorema del valor intermedio
- **📋 Material didáctico** interactivo y engaging
- **⚖️ Comparación** con otros métodos numéricos

### 🔬 Para Investigación
- **📈 Análisis de estabilidad** numérica
- **⚡ Validación rápida** de soluciones
- **📊 Documentación automática** del proceso iterativo
- **🔍 Estudio de casos límite** y comportamientos

---

## 🤝 Contribuciones y Desarrollo

### 🏗️ Estructura de Desarrollo
```bash
# Setup de desarrollo
git clone [repository]
cd Biseccion
pip install -r requirements.txt
pip install pytest pytest-cov  # Para testing

# Ejecución de tests antes de commits
python -m pytest tests/ -v
```

### 📝 Standards de Código
- **PEP 8** compliance para legibilidad
- **Type hints** para claridad de interfaces
- **Docstrings** completos en funciones públicas
- **Comentarios explicativos** en lógica compleja

### 🐛 Reportar Problemas
1. **Describe el problema** con pasos para reproducir
2. **Incluye información del sistema** (Python version, OS)
3. **Adjunta screenshot** si es problema visual
4. **Copia el traceback completo** si hay errores

---

## 📞 Soporte y Contacto

### 🎯 Soporte Técnico
Si encuentras problemas:
1. **Consulta esta documentación** - Cubre la mayoría de casos
2. **Revisa [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - Problemas específicos
3. **Verifica los requirements** - Python 3.8+ y dependencias actualizadas
4. **Prueba los ejemplos predefinidos** - Para validar funcionamiento básico

### 👥 Equipo de Desarrollo
**Andrés Monsivais Salazar** y **Luis Andrés Salinas Lozano**

### 📚 Uso Académico
Este software está específicamente diseñado para:
- **🎓 Cursos de métodos numéricos**
- **📊 Análisis matemático computacional**  
- **🔬 Investigación en matemática aplicada**
- **🏫 Material didáctico interactivo**

---

### 📜 Licencia Educativa
- **Uso libre** para propósitos educativos y académicos
- **Modificación permitida** para adaptación curricular
- **Distribución permitida** con atribución apropiada
- **Uso comercial** requiere autorización explícita

### 🏆 Reconocimientos
- **Instituciones académicas** que apoyan el desarrollo
- **Comunidad open source** por herramientas y librerías
- **Estudiantes y profesores** que proporcionan feedback

---

**🚀 ¡Explora el método de bisección de manera visual e interactiva!**

*Desarrollado con ❤️ para la educación en métodos numéricos*

**Última actualización: Septiembre 2025**