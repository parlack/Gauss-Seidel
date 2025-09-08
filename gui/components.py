import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import numpy as np
from typing import List, Callable, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# configurar el tema de customtkinter para una apariencia moderna
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ModernButton(ctk.CTkButton):
    """
    boton moderno personalizado
    
    extiende ctkbutton con estilos predefinidos para una apariencia moderna
    incluye configuraciones de esquinas redondeadas, fuentes y dimensiones
    """
    def __init__(self, parent, text, command=None, **kwargs):
        # configuracion por defecto para botones modernos
        default_kwargs = {
            "corner_radius": 8,  # esquinas redondeadas
            "font": ctk.CTkFont(size=14, weight="bold"),  # fuente en negrita
            "height": 40  # altura fija
        }
        # permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **default_kwargs)

class ModernEntry(ctk.CTkEntry):
    """
    campo de entrada moderno
    
    extiende ctkentry con estilos predefinidos para campos de entrada
    incluye placeholder text y configuracion de fuentes
    """
    def __init__(self, parent, placeholder="", **kwargs):
        # configuracion por defecto para campos de entrada
        default_kwargs = {
            "corner_radius": 8,  # esquinas redondeadas
            "font": ctk.CTkFont(size=12),  # fuente de tamano medio
            "height": 35,  # altura fija
            "placeholder_text": placeholder  # texto de ayuda
        }
        # permitir sobreescribir configuraciones default
        default_kwargs.update(kwargs)
        super().__init__(parent, **default_kwargs)

class MatrixInputGrid(ctk.CTkFrame):
    """
    grid para ingresar matriz de coeficientes
    
    widget personalizado que crea una grilla de campos de entrada para
    permitir al usuario introducir los coeficientes de la matriz del sistema
    incluye funcionalidades de redimensionamiento y validacion
    """
    
    def __init__(self, parent, size=3, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        # tamano actual del sistema (nxn)
        self.size = size
        # callback para notificar cambios
        self.on_change = on_change
        # matriz de widgets entry para los coeficientes
        self.entries = []
        # configurar interfaz inicial
        self.setup_ui()
    
    def setup_ui(self):
        # titulo del componente
        title = ctk.CTkLabel(
            self, 
            text="matriz de coeficientes (a)", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))
        
        # frame contenedor para el grid de entradas
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # crear la grilla inicial
        self.create_grid()
    
    def create_grid(self):
        """crea el grid de entradas para la matriz con diseno responsivo optimizado"""
        # limpiar entradas existentes antes de crear nuevas
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # crear frame scrollable si el sistema es grande
        if self.size > 4:
            # para sistemas grandes, usar frame con scroll para mejor visualizacion
            self.scroll_container = ctk.CTkScrollableFrame(
                self.grid_frame,
                width=min(650, self.size * 75),  # ancho optimizado
                height=min(450, self.size * 50)  # altura ajustada
            )
            self.scroll_container.pack(fill="both", expand=True, padx=8, pady=8)
            parent_frame = self.scroll_container
        else:
            # para sistemas pequenos, usar frame normal
            parent_frame = self.grid_frame
        
        # inicializar matriz de entradas
        self.entries = []
        
        # calcular tamano optimo de campos segun el tamano del sistema
        if self.size <= 3:
            field_width = 85
            font_size = 12
        elif self.size <= 5:
            field_width = 70
            font_size = 11
        elif self.size <= 7:
            field_width = 58
            font_size = 10
        else:
            field_width = 48
            font_size = 9
        
        # crear grid de entradas nxn
        for i in range(self.size):
            row_entries = []
            for j in range(self.size):
                # crear campo de entrada con placeholder descriptivo
                entry = ModernEntry(
                    parent_frame,
                    placeholder=f"a{i+1}{j+1}",  # a11, a12, etc.
                    width=field_width,
                    font=ctk.CTkFont(size=font_size)
                )
                # posicionar en la grilla
                entry.grid(row=i, column=j, padx=2, pady=2)
                
                # configurar callback para detectar cambios
                if self.on_change:
                    entry.bind('<KeyRelease>', self._on_entry_change)
                
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        # configurar peso de columnas para mejor distribucion del espacio
        if hasattr(parent_frame, 'grid_columnconfigure'):
            for j in range(self.size):
                parent_frame.grid_columnconfigure(j, weight=1)
    
    def resize_grid(self, new_size: int):
        """redimensiona el grid para un nuevo tamano de sistema"""
        # actualizar tamano y recrear grilla
        self.size = new_size
        self.create_grid()
    
    def get_values(self) -> List[List[str]]:
        """obtiene los valores actuales del grid como lista de listas"""
        values = []
        # recorrer cada fila de la matriz
        for i in range(self.size):
            row_values = []
            # recorrer cada columna de la fila
            for j in range(self.size):
                value = self.entries[i][j].get()
                # usar "0" como valor por defecto si esta vacio
                row_values.append(value if value else "0")
            values.append(row_values)
        return values
    
    def set_values(self, values: List[List[float]]):
        """establece valores en el grid desde una lista de listas"""
        # iterar solo hasta el minimo entre tamanos para evitar errores
        for i in range(min(self.size, len(values))):
            for j in range(min(self.size, len(values[i]))):
                # limpiar campo actual
                self.entries[i][j].delete(0, tk.END)
                # insertar nuevo valor como string
                self.entries[i][j].insert(0, str(values[i][j]))
    
    def clear_all(self):
        """limpia todas las entradas del grid"""
        # recorrer toda la matriz y limpiar cada campo
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)
    
    def _on_entry_change(self, event):
        """callback interno para cambios en las entradas"""
        # notificar cambios si hay callback configurado
        if self.on_change:
            self.on_change()

class VectorInputColumn(ctk.CTkFrame):
    """
    columna para ingresar vector de terminos independientes
    
    widget optimizado para layout de dos columnas que permite ingresar
    los terminos independientes del sistema de ecuaciones (vector b)
    incluye funcionalidades de redimensionamiento y validacion
    """
    
    def __init__(self, parent, size=3, on_change: Optional[Callable] = None):
        super().__init__(parent, corner_radius=10)
        # tamano actual del vector (n elementos)
        self.size = size
        # callback para notificar cambios
        self.on_change = on_change
        # lista de widgets entry para los terminos independientes
        self.entries = []
        # configurar interfaz inicial
        self.setup_ui()
    
    def setup_ui(self):
        # titulo mas compacto para el nuevo layout
        title = ctk.CTkLabel(
            self, 
            text="terminos independientes (b)", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(pady=(15, 12))
        
        # frame para las entradas - optimizado para columna
        self.entries_frame = ctk.CTkFrame(self)
        self.entries_frame.pack(padx=15, pady=(5, 15), fill="both", expand=True)
        
        # crear las entradas iniciales
        self.create_entries()
    
    def create_entries(self):
        """crea las entradas para el vector con diseno responsivo optimizado"""
        # limpiar entradas existentes antes de crear nuevas
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        
        # crear frame scrollable si el sistema es muy grande
        if self.size > 8:
            # para sistemas muy grandes, usar frame con scroll
            self.scroll_container = ctk.CTkScrollableFrame(
                self.entries_frame,
                height=min(350, self.size * 42)  # altura adaptable
            )
            self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
            parent_frame = self.scroll_container
        else:
            # para sistemas normales, usar frame normal
            parent_frame = self.entries_frame
        
        # inicializar lista de entradas
        self.entries = []
        
        # calcular tamano optimo de campos segun el tamano del sistema
        if self.size <= 3:
            field_width = 130  # mas ancho para el nuevo layout de dos columnas
            font_size = 12
            padding_y = 6
        elif self.size <= 5:
            field_width = 120
            font_size = 11
            padding_y = 5
        elif self.size <= 7:
            field_width = 110
            font_size = 10
            padding_y = 4
        else:
            field_width = 100
            font_size = 9
            padding_y = 3
        
        # crear entradas verticales para el vector
        for i in range(self.size):
            entry = ModernEntry(
                parent_frame,
                placeholder=f"b{i+1}",  # b1, b2, etc.
                width=field_width,
                font=ctk.CTkFont(size=font_size)
            )
            entry.pack(pady=padding_y)
            
            # configurar callback para detectar cambios
            if self.on_change:
                entry.bind('<KeyRelease>', self._on_entry_change)
            
            self.entries.append(entry)
    
    def resize_entries(self, new_size: int):
        """redimensiona las entradas para un nuevo tamano de vector"""
        # actualizar tamano y recrear entradas
        self.size = new_size
        self.create_entries()
    
    def get_values(self) -> List[str]:
        """obtiene los valores actuales del vector como lista de strings"""
        # retornar valores o "0" como default si estan vacios
        return [entry.get() if entry.get() else "0" for entry in self.entries]
    
    def set_values(self, values: List[float]):
        """establece valores en el vector desde una lista de floats"""
        # iterar sobre entradas y valores simultaneamente
        for i, entry in enumerate(self.entries):
            if i < len(values):
                # limpiar campo actual
                entry.delete(0, tk.END)
                # insertar nuevo valor como string
                entry.insert(0, str(values[i]))
    
    def clear_all(self):
        """limpia todas las entradas del vector"""
        # limpiar cada campo de entrada
        for entry in self.entries:
            entry.delete(0, tk.END)
    
    def _on_entry_change(self, event):
        """callback interno para cambios en las entradas del vector"""
        # notificar cambios si hay callback configurado
        if self.on_change:
            self.on_change()

class VisualizationPanel(ctk.CTkFrame):
    """
    panel para visualizar el proceso de solucion con interfaz moderna
    
    componente principal que muestra el proceso iterativo de gauss-seidel
    incluye navegacion entre iteraciones, graficos de convergencia,
    y visualizacion detallada de cada paso del algoritmo
    """
    
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        # configurar interfaz de usuario
        self.setup_ui()
        # indice de la iteracion actual mostrada
        self.current_iteration = 0
        # total de iteraciones del proceso
        self.total_iterations = 0
        # datos completos de todos los pasos
        self.steps_data = []
        # etiquetas para variables (x1, x2, etc)
        self.variable_labels = []
    
    def setup_ui(self):
        # titulo con diseno moderno
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="proceso de solucion - metodo de gauss-seidel",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        self.title_label.pack(side="left")
        
        # indicador de progreso visual
        self.progress_frame = ctk.CTkFrame(header_frame)
        self.progress_frame.pack(side="right")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=200,
            height=20,
            progress_color=("#1f538d", "#4a9eff")
        )
        self.progress_bar.pack(padx=10, pady=10)
        
        # frame de controles mejorado
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # informacion de iteracion con estilo
        info_frame = ctk.CTkFrame(controls_frame)
        info_frame.pack(side="left", padx=10, pady=5)
        
        # etiqueta para mostrar iteracion actual
        self.iteration_label = ctk.CTkLabel(
            info_frame,
            text="iteracion: 0 / 0",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.iteration_label.pack(side="left", padx=15, pady=8)
        
        # etiqueta para mostrar error actual
        self.error_label = ctk.CTkLabel(
            info_frame,
            text="error: 0.000000",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.error_label.pack(side="left", padx=15, pady=8)
        
        # botones de navegacion mejorados
        nav_frame = ctk.CTkFrame(controls_frame)
        nav_frame.pack(side="right", padx=10, pady=5)
        
        # boton ir al primero
        self.first_btn = ModernButton(
            nav_frame,
            text="primero",
            command=self.first_iteration,
            width=90,
            height=35
        )
        self.first_btn.pack(side="left", padx=2)
        
        # boton ir al anterior
        self.prev_btn = ModernButton(
            nav_frame,
            text="anterior",
            command=self.prev_iteration,
            width=90,
            height=35
        )
        self.prev_btn.pack(side="left", padx=2)
        
        # boton ir al siguiente
        self.next_btn = ModernButton(
            nav_frame,
            text="siguiente",
            command=self.next_iteration,
            width=90,
            height=35
        )
        self.next_btn.pack(side="left", padx=2)
        
        # boton ir al ultimo
        self.last_btn = ModernButton(
            nav_frame,
            text="ultimo",
            command=self.last_iteration,
            width=90,
            height=35
        )
        self.last_btn.pack(side="left", padx=2)
        
        # notebook moderno para diferentes vistas
        self.notebook = ctk.CTkTabview(self, width=1000)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # crear tabs principales
        self.notebook.add("vista iterativa")
        self.notebook.add("convergencia")
        self.notebook.add("resultado final")
        
        self.setup_iterations_tab()
        self.setup_convergence_tab()
        self.setup_result_tab()
    
    def setup_iterations_tab(self):
        """Configura la tab de iteraciones con diseño moderno"""
        self.iterations_frame = self.notebook.tab("📊 Vista Iterativa")
        
        # Scrollable frame para las iteraciones
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
    
    def setup_convergence_tab(self):
        """Configura la tab de convergencia con gráfico mejorado"""
        self.convergence_frame = self.notebook.tab("📈 Convergencia")
        
        # Frame para métricas
        metrics_frame = ctk.CTkFrame(self.convergence_frame)
        metrics_frame.pack(fill="x", padx=10, pady=10)
        
        # Métricas de convergencia
        self.convergence_metrics = []
        metrics_titles = ["🎯 Error Actual", "📉 Tasa de Convergencia", "⏱️ Iteraciones"]
        
        for i, title in enumerate(metrics_titles):
            metric_frame = ctk.CTkFrame(metrics_frame)
            metric_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(
                metric_frame,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(10, 5))
            
            metric_label = ctk.CTkLabel(
                metric_frame,
                text="0.000000",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            metric_label.pack(pady=(0, 10))
            
            self.convergence_metrics.append(metric_label)
        
        # Gráfico de convergencia
        self.convergence_fig = Figure(figsize=(10, 6), dpi=100, facecolor='white')
        self.convergence_ax = self.convergence_fig.add_subplot(111)
        
        self.convergence_canvas = FigureCanvasTkAgg(
            self.convergence_fig,
            self.convergence_frame
        )
        self.convergence_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_result_tab(self):
        """Configura la tab de resultado con diseño atractivo"""
        self.result_frame = self.notebook.tab("✅ Resultado Final")
        
        # Header del resultado
        result_header = ctk.CTkFrame(self.result_frame)
        result_header.pack(fill="x", padx=10, pady=10)
        
        self.convergence_status = ctk.CTkLabel(
            result_header,
            text="⏳ Procesando...",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="orange"
        )
        self.convergence_status.pack(pady=20)
        
        # Estadísticas del proceso
        stats_frame = ctk.CTkFrame(self.result_frame)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 Estadísticas del Proceso",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_title.pack(pady=(15, 10))
        
        # Grid de estadísticas
        self.stats_grid = ctk.CTkFrame(stats_frame)
        self.stats_grid.pack(fill="x", padx=20, pady=10)
        
        # Solución visual
        solution_frame = ctk.CTkFrame(self.result_frame)
        solution_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        solution_title = ctk.CTkLabel(
            solution_frame,
            text="🎯 Solución del Sistema",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        solution_title.pack(pady=(15, 10))
        
        # Contenedor para la solución
        self.solution_container = ctk.CTkFrame(solution_frame)
        self.solution_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_visualization(self, steps_data: List):
        """Actualiza la visualización con nuevos datos"""
        self.steps_data = steps_data
        self.total_iterations = len([s for s in steps_data if s['type'] == 'iteration'])
        self.current_iteration = 0
        self.update_current_step()
        self.update_convergence_plot()
        self.update_result_display()
    
    def update_current_step(self):
        """Actualiza la visualización del paso actual con diseño moderno"""
        if not self.steps_data:
            return
        
        # Encontrar pasos de iteración
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        
        if self.current_iteration < len(iteration_steps):
            step = iteration_steps[self.current_iteration]
            
            # Actualizar información en header
            self.iteration_label.configure(
                text=f"Iteración: {self.current_iteration + 1} / {len(iteration_steps)}"
            )
            
            self.error_label.configure(
                text=f"Error: {step['error']:.6f}"
            )
            
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
        """Crea una tarjeta visual moderna para mostrar una iteración"""
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
        
        error_badge = ctk.CTkLabel(
            title_frame,
            text=f"Error: {step['error']:.8f}",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=15,
            fg_color=("gray80", "gray20"),
            width=150,
            height=30
        )
        error_badge.pack(side="right", padx=10)
        
        # Contenedor principal con dos columnas
        main_container = ctk.CTkFrame(self.current_iteration_frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Columna izquierda: Cálculos
        left_column = ctk.CTkFrame(main_container)
        left_column.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        calc_title = ctk.CTkLabel(
            left_column,
            text="📝 Cálculos de Variables",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        calc_title.pack(pady=(15, 10))
        
        # Mostrar cada cálculo como una tarjeta
        for i, calc in enumerate(step['calculations']):
            calc_card = ctk.CTkFrame(left_column)
            calc_card.pack(fill="x", padx=10, pady=5)
            
            # Header de la variable
            var_header = ctk.CTkFrame(calc_card, height=40)
            var_header.pack(fill="x", padx=10, pady=(10, 5))
            var_header.pack_propagate(False)
            
            var_label = ctk.CTkLabel(
                var_header,
                text=f"x{calc['variable'] + 1}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            var_label.pack(side="left", pady=10)
            
            result_label = ctk.CTkLabel(
                var_header,
                text=f"= {calc['result']:.6f}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            )
            result_label.pack(side="right", pady=10)
            
            # Fórmula en formato amigable
            formula_label = ctk.CTkLabel(
                calc_card,
                text=calc['formula'],
                font=ctk.CTkFont(size=11),
                text_color="gray60",
                wraplength=300
            )
            formula_label.pack(padx=10, pady=(0, 10))
        
        # Columna derecha: Solución actual
        right_column = ctk.CTkFrame(main_container)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        solution_title = ctk.CTkLabel(
            right_column,
            text="🎯 Vector Solución",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        solution_title.pack(pady=(15, 10))
        
        # Mostrar solución como tabla visual
        solution_table = ctk.CTkFrame(right_column)
        solution_table.pack(fill="x", padx=10, pady=10)
        
        for i, value in enumerate(step['solution']):
            row_frame = ctk.CTkFrame(solution_table)
            row_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(
                row_frame,
                text=f"x{i+1}",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=40
            ).pack(side="left", padx=(10, 5), pady=8)
            
            ctk.CTkLabel(
                row_frame,
                text="=",
                font=ctk.CTkFont(size=14),
                width=20
            ).pack(side="left", pady=8)
            
            ctk.CTkLabel(
                row_frame,
                text=f"{value:.6f}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            ).pack(side="left", padx=(5, 10), pady=8)
        
        # Comparación con iteración anterior si existe
        if self.current_iteration > 0:
            prev_step = [s for s in self.steps_data if s['type'] == 'iteration'][self.current_iteration - 1]
            self.show_comparison(right_column, step['solution'], prev_step['solution'])
    
    def show_comparison(self, parent, current_solution, previous_solution):
        """Muestra comparación visual con la iteración anterior"""
        comparison_frame = ctk.CTkFrame(parent)
        comparison_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(
            comparison_frame,
            text="📊 Cambio Respecto Anterior",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        for i, (current, previous) in enumerate(zip(current_solution, previous_solution)):
            change = abs(current - previous)
            change_frame = ctk.CTkFrame(comparison_frame)
            change_frame.pack(fill="x", padx=5, pady=1)
            
            ctk.CTkLabel(
                change_frame,
                text=f"Δx{i+1}",
                font=ctk.CTkFont(size=11),
                width=40
            ).pack(side="left", padx=5, pady=3)
            
            # Color según el cambio
            if change < 1e-6:
                color = "green"
                icon = "✅"
            elif change < 1e-3:
                color = "orange"
                icon = "⚡"
            else:
                color = "red"
                icon = "🔄"
            
            ctk.CTkLabel(
                change_frame,
                text=f"{icon} {change:.2e}",
                font=ctk.CTkFont(size=11),
                text_color=color
            ).pack(side="left", padx=5, pady=3)
    
    def update_navigation_buttons(self):
        """Actualiza el estado de los botones de navegación"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
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
            self.update_convergence_plot()
    
    def last_iteration(self):
        """Ir a la última iteración"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration = len(iteration_steps) - 1
            self.update_current_step()
            self.update_convergence_plot()
    
    def update_convergence_plot(self):
        """Actualiza el gráfico de convergencia mejorado"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        
        if not iteration_steps:
            return
        
        errors = [step['error'] for step in iteration_steps]
        iterations = list(range(1, len(errors) + 1))
        
        # Actualizar métricas
        if self.current_iteration < len(errors):
            current_error = errors[self.current_iteration]
            self.convergence_metrics[0].configure(text=f"{current_error:.2e}")
            
            # Calcular tasa de convergencia
            if self.current_iteration > 0:
                rate = errors[self.current_iteration-1] / current_error if current_error > 0 else float('inf')
                self.convergence_metrics[1].configure(text=f"{rate:.2f}")
            else:
                self.convergence_metrics[1].configure(text="N/A")
            
            self.convergence_metrics[2].configure(text=f"{self.current_iteration + 1}")
        
        # Limpiar y configurar gráfico
        self.convergence_ax.clear()
        
        # Gráfico principal
        line = self.convergence_ax.semilogy(iterations, errors, 'b-', linewidth=3, alpha=0.7, label='Error por iteración')
        self.convergence_ax.semilogy(iterations, errors, 'bo', markersize=8, alpha=0.8)
        
        # Resaltar iteración actual
        if self.current_iteration < len(errors):
            self.convergence_ax.semilogy(
                self.current_iteration + 1,
                errors[self.current_iteration],
                'ro',
                markersize=12,
                label=f'Iteración actual: {self.current_iteration + 1}',
                zorder=10
            )
        
        # Estilo mejorado
        self.convergence_ax.set_xlabel('Iteración', fontsize=13, fontweight='bold')
        self.convergence_ax.set_ylabel('Error (escala logarítmica)', fontsize=13, fontweight='bold')
        self.convergence_ax.set_title('🔄 Convergencia del Método de Gauss-Seidel', fontsize=15, fontweight='bold', pad=20)
        
        # Grid y estilo
        self.convergence_ax.grid(True, alpha=0.3, linestyle='--')
        self.convergence_ax.legend(fontsize=11, framealpha=0.9)
        
        # Colores y estilo
        self.convergence_ax.spines['top'].set_visible(False)
        self.convergence_ax.spines['right'].set_visible(False)
        
        self.convergence_fig.tight_layout()
        self.convergence_canvas.draw()
    
    def update_result_display(self):
        """Actualiza la visualización del resultado con diseño moderno"""
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
                text="✅ ¡Sistema Resuelto Exitosamente!",
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
            ("🎯 Convergió", "Sí" if result_step['converged'] else "No"),
            ("🔄 Iteraciones", str(result_step['iterations'])),
            ("📉 Error Final", f"{result_step['final_error']:.2e}"),
            ("⏱️ Precisión", f"{result_step['final_error']:.8f}")
        ]
        
        for i, (label, value) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(self.stats_grid)
            stat_frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=(10, 2))
            
            color = "green" if i == 0 and result_step['converged'] else "#1f538d"
            ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(pady=(2, 10))
        
        # Configurar grid
        self.stats_grid.grid_columnconfigure(0, weight=1)
        self.stats_grid.grid_columnconfigure(1, weight=1)
        
        # Limpiar solución anterior
        for widget in self.solution_container.winfo_children():
            widget.destroy()
        
        # Mostrar solución en formato visual atractivo
        solution_grid = ctk.CTkFrame(self.solution_container)
        solution_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Calcular número de columnas (máximo 4)
        n_variables = len(result_step['solution'])
        n_cols = min(4, n_variables)
        n_rows = (n_variables + n_cols - 1) // n_cols
        
        for i, value in enumerate(result_step['solution']):
            row = i // n_cols
            col = i % n_cols
            
            var_frame = ctk.CTkFrame(solution_grid)
            var_frame.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            
            # Nombre de variable
            var_label = ctk.CTkLabel(
                var_frame,
                text=f"x{i+1}",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            var_label.pack(pady=(15, 5))
            
            # Valor
            value_label = ctk.CTkLabel(
                var_frame,
                text=f"{value:.6f}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#d32f2f", "#f44336")
            )
            value_label.pack(pady=(0, 15))
        
        # Configurar grid para que se expanda
        for col in range(n_cols):
            solution_grid.grid_columnconfigure(col, weight=1)
    
    def prev_iteration(self):
        """Ir a la iteración anterior"""
        if self.current_iteration > 0:
            self.current_iteration -= 1
            self.update_current_step()
            self.update_convergence_plot()
    
    def next_iteration(self):
        """Ir a la siguiente iteración"""
        iteration_steps = [s for s in self.steps_data if s['type'] == 'iteration']
        if self.current_iteration < len(iteration_steps) - 1:
            self.current_iteration += 1
            self.update_current_step()
            self.update_convergence_plot()
    
    def clear(self):
        """Limpia la visualización moderna"""
        self.steps_data = []
        self.current_iteration = 0
        self.total_iterations = 0
        
        # Limpiar frame de iteración actual
        for widget in self.current_iteration_frame.winfo_children():
            widget.destroy()
        
        # Reiniciar labels
        self.iteration_label.configure(text="Iteración: 0 / 0")
        self.error_label.configure(text="Error: 0.000000")
        
        # Reiniciar barra de progreso
        self.progress_bar.set(0)
        
        # Limpiar métricas de convergencia
        for metric in self.convergence_metrics:
            metric.configure(text="0.000000")
        
        # Limpiar gráfico
        self.convergence_ax.clear()
        self.convergence_canvas.draw()
        
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
