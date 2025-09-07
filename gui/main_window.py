import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import numpy as np
from typing import Optional

from .components import (
    ModernButton, ModernEntry, MatrixInputGrid, 
    VectorInputColumn, VisualizationPanel
)
from solver.gauss_seidel import GaussSeidelSolver
from utils.validators import EquationValidator

class GaussSeidelApp(ctk.CTk):
    """Aplicación principal para resolver sistemas con Gauss-Seidel"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Resolver Sistemas de Ecuaciones - Método de Gauss-Seidel")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Variables
        self.current_size = 3
        self.solver = GaussSeidelSolver()
        self.last_solution = None
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Frame de contenido principal
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear notebook principal
        self.main_notebook = ctk.CTkTabview(content_frame)
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabs
        self.setup_input_tab()
        self.setup_solution_tab()
    
    def create_header(self, parent):
        """Crea el header de la aplicación"""
        header_frame = ctk.CTkFrame(parent, height=100, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔢 Resolver Sistemas de Ecuaciones Lineales",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Método iterativo de Gauss-Seidel con visualización paso a paso",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="left", padx=(0, 30), pady=(45, 5))
        
        # Información del sistema actual
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="right", padx=30, pady=20)
        
        self.system_info_label = ctk.CTkLabel(
            info_frame,
            text=f"Sistema: {self.current_size}×{self.current_size}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.system_info_label.pack(padx=15, pady=10)
    
    def setup_input_tab(self):
        """Configura la pestaña de entrada de datos"""
        input_tab = self.main_notebook.add("📝 Entrada de Datos")
        
        # Frame de controles superiores
        controls_frame = ctk.CTkFrame(input_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Selector de tamaño del sistema
        size_frame = ctk.CTkFrame(controls_frame)
        size_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(
            size_frame,
            text="Tamaño del Sistema:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.size_var = tk.StringVar(value=str(self.current_size))
        self.size_spinbox = ctk.CTkComboBox(
            size_frame,
            values=[str(i) for i in range(2, 11)],
            variable=self.size_var,
            command=self.on_size_change,
            width=100
        )
        self.size_spinbox.pack(side="left", padx=5, pady=10)
        
        # Botones de control
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)
        
        ModernButton(
            buttons_frame,
            text="🧹 Limpiar Todo",
            command=self.clear_all_inputs,
            fg_color="gray50",
            width=120
        ).pack(side="left", padx=5, pady=5)
        
        ModernButton(
            buttons_frame,
            text="📋 Ejemplo",
            command=self.load_example,
            fg_color="orange",
            width=120
        ).pack(side="left", padx=5, pady=5)
        
        ModernButton(
            buttons_frame,
            text="✅ Validar",
            command=self.validate_input,
            fg_color="green",
            width=120
        ).pack(side="left", padx=5, pady=5)
        
        # Frame principal para matriz y vector
        input_main_frame = ctk.CTkFrame(input_tab)
        input_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame izquierdo para la matriz
        left_frame = ctk.CTkFrame(input_main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # Matriz de coeficientes
        self.matrix_input = MatrixInputGrid(
            left_frame,
            size=self.current_size,
            on_change=self.on_input_change
        )
        self.matrix_input.pack(fill="both", expand=True)
        
        # Frame derecho con dos columnas para mejor uso del espacio
        right_frame = ctk.CTkFrame(input_main_frame)
        right_frame.pack(side="right", fill="both", padx=(5, 10), pady=10)
        
        # Contenedor principal para las dos columnas
        columns_container = ctk.CTkFrame(right_frame)
        columns_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Columna izquierda: Vector de términos independientes
        vector_column = ctk.CTkFrame(columns_container)
        vector_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.vector_input = VectorInputColumn(
            vector_column,
            size=self.current_size,
            on_change=self.on_input_change
        )
        self.vector_input.pack(fill="both", expand=True)
        
        # Columna derecha: Configuración del solver
        config_column = ctk.CTkFrame(columns_container)
        config_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Título de configuración
        config_title = ctk.CTkLabel(
            config_column,
            text="Configuración del Solver",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        config_title.pack(pady=(15, 20))
        
        # Frame contenedor para los controles
        solver_controls_frame = ctk.CTkFrame(config_column)
        solver_controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Tolerancia
        tol_frame = ctk.CTkFrame(solver_controls_frame)
        tol_frame.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(
            tol_frame,
            text="Tolerancia:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        self.tolerance_var = tk.StringVar(value="1e-6")
        self.tolerance_entry = ModernEntry(
            tol_frame,
            textvariable=self.tolerance_var,
            width=140,
            placeholder="1e-6"
        )
        self.tolerance_entry.pack(pady=(0, 8))
        
        # Máximo de iteraciones
        max_iter_frame = ctk.CTkFrame(solver_controls_frame)
        max_iter_frame.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(
            max_iter_frame,
            text="Máx. Iteraciones:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        self.max_iter_var = tk.StringVar(value="100")
        self.max_iter_entry = ModernEntry(
            max_iter_frame,
            textvariable=self.max_iter_var,
            width=140,
            placeholder="100"
        )
        self.max_iter_entry.pack(pady=(0, 8))
        
        # Vector inicial (opcional)
        initial_frame = ctk.CTkFrame(solver_controls_frame)
        initial_frame.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(
            initial_frame,
            text="Vector Inicial:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        self.use_zero_initial = tk.BooleanVar(value=True)
        initial_checkbox = ctk.CTkCheckBox(
            initial_frame,
            text="Usar vector cero",
            variable=self.use_zero_initial,
            font=ctk.CTkFont(size=11)
        )
        initial_checkbox.pack(pady=(0, 8))
        
        # Botón de resolver - ahora en la parte inferior del frame derecho
        self.solve_button = ModernButton(
            right_frame,
            text="🚀 RESOLVER SISTEMA",
            command=self.solve_system,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f538d"
        )
        self.solve_button.pack(fill="x", padx=10, pady=(10, 15), side="bottom")
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            input_tab,
            text="💡 Introduce los coeficientes del sistema de ecuaciones",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)
    
    def setup_solution_tab(self):
        """Configura la pestaña de solución"""
        solution_tab = self.main_notebook.add("📊 Proceso de Solución")
        
        # Panel de visualización
        self.visualization_panel = VisualizationPanel(solution_tab)
        self.visualization_panel.pack(fill="both", expand=True, padx=10, pady=10)
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_size_change(self, value):
        """Callback cuando cambia el tamaño del sistema con optimización automática"""
        try:
            new_size = int(value)
            if new_size != self.current_size:
                self.current_size = new_size
                self.matrix_input.resize_grid(new_size)
                self.vector_input.resize_entries(new_size)
                self.system_info_label.configure(text=f"Sistema: {new_size}×{new_size}")
                
                # Auto-optimización de la ventana para sistemas grandes
                if new_size >= 7:
                    # Para sistemas grandes, maximizar la ventana automáticamente
                    self.state('zoomed')  # Maximizar en Windows
                    self.update_status("🔍 Ventana maximizada automáticamente para mejor visualización")
                elif new_size >= 5:
                    # Para sistemas medianos, aumentar el tamaño de la ventana
                    self.geometry("1500x950")
                    self.update_status("📐 Ventana redimensionada para mejor visualización")
                else:
                    # Para sistemas pequeños, tamaño normal
                    self.geometry("1400x900")
                    self.update_status("📏 Tamaño del sistema actualizado")
                
                # Forzar actualización del layout
                self.update_idletasks()
        except ValueError:
            pass
    
    def on_input_change(self):
        """Callback cuando cambian los datos de entrada"""
        # Aquí podrías implementar validación en tiempo real
        pass
    
    def clear_all_inputs(self):
        """Limpia todas las entradas"""
        self.matrix_input.clear_all()
        self.vector_input.clear_all()
        self.visualization_panel.clear()
        self.update_status("🧹 Todas las entradas han sido limpiadas")
    
    def load_example(self):
        """Carga un ejemplo predefinido (incluyendo casos que requieren reordenamiento)"""
        import random
        
        # Ofrecer diferentes tipos de ejemplos
        example_type = messagebox.askyesno(
            "Tipo de Ejemplo",
            "¿Quieres cargar un ejemplo que demuestre el reordenamiento automático?\n\n"
            "✅ SÍ: Ejemplo que necesita reordenamiento\n"
            "❌ NO: Ejemplo ya diagonalmente dominante"
        )
        
        if example_type:  # Ejemplo que necesita reordenamiento
            if self.current_size == 3:
                # Sistema que NO es diagonalmente dominante inicialmente
                matrix_values = [
                    [1, 8, 2],     # Esta fila necesita intercambio
                    [2, 1, 9],     # Esta también
                    [15, -1, 2]    # Esta está bien (15 > 3)
                ]
                vector_values = [11, 12, 16]
                example_msg = "🔧 Ejemplo cargado: Sistema que requiere reordenamiento para ser diagonalmente dominante"
            elif self.current_size == 2:
                matrix_values = [
                    [1, 4],  # 1 < 4, necesita intercambio
                    [6, 2]   # 6 > 2, está bien
                ]
                vector_values = [5, 8]
                example_msg = "🔧 Ejemplo cargado: Sistema 2×2 que requiere reordenamiento"
            else:
                # Generar sistema que necesite reordenamiento
                matrix_values = []
                vector_values = []
                for i in range(self.current_size):
                    row = []
                    for j in range(self.current_size):
                        if i == j:
                            # Diagonal débil inicialmente
                            row.append(random.randint(1, 3))
                        else:
                            # Elementos off-diagonal más fuertes
                            row.append(random.randint(2, 8))
                    matrix_values.append(row)
                    vector_values.append(random.randint(1, 20))
                
                # Asegurar que al menos una fila pueda ser dominante
                strong_row_idx = random.randint(0, self.current_size - 1)
                matrix_values[strong_row_idx][strong_row_idx] = sum(abs(x) for x in matrix_values[strong_row_idx]) + 2
                
                example_msg = f"🔧 Ejemplo {self.current_size}×{self.current_size} generado: Sistema que puede requerir reordenamiento"
        
        else:  # Ejemplo ya diagonalmente dominante
            if self.current_size == 3:
                # Sistema ya diagonalmente dominante
                matrix_values = [
                    [10, -1, 2],
                    [-1, 11, -1],
                    [2, -1, 10]
                ]
                vector_values = [6, 25, -11]
                example_msg = "✅ Ejemplo cargado: Sistema ya diagonalmente dominante"
            elif self.current_size == 2:
                matrix_values = [
                    [4, 1],
                    [2, 3]
                ]
                vector_values = [1, 11]
                example_msg = "✅ Ejemplo cargado: Sistema 2×2 diagonalmente dominante"
            else:
                # Ejemplo genérico diagonalmente dominante
                matrix_values = []
                vector_values = []
                for i in range(self.current_size):
                    row = [0] * self.current_size
                    row[i] = self.current_size + 5  # Diagonal dominante
                    for j in range(self.current_size):
                        if i != j:
                            row[j] = 1
                    matrix_values.append(row)
                    vector_values.append(i + 1)
                example_msg = f"✅ Ejemplo {self.current_size}×{self.current_size} cargado: Sistema diagonalmente dominante"
        
        self.matrix_input.set_values(matrix_values)
        self.vector_input.set_values(vector_values)
        self.update_status(example_msg)
    
    def validate_input(self):
        """Valida la entrada actual"""
        try:
            # Obtener valores
            matrix_data = self.matrix_input.get_values()
            vector_data = self.vector_input.get_values()
            
            # Validar matriz
            is_valid_matrix, matrix_error, matrix_np = EquationValidator.validate_matrix(matrix_data)
            if not is_valid_matrix:
                self.update_status(f"❌ Error en matriz: {matrix_error}", is_error=True)
                messagebox.showerror("Error de Validación", f"Matriz: {matrix_error}")
                return False
            
            # Validar vector
            is_valid_vector, vector_error, vector_np = EquationValidator.validate_vector(vector_data)
            if not is_valid_vector:
                self.update_status(f"❌ Error en vector: {vector_error}", is_error=True)
                messagebox.showerror("Error de Validación", f"Vector: {vector_error}")
                return False
            
            # Intentar hacer la matriz diagonalmente dominante
            dominance_result = EquationValidator.make_diagonally_dominant(matrix_np, vector_np)
            
            if dominance_result['success']:
                # Actualizar las matrices con la versión optimizada
                matrix_np = dominance_result['matrix']
                vector_np = dominance_result['vector']
                
                # Actualizar la interfaz con los nuevos valores
                self.matrix_input.set_values(matrix_np.tolist())
                self.vector_input.set_values(vector_np.tolist())
                
                # Informar al usuario
                swaps_count = len(dominance_result['swaps_made'])
                if swaps_count > 0:
                    success_msg = f"✅ {dominance_result['message']}"
                    self.update_status(success_msg)
                    
                    # Mostrar detalles de los intercambios
                    swaps_details = "Intercambios realizados:\n"
                    for swap in dominance_result['swaps_made']:
                        swaps_details += f"• Fila {swap[0]+1} ↔ Fila {swap[1]+1}\n"
                    
                    messagebox.showinfo(
                        "Matriz Optimizada",
                        f"🔧 Sistema reordenado automáticamente\n\n"
                        f"{dominance_result['message']}\n\n"
                        f"{swaps_details}\n"
                        f"✅ Ahora la matriz es diagonalmente dominante.\n"
                        f"🚀 La convergencia está garantizada."
                    )
                else:
                    self.update_status("✅ La matriz ya es diagonalmente dominante")
            else:
                # No se pudo hacer diagonalmente dominante
                warning_msg = f"⚠️ {dominance_result['message']}. La convergencia no está garantizada."
                self.update_status(warning_msg, is_warning=True)
                result = messagebox.askyesno(
                    "Advertencia - Convergencia No Garantizada",
                    f"🔧 Se intentó optimizar la matriz intercambiando filas.\n\n"
                    f"❌ {dominance_result['message']}\n\n"
                    f"⚠️ El método de Gauss-Seidel puede no converger.\n\n"
                    f"¿Deseas continuar de todos modos?"
                )
                if not result:
                    return False
            
            self.update_status("✅ Validación exitosa. Sistema listo para resolver")
            return True
            
        except Exception as e:
            error_msg = f"❌ Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            return False
    
    def solve_system(self):
        """Resuelve el sistema de ecuaciones"""
        # Validar entrada primero
        if not self.validate_input():
            return
        
        try:
            # Obtener valores
            matrix_data = self.matrix_input.get_values()
            vector_data = self.vector_input.get_values()
            
            # Convertir a numpy arrays
            _, _, A = EquationValidator.validate_matrix(matrix_data)
            _, _, b = EquationValidator.validate_vector(vector_data)
            
            # Intentar optimización automática (sin mostrar mensaje si ya es dominante)
            dominance_result = EquationValidator.make_diagonally_dominant(A, b)
            
            if dominance_result['success'] and len(dominance_result['swaps_made']) > 0:
                # Solo actualizar si se hicieron cambios
                A = dominance_result['matrix']
                b = dominance_result['vector']
                
                # Actualizar la interfaz silenciosamente
                self.matrix_input.set_values(A.tolist())
                self.vector_input.set_values(b.tolist())
                
                # Mensaje discreto en el status
                self.update_status(f"🔧 Sistema optimizado: {dominance_result['message']}")
            elif not dominance_result['success']:
                # Solo mostrar advertencia si no se pudo optimizar y no es dominante
                self.update_status("⚠️ Sistema sin dominancia diagonal - convergencia no garantizada", is_warning=True)
            
            # Configurar solver
            try:
                self.solver.tolerance = float(self.tolerance_var.get())
                self.solver.max_iterations = int(self.max_iter_var.get())
            except ValueError:
                messagebox.showerror("Error", "Valores de configuración inválidos")
                return
            
            # Resolver
            self.update_status("🔄 Resolviendo sistema...")
            self.solve_button.configure(text="🔄 Resolviendo...", state="disabled")
            self.update_idletasks()
            
            # Generar pasos detallados
            steps_data = self.solver.generate_step_by_step(A, b)
            
            # Actualizar visualización
            self.visualization_panel.update_visualization(steps_data)
            
            # Cambiar a la pestaña de solución
            self.main_notebook.set("📊 Proceso de Solución")
            
            # Actualizar status
            result = steps_data[-1]  # Último paso es el resultado
            if result['converged']:
                self.update_status("✅ Sistema resuelto con éxito")
            else:
                self.update_status("⚠️ Sistema resuelto (convergencia no alcanzada)", is_warning=True)
            
        except Exception as e:
            error_msg = f"❌ Error al resolver: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error de Resolución", error_msg)
        
        finally:
            # Restaurar botón
            self.solve_button.configure(text="🚀 RESOLVER SISTEMA", state="normal")
    
    def update_status(self, message: str, is_error: bool = False, is_warning: bool = False):
        """Actualiza el mensaje de estado"""
        if is_error:
            color = "red"
        elif is_warning:
            color = "orange"
        else:
            color = ("gray60", "gray40")
        
        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()
