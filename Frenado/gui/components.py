# Andres Monsivais Salazar
# Luis Andres Salinas Lozano

import customtkinter as ctk
import tkinter as tk
from typing import List, Callable, Optional, Tuple


class ModernButton(ctk.CTkButton):
    """
    Botón personalizado con estilos modernos
    """
    def __init__(self, parent, text, command=None, **kwargs):
        default_kwargs = {
            "corner_radius": 8,
            "font": ctk.CTkFont(size=14, weight="bold"),
            "height": 40
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **default_kwargs)


class ModernEntry(ctk.CTkEntry):
    """
    Campo de entrada personalizado
    """
    def __init__(self, parent, placeholder="", **kwargs):
        default_kwargs = {
            "corner_radius": 8,
            "font": ctk.CTkFont(size=12),
            "height": 35,
            "placeholder_text": placeholder
        }
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)


class DatosExperimentalesPanel(ctk.CTkFrame):
    """
    Panel para ingresar datos experimentales de velocidad vs distancia de frenado
    """
    
    def __init__(self, parent, initial_size: int = 5, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_change = on_change
        self.current_size = initial_size
        self.entries = []  # Lista de tuplas (entry_velocidad, entry_distancia)
        self.setup_ui()
    
    def setup_ui(self):
        # Título del panel
        title = ctk.CTkLabel(
            self,
            text="Datos Experimentales",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        # Subtítulo explicativo
        subtitle = ctk.CTkLabel(
            self,
            text="Mediciones reales de velocidad y distancia de frenado",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        subtitle.pack(pady=(0, 10))
        
        # Frame para el control de tamaño
        size_control_frame = ctk.CTkFrame(self)
        size_control_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(
            size_control_frame,
            text="Número de mediciones:",
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
            height=350
        )
        self.table_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Crear tabla inicial
        self.create_table()
        
        # Panel de ayuda
        help_frame = ctk.CTkFrame(self)
        help_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        help_title = ctk.CTkLabel(
            help_frame,
            text="Informacion:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        help_title.pack(pady=(10, 5))
        
        help_text = """- Las velocidades deben ser unicas (no duplicadas)
- Se necesitan al menos 2 mediciones
- Rango tipico: 20-200 km/h, 5-150 metros"""
        
        help_label = ctk.CTkLabel(
            help_frame,
            text=help_text,
            font=ctk.CTkFont(size=10),
            text_color="gray60",
            justify="left"
        )
        help_label.pack(padx=15, pady=(0, 10))
    
    def create_table(self):
        """Crea la tabla de entrada de datos experimentales"""
        # Limpiar tabla anterior
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        self.entries = []
        
        # Header de la tabla
        header_frame = ctk.CTkFrame(self.table_scroll)
        header_frame.pack(fill="x", padx=5, pady=(5, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="#",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=40
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Velocidad (km/h)",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=150
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Distancia (m)",
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
                text=str(i + 1),
                font=ctk.CTkFont(size=12),
                width=40
            ).pack(side="left", padx=5)
            
            # Entry para velocidad
            entry_v = ModernEntry(
                row_frame,
                placeholder=f"v{i+1}",
                width=150
            )
            entry_v.pack(side="left", padx=5)
            
            # Entry para distancia
            entry_d = ModernEntry(
                row_frame,
                placeholder=f"d{i+1}",
                width=150
            )
            entry_d.pack(side="left", padx=5)
            
            # Configurar callbacks
            if self.on_change:
                entry_v.bind('<KeyRelease>', self._on_table_change)
                entry_d.bind('<KeyRelease>', self._on_table_change)
            
            self.entries.append((entry_v, entry_d))
    
    def accept_size_change(self):
        """Acepta y aplica el cambio de tamaño de la tabla"""
        try:
            new_size = int(self.size_var.get())
            if new_size < 2:
                tk.messagebox.showerror("Error", "Se necesitan al menos 2 mediciones")
                self.size_var.set(str(self.current_size))
                return
            
            if new_size > 20:
                result = tk.messagebox.askyesno(
                    "Advertencia",
                    f"¿Estás seguro de crear una tabla con {new_size} mediciones?"
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
        velocidades = []
        distancias = []
        
        for entry_v, entry_d in self.entries:
            v_val = entry_v.get().strip()
            d_val = entry_d.get().strip()
            
            velocidades.append(v_val)
            distancias.append(d_val)
        
        return velocidades, distancias
    
    def set_values(self, datos: List[Tuple[float, float]]):
        """Establece valores en la tabla"""
        # Ajustar tamaño si es necesario
        if len(datos) != self.current_size:
            self.current_size = len(datos)
            self.size_var.set(str(self.current_size))
            self.create_table()
        
        # Llenar valores
        for i, (v, d) in enumerate(datos):
            if i < len(self.entries):
                entry_v, entry_d = self.entries[i]
                entry_v.delete(0, tk.END)
                entry_v.insert(0, str(v))
                entry_d.delete(0, tk.END)
                entry_d.insert(0, str(d))
    
    def clear_all(self):
        """Limpia todos los campos de la tabla"""
        for entry_v, entry_d in self.entries:
            entry_v.delete(0, tk.END)
            entry_d.delete(0, tk.END)
    
    def _on_table_change(self, event):
        """Callback interno para cambios en la tabla"""
        if self.on_change:
            self.on_change()


class InterpolacionPanel(ctk.CTkFrame):
    """
    Panel para evaluar distancia de frenado a una velocidad específica
    """
    
    def __init__(self, parent, on_evaluate: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_evaluate = on_evaluate
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title = ctk.CTkLabel(
            self,
            text="Interpolacion: Predecir Distancia de Frenado",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Usa los datos experimentales para predecir la distancia a cualquier velocidad",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            wraplength=400
        )
        subtitle.pack(pady=(0, 15))
        
        # Frame para entrada
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            input_frame,
            text="Velocidad (km/h):",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(15, 5), pady=15)
        
        self.v_entry = ModernEntry(
            input_frame,
            placeholder="Ej: 75",
            width=200
        )
        self.v_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=15)
        
        # Permitir presionar enter para evaluar
        self.v_entry.bind('<Return>', lambda event: self._on_evaluate_clicked())
        
        # Botón de evaluar
        self.eval_button = ModernButton(
            self,
            text="Calcular Distancia de Frenado",
            command=self._on_evaluate_clicked,
            fg_color="#1f538d",
            height=45
        )
        self.eval_button.pack(fill="x", padx=20, pady=(0, 15))
    
    def get_velocity(self) -> str:
        """Obtiene el valor de velocidad ingresado"""
        return self.v_entry.get().strip()
    
    def set_velocity(self, v: float):
        """Establece un valor de velocidad"""
        self.v_entry.delete(0, tk.END)
        self.v_entry.insert(0, str(v))
    
    def clear(self):
        """Limpia el campo"""
        self.v_entry.delete(0, tk.END)
    
    def _on_evaluate_clicked(self):
        """Callback interno para el botón de evaluar"""
        if self.on_evaluate:
            self.on_evaluate()


class BiseccionPanel(ctk.CTkScrollableFrame):
    """
    Panel para encontrar velocidad máxima segura dado un límite de distancia
    """
    
    def __init__(self, parent, on_solve: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        self.on_solve = on_solve
        self.setup_ui()
    
    def setup_ui(self):
        # Título
        title = ctk.CTkLabel(
            self,
            text="Biseccion: Encontrar Velocidad Maxima Segura",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(15, 10))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Determina la velocidad máxima que permite frenar dentro de una distancia límite",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            wraplength=400
        )
        subtitle.pack(pady=(0, 15))
        
        # Frame para distancia límite
        dist_frame = ctk.CTkFrame(self)
        dist_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            dist_frame,
            text="Distancia maxima disponible (m):",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(10, 5))
        
        self.dist_entry = ModernEntry(
            dist_frame,
            placeholder="Ej: 50",
            width=200
        )
        self.dist_entry.pack(pady=(0, 10))
        
        # Frame para tolerancia (margen de error)
        tol_frame = ctk.CTkFrame(self)
        tol_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            tol_frame,
            text="Tolerancia / Margen de error (km/h):",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(10, 5))
        
        self.tol_var = tk.StringVar(value="0.01")
        self.tol_entry = ModernEntry(
            tol_frame,
            textvariable=self.tol_var,
            placeholder="Ej: 0.01",
            width=200
        )
        self.tol_entry.pack(pady=(0, 10))
        
        # Frame para intervalo de búsqueda
        interval_frame = ctk.CTkFrame(self)
        interval_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            interval_frame,
            text="Intervalo de búsqueda de velocidad:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(10, 5))
        
        # Sublabels para los límites
        limits_container = ctk.CTkFrame(interval_frame)
        limits_container.pack(fill="x", padx=10, pady=5)
        
        # Límite inferior
        left_frame = ctk.CTkFrame(limits_container)
        left_frame.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(
            left_frame,
            text="Mínima (km/h):",
            font=ctk.CTkFont(size=11)
        ).pack()
        
        self.a_entry = ModernEntry(
            left_frame,
            placeholder="Ej: 20",
            width=100
        )
        self.a_entry.pack(pady=5)
        
        # Límite superior
        right_frame = ctk.CTkFrame(limits_container)
        right_frame.pack(side="right", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(
            right_frame,
            text="Máxima (km/h):",
            font=ctk.CTkFont(size=11)
        ).pack()
        
        self.b_entry = ModernEntry(
            right_frame,
            placeholder="Ej: 150",
            width=100
        )
        self.b_entry.pack(pady=5)
        
        # Botón de resolver
        self.solve_button = ModernButton(
            self,
            text="Calcular Velocidad Maxima Segura",
            command=self._on_solve_clicked,
            fg_color="darkorange",
            height=45
        )
        self.solve_button.pack(fill="x", padx=20, pady=(10, 15))
    
    def get_values(self) -> Tuple[str, str, str, str]:
        """Obtiene los valores ingresados"""
        return (
            self.dist_entry.get().strip(),
            self.a_entry.get().strip(),
            self.b_entry.get().strip(),
            self.tol_entry.get().strip()
        )
    
    def set_values(self, dist: float, a: float, b: float, tol: float = 0.01):
        """Establece valores en los campos"""
        self.dist_entry.delete(0, tk.END)
        self.dist_entry.insert(0, str(dist))
        
        self.a_entry.delete(0, tk.END)
        self.a_entry.insert(0, str(a))
        
        self.b_entry.delete(0, tk.END)
        self.b_entry.insert(0, str(b))
        
        self.tol_entry.delete(0, tk.END)
        self.tol_entry.insert(0, str(tol))
    
    def clear(self):
        """Limpia todos los campos"""
        self.dist_entry.delete(0, tk.END)
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.tol_var.set("0.01")  # Restaurar valor por defecto
    
    def _on_solve_clicked(self):
        """Callback interno para el botón de resolver"""
        if self.on_solve:
            self.on_solve()


class VisualizationPanel(ctk.CTkFrame):
    """
    Panel unificado para visualizar resultados de ambos métodos
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
            text="Visualización de Resultados",
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
            width=100,
            height=35
        )
        self.first_btn.pack(side="left", padx=2)
        
        self.prev_btn = ModernButton(
            nav_frame,
            text="Anterior",
            command=self.prev_step,
            width=100,
            height=35
        )
        self.prev_btn.pack(side="left", padx=2)
        
        self.next_btn = ModernButton(
            nav_frame,
            text="Siguiente",
            command=self.next_step,
            width=100,
            height=35
        )
        self.next_btn.pack(side="left", padx=2)
        
        self.last_btn = ModernButton(
            nav_frame,
            text="Ultimo",
            command=self.last_step,
            width=100,
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
        
        if step_type == 'context':
            self.create_context_card(step)
        elif step_type == 'method':
            self.create_method_card(step)
        elif step_type == 'initial':
            self.create_initial_card(step)
        elif step_type == 'iteration':
            self.create_iteration_card(step)
        elif step_type == 'result':
            self.create_result_card(step)
        elif step_type == 'error':
            self.create_error_card(step)
        elif step_type == 'points':
            self.create_points_card(step)
        elif step_type == 'calculations':
            self.create_calculations_card(step)
        
        # Actualizar botones
        self.update_navigation_buttons()
    
    def create_context_card(self, step):
        """Crea tarjeta para mostrar contexto del problema"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        content_label = ctk.CTkLabel(
            self.current_step_frame,
            text=step['content'],
            font=ctk.CTkFont(size=14),
            wraplength=700,
            justify="left"
        )
        content_label.pack(pady=15, padx=30)
        
        if 'data' in step and step['data']:
            data_frame = ctk.CTkFrame(self.current_step_frame)
            data_frame.pack(fill="x", padx=30, pady=10)
            
            for key, value in step['data'].items():
                row = ctk.CTkFrame(data_frame)
                row.pack(fill="x", padx=10, pady=3)
                
                ctk.CTkLabel(
                    row,
                    text=f"{key}:",
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    row,
                    text=str(value),
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=5)
    
    def create_method_card(self, step):
        """Crea tarjeta para explicar el método"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
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
        
        if 'requirement' in step:
            req_label = ctk.CTkLabel(
                self.current_step_frame,
                text=f"Requisito: {step['requirement']}",
                font=ctk.CTkFont(size=12),
                text_color="orange"
            )
            req_label.pack(pady=5)
        
        if 'where' in step:
            where_label = ctk.CTkLabel(
                self.current_step_frame,
                text=f"Donde: {step['where']}",
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            )
            where_label.pack(pady=5, padx=30)
    
    def create_initial_card(self, step):
        """Crea tarjeta para mostrar intervalo inicial de bisección"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        # Mostrar intervalo
        interval_frame = ctk.CTkFrame(self.current_step_frame)
        interval_frame.pack(fill="x", padx=30, pady=15)
        
        data = [
            ("a (límite inferior)", f"{step['a']:.2f} km/h", step['fa']),
            ("b (límite superior)", f"{step['b']:.2f} km/h", step['fb'])
        ]
        
        for label, value, func_val in data:
            row = ctk.CTkFrame(interval_frame)
            row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                row,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=200
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=f"f({value}) = {func_val:.4f}",
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            ).pack(side="left", padx=10)
        
        # Verificar signos opuestos
        status_color = "green" if step['signs_opposite'] else "red"
        status_text = "Signos opuestos (metodo aplicable)" if step['signs_opposite'] else "Los signos deben ser opuestos"
        
        status_label = ctk.CTkLabel(
            self.current_step_frame,
            text=status_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=status_color
        )
        status_label.pack(pady=10)
    
    def create_iteration_card(self, step):
        """Crea tarjeta para mostrar una iteración de bisección"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        # Información de la iteración
        iter_frame = ctk.CTkFrame(self.current_step_frame)
        iter_frame.pack(fill="x", padx=30, pady=15)
        
        # Verificar si tenemos información de distancia límite para mostrar d(v)
        dist_limit = step.get('dist_limit', None)
        
        data = [
            ("a", f"{step['a']:.4f}", f"f(a) = {step['fa']:.6f}"),
            ("c (punto medio)", f"{step['c']:.4f}", f"f(c) = {step['fc']:.6f}"),
            ("b", f"{step['b']:.4f}", f"f(b) = {step['fb']:.6f}"),
        ]
        
        for label, value, func_text in data:
            row = ctk.CTkFrame(iter_frame)
            row.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                row,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                width=150
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=13),
                text_color=("#1f538d", "#4a9eff") if "medio" in label else None
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=func_text,
                font=ctk.CTkFont(size=11),
                text_color="gray60"
            ).pack(side="left", padx=10)
            
            # Si es el punto medio y tenemos dist_limit, mostrar d(v)
            if "medio" in label and dist_limit is not None:
                v_val = step['c']
                f_val = step['fc']
                d_val = f_val + dist_limit  # d(v) = f(v) + dist_limit
                
                ctk.CTkLabel(
                    row,
                    text=f"→ d({v_val:.2f}) = {d_val:.2f}m (Lagrange)",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    text_color=("green", "lightgreen")
                ).pack(side="left", padx=10)
        
        # Error
        error_frame = ctk.CTkFrame(self.current_step_frame)
        error_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(
            error_frame,
            text=f"Error: {step['error']:.6f} km/h",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="orange"
        ).pack(pady=10)
        
        if step.get('is_last', False):
            final_label = ctk.CTkLabel(
                self.current_step_frame,
                text="Convergencia alcanzada",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="green"
            )
            final_label.pack(pady=5)
    
    def create_result_card(self, step):
        """Crea tarjeta para mostrar resultado final"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="green"
        )
        title_label.pack(pady=(20, 10))
        
        # Resultado destacado
        result_frame = ctk.CTkFrame(self.current_step_frame)
        result_frame.pack(fill="x", padx=20, pady=15)
        
        if 'root' in step:
            # Resultado de bisección
            ctk.CTkLabel(
                result_frame,
                text=f"Velocidad Máxima Segura:",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                result_frame,
                text=f"{step['root']:.2f} km/h",
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            ).pack(pady=(0, 15))
            
            # Información adicional
            info_frame = ctk.CTkFrame(result_frame)
            info_frame.pack(fill="x", padx=20, pady=10)
            
            stats = [
                ("Iteraciones realizadas", str(step['iterations'])),
                ("Error final", f"{step['final_error']:.6f} km/h"),
                    ("Convergencia", "Si" if step['converged'] else "No (max. iteraciones)")
            ]
            
            for label, value in stats:
                row = ctk.CTkFrame(info_frame)
                row.pack(fill="x", padx=10, pady=3)
                
                ctk.CTkLabel(
                    row,
                    text=f"{label}:",
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    row,
                    text=value,
                    font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=5)
            
            # Interpretación
            if step.get('context'):
                interp_frame = ctk.CTkFrame(self.current_step_frame)
                interp_frame.pack(fill="x", padx=30, pady=15)
                
                ctk.CTkLabel(
                    interp_frame,
                    text="Interpretacion:",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(pady=(10, 5))
                
                interp_text = (f"Para poder frenar dentro de {step['context'].get('dist_limit', 'N/A')} metros, "
                             f"la velocidad máxima segura es de {step['root']:.1f} km/h.")
                
                ctk.CTkLabel(
                    interp_frame,
                    text=interp_text,
                    font=ctk.CTkFont(size=12),
                    wraplength=700,
                    justify="left"
                ).pack(pady=(0, 10), padx=15)
        
        elif 'result' in step:
            # Resultado de Lagrange
            ctk.CTkLabel(
                result_frame,
                text=f"Distancia de frenado a {step['x_eval']:.1f} km/h:",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                result_frame,
                text=f"{step['result']:.2f} metros",
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            ).pack(pady=(0, 15))
            
            # Cálculo
            if 'calculation' in step:
                calc_frame = ctk.CTkFrame(self.current_step_frame)
                calc_frame.pack(fill="x", padx=30, pady=10)
                
                ctk.CTkLabel(
                    calc_frame,
                    text="Cálculo completo:",
                    font=ctk.CTkFont(size=13, weight="bold")
                ).pack(pady=(10, 5))
                
                ctk.CTkLabel(
                    calc_frame,
                    text=step['calculation'],
                    font=ctk.CTkFont(size=11),
                    wraplength=700
                ).pack(pady=(0, 10), padx=15)
    
    def create_error_card(self, step):
        """Crea tarjeta para mostrar error"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
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
    
    def create_points_card(self, step):
        """Crea tarjeta para mostrar puntos experimentales"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
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
        
        ctk.CTkLabel(header, text="#", font=ctk.CTkFont(size=12, weight="bold"), width=50).pack(side="left", padx=5)
        ctk.CTkLabel(header, text=step.get('x_label', 'x'), font=ctk.CTkFont(size=12, weight="bold"), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header, text=step.get('y_label', 'y'), font=ctk.CTkFont(size=12, weight="bold"), width=150).pack(side="left", padx=5)
        
        # Puntos
        for i, (x, y) in enumerate(step['points']):
            row = ctk.CTkFrame(points_frame)
            row.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(row, text=str(i+1), font=ctk.CTkFont(size=12), width=50).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{x:.2f}", font=ctk.CTkFont(size=12), width=150).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=f"{y:.2f}", font=ctk.CTkFont(size=12), width=150).pack(side="left", padx=5)
    
    def create_calculations_card(self, step):
        """Crea tarjeta para mostrar cálculos de Lagrange"""
        title_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"{step['title']}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(pady=(20, 10))
        
        info_label = ctk.CTkLabel(
            self.current_step_frame,
            text=f"Evaluar para {step.get('x_label', 'x')} = {step['x_eval']:.2f}",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        info_label.pack(pady=10)
        
        # Mostrar cada contribución
        for detail in step['basis_details']:
            contrib_frame = ctk.CTkFrame(self.current_step_frame)
            contrib_frame.pack(fill="x", padx=20, pady=8)
            
            # Header del término
            header = ctk.CTkFrame(contrib_frame)
            header.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(
                header,
                text=f"Término {detail['j'] + 1}:  {detail['y_j']:.2f} × L_{detail['j']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            ).pack(side="left")
            
            ctk.CTkLabel(
                header,
                text=f"= {detail['contribution']:.6f}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            ).pack(side="right", padx=10)
            
            # Fórmula
            formula_text = f"L_{detail['j']} = [{detail['numerator_formula']}] / [{detail['denominator_formula']}]"
            
            ctk.CTkLabel(
                contrib_frame,
                text=formula_text,
                font=ctk.CTkFont(size=10),
                text_color="gray60",
                wraplength=700
            ).pack(padx=15, pady=2)
        
        # Resultado final
        total = sum(d['contribution'] for d in step['basis_details'])
        result_frame = ctk.CTkFrame(self.current_step_frame)
        result_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            result_frame,
            text=f"Resultado: {total:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#d32f2f", "#f44336")
        ).pack(pady=15)
    
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

