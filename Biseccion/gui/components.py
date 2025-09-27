import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
from typing import List, Callable, Optional


class ModernButton(ctk.CTkButton):
    """
    Botón personalizado con estilos modernos
    
    Extiende CTkButton con configuraciones predefinidas
    para mantener consistencia visual en toda la aplicación
    """
    def __init__(self, parent, text, command=None, **kwargs):
        # Configuración por defecto para botones modernos
        default_kwargs = {
            "corner_radius": 8,  # esquinas redondeadas
            "font": ctk.CTkFont(size=14, weight="bold"),  # fuente en negrita
            "height": 40  # altura fija
        }
        # Permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **default_kwargs)


class ModernEntry(ctk.CTkEntry):
    """
    Campo de entrada personalizado
    
    Extiende CTkEntry con estilos predefinidos para campos de entrada
    incluye placeholder text y configuración de fuentes
    """
    def __init__(self, parent, placeholder="", **kwargs):
        # Configuración por defecto para campos de entrada
        default_kwargs = {
            "corner_radius": 8,  # esquinas redondeadas
            "font": ctk.CTkFont(size=12),  # fuente de tamaño medio
            "height": 35,  # altura fija
            "placeholder_text": placeholder  # texto de ayuda
        }
        # Permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)


class FunctionInputPanel(ctk.CTkFrame):
    """
    Panel para ingresar la función matemática
    
    Widget especializado que permite al usuario introducir funciones
    matemáticas con validación y ayuda visual
    """

    def __init__(self, parent, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        # callback para notificar cambios
        self.on_change = on_change
        # configurar interfaz inicial
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del panel de función"""
        # Título del componente
        title = ctk.CTkLabel(
            self,
            text="Función Matemática f(x)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))

        # Frame para la entrada principal
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=20, pady=10)

        # Campo principal para la función
        self.function_entry = ModernEntry(
            entry_frame,
            placeholder="Ej: x**2 - 4, sin(x) - 0.5, exp(x) - 2",
            width=400,
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.function_entry.pack(fill="x", padx=10, pady=10)

        # Configurar callback para detectar cambios
        if self.on_change:
            self.function_entry.bind('<KeyRelease>', self._on_entry_change)

        # Frame de ayuda con ejemplos
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=20, pady=(5, 15))

        # Título de ayuda
        help_title = ctk.CTkLabel(
            help_frame,
            text="💡 Funciones y Operadores Disponibles",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        help_title.pack(pady=(10, 5))

        # Grid de ayuda con funciones disponibles
        help_grid = ctk.CTkFrame(help_frame)
        help_grid.pack(fill="x", padx=10, pady=5)

        # Funciones matemáticas disponibles
        functions_info = [
            ("Básicas:", "x, +, -, *, /, **"),
            ("Trigonométricas:", "sin(x), cos(x), tan(x)"),
            ("Logarítmicas:", "log(x), ln(x), log10(x)"),
            ("Exponencial:", "exp(x), e**x"),
            ("Otras:", "sqrt(x), abs(x), pi, e")
        ]

        # Crear labels informativos
        for i, (category, funcs) in enumerate(functions_info):
            row = i // 2
            col = i % 2

            info_frame = ctk.CTkFrame(help_grid)
            info_frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")

            # Categoría
            ctk.CTkLabel(
                info_frame,
                text=category,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            ).pack(anchor="w", padx=8, pady=(5, 0))

            # Funciones
            ctk.CTkLabel(
                info_frame,
                text=funcs,
                font=ctk.CTkFont(size=9),
                text_color="gray60"
            ).pack(anchor="w", padx=8, pady=(0, 5))

        # Configurar grid para expandirse
        help_grid.grid_columnconfigure(0, weight=1)
        help_grid.grid_columnconfigure(1, weight=1)

        # Ejemplos rápidos con botones
        examples_frame = ctk.CTkFrame(help_frame)
        examples_frame.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(
            examples_frame,
            text="⚡ Ejemplos Rápidos:",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=8, pady=(5, 3))

        # Botones de ejemplos
        examples_buttons_frame = ctk.CTkFrame(examples_frame)
        examples_buttons_frame.pack(fill="x", padx=8, pady=(0, 5))

        examples = [
            ("x**2 - 4", "Polinomial cuadrática"),
            ("sin(x)", "Función trigonométrica"),
            ("exp(x) - 2", "Función exponencial"),
            ("log(x) - 1", "Función logarítmica")
        ]

        for i, (func, desc) in enumerate(examples):
            btn = ctk.CTkButton(
                examples_buttons_frame,
                text=func,
                command=lambda f=func: self.set_function(f),
                width=100,
                height=25,
                font=ctk.CTkFont(size=10),
                fg_color="gray70",
                text_color="black"
            )
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")

        # Configurar grid de botones
        examples_buttons_frame.grid_columnconfigure(0, weight=1)
        examples_buttons_frame.grid_columnconfigure(1, weight=1)

    def get_function(self) -> str:
        """Obtiene la función actual"""
        return self.function_entry.get().strip()

    def set_function(self, function_str: str):
        """Establece una función específica"""
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, function_str)
        if self.on_change:
            self.on_change()

    def clear(self):
        """Limpia el campo de función"""
        self.function_entry.delete(0, tk.END)

    def _on_entry_change(self, event):
        """Callback interno para cambios en la función"""
        if self.on_change:
            self.on_change()


class IntervalInputPanel(ctk.CTkFrame):
    """
    Panel para ingresar el intervalo de búsqueda [a, b]
    
    Widget especializado para entrada del intervalo donde
    se buscará la raíz de la función
    """

    def __init__(self, parent, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        # callback para notificar cambios
        self.on_change = on_change
        # configurar interfaz inicial
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del panel de intervalo"""
        # Título del componente
        title = ctk.CTkLabel(
            self,
            text="Intervalo de Búsqueda [a, b]",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))

        # Frame principal para los campos
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="x", padx=20, pady=10)

        # Frame para límite inferior
        a_frame = ctk.CTkFrame(main_frame)
        a_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            a_frame,
            text="Límite Inferior (a):",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(8, 2))

        self.a_entry = ModernEntry(
            a_frame,
            placeholder="Ej: -5, 0, 1.5",
            width=200,
            font=ctk.CTkFont(size=12)
        )
        self.a_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Frame para límite superior
        b_frame = ctk.CTkFrame(main_frame)
        b_frame.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(
            b_frame,
            text="Límite Superior (b):",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(8, 2))

        self.b_entry = ModernEntry(
            b_frame,
            placeholder="Ej: 5, 10, 2.5",
            width=200,
            font=ctk.CTkFont(size=12)
        )
        self.b_entry.pack(fill="x", padx=10, pady=(0, 8))

        # Configurar callbacks para detectar cambios
        if self.on_change:
            self.a_entry.bind('<KeyRelease>', self._on_entry_change)
            self.b_entry.bind('<KeyRelease>', self._on_entry_change)

        # Frame de información adicional
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=20, pady=(5, 15))

        # Información sobre el método
        info_text = (
            "ℹ️ Requisito: La función debe cambiar de signo en el intervalo\n"
            "   Es decir: f(a) × f(b) < 0"
        )
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60",
            justify="left"
        ).pack(padx=10, pady=8)

        # Ejemplos de intervalos comunes
        examples_frame = ctk.CTkFrame(info_frame)
        examples_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            examples_frame,
            text="⚡ Intervalos Comunes:",
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=8, pady=(5, 3))

        # Botones de ejemplos de intervalos
        intervals = [
            ("[-5, 5]", -5, 5),
            ("[-2, 2]", -2, 2),
            ("[0, 10]", 0, 10),
            ("[-10, 10]", -10, 10)
        ]

        buttons_frame = ctk.CTkFrame(examples_frame)
        buttons_frame.pack(fill="x", padx=8, pady=(0, 5))

        for i, (label, a, b) in enumerate(intervals):
            btn = ctk.CTkButton(
                buttons_frame,
                text=label,
                command=lambda a_val=a, b_val=b: self.set_interval(a_val, b_val),
                width=80,
                height=25,
                font=ctk.CTkFont(size=10),
                fg_color="gray70",
                text_color="black"
            )
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")

        # Configurar grid de botones
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

    def get_interval(self) -> tuple:
        """
        Obtiene el intervalo actual
        
        Returns:
            tuple con (a, b) o (None, None) si hay error
        """
        try:
            a_str = self.a_entry.get().strip()
            b_str = self.b_entry.get().strip()
            
            if not a_str or not b_str:
                return None, None
                
            a = float(a_str)
            b = float(b_str)
            
            return a, b
        except ValueError:
            return None, None

    def set_interval(self, a: float, b: float):
        """Establece un intervalo específico"""
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.a_entry.insert(0, str(a))
        self.b_entry.insert(0, str(b))
        if self.on_change:
            self.on_change()

    def clear(self):
        """Limpia los campos del intervalo"""
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)

    def _on_entry_change(self, event):
        """Callback interno para cambios en el intervalo"""
        if self.on_change:
            self.on_change()


class BiseccionVisualizationPanel(ctk.CTkFrame):
    """
    Panel para visualizar el proceso de bisección
    
    Componente principal que muestra el proceso iterativo de bisección
    con navegación entre iteraciones y visualización detallada
    """

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        # configurar interfaz de usuario
        self.setup_ui()
        # índice de la iteración actual mostrada
        self.current_iteration = 0
        # total de iteraciones del proceso
        self.total_iterations = 0
        # datos completos de todos los pasos
        self.steps_data = []

    def setup_ui(self):
        """Configura la interfaz del panel de visualización"""
        # Header con título y progreso
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

        # Frame de controles de navegación
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=10)

        # Información de iteración actual
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

        # Botón ir al primero
        self.first_btn = ModernButton(
            nav_frame,
            text="⏮ Primero",
            command=self.first_iteration,
            width=100,
            height=35
        )
        self.first_btn.pack(side="left", padx=2)

        # Botón ir al anterior
        self.prev_btn = ModernButton(
            nav_frame,
            text="⏪ Anterior",
            command=self.prev_iteration,
            width=100,
            height=35
        )
        self.prev_btn.pack(side="left", padx=2)

        # Botón ir al siguiente
        self.next_btn = ModernButton(
            nav_frame,
            text="Siguiente ⏩",
            command=self.next_iteration,
            width=100,
            height=35
        )
        self.next_btn.pack(side="left", padx=2)

        # Botón ir al último
        self.last_btn = ModernButton(
            nav_frame,
            text="Último ⏭",
            command=self.last_iteration,
            width=100,
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
        """Configura la pestaña de iteraciones"""
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
        """Configura la pestaña de resultado final"""
        self.result_frame = self.notebook.tab("Resultado Final")

        # Contenedor con scroll para el resultado
        self.result_scroll = ctk.CTkScrollableFrame(self.result_frame)
        self.result_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Header del resultado
        result_header = ctk.CTkFrame(self.result_scroll)
        result_header.pack(fill="x", padx=10, pady=10)

        self.convergence_status = ctk.CTkLabel(
            result_header,
            text="⏳ Esperando datos...",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="gray60"
        )
        self.convergence_status.pack(pady=20)

        # Estadísticas del proceso
        stats_frame = ctk.CTkFrame(self.result_scroll)
        stats_frame.pack(fill="x", padx=10, pady=10)

        self.stats_grid = ctk.CTkFrame(stats_frame)
        self.stats_grid.pack(fill="x", padx=20, pady=10)

        # Información de la raíz
        root_frame = ctk.CTkFrame(self.result_scroll)
        root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        root_title = ctk.CTkLabel(
            root_frame,
            text="🎯 Raíz Encontrada",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        root_title.pack(pady=(15, 10))

        # Contenedor para mostrar la raíz
        self.root_container = ctk.CTkFrame(root_frame)
        self.root_container.pack(fill="both", expand=True, padx=20, pady=10)

    def update_visualization(self, steps_data: List):
        """Actualiza la visualización con nuevos datos"""
        self.steps_data = steps_data
        # Contar solo las iteraciones reales (no pasos de setup)
        self.total_iterations = len([s for s in steps_data if s['type'] == 'iteration'])
        self.current_iteration = 0
        
        if self.total_iterations > 0:
            self.update_current_step()
        self.update_result_display()

    def update_current_step(self):
        """Actualiza la visualización del paso actual"""
        if not self.steps_data:
            return

        # Encontrar pasos de iteración
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        
        if not iteration_steps:
            return

        if self.current_iteration < len(iteration_steps):
            step = iteration_steps[self.current_iteration]

            # Actualizar información en header
            self.iteration_label.configure(
                text=f"Iteración: {self.current_iteration + 1} / {len(iteration_steps)}"
            )

            if 'error' in step:
                self.error_label.configure(
                    text=f"Error: {step['error']:.6f}%"
                )

            # Actualizar barra de progreso
            progress = (self.current_iteration + 1) / len(iteration_steps)
            self.progress_bar.set(progress)

            # Limpiar frame actual
            for widget in self.current_iteration_frame.winfo_children():
                widget.destroy()

            # Crear visualización de la iteración
            self.create_iteration_display(step)

        # Actualizar botones de navegación
        self.update_navigation_buttons()

    def create_iteration_display(self, step):
        """Crea la visualización de una iteración específica"""
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

        # Badge con error
        if 'error' in step:
            error_badge = ctk.CTkLabel(
                title_frame,
                text=f"Error: {step['error']:.6f}%",
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=15,
                fg_color=("gray80", "gray20"),
                width=150,
                height=30
            )
            error_badge.pack(side="right", padx=10)

        # Contenedor principal con información de la iteración
        main_container = ctk.CTkFrame(self.current_iteration_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Columna izquierda: Cálculos
        left_column = ctk.CTkFrame(main_container)
        left_column.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        calc_title = ctk.CTkLabel(
            left_column,
            text="📝 Cálculos de la Iteración",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        calc_title.pack(pady=(15, 10))

        # Mostrar detalles de cálculo si están disponibles
        if 'calculation_details' in step:
            details = step['calculation_details']
            
            # Crear cards para cada cálculo
            calc_items = [
                ("Punto Medio:", details.get('midpoint_formula', '')),
                ("Resultado:", details.get('midpoint_result', '')),
                ("Evaluación:", details.get('function_eval', '')),
                ("Test Signos:", details.get('sign_test', '')),
                ("Nuevo Intervalo:", details.get('new_interval', ''))
            ]

            for label, value in calc_items:
                if value:
                    calc_card = ctk.CTkFrame(left_column)
                    calc_card.pack(fill="x", padx=10, pady=3)

                    ctk.CTkLabel(
                        calc_card,
                        text=label,
                        font=ctk.CTkFont(size=12, weight="bold"),
                        text_color=("#1f538d", "#4a9eff")
                    ).pack(anchor="w", padx=10, pady=(8, 2))

                    ctk.CTkLabel(
                        calc_card,
                        text=value,
                        font=ctk.CTkFont(size=11),
                        text_color="gray60",
                        wraplength=300
                    ).pack(anchor="w", padx=10, pady=(0, 8))

        # Columna derecha: Estado del intervalo
        right_column = ctk.CTkFrame(main_container)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        interval_title = ctk.CTkLabel(
            right_column,
            text="📊 Estado del Intervalo",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        interval_title.pack(pady=(15, 10))

        # Tabla con valores actuales
        values_table = ctk.CTkFrame(right_column)
        values_table.pack(fill="x", padx=10, pady=10)

        # Datos del intervalo
        interval_data = [
            ("xl (límite inferior)", f"{step.get('xl', 0):.6f}", f"f(xl) = {step.get('fxl', 0):.6f}"),
            ("xr (punto medio)", f"{step.get('xr', 0):.6f}", f"f(xr) = {step.get('fxr', 0):.6f}"),
            ("xu (límite superior)", f"{step.get('xu', 0):.6f}", f"f(xu) = {step.get('fxu', 0):.6f}")
        ]

        for i, (label, value, func_value) in enumerate(interval_data):
            row_frame = ctk.CTkFrame(values_table)
            row_frame.pack(fill="x", padx=5, pady=2)

            # Label del punto
            ctk.CTkLabel(
                row_frame,
                text=label + ":",
                font=ctk.CTkFont(size=11, weight="bold"),
                width=120,
                anchor="w"
            ).pack(side="left", padx=(5, 0), pady=5)

            # Valor del punto
            ctk.CTkLabel(
                row_frame,
                text=value,
                font=ctk.CTkFont(size=11),
                text_color=("#1f538d", "#4a9eff"),
                width=80,
                anchor="center"
            ).pack(side="left", padx=2, pady=5)

            # Valor de la función
            ctk.CTkLabel(
                row_frame,
                text=func_value,
                font=ctk.CTkFont(size=10),
                text_color="gray60",
                anchor="w"
            ).pack(side="left", padx=(10, 5), pady=5)

        # Longitud del intervalo
        if 'interval_length' in step:
            length_frame = ctk.CTkFrame(right_column)
            length_frame.pack(fill="x", padx=10, pady=(10, 0))

            ctk.CTkLabel(
                length_frame,
                text=f"📏 Longitud del intervalo: {step['interval_length']:.8f}",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=8)

    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        total = len(iteration_steps)
        current = self.current_iteration

        # Estados de botones basados en posición actual
        self.first_btn.configure(state="normal" if current > 0 else "disabled")
        self.prev_btn.configure(state="normal" if current > 0 else "disabled")
        self.next_btn.configure(state="normal" if current < total - 1 else "disabled")
        self.last_btn.configure(state="normal" if current < total - 1 else "disabled")

    def first_iteration(self):
        """Ir a la primera iteración"""
        if self.current_iteration > 0:
            self.current_iteration = 0
            self.update_current_step()

    def prev_iteration(self):
        """Ir a la iteración anterior"""
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.update_current_step()

    def next_iteration(self):
        """Ir a la siguiente iteración"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration += 1
            self.update_current_step()

    def last_iteration(self):
        """Ir a la última iteración"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration = len(iteration_steps) - 1
            self.update_current_step()

    def update_result_display(self):
        """Actualiza la visualización del resultado final"""
        result_step = None
        for step in self.steps_data:
            if step['type'] == 'result':
                result_step = step
                break

        if not result_step:
            return

        # Actualizar status de convergencia
        if result_step.get('converged', False):
            self.convergence_status.configure(
                text="✅ ¡Raíz Encontrada Exitosamente!",
                text_color="green"
            )
        else:
            self.convergence_status.configure(
                text="⚠️ Máximo de Iteraciones Alcanzado",
                text_color="orange"
            )

        # Limpiar estadísticas anteriores
        for widget in self.stats_grid.winfo_children():
            widget.destroy()

        # Crear estadísticas visuales
        stats_data = [
            ("🔄 Iteraciones", str(result_step.get('iterations', 0))),
            ("📉 Error Final", f"{result_step.get('final_error', 0):.8f}%"),
            ("🎯 Raíz", f"{result_step.get('root', 0):.8f}"),
            ("📊 f(raíz)", f"{result_step.get('final_function_value', 0):.8f}")
        ]

        for i, (label, value) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(self.stats_grid)
            stat_frame.grid(row=i//2, column=i % 2, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(10, 2))

            # Color especial para la raíz
            color = "green" if "Raíz" in label else "#1f538d"
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=color
            ).pack(pady=(2, 10))

        # Configurar grid
        self.stats_grid.grid_columnconfigure(0, weight=1)
        self.stats_grid.grid_columnconfigure(1, weight=1)

        # Limpiar contenedor de raíz anterior
        for widget in self.root_container.winfo_children():
            widget.destroy()

        # Mostrar información detallada de la raíz
        if 'root' in result_step:
            root_info = ctk.CTkFrame(self.root_container)
            root_info.pack(fill="x", padx=10, pady=10)

            # Función original
            if 'function' in result_step:
                func_label = ctk.CTkLabel(
                    root_info,
                    text=f"Función: f(x) = {result_step['function']}",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                func_label.pack(pady=(15, 5))

            # Intervalo original
            if 'original_interval' in result_step:
                interval_label = ctk.CTkLabel(
                    root_info,
                    text=f"Intervalo inicial: [{result_step['original_interval'][0]}, {result_step['original_interval'][1]}]",
                    font=ctk.CTkFont(size=12),
                    text_color="gray60"
                )
                interval_label.pack(pady=2)

            # Raíz encontrada (destacada)
            root_display = ctk.CTkFrame(root_info)
            root_display.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                root_display,
                text=f"x = {result_step['root']:.8f}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            ).pack(pady=15)

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

        # Limpiar contenedor de raíz
        for widget in self.root_container.winfo_children():
            widget.destroy()

        # Reiniciar botones
        self.update_navigation_buttons()
