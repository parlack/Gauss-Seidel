import customtkinter as ctk
import tkinter as tk
from typing import List, Callable, Optional, Tuple
import math


class ModernButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        # Configuración por defecto para botones modernos
        default_kwargs = {
            "corner_radius": 8,  # Esquinas redondeadas
            "font": ctk.CTkFont(size=14, weight="bold"),  # Fuente en negrita
            "height": 40  # Altura fija
        }
        # Permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **default_kwargs)


class ModernEntry(ctk.CTkEntry):
    def __init__(self, parent, placeholder="", **kwargs):
        # Configuración por defecto para campos de entrada
        default_kwargs = {
            "corner_radius": 8,  # Esquinas redondeadas
            "font": ctk.CTkFont(size=12),  # Fuente de tamaño medio
            "height": 35,  # Altura fija
            "placeholder_text": placeholder  # Texto de ayuda
        }
        # Permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)


class FunctionInputPanel(ctk.CTkFrame):
    """
    Panel para ingresar la función f(x)
    
    Widget especializado para introducir funciones matemáticas
    con validación y ayuda visual
    """
    
    def __init__(self, parent, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_change = on_change
        self.setup_ui()
    
    def setup_ui(self):
        # Título del panel
        title = ctk.CTkLabel(
            self,
            text="Función f(x)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        # Subtitle explicativo
        subtitle = ctk.CTkLabel(
            self,
            text="Ingresa la función para encontrar sus raíces (f(x) = 0)",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        subtitle.pack(pady=(0, 15))
        
        # Frame para la entrada de función
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Etiqueta f(x) =
        func_label = ctk.CTkLabel(
            input_frame,
            text="f(x) =",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        func_label.pack(side="left", padx=(15, 5), pady=15)
        
        # Campo de entrada para la función
        self.function_entry = ModernEntry(
            input_frame,
            placeholder="Ej: x**3 - 2*x - 5",
            font=ctk.CTkFont(size=14),
            width=400
        )
        self.function_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=15)
        
        # Configurar callback para detectar cambios
        if self.on_change:
            self.function_entry.bind('<KeyRelease>', self._on_function_change)
        
        # Panel de ayuda
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Título de ayuda
        help_title = ctk.CTkLabel(
            help_frame,
            text="💡 Funciones Disponibles:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        help_title.pack(pady=(10, 5))
        
        # Lista de funciones disponibles
        help_text = """
• Potencias: x**2, x**3, pow(x, n)
• Exponenciales: exp(x), e**x  
• Logaritmos: log(x), log10(x)
• Trigonométricas: sin(x), cos(x), tan(x)
• Raíz cuadrada: sqrt(x)
• Constantes: pi, e
• Operaciones: +, -, *, /, ()"""
        
        help_label = ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60",
            justify="left"
        )
        help_label.pack(padx=15, pady=(0, 10))
    
    def get_function(self) -> str:
        """Obtiene la función ingresada"""
        return self.function_entry.get().strip()
    
    def set_function(self, function_str: str):
        """Establece una función en el campo"""
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, function_str)
    
    def clear(self):
        """Limpia el campo de función"""
        self.function_entry.delete(0, tk.END)
    
    def _on_function_change(self, event):
        """Callback interno para cambios en la función"""
        if self.on_change:
            self.on_change()


class IntervalInputPanel(ctk.CTkFrame):
    """
    Panel para ingresar el intervalo [xl, xu]
    
    Widget especializado para introducir el intervalo inicial
    donde se buscará la raíz
    """
    
    def __init__(self, parent, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_change = on_change
        self.setup_ui()
    
    def setup_ui(self):
        # Título del panel
        title = ctk.CTkLabel(
            self,
            text="Intervalo Inicial [xl, xu]",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        # Subtítulo explicativo
        subtitle = ctk.CTkLabel(
            self,
            text="Define el intervalo donde f(xl) y f(xu) tienen signos opuestos",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=280
        )
        subtitle.pack(pady=(0, 15))
        
        # Frame para xl (límite inferior)
        xl_frame = ctk.CTkFrame(self)
        xl_frame.pack(fill="x", padx=20, pady=5)
        
        xl_label = ctk.CTkLabel(
            xl_frame,
            text="xl =",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=40
        )
        xl_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.xl_entry = ModernEntry(
            xl_frame,
            placeholder="Límite inferior",
            width=150
        )
        self.xl_entry.pack(side="left", padx=(0, 15), pady=10, fill="x", expand=True)
        
        # Frame para xu (límite superior)
        xu_frame = ctk.CTkFrame(self)
        xu_frame.pack(fill="x", padx=20, pady=5)
        
        xu_label = ctk.CTkLabel(
            xu_frame,
            text="xu =",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=40
        )
        xu_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.xu_entry = ModernEntry(
            xu_frame,
            placeholder="Límite superior",
            width=150
        )
        self.xu_entry.pack(side="left", padx=(0, 15), pady=10, fill="x", expand=True)
        
        # Configurar callbacks para detectar cambios
        if self.on_change:
            self.xl_entry.bind('<KeyRelease>', self._on_interval_change)
            self.xu_entry.bind('<KeyRelease>', self._on_interval_change)
        
        # Panel de ayuda para intervalos
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        help_title = ctk.CTkLabel(
            help_frame,
            text="📋 Requisitos:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        help_title.pack(pady=(10, 5))
        
        help_text = """
• xl < xu (límite inferior menor que superior)
• f(xl) y f(xu) deben tener signos opuestos
• La función debe ser continua en [xl, xu]"""
        
        help_label = ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60",
            justify="left"
        )
        help_label.pack(padx=15, pady=(0, 10))
    
    def get_values(self) -> Tuple[float, float]:
        """Obtiene los valores del intervalo como (xl, xu)"""
        try:
            xl = float(self.xl_entry.get()) if self.xl_entry.get().strip() else 0.0
            xu = float(self.xu_entry.get()) if self.xu_entry.get().strip() else 1.0
            return xl, xu
        except ValueError:
            return 0.0, 1.0
    
    def set_values(self, xl: float, xu: float):
        """Establece los valores del intervalo"""
        self.xl_entry.delete(0, tk.END)
        self.xl_entry.insert(0, str(xl))
        
        self.xu_entry.delete(0, tk.END)
        self.xu_entry.insert(0, str(xu))
    
    def clear(self):
        """Limpia los campos del intervalo"""
        self.xl_entry.delete(0, tk.END)
        self.xu_entry.delete(0, tk.END)
    
    def _on_interval_change(self, event):
        """Callback interno para cambios en el intervalo"""
        if self.on_change:
            self.on_change()


class VisualizationPanel(ctk.CTkFrame):
    """
    Panel para visualizar el proceso de bisección
    
    Componente principal que muestra el proceso iterativo de bisección
    incluye navegación entre iteraciones y visualización detallada de cada paso
    """
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.setup_ui()
        self.current_iteration = 0
        self.total_iterations = 0
        self.steps_data = []
    
    def setup_ui(self):
        # Título con diseño
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Proceso de Solución - Método de Bisección",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        self.title_label.pack(side="left")
        
        # Indicador de progreso visual
        self.progress_frame = ctk.CTkFrame(header_frame)
        self.progress_frame.pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=200,
            height=20,
            progress_color=("#1f538d", "#4a9eff")
        )
        self.progress_bar.pack(padx=10, pady=10)
        
        # Frame de controles
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Información de iteración
        info_frame = ctk.CTkFrame(controls_frame)
        info_frame.pack(side="left", padx=10, pady=5)
        
        self.iteration_label = ctk.CTkLabel(
            info_frame,
            text="Iteración: 0 / 0",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.iteration_label.pack(side="left", padx=15, pady=8)
        
        self.error_label = ctk.CTkLabel(
            info_frame,
            text="Error: 0.000000%",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.error_label.pack(side="left", padx=15, pady=8)
        
        # Botones de navegación
        nav_frame = ctk.CTkFrame(controls_frame)
        nav_frame.pack(side="right", padx=10, pady=5)
        
        self.first_btn = ModernButton(
            nav_frame,
            text="Primero",
            command=self.first_iteration,
            width=90,
            height=35
        )
        self.first_btn.pack(side="left", padx=2)
        
        self.prev_btn = ModernButton(
            nav_frame,
            text="Anterior",
            command=self.prev_iteration,
            width=90,
            height=35
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.next_btn = ModernButton(
            nav_frame,
            text="Siguiente",
            command=self.next_iteration,
            width=90,
            height=35
        )
        self.next_btn.pack(side="left", padx=2)
        
        self.last_btn = ModernButton(
            nav_frame,
            text="Último",
            command=self.last_iteration,
            width=90,
            height=35
        )
        self.last_btn.pack(side="left", padx=2)
        
        # Notebook para diferentes vistas
        self.notebook = ctk.CTkTabview(self, width=1000)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear tabs principales
        self.notebook.add("Vista Iterativa")
        self.notebook.add("Resultado Final")
        
        self.setup_iterations_tab()
        self.setup_result_tab()
    
    def setup_iterations_tab(self):
        """Configura la tab de iteraciones"""
        self.iterations_frame = self.notebook.tab("Vista Iterativa")
        
        # Frame scrollable para las iteraciones
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.iterations_frame,
            corner_radius=10
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para mostrar la iteración actual
        self.current_iteration_frame = ctk.CTkFrame(
            self.scroll_frame,
            corner_radius=15
        )
        self.current_iteration_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_result_tab(self):
        """Configura la tab de resultado"""
        self.result_frame = self.notebook.tab("Resultado Final")
        
        # Contenedor con scroll para todo el contenido del resultado
        self.result_scroll = ctk.CTkScrollableFrame(self.result_frame)
        self.result_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header del resultado
        result_header = ctk.CTkFrame(self.result_scroll)
        result_header.pack(fill="x", padx=10, pady=10)
        
        self.convergence_status = ctk.CTkLabel(
            result_header,
            text="⏳ Procesando...",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="orange"
        )
        self.convergence_status.pack(pady=20)
        
        # Estadísticas del proceso
        stats_frame = ctk.CTkFrame(self.result_scroll)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        # Grid de estadísticas
        self.stats_grid = ctk.CTkFrame(stats_frame)
        self.stats_grid.pack(fill="x", padx=20, pady=10)
        
        # Solución visual
        solution_frame = ctk.CTkFrame(self.result_scroll)
        solution_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        solution_title = ctk.CTkLabel(
            solution_frame,
            text="🎯 Raíz Encontrada",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        solution_title.pack(pady=(15, 10))
        
        # Contenedor para la solución
        self.solution_container = ctk.CTkFrame(solution_frame)
        self.solution_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_visualization(self, steps_data: List):
        """Actualiza la visualización con nuevos datos"""
        self.steps_data = steps_data
        self.total_iterations = len([s for s in steps_data if s.get('type') == 'iteration'])
        self.current_iteration = 0
        self.update_current_step()
        self.update_result_display()
    
    def update_current_step(self):
        """Actualiza la visualización del paso actual"""
        if not self.steps_data:
            return
        
        # Encontrar pasos de iteración
        iteration_steps = [s for s in self.steps_data if s.get('type') == 'iteration']
        
        if self.current_iteration < len(iteration_steps):
            step = iteration_steps[self.current_iteration]
            
            # Actualizar información en header
            self.iteration_label.configure(
                text=f"Iteración: {self.current_iteration + 1} / {len(iteration_steps)}"
            )
            
            error_percent = step.get('error_percent', 0)
            try:
                err_val = float(error_percent)
                if math.isfinite(err_val):
                    self.error_label.configure(text=f"Error: {err_val:.6f}%")
                else:
                    self.error_label.configure(text=f"Error: {error_percent}")
            except Exception:
                self.error_label.configure(text=f"Error: {error_percent}")
            
            # Actualizar barra de progreso
            progress = (self.current_iteration + 1) / len(iteration_steps)
            self.progress_bar.set(progress)
            
            # Limpiar frame actual
            for widget in self.current_iteration_frame.winfo_children():
                widget.destroy()
            
            # Crear card visual para la iteración
            self.create_iteration_card(step)
        
        # Actualizar botones
        self.update_navigation_buttons()
    
    def create_iteration_card(self, step):
        """Crea una tarjeta visual para mostrar una iteración de bisección"""
        # Título de la iteración
        title_frame = ctk.CTkFrame(self.current_iteration_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"🔄 Iteración {step['iteration']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(side="left")
        
        # Crear badge de error con protección ante valores no numéricos
        try:
            err_val = float(step.get('error_percent', 0))
            err_text = f"Error: {err_val:.8f}%"
        except Exception:
            err_text = f"Error: {step.get('error_percent')}%"

        error_badge = ctk.CTkLabel(
            title_frame,
            text=err_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=15,
            fg_color=("gray80", "gray20"),
            width=150,
            height=30
        )
        error_badge.pack(side="right", padx=10)
        
        # Contenedor principal con layout organizado
        main_container = ctk.CTkFrame(self.current_iteration_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sección 1: Valores del intervalo
        interval_section = ctk.CTkFrame(main_container)
        interval_section.pack(fill="x", padx=10, pady=(10, 5))
        
        interval_title = ctk.CTkLabel(
            interval_section,
            text="📊 Valores del Intervalo",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        interval_title.pack(pady=(15, 10))
        
        # Grid para mostrar xl, xr, xu
        values_grid = ctk.CTkFrame(interval_section)
        values_grid.pack(fill="x", padx=20, pady=(0, 15))
        
        # Crear columnas para xl, xr, xu con validación
        values_data = [
            ("xl", step.get('xl', 0), step.get('f_xl', 0)),
            ("xr", step.get('xr', 0), step.get('f_xr', 0)),
            ("xu", step.get('xu', 0), step.get('f_xu', 0))
        ]
        
        for i, (label, value, f_value) in enumerate(values_data):
            col_frame = ctk.CTkFrame(values_grid)
            col_frame.grid(row=0, column=i, padx=5, pady=10, sticky="ew")
            
            # Variable name
            var_label = ctk.CTkLabel(
                col_frame,
                text=label,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            var_label.pack(pady=(10, 2))
            
            # Variable value con validación
            if isinstance(value, (int, float)) and math.isfinite(value):
                val_text = f"{value:.6f}"
            else:
                val_text = str(value)
                
            val_label = ctk.CTkLabel(
                col_frame,
                text=val_text,
                font=ctk.CTkFont(size=14)
            )
            val_label.pack(pady=2)
            
            # Function value
            if isinstance(f_value, (int, float)) and math.isfinite(f_value):
                func_color = "green" if abs(f_value) < 0.001 else ("red" if f_value < 0 else "orange")
                func_text = f"f({label}) = {f_value:.6f}"
            else:
                func_color = "red"
                func_text = f"f({label}) = {f_value}"
                
            func_label = ctk.CTkLabel(
                col_frame,
                text=func_text,
                font=ctk.CTkFont(size=12),
                text_color=func_color
            )
            func_label.pack(pady=(2, 10))
        
        # Configurar grid weights
        for j in range(3):
            values_grid.grid_columnconfigure(j, weight=1)
        
        # Sección 2: Criterio de decisión
        decision_section = ctk.CTkFrame(main_container)
        decision_section.pack(fill="x", padx=10, pady=5)
        
        decision_title = ctk.CTkLabel(
            decision_section,
            text="🎯 Criterio de Decisión",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        decision_title.pack(pady=(15, 10))
        
        # Mostrar el producto f(xl) * f(xr)
        product_frame = ctk.CTkFrame(decision_section)
        product_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        product_value = step.get('f_xl_times_f_xr', 0)
        f_xl = step.get('f_xl', 0)
        f_xr = step.get('f_xr', 0)
        
        # Verificar que los valores sean válidos para mostrar
        try:
            if all(isinstance(val, (int, float)) and math.isfinite(val) for val in [f_xl, f_xr, product_value]):
                product_text = f"f(xl) × f(xr) = {f_xl:.6f} × {f_xr:.6f} = {product_value:.6f}"
            else:
                product_text = f"f(xl) × f(xr) = {f_xl} × {f_xr} = {product_value}"
        except Exception:
            product_text = "f(xl) × f(xr) = (valores no disponibles)"
        
        product_label = ctk.CTkLabel(
            product_frame,
            text=product_text,
            font=ctk.CTkFont(size=13)
        )
        product_label.pack(pady=10)
        
        # Decisión basada en el signo
        decision_text = ""
        decision_color = ""
        
        if product_value < 0:
            decision_text = "f(xl) × f(xr) < 0 → La raíz está en [xl, xr] → xu = xr"
            decision_color = "green"
        else:
            decision_text = "f(xl) × f(xr) > 0 → La raíz está en [xr, xu] → xl = xr"
            decision_color = "orange"
        
        decision_label = ctk.CTkLabel(
            product_frame,
            text=decision_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=decision_color,
            wraplength=600
        )
        decision_label.pack(pady=(0, 10))
        
        # Sección 3: Nuevo intervalo (si no es la última iteración)
        if 'new_interval' in step:
            new_interval_section = ctk.CTkFrame(main_container)
            new_interval_section.pack(fill="x", padx=10, pady=(5, 10))
            
            new_interval_title = ctk.CTkLabel(
                new_interval_section,
                text="📍 Nuevo Intervalo",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            new_interval_title.pack(pady=(15, 10))
            
            new_interval_text = f"Se selecciona el subintervalo: {step['new_interval']}"
            new_interval_label = ctk.CTkLabel(
                new_interval_section,
                text=new_interval_text,
                font=ctk.CTkFont(size=12),
                text_color=("#1f538d", "#4a9eff")
            )
            new_interval_label.pack(pady=(0, 15))
        
        # Indicador de convergencia
        if step.get('converged', False):
            conv_section = ctk.CTkFrame(main_container)
            conv_section.pack(fill="x", padx=10, pady=(5, 10))
            
            conv_label = ctk.CTkLabel(
                conv_section,
                text="✅ ¡CONVERGENCIA ALCANZADA!",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="green"
            )
            conv_label.pack(pady=20)
    
    def update_result_display(self):
        """Actualiza la visualización del resultado"""
        result_step = None
        for step in self.steps_data:
            if step['type'] == 'result':
                result_step = step
                break
        
        if not result_step:
            return
        
        # Actualizar status de convergencia
        if result_step['converged']:
            self.convergence_status.configure(
                text="✅ ¡Raíz Encontrada Exitosamente!",
                text_color="green"
            )
        else:
            self.convergence_status.configure(
                text="⚠️ Convergencia No Alcanzada",
                text_color="orange"
            )
        
        # Limpiar estadísticas anteriores
        for widget in self.stats_grid.winfo_children():
            widget.destroy()
        
        # Crear estadísticas visuales
        stats_data = [
            ("🔄 Iteraciones", str(result_step['iterations'])),
            ("📉 Error Final", f"{result_step['final_error']:.8f}%"),
            ("🎯 Raíz", f"{result_step['solution']:.8f}"),
            ("📊 Función", result_step.get('expression', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(self.stats_grid)
            stat_frame.grid(row=i//2, column=i % 2, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(10, 2))
            
            color = "green" if i == 0 and result_step['converged'] else "#1f538d"
            # Construir kwargs sin pasar wraplength=None (customtkinter no lo acepta)
            label_kwargs = {
                'text': value,
                'font': ctk.CTkFont(size=14, weight="bold") if i < 3 else ctk.CTkFont(size=12),
                'text_color': color,
            }
            if i == 3:
                label_kwargs['wraplength'] = 200
            ctk.CTkLabel(stat_frame, **label_kwargs).pack(pady=(2, 10))
        
        # Configurar grid
        self.stats_grid.grid_columnconfigure(0, weight=1)
        self.stats_grid.grid_columnconfigure(1, weight=1)
        
        # Limpiar solución anterior
        for widget in self.solution_container.winfo_children():
            widget.destroy()
        
        # Mostrar solución en formato visual atractivo
        solution_display = ctk.CTkFrame(self.solution_container)
        solution_display.pack(fill="x", padx=10, pady=10)
        
        # Raíz principal
        root_frame = ctk.CTkFrame(solution_display)
        root_frame.pack(fill="x", padx=20, pady=20)
        
        root_label = ctk.CTkLabel(
            root_frame,
            text="Raíz aproximada:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        root_label.pack(pady=(15, 5))
        
        root_value = ctk.CTkLabel(
            root_frame,
            text=f"x ≈ {result_step['solution']:.8f}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#d32f2f", "#f44336")
        )
        root_value.pack(pady=(0, 15))
        
        # Verificación (si está disponible)
        if result_step.get('expression'):
            verification_frame = ctk.CTkFrame(solution_display)
            verification_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            verify_title = ctk.CTkLabel(
                verification_frame,
                text="🔍 Verificación:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            verify_title.pack(pady=(15, 5))
            
            # Intentar evaluar f(x) en la raíz encontrada
            try:
                from solver.biseccion import BiseccionSolver
                solver = BiseccionSolver()
                func = solver.create_function_from_expression(result_step['expression'])
                f_root = func(result_step['solution'])
                
                verify_text = f"f({result_step['solution']:.8f}) = {f_root:.8f}"
                verify_color = "green" if abs(f_root) < 0.001 else "orange"
                
                verify_label = ctk.CTkLabel(
                    verification_frame,
                    text=verify_text,
                    font=ctk.CTkFont(size=16),
                    text_color=verify_color
                )
                verify_label.pack(pady=(0, 15))
            except:
                pass  # Si no se puede verificar, no mostrar nada
    
    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación"""
        iteration_steps = [s for s in self.steps_data if s.get('type') == 'iteration']
        total = len(iteration_steps)
        current = self.current_iteration
        
        # Primer botón
        self.first_btn.configure(state="normal" if current > 0 else "disabled")
        
        # Botón anterior
        self.prev_btn.configure(state="normal" if current > 0 else "disabled")
        
        # Botón siguiente
        self.next_btn.configure(state="normal" if current < total - 1 else "disabled")
        
        # Último botón
        self.last_btn.configure(state="normal" if current < total - 1 else "disabled")
    
    def first_iteration(self):
        """Ir a la primera iteración"""
        if self.current_iteration > 0:
            self.current_iteration = 0
            self.update_current_step()
    
    def last_iteration(self):
        """Ir a la última iteración"""
        iteration_steps = [s for s in self.steps_data if s.get('type') == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration = len(iteration_steps) - 1
            self.update_current_step()
    
    def prev_iteration(self):
        """Ir a la iteración anterior"""
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.update_current_step()
    
    def next_iteration(self):
        """Ir a la siguiente iteración"""
        iteration_steps = [s for s in self.steps_data if s.get('type') == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration += 1
            self.update_current_step()
    
    def clear(self):
        """Limpia la visualización"""
        self.steps_data = []
        self.current_iteration = 0
        self.total_iterations = 0
        
        # Limpiar frame de iteración actual
        for widget in self.current_iteration_frame.winfo_children():
            widget.destroy()
        
        # Reiniciar labels
        self.iteration_label.configure(text="Iteración: 0 / 0")
        self.error_label.configure(text="Error: 0.000000%")
        
        # Reiniciar barra de progreso
        self.progress_bar.set(0)
        
        # Reiniciar resultado
        self.convergence_status.configure(
            text="⏳ Esperando datos...",
            text_color="gray60"
        )
        
        # Limpiar estadísticas
        for widget in self.stats_grid.winfo_children():
            widget.destroy()
        
        # Limpiar solución
        for widget in self.solution_container.winfo_children():
            widget.destroy()
        
        # Reiniciar botones
        self.update_navigation_buttons()
