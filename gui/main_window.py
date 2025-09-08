import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from .components import (
    ModernButton, ModernEntry, MatrixInputGrid, 
    VectorInputColumn, VisualizationPanel
)
from solver.gauss_seidel import GaussSeidelSolver
from utils.validators import EquationValidator

class GaussSeidelApp(ctk.CTk):
    """
    aplicacion principal para resolver sistemas con gauss-seidel
    
    interfaz grafica principal que integra todos los componentes
    para resolver sistemas de ecuaciones lineales usando el metodo
    iterativo de gauss-seidel con visualizacion paso a paso
    """
    
    def __init__(self):
        super().__init__()
        
        # configuracion de la ventana principal
        self.title("resolver sistemas de ecuaciones - metodo de gauss-seidel")
        self.geometry("1280x720")
        self.minsize(1024, 500)
        
        # variables de estado de la aplicacion
        self.current_size = 3  # tamano actual del sistema
        self.solver = GaussSeidelSolver()  # instancia del solver
        # estado: ultima solucion calculada (no se usa)
        # eliminado para simplificar
        
        # configurar tema visual
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # configurar interfaz de usuario
        self.setup_ui()
        # centrar ventana en pantalla
        self.center_window()
    
    def setup_ui(self):
        """configura la interfaz de usuario principal"""
        
        # frame principal que contiene todo
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # crear header con titulo y informacion
        self.create_header(main_frame)
        
        # frame de contenido principal
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # crear notebook principal con pestanas
        self.main_notebook = ctk.CTkTabview(content_frame)
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # configurar pestanas principales
        self.setup_input_tab()
        self.setup_solution_tab()
    
    def create_header(self, parent):
        """crea el header de la aplicacion con titulo e informacion"""
        header_frame = ctk.CTkFrame(parent, height=100, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # titulo principal de la aplicacion
        title_label = ctk.CTkLabel(
            header_frame,
            text="resolver sistemas de ecuaciones lineales",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(side="left", padx=30, pady=25)
        
        # subtitulo explicativo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="metodo iterativo de gauss-seidel con visualizacion paso a paso",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="left", padx=(0, 30), pady=(45, 5))
        
        # informacion del sistema actual
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="right", padx=30, pady=20)
        
        # etiqueta que muestra el tamano actual del sistema
        self.system_info_label = ctk.CTkLabel(
            info_frame,
            text=f"sistema: {self.current_size}x{self.current_size}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.system_info_label.pack(padx=15, pady=10)
    
    def setup_input_tab(self):
        """configura la pestana de entrada de datos"""
        input_tab = self.main_notebook.add("entrada de datos")
        
        # frame de controles superiores
        controls_frame = ctk.CTkFrame(input_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # selector de tamano del sistema
        size_frame = ctk.CTkFrame(controls_frame)
        size_frame.pack(side="left", padx=10, pady=10)
        
        # etiqueta para selector de tamano
        ctk.CTkLabel(
            size_frame,
            text="tamano del sistema:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        # campo de entrada para tamano del sistema
        self.size_var = tk.StringVar(value=str(self.current_size))
        self.size_entry = ModernEntry(
            size_frame,
            textvariable=self.size_var,
            width=80,
            placeholder="n",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.size_entry.pack(side="left", padx=5, pady=10)
        
        # permitir presionar enter para aceptar
        self.size_entry.bind('<Return>', lambda event: self.accept_size_change())
        
        # boton de aceptar tamano con icono de palomita
        self.accept_size_btn = ModernButton(
            size_frame,
            text="✓",
            command=self.accept_size_change,
            width=40,
            height=35,
            fg_color="green",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.accept_size_btn.pack(side="left", padx=3, pady=10)
        
        # botones de control
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)
        
        # boton para limpiar todo
        ModernButton(
            buttons_frame,
            text="limpiar todo",
            command=self.clear_all_inputs,
            fg_color="gray50",
            width=120
        ).pack(side="left", padx=5, pady=5)
        

        # boton principal de resolver - en la parte inferior del frame derecho
        self.solve_button = ModernButton(
            buttons_frame,
            text="resolver sistema",
            command=self.solve_system,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f538d"
        )
        self.solve_button.pack(fill="x", padx=10, pady=(10, 15), side="bottom")
        

        # boton para cargar ejemplo
        ModernButton(
            buttons_frame,
            text="ejemplo",
            command=self.load_example,
            fg_color="orange",
            width=120
        ).pack(side="left", padx=5, pady=5)
        
        # boton para validar entrada
        ModernButton(
            buttons_frame,
            text="validar",
            command=self.validate_input,
            fg_color="green",
            width=120
        ).pack(side="left", padx=5, pady=5)
        
        # frame principal para matriz y vector
        input_main_frame = ctk.CTkFrame(input_tab)
        input_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # frame izquierdo para la matriz de coeficientes
        left_frame = ctk.CTkFrame(input_main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # widget para ingresar matriz de coeficientes
        self.matrix_input = MatrixInputGrid(
            left_frame,
            size=self.current_size,
            on_change=self.on_input_change
        )
        self.matrix_input.pack(fill="both", expand=True)
        
        # frame derecho con dos columnas para mejor uso del espacio
        right_frame = ctk.CTkFrame(input_main_frame)
        right_frame.pack(side="right", fill="both", padx=(5, 10), pady=10)
        
        # contenedor principal para las dos columnas
        columns_container = ctk.CTkFrame(right_frame)
        columns_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # columna izquierda: vector de terminos independientes
        vector_column = ctk.CTkFrame(columns_container)
        vector_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # widget para ingresar vector de terminos independientes
        self.vector_input = VectorInputColumn(
            vector_column,
            size=self.current_size,
            on_change=self.on_input_change
        )
        self.vector_input.pack(fill="both", expand=True)
        
        # columna derecha: configuracion del solver
        config_column = ctk.CTkFrame(columns_container)
        config_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # titulo de configuracion
        config_title = ctk.CTkLabel(
            config_column,
            text="configuracion del solver",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        config_title.pack(pady=(15, 20))
        
        # frame contenedor para los controles del solver
        solver_controls_frame = ctk.CTkFrame(config_column)
        solver_controls_frame.pack(fill="x", padx=10, pady=5)
        
        # configuracion de tolerancia
        tol_frame = ctk.CTkFrame(solver_controls_frame)
        tol_frame.pack(fill="x", padx=10, pady=8)
        
        # etiqueta para tolerancia
        ctk.CTkLabel(
            tol_frame,
            text="tolerancia:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        # campo para ingresar tolerancia
        self.tolerance_var = tk.StringVar(value="1e-6")
        self.tolerance_entry = ModernEntry(
            tol_frame,
            textvariable=self.tolerance_var,
            width=140,
            placeholder="1e-6"
        )
        self.tolerance_entry.pack(pady=(0, 8))
        
        # configuracion de maximo de iteraciones
        max_iter_frame = ctk.CTkFrame(solver_controls_frame)
        max_iter_frame.pack(fill="x", padx=10, pady=8)
        
        # etiqueta para maximo de iteraciones
        ctk.CTkLabel(
            max_iter_frame,
            text="max. iteraciones:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        # campo para ingresar maximo de iteraciones
        self.max_iter_var = tk.StringVar(value="100")
        self.max_iter_entry = ModernEntry(
            max_iter_frame,
            textvariable=self.max_iter_var,
            width=140,
            placeholder="100"
        )
        self.max_iter_entry.pack(pady=(0, 8))
        
        # configuracion de vector inicial (opcional)
        initial_frame = ctk.CTkFrame(solver_controls_frame)
        initial_frame.pack(fill="x", padx=10, pady=8)
        
        # etiqueta para vector inicial
        ctk.CTkLabel(
            initial_frame,
            text="vector inicial:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(8, 4))
        
        # checkbox para usar vector cero como inicial
        self.use_zero_initial = tk.BooleanVar(value=True)
        initial_checkbox = ctk.CTkCheckBox(
            initial_frame,
            text="usar vector cero",
            variable=self.use_zero_initial,
            font=ctk.CTkFont(size=11)
        )
        initial_checkbox.pack(pady=(0, 8))
        
        # barra de estado para mostrar mensajes al usuario
        self.status_label = ctk.CTkLabel(
            input_tab,
            text="introduce los coeficientes del sistema de ecuaciones",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)
    
    def setup_solution_tab(self):
        """configura la pestana de solucion"""
        solution_tab = self.main_notebook.add("proceso de solucion")
        
        # panel principal de visualizacion del proceso
        self.visualization_panel = VisualizationPanel(solution_tab)
        self.visualization_panel.pack(fill="both", expand=True, padx=10, pady=10)
    
    def center_window(self):
        """centra la ventana en la pantalla"""
        # actualizar geometria para obtener tamano real
        self.update_idletasks()
        # obtener dimensiones de la ventana
        width = self.winfo_width()
        height = self.winfo_height()
        # calcular posicion central
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        # aplicar geometria centrada
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def accept_size_change(self):
        """acepta y valida el cambio de tamano del sistema"""
        try:
            value_str = self.size_var.get().strip()
            if not value_str:
                self.update_status("por favor ingresa un tamano para el sistema", is_error=True)
                messagebox.showerror("error", "debes ingresar un tamano para el sistema")
                return
            new_size = int(value_str)
            if new_size < 2:
                self.update_status("el tamano del sistema debe ser mayor o igual a 2", is_error=True)
                messagebox.showerror("error", "el tamano del sistema debe ser al menos 2x2")
                self.size_var.set(str(self.current_size))
                return
            if new_size > 50:
                result = messagebox.askyesno(
                    "advertencia - sistema grande",
                    f"estas creando un sistema de {new_size}x{new_size} ({new_size*new_size} coeficientes).\n\n"
                    f"sistemas muy grandes pueden ser lentos de procesar y ocupar mucha memoria.\n\n"
                    f"¿deseas continuar?"
                )
                if not result:
                    self.size_var.set(str(self.current_size))
                    return
            if new_size != self.current_size:
                self.current_size = new_size
                self.matrix_input.resize_grid(new_size)
                self.vector_input.resize_entries(new_size)
                self.system_info_label.configure(text=f"sistema: {new_size}x{new_size}")
                if new_size >= 15:
                    self.state('zoomed')
                    self.update_status(f"sistema {new_size}x{new_size} creado - ventana maximizada automaticamente")
                elif new_size >= 8:
                    self.geometry("1600x1000")
                    self.update_status(f"sistema {new_size}x{new_size} creado - ventana redimensionada")
                elif new_size >= 5:
                    self.geometry("1500x950")
                    self.update_status(f"sistema {new_size}x{new_size} creado")
                else:
                    self.geometry("1400x900")
                    self.update_status(f"sistema {new_size}x{new_size} creado")
                self.visualization_panel.clear()
                self.update_idletasks()
            else:
                self.update_status("el tamano ya es el mismo")
        except ValueError:
            self.update_status("por favor ingresa un numero valido", is_error=True)
            messagebox.showerror("error", f"'{self.size_var.get()}' no es un numero valido")
            self.size_var.set(str(self.current_size))
        except Exception as e:
            error_msg = f"error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("error", error_msg)
            self.size_var.set(str(self.current_size))
    
    
    
    def on_input_change(self):
        """callback cuando cambian los datos de entrada"""
        # aqui se podria implementar validacion en tiempo real
        # por ahora solo es un placeholder para futuras funcionalidades
        pass
    
    def clear_all_inputs(self):
        """limpia todas las entradas de la interfaz"""
        # limpiar matriz de coeficientes
        self.matrix_input.clear_all()
        # limpiar vector de terminos independientes
        self.vector_input.clear_all()
        # limpiar panel de visualizacion
        self.visualization_panel.clear()
        # actualizar mensaje de estado
        self.update_status("todas las entradas han sido limpiadas")
    
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
        """valida la entrada actual del usuario"""
        try:
            # obtener valores ingresados por el usuario
            matrix_data = self.matrix_input.get_values()
            vector_data = self.vector_input.get_values()
            
            # validar matriz de coeficientes
            is_valid_matrix, matrix_error, matrix_np = EquationValidator.validate_matrix(matrix_data)
            if not is_valid_matrix:
                self.update_status(f"error en matriz: {matrix_error}", is_error=True)
                messagebox.showerror("error de validacion", f"matriz: {matrix_error}")
                return False
            
            # validar vector de terminos independientes
            is_valid_vector, vector_error, vector_np = EquationValidator.validate_vector(vector_data)
            if not is_valid_vector:
                self.update_status(f"error en vector: {vector_error}", is_error=True)
                messagebox.showerror("error de validacion", f"vector: {vector_error}")
                return False
            
            # intentar hacer la matriz diagonalmente dominante
            dominance_result = EquationValidator.make_diagonally_dominant(matrix_np, vector_np)
            
            if dominance_result['success']:
                # actualizar las matrices con la version optimizada
                matrix_np = dominance_result['matrix']
                vector_np = dominance_result['vector']
                
                # actualizar la interfaz con los nuevos valores
                self.matrix_input.set_values(matrix_np.tolist())
                self.vector_input.set_values(vector_np.tolist())
                
                # informar al usuario sobre los cambios
                swaps_count = len(dominance_result['swaps_made'])
                if swaps_count > 0:
                    success_msg = f"{dominance_result['message']}"
                    self.update_status(success_msg)
                    
                    # mostrar detalles de los intercambios realizados
                    swaps_details = "intercambios realizados:\n"
                    for swap in dominance_result['swaps_made']:
                        swaps_details += f"fila {swap[0]+1} <-> fila {swap[1]+1}\n"
                    
                    messagebox.showinfo(
                        "matriz optimizada",
                        f"sistema reordenado automaticamente\n\n"
                        f"{dominance_result['message']}\n\n"
                        f"{swaps_details}\n"
                        f"ahora la matriz es diagonalmente dominante.\n"
                        f"la convergencia esta garantizada."
                    )
                else:
                    self.update_status("la matriz ya es diagonalmente dominante")
            else:
                # no se pudo hacer diagonalmente dominante
                warning_msg = f"{dominance_result['message']}. la convergencia no esta garantizada."
                self.update_status(warning_msg, is_warning=True)
                result = messagebox.askyesno(
                    "advertencia - convergencia no garantizada",
                    f"se intento optimizar la matriz intercambiando filas.\n\n"
                    f"{dominance_result['message']}\n\n"
                    f"el metodo de gauss-seidel puede no converger.\n\n"
                    f"deseas continuar de todos modos?"
                )
                if not result:
                    return False
            
            self.update_status("validacion exitosa. sistema listo para resolver")
            return True
            
        except Exception as e:
            error_msg = f"error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("error", error_msg)
            return False
    
    def solve_system(self):
        """resuelve el sistema de ecuaciones usando gauss-seidel"""
        # validar entrada primero antes de proceder
        if not self.validate_input():
            return
        
        try:
            # obtener valores ingresados por el usuario
            matrix_data = self.matrix_input.get_values()
            vector_data = self.vector_input.get_values()
            
            # convertir a numpy arrays para procesamiento
            _, _, A = EquationValidator.validate_matrix(matrix_data)
            _, _, b = EquationValidator.validate_vector(vector_data)
            
            # intentar optimizacion automatica (sin mostrar mensaje si ya es dominante)
            dominance_result = EquationValidator.make_diagonally_dominant(A, b)
            
            if dominance_result['success'] and len(dominance_result['swaps_made']) > 0:
                # solo actualizar si se hicieron cambios
                A = dominance_result['matrix']
                b = dominance_result['vector']
                
                # actualizar la interfaz silenciosamente
                self.matrix_input.set_values(A.tolist())
                self.vector_input.set_values(b.tolist())
                
                # mensaje discreto en el status
                self.update_status(f"sistema optimizado: {dominance_result['message']}")
            elif not dominance_result['success']:
                # solo mostrar advertencia si no se pudo optimizar y no es dominante
                self.update_status("sistema sin dominancia diagonal - convergencia no garantizada", is_warning=True)
            
            # configurar parametros del solver
            try:
                # configurar tolerancia
                self.solver.tolerance = float(self.tolerance_var.get())
                # configurar maximo numero de iteraciones
                self.solver.max_iterations = int(self.max_iter_var.get())
            except ValueError:
                messagebox.showerror("error", "valores de configuracion invalidos")
                return
            
            # iniciar proceso de resolucion
            self.update_status("resolviendo sistema...")
            self.solve_button.configure(text="resolviendo...", state="disabled")
            self.update_idletasks()
            
            # generar pasos detallados del proceso
            steps_data = self.solver.generate_step_by_step(A, b)
            
            # actualizar panel de visualizacion con los resultados
            self.visualization_panel.update_visualization(steps_data)
            
            # cambiar a la pestana de solucion para mostrar resultados
            self.main_notebook.set("proceso de solucion")
            
            # actualizar status basado en el resultado
            result = steps_data[-1]  # ultimo paso contiene el resultado final
            if result['converged']:
                self.update_status("sistema resuelto con exito")
            else:
                self.update_status("sistema resuelto (convergencia no alcanzada)", is_warning=True)
            
        except Exception as e:
            error_msg = f"error al resolver: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("error de resolucion", error_msg)
        
        finally:
            # restaurar estado del boton principal
            self.solve_button.configure(text="resolver sistema", state="normal")
    
    def update_status(self, message: str, is_error: bool = False, is_warning: bool = False):
        """actualiza el mensaje de estado en la barra inferior"""
        # determinar color segun tipo de mensaje
        if is_error:
            color = "red"
        elif is_warning:
            color = "orange"
        else:
            color = ("gray60", "gray40")
        
        # actualizar texto y color del label de status
        self.status_label.configure(text=message, text_color=color)
        # forzar actualizacion inmediata de la interfaz
        self.update_idletasks()
