# 🧮 Métodos Numéricos - Resolución de Ecuaciones y Sistemas

Una colección completa de aplicaciones Python con interfaz gráfica moderna para resolver diferentes tipos de problemas matemáticos usando métodos numéricos clásicos.

**Desarrollado por:**
- **Andrés Monsivais Salazar**
- **Luis Andrés Salinas Lozano**

---

## 🎯 Métodos Implementados

### 🔢 [Método de Gauss-Seidel](./Gauss-Seidel/README.md)
**Resolución de Sistemas de Ecuaciones Lineales**

Resuelve sistemas de ecuaciones de la forma **Ax = b** usando el método iterativo de Gauss-Seidel.

**Características principales:**
- ✅ **Sistemas de 2×2 hasta 50×50** ecuaciones
- 🔧 **Auto-optimización**: Reordena matrices automáticamente para garantizar convergencia
- 🎨 **Visualización paso a paso** con navegación entre iteraciones
- 📊 **Interfaz adaptativa** que se redimensiona según el tamaño del sistema
- ✅ **Verificación por sustitución** de resultados

**Ejemplo de uso:**
```
10x₁ -  1x₂ + 2x₃ =  6
-1x₁ + 11x₂ - 1x₃ = 25
 2x₁ -  1x₂ +10x₃ = -11
```

---

### 📈 [Método de Bisección](./Biseccion/README.md)
**Resolución de Ecuaciones No Lineales**

Encuentra raíces de ecuaciones de la forma **f(x) = 0** usando el método de bisección basado en el teorema del valor intermedio.

**Características principales:**
- 🎯 **Múltiples tipos de funciones**: Polinomiales, exponenciales, trigonométricas, logarítmicas
- 🔄 **Visualización detallada** del proceso iterativo con navegación
- ✅ **Validación automática** de funciones e intervalos
- 📊 **Análisis paso a paso** de cada iteración
- 🔍 **Verificación de resultados** con sustitución

**Ejemplos de funciones soportadas:**
```python
x**3 - 2*x - 5         # Polinomiales
exp(-x) - x            # Exponenciales  
cos(x) - x             # Trigonométricas
log(x) - 1             # Logarítmicas
```

---

## 🚀 Instalación Rápida

### Requisitos Generales
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

### Instalación por Método

#### Para Gauss-Seidel:
```bash
cd Gauss-Seidel
pip install -r requirements.txt
python main.py
```

#### Para Bisección:
```bash
cd Biseccion
pip install -r requirements.txt
python main.py
```

### Dependencias Principales
Ambos proyectos comparten las mismas dependencias básicas:
- `customtkinter>=5.2.0` - Interfaz gráfica moderna
- `numpy>=1.21.0` - Cálculos numéricos eficientes

---

## 💡 ¿Cuál Método Usar?

### 🔢 Usa **Gauss-Seidel** cuando tengas:
- ✅ **Sistemas de ecuaciones lineales** (múltiples incógnitas)
- ✅ **Matrices grandes** (hasta 50×50)
- ✅ **Necesidad de soluciones exactas** para sistemas bien condicionados
- ✅ **Sistemas con estructura especial** (diagonalmente dominantes)

**Ejemplo típico:**
```
Encuentra x₁, x₂, x₃ tal que:
4x₁ + 1x₂ + 0x₃ = 7
1x₁ + 3x₂ + 1x₃ = 8
0x₁ + 1x₂ + 2x₃ = 5
```

### 📈 Usa **Bisección** cuando tengas:
- ✅ **Ecuaciones no lineales** (una incógnita)
- ✅ **Funciones transcendentales** complejas
- ✅ **Necesidad de garantía de convergencia**
- ✅ **Análisis de comportamiento** de funciones

**Ejemplo típico:**
```
Encuentra x tal que:
e^(-x) - x = 0
cos(x) - x = 0
x³ - 2x - 5 = 0
```

---

## 🎨 Características de la Interfaz

Ambas aplicaciones comparten un diseño moderno y consistente:

### 🎯 Diseño Visual Moderno
- **CustomTkinter**: Interfaz elegante con tema claro/oscuro
- **Cards visuales**: Cada paso mostrado en tarjetas organizadas
- **Código de colores**: Estados e indicadores visuales claros
- **Typography profesional**: Fuentes y tamaños optimizados

### 🔄 Navegación Intuitiva
- **Controles paso a paso**: Primera/Anterior/Siguiente/Última iteración
- **Barra de progreso**: Seguimiento visual del proceso
- **Pestañas organizadas**: Entrada de datos vs Proceso de solución
- **Estados interactivos**: Botones y controles con feedback

### 📊 Visualización Avanzada
- **Proceso iterativo completo**: Cada paso con cálculos detallados
- **Comparación entre iteraciones**: Cambios y convergencia
- **Verificación automática**: Sustitución de resultados
- **Estadísticas del proceso**: Iteraciones, errores, tiempo

---

## 📁 Estructura del Proyecto

```
Gauss-Seidel/
├── 📄 README.md
├── 🚀 main.py
├── 📋 requirements.txt
├── 🎨 gui/
│   ├── main_window.py
│   └── components.py
├── 🔢 solver/
│   └── gauss_seidel.py
├── 🛠️ utils/
│   └── validators.py
└── ✅ tests/

Biseccion/
├── 📄 README.md  
├── 🚀 main.py
├── 📋 requirements.txt
├── 🎨 gui/
│   ├── main_window.py
│   └── components.py
├── 📈 solver/
│   └── biseccion.py
├── 🛠️ utils/
│   └── validators.py
└── ✅ tests/

Bierge-Vieta/              # 🚧 En desarrollo
├── gui/
├── solver/
├── tests/
└── utils/
```

---

## 🔧 Características Técnicas Avanzadas

### 🛡️ Validación Robusta
- **Detección automática de errores** en entrada de datos
- **Sugerencias inteligentes** para corrección de problemas
- **Manejo de casos límite** y situaciones especiales
- **Mensajes de error descriptivos** y soluciones sugeridas

### ⚡ Optimizaciones de Performance
- **Algoritmos optimizados** para sistemas grandes
- **Manejo eficiente de memoria** para matrices extensas
- **Cálculos paralelos** donde es posible
- **Interface responsive** que no se bloquea durante cálculos

### 🎯 Precisión Numérica
- **Tolerancias configurables** para diferentes niveles de precisión
- **Detección de convergencia** inteligente
- **Análisis de estabilidad** numérica
- **Verificación cruzada** de resultados

---

## 🧪 Casos de Uso Educativos

### 👨‍🎓 Para Estudiantes
- **Visualización completa** del proceso iterativo
- **Comprensión paso a paso** de los algoritmos
- **Experimentación interactiva** con diferentes parámetros
- **Verificación manual** de cálculos

### 👨‍🏫 Para Profesores
- **Material didáctico visual** para clases
- **Ejemplos predefinidos** listos para usar
- **Comparación de métodos** y comportamientos
- **Análisis de convergencia** en tiempo real

### 🔬 Para Investigación
- **Análisis de estabilidad** numérica
- **Comparación de performance** entre métodos
- **Validación de resultados** con métodos alternativos
- **Documentación detallada** del proceso

---

## 🛠️ Desarrollo y Contribución

### 🏗️ Arquitectura del Código
- **Separación clara** entre lógica y presentación
- **Módulos reutilizables** entre proyectos
- **Testing comprehensivo** con pytest
- **Documentación completa** en código

### 🤝 Cómo Contribuir
1. **Fork** el proyecto
2. **Crear rama** de feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** los cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abrir Pull Request**

### ✅ Standards de Calidad
- **PEP 8** compliance para Python
- **Type hints** donde sea apropiado
- **Docstrings** completos para funciones públicas
- **Tests unitarios** para nueva funcionalidad

---

## 🚨 Solución de Problemas

### Problemas Comunes

#### ❌ Error al iniciar la aplicación
```bash
# Verificar versión de Python
python --version  # Debe ser 3.8+

# Instalar dependencias
pip install -r requirements.txt
```

#### ❌ Error "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
cd Gauss-Seidel  # o cd Biseccion
pip install -r requirements.txt
```

#### ❌ Interfaz se ve mal en Windows
```bash
# Actualizar customtkinter a la última versión
pip install --upgrade customtkinter
```

### 🔍 Debugging
Si encuentras errores:
1. **Revisa la consola** para mensajes de error detallados
2. **Verifica los datos de entrada** (números válidos, sin celdas vacías)
3. **Comprueba las condiciones** de convergencia del método
4. **Consulta el README específico** del método que estés usando

---

## 📚 Recursos Adicionales

### 📖 Documentación Detallada
- [🔢 Guía completa de Gauss-Seidel](./Gauss-Seidel/README.md)
- [📈 Guía completa de Bisección](./Biseccion/README.md)

### 🎓 Material Educativo
- **Ejemplos paso a paso** incluidos en cada aplicación
- **Casos de prueba** documentados en los tests
- **Explicaciones teóricas** en los comentarios del código

### 🔬 Referencias Académicas
- Burden, R.L., Faires, J.D. - "Análisis Numérico"
- Chapra, S.C., Canale, R.P. - "Métodos Numéricos para Ingenieros"

---

## 📄 Licencia

Este proyecto es de **uso educativo**.

---

## 📞 Contacto y Soporte

**Desarrolladores:**
- **Andrés Monsivais Salazar**
- **Luis Andrés Salinas Lozano**

**Uso académico:** Este software está diseñado para fines educativos y de investigación en el área de métodos numéricos.

---

**¡Explora el fascinante mundo de los métodos numéricos con herramientas visuales e interactivas! 🚀**

*Última actualización: Septiembre 2025*
