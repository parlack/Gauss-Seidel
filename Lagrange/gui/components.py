import customtkinter as ctk
import tkinter as tk
from typing import List, Callable, Optional, Tuple
import math


class ModernButton(ctk.CTkButton):
    def __init__(self, parent, text, command=None, **kwargs):
        # Configuración por defecto para botones
        default_kwargs = {
            "corner_radius": 8,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "height": 40
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **default_kwargs)


class ModernEntry(ctk.CTkEntry):
    def __init__(self, parent, placeholder="", **kwargs):
        # Configuración por defecto para campos de entrada
        default_kwargs = {
            "corner_radius": 8,
            "font": ctk.CTkFont(size=12),
            "height": 35,
            "placeholder_text": placeholder
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)


class PointsTableInput(ctk.CTkFrame):
    """
    Widget de tabla para ingresar puntos (x, y) de interpolación
    
    Permite ingresar múltiples puntos en formato de tabla
    con validación en tiempo real
    """
    
    def __init__(self, parent, initial_size: int = 3, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_change = on_change
        self.current_size = initial_size
        self.entries = []  # Lista de tuplas (entry_x, entry_y)
        self.setup_ui()
    
    def setup_ui(self):
        # Título del panel
        title = ctk.CTkLabel(
            self,
            text="Tabla de Puntos (x, y)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        # Subtítulo explicativo
        subtitle = ctk.CTkLabel(
            self,
            text="Ingresa los puntos de interpolación",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        subtitle.pack(pady=(0, 10))
        
        # Frame para el control de tamaño
        size_control_frame = ctk.CTkFrame(self)
        size_control_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            size_control_frame,
            text="Número de puntos:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(10, 5), pady=10)
        
        self.size_var = tk.StringVar(value=str(self.current_size))
        self.size_entry = ModernEntry(
            size_control_frame,
            textvariable=self.size_var,
            width=80,
            placeholder="n"
        )
        self.size_entry.pack(side="left", padx=5, pady=10)
        
        # Permitir presionar enter para aceptar
        self.size_entry.bind('<Return>', lambda event: self.accept_size_change())
        
        # Botón de aceptar tamaño
        self.accept_size_btn = ModernButton(
            size_control_frame,
            text="✓",
            command=self.accept_size_change,
            width=40,
            height=35,
            fg_color="green",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.accept_size_btn.pack(side="left", padx=3, pady=10)
        
        # Frame scrollable para la tabla
        self.table_scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=10,
            height=400
        )
        self.table_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Crear tabla inicial
        self.create_table()
        
        # Panel de ayuda
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        help_title = ctk.CTkLabel(
            help_frame,
            text="💡 Requisitos:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        help_title.pack(pady=(10, 5))
        
        help_text = """• Los valores de x deben ser únicos (no duplicados)
• Se necesitan al menos 2 puntos para interpolar
• Todos los valores deben ser números válidos"""
        
        help_label = ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60",
            justify="left"
        )
        help_label.pack(padx=15, pady=(0, 10))
    
    def create_table(self):
        """Crea la tabla de entrada de puntos"""
        # Limpiar tabla anterior
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        self.entries = []
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(self.table_scroll)
        header_frame.pack(fill="x", padx=5, pady=(5, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="i",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=40
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="x",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="y",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150
        ).pack(side="left", padx=5)
        
        # Crear filas de entrada
        for i in range(self.current_size):
            row_frame = ctk.CTkFrame(self.table_scroll)
            row_frame.pack(fill="x", padx=5, pady=2)
            
            # Índice
            ctk.CTkLabel(
                row_frame,
                text=str(i),
                font=ctk.CTkFont(size=12),
                width=40
            ).pack(side="left", padx=5)
            
            # Entry para x
            entry_x = ModernEntry(
                row_frame,
                placeholder=f"x{i}",
                width=150
            )
            entry_x.pack(side="left", padx=5)
            
            # Entry para y
            entry_y = ModernEntry(
                row_frame,
                placeholder=f"y{i}",
                width=150
            )
            entry_y.pack(side="left", padx=5)
            
            # Configurar callbacks
            if self.on_change:
                entry_x.bind('<KeyRelease>', self._on_table_change)
                entry_y.bind('<KeyRelease>', self._on_table_change)
            
            self.entries.append((entry_x, entry_y))
    
    def accept_size_change(self):
        """Acepta y aplica el cambio de tamaño de la tabla"""
        try:
            new_size = int(self.size_var.get())
            if new_size < 2:
                tk.messagebox.showerror("Error", "Se necesitan al menos 2 puntos")
                self.size_var.set(str(self.current_size))
                return
            
            if new_size > 50:
                result = tk.messagebox.askyesno(
                    "Advertencia",
                    f"¿Estás seguro de crear una tabla con {new_size} puntos?"
                )
                if not result:
                    self.size_var.set(str(self.current_size))
                    return
            
            self.current_size = new_size
            self.create_table()
            
        except ValueError:
            tk.messagebox.showerror("Error", "Ingresa un número válido")
            self.size_var.set(str(self.current_size))
    
    def get_values(self) -> Tuple[List[str], List[str]]:
        """Obtiene los valores de la tabla como listas de strings"""
        x_values = []
        y_values = []
        
        for entry_x, entry_y in self.entries:
            x_val = entry_x.get().strip()
            y_val = entry_y.get().strip()
            
            x_values.append(x_val)
            y_values.append(y_val)
        
        return x_values, y_values
    
    def set_values(self, points: List[Tuple[float, float]]):
        """Establece valores en la tabla"""
        # Ajustar tamaño si es necesario
        if len(points) != self.current_size:
            self.current_size = len(points)
            self.size_var.set(str(self.current_size))
            self.create_table()
        
        # Llenar valores
        for i, (x, y) in enumerate(points):
            if i < len(self.entries):
                entry_x, entry_y = self.entries[i]
                entry_x.delete(0, tk.END)
                entry_x.insert(0, str(x))
                entry_y.delete(0, tk.END)
                entry_y.insert(0, str(y))
    
    def clear_all(self):
        """Limpia todos los campos de la tabla"""
        for entry_x, entry_y in self.entries:
            entry_x.delete(0, tk.END)
            entry_y.delete(0, tk.END)
    
    def _on_table_change(self, event):
        """Callback interno para cambios en la tabla"""
        if self.on_change:
            self.on_change()


class EvaluationPanel(ctk.CTkFrame):
    """
    Panel para evaluar el polinomio en un punto específico
    """
    
    def __init__(self, parent, on_evaluate: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_evaluate = on_evaluate
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title = ctk.CTkLabel(
            self,
            text="Evaluar Polinomio",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        # Frame para entrada
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            input_frame,
            text="x =",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(15, 5), pady=15)
        
        self.x_entry = ModernEntry(
            input_frame,
            placeholder="Punto a evaluar",
            width=200
        )
        self.x_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=15)
        
        # Permitir presionar enter para evaluar
        self.x_entry.bind('<Return>', lambda event: self._on_evaluate_clicked())
        
        # Botón de evaluar
        self.eval_button = ModernButton(
            self,
            text="Evaluar P(x)",
            command=self._on_evaluate_clicked,
            fg_color="#1f538d",
            height=45
        )
        self.eval_button.pack(fill="x", padx=20, pady=(0, 15))
    
    def get_x_value(self) -> str:
        """Obtiene el valor de x ingresado"""
        return self.x_entry.get().strip()
    
    def set_x_value(self, x: float):
        """Establece un valor de x"""
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
    
    def clear(self):
        """Limpia el campo"""
        self.x_entry.delete(0, tk.END)
    
    def _on_evaluate_clicked(self):
        """Callback interno para el botón de evaluar"""
        if self.on_evaluate:
            self.on_evaluate()


class VisualizationPanel(ctk.CTkFrame):
    """
    Panel para visualizar el proceso de interpolación de Lagrange
    """
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.setup_ui()
        self.current_step = 0
        self.total_steps = 0
        self.steps_data = []
    
    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Proceso de Interpolación - Método de Lagrange",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        self.title_label.pack(side="left")
        
        # Indicador de progreso
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
        
        # Información de paso
        info_frame = ctk.CTkFrame(controls_frame)
        info_frame.pack(side="left", padx=10, pady=5)
        
        self.step_label = ctk.CTkLabel(
            info_frame,
            text="Paso: 0 / 0",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.step_label.pack(side="left", padx=15, pady=8)
        
        # Botones de navegación
        nav_frame = ctk.CTkFrame(controls_frame)
        nav_frame.pack(side="right", padx=10, pady=5)
        
        self.first_btn = ModernButton(
            nav_frame,
            text="Primero",
            command=self.first_step,
            width=90,
            height=35
        )
        self.first_btn.pack(side="left", padx=2)
        
        self.prev_btn = ModernButton(
            nav_frame,
            text="Anterior",
            command=self.prev_step,
            width=90,
            height=35
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.next_btn = ModernButton(
            nav_frame,
            text="Siguiente",
            command=self.next_step,
            width=90,
            height=35
        )
        self.next_btn.pack(side="left", padx=2)
        
        self.last_btn = ModernButton(
            nav_frame,
            text="Último",
            command=self.last_step,
            width=90,
            height=35
        )
        self.last_btn.pack(side="left", padx=2)
        
        # Área de contenido con scroll
        self.content_scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=10
        )
        self.content_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para mostrar el paso actual
        self.current_step_frame = ctk.CTkFrame(
            self.content_scroll,
            corner_radius=15
        )
        self.current_step_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def update_visualization(self, steps_data: List):
        """Actualiza la visualización con nuevos datos"""
        self.steps_data = steps_data
        self.total_steps = len(steps_data)
        self.current_step = 0
        self.update_current_step()
    
    def update_current_step(self):
        """Actualiza la visualización del paso actual"""
        if not self.steps_data or self.current_step >= len(self.steps_data):
            return
        
        step = self.steps_data[self.current_step]
        
        # Actualizar información en header
        self.step_label.configure(
            text=f"Paso: {self.current_step + 1} / {self.total_steps}"
        )
        
        # Actualizar barra de progreso
        progress = (self.current_step + 1) / self.total_steps if self.total_steps > 0 else 0
        self.progress_bar.set(progress)
        
        # Limpiar frame actual
        for widget in self.current_step_frame.winfo_children():
            widget.destroy()
        
        # Crear visualización según el tipo de paso
        step_type = step.get('type', 'unknown')
        
        if step_type == 'points':
            self.create_points_card(step)
        elif step_type == 'method':
            self.create_method_card(step)
        elif step_type == 'basis':
            self.create_basis_card(step)
        elif step_type == 'calculations':
            self.create_calculations_card(step)
        elif step_type == 'result':
            self.create_result_card(step)
        elif step_type == 'error':
            self.create_error_card(step)
        
        # Actualizar botones
        self.update_navigation_buttons()
    
    def create_points_card(self, step):
        """Crea tarjeta para mostrar puntos de interpolación"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"📊 {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        content_label = ctk.CTkLabel(
            self.current_step_frame,
            text=step['content'],
            font=ctk.CTkFont(size=14)
        )
        content_label.pack(pady=10)
        
        # Mostrar tabla de puntos
        points_frame = ctk.CTkFrame(self.current_step_frame)
        points_frame.pack(fill="x", padx=20, pady=15)
        
        # Header
        header = ctk.CTkFrame(points_frame)
        header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header, text="i", font=ctk.CTkFont(size=12, weight="bold"), width=50).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="x", font=ctk.CTkFont(size=12, weight="bold"), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="y", font=ctk.CTkFont(size=12, weight="bold"), width=150).pack(side="left", padx=5)
        
        # Puntos
        for i, (x, y) in enumerate(step['points']):
            row = ctk.CTkFrame(points_frame)
            row.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row, text=str(i), font=ctk.CTkFont(size=12), width=50).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{x:.6f}", font=ctk.CTkFont(size=12), width=150).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{y:.6f}", font=ctk.CTkFont(size=12), width=150).pack(side="left", padx=5)
    
    def create_method_card(self, step):
        """Crea tarjeta para explicar el método"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"📖 {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        content_label = ctk.CTkLabel(
            self.current_step_frame,
            text=step['content'],
            font=ctk.CTkFont(size=13),
            wraplength=800,
            justify="left"
        )
        content_label.pack(pady=15, padx=30)
        
        if 'formula' in step:
            formula_frame = ctk.CTkFrame(self.current_step_frame)
            formula_frame.pack(fill="x", padx=30, pady=10)
            
            ctk.CTkLabel(
                formula_frame,
                text=step['formula'],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            ).pack(pady=15)
    
    def format_fraction_vertical(self, numerator_text, denominator_text):
        """Formatea una fracción con línea horizontal"""
        # Encontrar el ancho máximo
        max_width = max(len(numerator_text), len(denominator_text))
        
        # Centrar numerador y denominador
        num_centered = numerator_text.center(max_width)
        den_centered = denominator_text.center(max_width)
        
        # Crear línea divisoria
        line = "─" * max_width
        
        return f"{num_centered}\n{line}\n{den_centered}"
    
    def create_calculations_card(self, step):
        """Crea tarjeta para mostrar todos los cálculos en una sola página"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"🔢 {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        # Información del punto a evaluar
        info_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"Encontrar y({step['x_eval']:.3g})",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        # Mostrar la fórmula completa de y(x) con todas las fracciones
        formula_frame = ctk.CTkFrame(self.current_step_frame)
        formula_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            formula_frame,
            text="Fórmula del Polinomio Interpolador:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        # Mostrar todas las fracciones en una sola línea horizontal
        fractions_container = ctk.CTkFrame(formula_frame)
        fractions_container.pack(fill="x", padx=20, pady=10)
        
        # Frame horizontal para todas las fracciones
        horizontal_frame = ctk.CTkFrame(fractions_container)
        horizontal_frame.pack(anchor="w", pady=5)
        
        # Etiqueta inicial "y(x) = "
        ctk.CTkLabel(
            horizontal_frame,
            text="y(x) = ",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        for i, detail in enumerate(step['basis_details']):
            # Signo
            if i > 0:
                sign_text = " + " if detail['y_j'] >= 0 else " - "
                ctk.CTkLabel(
                    horizontal_frame,
                    text=sign_text,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=2)
            
            # Coeficiente y_j
            coef_text = f"{abs(detail['y_j']):.3g} × "
            ctk.CTkLabel(
                horizontal_frame,
                text=coef_text,
                font=ctk.CTkFont(size=11)
            ).pack(side="left")
            
            # Construir numerador y denominador
            num_terms = detail['numerator_formula'].replace(' × ', ' ')
            den_terms = detail['denominator_formula'].replace(' × ', ' ')
            
            # Crear fracción vertical en línea
            max_width = max(len(num_terms), len(den_terms))
            line = "─" * max_width
            
            # Frame para la fracción (vertical pero en línea horizontal)
            vert_frac = ctk.CTkFrame(horizontal_frame)
            vert_frac.pack(side="left", padx=3)
            
            ctk.CTkLabel(
                vert_frac,
                text=num_terms,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=line,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=den_terms,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
        
        # Mostrar la sustitución con el valor de x
        substitution_frame = ctk.CTkFrame(self.current_step_frame)
        substitution_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            substitution_frame,
            text=f"Sustituyendo x = {step['x_eval']:.3g}:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        # Mostrar todas las fracciones sustituidas en una sola línea horizontal
        subst_container = ctk.CTkFrame(substitution_frame)
        subst_container.pack(fill="x", padx=20, pady=10)
        
        # Frame horizontal para todas las fracciones sustituidas
        subst_horizontal_frame = ctk.CTkFrame(subst_container)
        subst_horizontal_frame.pack(anchor="w", pady=5)
        
        # Etiqueta inicial
        ctk.CTkLabel(
            subst_horizontal_frame,
            text=f"y({step['x_eval']:.3g}) = ",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        for i, detail in enumerate(step['basis_details']):
            # Signo
            if i > 0:
                sign_text = " + " if detail['y_j'] >= 0 else " - "
                ctk.CTkLabel(
                    subst_horizontal_frame,
                    text=sign_text,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=2)
            
            # Coeficiente
            coef_text = f"{abs(detail['y_j']):.3g} × "
            ctk.CTkLabel(
                subst_horizontal_frame,
                text=coef_text,
                font=ctk.CTkFont(size=11)
            ).pack(side="left")
            
            # Construir numerador y denominador con valores
            num_eval = detail['numerator_eval'].replace(' × ', ' × ')
            den_eval = detail['denominator_eval'].replace(' × ', ' × ')
            
            # Crear fracción vertical en línea
            max_width = max(len(num_eval), len(den_eval))
            line = "─" * max_width
            
            # Frame para la fracción (vertical pero en línea horizontal)
            vert_frac = ctk.CTkFrame(subst_horizontal_frame)
            vert_frac.pack(side="left", padx=3)
            
            ctk.CTkLabel(
                vert_frac,
                text=num_eval,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=line,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=den_eval,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
        
        # Mostrar los resultados numéricos de las fracciones en una sola línea horizontal
        results_container = ctk.CTkFrame(substitution_frame)
        results_container.pack(fill="x", padx=20, pady=10)
        
        # Frame horizontal para todos los resultados numéricos
        results_horizontal_frame = ctk.CTkFrame(results_container)
        results_horizontal_frame.pack(anchor="w", pady=5)
        
        ctk.CTkLabel(
            results_horizontal_frame,
            text=f"y({step['x_eval']:.3g}) = ",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        for i, detail in enumerate(step['basis_details']):
            # Signo
            if i > 0:
                sign_text = " + " if detail['y_j'] >= 0 else " - "
                ctk.CTkLabel(
                    results_horizontal_frame,
                    text=sign_text,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=2)
            
            # Coeficiente
            coef_text = f"{abs(detail['y_j']):.3g} × "
            ctk.CTkLabel(
                results_horizontal_frame,
                text=coef_text,
                font=ctk.CTkFont(size=11)
            ).pack(side="left")
            
            # Valores numéricos
            num_text = f"{detail['numerator_product']:.6f}"
            den_text = f"{detail['denominator_product']:.6f}"
            
            # Crear fracción vertical en línea
            max_width = max(len(num_text), len(den_text))
            line = "─" * max_width
            
            # Frame para la fracción (vertical pero en línea horizontal)
            vert_frac = ctk.CTkFrame(results_horizontal_frame)
            vert_frac.pack(side="left", padx=3)
            
            ctk.CTkLabel(
                vert_frac,
                text=num_text,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=line,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
            
            ctk.CTkLabel(
                vert_frac,
                text=den_text,
                font=ctk.CTkFont(size=10, family="Courier New")
            ).pack()
        
        # Calcular y mostrar el resultado final
        total_contribution = sum(d['contribution'] for d in step['basis_details'])
        
        # Mostrar la suma de contribuciones
        sum_frame = ctk.CTkFrame(self.current_step_frame)
        sum_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            sum_frame,
            text="Suma:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        sum_parts = []
        for i, detail in enumerate(step['basis_details']):
            contrib = detail['contribution']
            if i == 0:
                sum_parts.append(f"{contrib:.6f}")
            else:
                if contrib >= 0:
                    sum_parts.append(f" + {contrib:.6f}")
                else:
                    sum_parts.append(f" {contrib:.6f}")
        
        sum_text = f"y({step['x_eval']:.3g}) = " + "".join(sum_parts)
        
        ctk.CTkLabel(
            sum_frame,
            text=sum_text,
            font=ctk.CTkFont(size=13),
            wraplength=1000,
            justify="left"
        ).pack(pady=(0, 15), padx=20)
        
        # Resultado final 
        result_frame = ctk.CTkFrame(self.current_step_frame)
        result_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            result_frame,
            text=f"y({step['x_eval']:.3g}) = {total_contribution:.6f}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#d32f2f", "#f44336")
        ).pack(pady=20)
    
    def create_basis_card(self, step):
        """Crea tarjeta para mostrar cálculo de polinomio base"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"🔢 {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        # Información del punto
        info_frame = ctk.CTkFrame(self.current_step_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text=f"Punto: ({step['x_j']:.3f}, {step['y_j']:.3f})",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)
        
        # Fórmula
        formula_frame = ctk.CTkFrame(self.current_step_frame)
        formula_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            formula_frame,
            text="Fórmula:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            formula_frame,
            text=step['formula'],
            font=ctk.CTkFont(size=11),
            wraplength=700
        ).pack(pady=(0, 10), padx=15)
        
        # Evaluación
        eval_frame = ctk.CTkFrame(self.current_step_frame)
        eval_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            eval_frame,
            text="Evaluación:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            eval_frame,
            text=step['evaluation'],
            font=ctk.CTkFont(size=11),
            wraplength=700
        ).pack(pady=(0, 10), padx=15)
        
        # Resultado
        result_frame = ctk.CTkFrame(self.current_step_frame)
        result_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            result_frame,
            text=f"L_{step['j']} = {step['value']:.6f}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="green"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            result_frame,
            text=f"Contribución: {step['y_j']:.3f} × {step['value']:.6f} = {step['contribution']:.6f}",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(0, 10))
    
    def create_result_card(self, step):
        """Crea tarjeta para mostrar resultado final"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"🎯 {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="green"
        )
        title_label.pack(pady=(20, 10))
        
        # Cálculo
        calc_frame = ctk.CTkFrame(self.current_step_frame)
        calc_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            calc_frame,
            text="Cálculo completo:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        ctk.CTkLabel(
            calc_frame,
            text=step['calculation'],
            font=ctk.CTkFont(size=12),
            wraplength=700
        ).pack(pady=(0, 15), padx=20)
        
        # Resultado destacado
        result_frame = ctk.CTkFrame(self.current_step_frame)
        result_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            result_frame,
            text=f"P({step['x_eval']:.3f}) = {step['result']:.6f}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#d32f2f", "#f44336")
        ).pack(pady=20)
    
    def create_error_card(self, step):
        """Crea tarjeta para mostrar error"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"❌ {step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="red"
        )
        title_label.pack(pady=(20, 10))
        
        content_label = ctk.CTkLabel(
            self.current_step_frame,
            text=step['content'],
            font=ctk.CTkFont(size=14),
            wraplength=700
        )
        content_label.pack(pady=20, padx=30)
    
    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación"""
        self.first_btn.configure(state="normal" if self.current_step > 0 else "disabled")
        self.prev_btn.configure(state="normal" if self.current_step > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_step < self.total_steps - 1 else "disabled")
        self.last_btn.configure(state="normal" if self.current_step < self.total_steps - 1 else "disabled")
    
    def first_step(self):
        """Ir al primer paso"""
        if self.current_step > 0:
            self.current_step = 0
            self.update_current_step()
    
    def last_step(self):
        """Ir al último paso"""
        if self.current_step < self.total_steps - 1:
            self.current_step = self.total_steps - 1
            self.update_current_step()
    
    def prev_step(self):
        """Ir al paso anterior"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_current_step()
    
    def next_step(self):
        """Ir al siguiente paso"""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_current_step()
    
    def clear(self):
        """Limpia la visualización"""
        self.steps_data = []
        self.current_step = 0
        self.total_steps = 0
        
        for widget in self.current_step_frame.winfo_children():
            widget.destroy()
        
        self.step_label.configure(text="Paso: 0 / 0")
        self.progress_bar.set(0)
        self.update_navigation_buttons()

