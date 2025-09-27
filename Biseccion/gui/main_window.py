import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from .components import (
    ModernButton, ModernEntry, FunctionInputPanel,
    IntervalInputPanel, BiseccionVisualizationPanel
)
from solver.biseccion import BiseccionSolver
from utils.validators import FunctionValidator


class BiseccionApp(ctk.CTk):
    """
    Aplicación principal para resolver ecuaciones no lineales con bisección
    
    Interfaz gráfica principal que integra todos los componentes
    para resolver ecuaciones no lineales usando el método numérico
    de bisección con visualización paso a paso
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Resolver Ecuaciones No Lineales - Método de Bisección")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        # Variables de estado de la aplicación
        self.solver = BiseccionSolver()  # instancia del solver
        
        # Configurar tema visual
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configurar interfaz de usuario
        self.setup_ui()
        # Centrar ventana en pantalla
        self.center_window()

    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        
        # Frame principal que contiene todo
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True)

        # Crear header con título e información
        self.create_header(main_frame)

        # Frame de contenido principal
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear notebook principal con pestañas
        self.main_notebook = ctk.CTkTabview(content_frame)
        self.main_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar pestañas principales
        self.setup_input_tab()
        self.setup_solution_tab()

    def create_header(self, parent):
        """Crea el header de la aplicación con título e información"""
        header_frame = ctk.CTkFrame(parent, height=100, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Título principal de la aplicación
        title_label = ctk.CTkLabel(
            header_frame,
            text="Resolver Ecuaciones No Lineales",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(side="left", padx=30, pady=25)

        # Subtítulo explicativo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Método numérico de bisección con visualización paso a paso",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="left", padx=(0, 30), pady=(45, 5))

        # Información del método
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="right", padx=30, pady=20)

        # Etiqueta que muestra información del método
        method_info_label = ctk.CTkLabel(
            info_frame,
            text="Método: Bisección",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        method_info_label.pack(padx=15, pady=10)

    def setup_input_tab(self):
        """Configura la pestaña de entrada de datos"""
        input_tab = self.main_notebook.add("Entrada de Datos")

        # Frame de controles superiores
        controls_frame = ctk.CTkFrame(input_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)

        # Botones de control
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="left", padx=10, pady=10)

        # Botón para limpiar todo
        ModernButton(
            buttons_frame,
            text="🗑 Limpiar Todo",
            command=self.clear_all_inputs,
            fg_color="gray50",
            width=130
        ).pack(side="left", padx=5, pady=5)

        # Botón para cargar ejemplo
        ModernButton(
            buttons_frame,
            text="📋 Ejemplo",
            command=self.load_example,
            fg_color="orange",
            width=130
        ).pack(side="left", padx=5, pady=5)

        # Botón para validar entrada
        ModernButton(
            buttons_frame,
            text="✅ Validar",
            command=self.validate_input,
            fg_color="green",
            width=130
        ).pack(side="left", padx=5, pady=5)

        # BOTÓN PRINCIPAL DE RESOLVER - Movido aquí para mejor visibilidad
        self.solve_button = ModernButton(
            buttons_frame,
            text="🚀 Resolver Ecuación",
            command=self.solve_equation,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f538d",
            width=180
        )
        self.solve_button.pack(side="left", padx=10, pady=5)

        # Configuración del solver
        config_frame = ctk.CTkFrame(controls_frame)
        config_frame.pack(side="right", padx=10, pady=10)

        # Frame para tolerancia
        tol_frame = ctk.CTkFrame(config_frame)
        tol_frame.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            tol_frame,
            text="Tolerancia:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(8, 2), pady=5)

        self.tolerance_var = tk.StringVar(value="0.000001")
        self.tolerance_entry = ModernEntry(
            tol_frame,
            textvariable=self.tolerance_var,
            width=100,
            placeholder="0.000001"
        )
        self.tolerance_entry.pack(side="left", padx=(2, 8), pady=5)

        # Frame para máximo de iteraciones
        max_iter_frame = ctk.CTkFrame(config_frame)
        max_iter_frame.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(
            max_iter_frame,
            text="Max. Iter:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=(8, 2), pady=5)

        self.max_iter_var = tk.StringVar(value="100")
        self.max_iter_entry = ModernEntry(
            max_iter_frame,
            textvariable=self.max_iter_var,
            width=80,
            placeholder="100"
        )
        self.max_iter_entry.pack(side="left", padx=(2, 8), pady=5)

        # Frame principal scrollable para función e intervalo
        input_main_scroll = ctk.CTkScrollableFrame(input_tab)
        input_main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame contenedor dentro del scroll
        input_main_frame = ctk.CTkFrame(input_main_scroll)
        input_main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame izquierdo para la función
        left_frame = ctk.CTkFrame(input_main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Widget para ingresar función matemática
        self.function_input = FunctionInputPanel(
            left_frame,
            on_change=self.on_input_change
        )
        self.function_input.pack(fill="both", expand=True)

        # Frame derecho para intervalo y gráfica
        right_frame = ctk.CTkFrame(input_main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Contenedor superior: intervalo
        interval_container = ctk.CTkFrame(right_frame)
        interval_container.pack(fill="x", padx=10, pady=10)

        # Widget para ingresar intervalo
        self.interval_input = IntervalInputPanel(
            interval_container,
            on_change=self.on_input_change
        )
        self.interval_input.pack(fill="both", expand=True)

        # Frame para vista previa (tamaño fijo para no ocultar otros elementos)
        graph_frame = ctk.CTkFrame(right_frame, height=120)
        graph_frame.pack(fill="x", padx=10, pady=(10, 10))
        graph_frame.pack_propagate(False)  # Mantener altura fija

        graph_title = ctk.CTkLabel(
            graph_frame,
            text="📈 Vista Previa de la Función",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        graph_title.pack(pady=(8, 5))

        # Placeholder para gráfica
        self.graph_placeholder = ctk.CTkLabel(
            graph_frame,
            text="La gráfica aparecerá aquí cuando\ningreses una función válida",
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        )
        self.graph_placeholder.pack(pady=(0, 8))

        # Barra de estado
        self.status_label = ctk.CTkLabel(
            input_tab,
            text="Introduce una función matemática y el intervalo de búsqueda",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)

    def setup_solution_tab(self):
        """Configura la pestaña de solución"""
        solution_tab = self.main_notebook.add("Proceso de Solución")

        # Panel principal de visualización del proceso
        self.visualization_panel = BiseccionVisualizationPanel(solution_tab)
        self.visualization_panel.pack(fill="both", expand=True, padx=10, pady=10)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        # Actualizar geometría para obtener tamaño real
        self.update_idletasks()
        # Obtener dimensiones de la ventana
        width = self.winfo_width()
        height = self.winfo_height()
        # Calcular posición central
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        # Aplicar geometría centrada
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_input_change(self):
        """Callback cuando cambian los datos de entrada"""
        # Actualizar vista previa si es posible
        self.update_function_preview()

    def update_function_preview(self):
        """Actualiza la vista previa de la función"""
        try:
            func_str = self.function_input.get_function()
            if not func_str:
                return

            # Validar función
            is_valid, _ = FunctionValidator.validate_function_syntax(func_str)
            if not is_valid:
                return

            # Obtener intervalo si está disponible
            a, b = self.interval_input.get_interval()
            if a is None or b is None:
                a, b = -5, 5  # intervalo por defecto

            # Crear gráfica simple (esto se podría mejorar con matplotlib)
            self.graph_placeholder.configure(
                text=f"Función: f(x) = {func_str}\nIntervalo: [{a}, {b}]"
            )

        except Exception:
            # Si hay error, no actualizar
            pass

    def clear_all_inputs(self):
        """Limpia todas las entradas de la interfaz"""
        # Limpiar función
        self.function_input.clear()
        # Limpiar intervalo
        self.interval_input.clear()
        # Limpiar panel de visualización
        self.visualization_panel.clear()
        # Actualizar mensaje de estado
        self.update_status("Todas las entradas han sido limpiadas")
        # Resetear vista previa
        self.graph_placeholder.configure(
            text="La gráfica aparecerá aquí cuando\ningreses una función válida"
        )

    def load_example(self):
        """Carga un ejemplo predefinido"""
        # Obtener ejemplos disponibles
        examples = FunctionValidator.get_function_examples()
        
        # Mostrar dialog para seleccionar ejemplo
        example_names = [f"{func} ({desc})" for func, desc, _ in examples]
        
        # Usar messagebox simple para selección (se podría mejorar con un dialog personalizado)
        choice = messagebox.askyesno(
            "Cargar Ejemplo",
            "¿Quieres cargar un ejemplo de función cuadrática?\n\n"
            "Función: x**2 - 4\n"
            "Intervalo: [1, 3]\n"
            "Raíces esperadas en x = ±2"
        )
        
        if choice:
            # Cargar ejemplo de función cuadrática
            self.function_input.set_function("x**2 - 4")
            self.interval_input.set_interval(1, 3)
            self.update_status("Ejemplo cargado: función cuadrática con raíz en x = 2")
            self.update_function_preview()

    def validate_input(self):
        """Valida la entrada actual del usuario"""
        try:
            # Obtener función del usuario
            func_str = self.function_input.get_function()
            if not func_str:
                self.update_status("Error: La función no puede estar vacía", is_error=True)
                messagebox.showerror("Error de validación", "Debes ingresar una función matemática")
                return False

            # Validar sintaxis de la función
            is_valid, message = FunctionValidator.validate_function_syntax(func_str)
            if not is_valid:
                self.update_status(f"Error en función: {message}", is_error=True)
                messagebox.showerror("Error de validación", f"Función inválida: {message}")
                return False

            # Obtener intervalo
            a, b = self.interval_input.get_interval()
            if a is None or b is None:
                self.update_status("Error: Debes ingresar un intervalo válido", is_error=True)
                messagebox.showerror("Error de validación", "Debes ingresar valores numéricos para el intervalo")
                return False

            # Validar intervalo para bisección
            is_valid, message, fa, fb = FunctionValidator.validate_bisection_interval(func_str, a, b)
            if not is_valid:
                self.update_status("Error en intervalo: No hay cambio de signo", is_error=True)
                messagebox.showerror("Error de validación", message)
                
                # Sugerir intervalos alternativos
                suggestions = FunctionValidator.suggest_interval_for_function(func_str)
                if suggestions:
                    suggestion_text = "Intervalos sugeridos donde f(x) cambia de signo:\n\n"
                    for i, (sugg_a, sugg_b) in enumerate(suggestions[:3], 1):
                        suggestion_text += f"{i}. [{sugg_a:.3f}, {sugg_b:.3f}]\n"
                    
                    use_suggestion = messagebox.askyesno(
                        "Sugerencias de Intervalos",
                        f"{suggestion_text}\n¿Quieres usar la primera sugerencia?"
                    )
                    
                    if use_suggestion and suggestions:
                        sugg_a, sugg_b = suggestions[0]
                        self.interval_input.set_interval(sugg_a, sugg_b)
                        self.update_status(f"Usando intervalo sugerido: [{sugg_a:.3f}, {sugg_b:.3f}]")
                        return True
                
                return False

            # Todo válido
            self.update_status(f"Validación exitosa. f({a}) = {fa:.6f}, f({b}) = {fb:.6f}")
            return True

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            return False

    def solve_equation(self):
        """Resuelve la ecuación usando bisección"""
        # Validar entrada primero
        if not self.validate_input():
            return

        try:
            # Obtener función e intervalo
            func_str = self.function_input.get_function()
            a, b = self.interval_input.get_interval()

            # Configurar parámetros del solver
            try:
                self.solver.tolerance = float(self.tolerance_var.get())
                self.solver.max_iterations = int(self.max_iter_var.get())
            except ValueError:
                messagebox.showerror("Error", "Valores de configuración inválidos")
                return

            # Iniciar proceso de resolución
            self.update_status("Resolviendo ecuación...")
            self.solve_button.configure(text="Resolviendo...", state="disabled")
            self.update_idletasks()

            # Generar pasos detallados del proceso
            steps_data = self.solver.generate_step_by_step(func_str, a, b)

            # Verificar si hubo errores en el proceso
            if steps_data and steps_data[0].get('type') == 'error':
                error_msg = steps_data[0]['content']
                self.update_status(f"Error: {error_msg}", is_error=True)
                messagebox.showerror("Error de resolución", error_msg)
                return

            # Actualizar panel de visualización con los resultados
            self.visualization_panel.update_visualization(steps_data)

            # Cambiar a la pestaña de solución para mostrar resultados
            self.main_notebook.set("Proceso de Solución")

            # Actualizar status basado en el resultado
            result = steps_data[-1]  # último paso contiene el resultado final
            if result.get('converged', False):
                root = result.get('root', 0)
                iterations = result.get('iterations', 0)
                self.update_status(f"¡Raíz encontrada! x = {root:.8f} en {iterations} iteraciones")
            else:
                self.update_status("Máximo de iteraciones alcanzado - Solución aproximada obtenida", is_warning=True)

        except Exception as e:
            error_msg = f"Error al resolver: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error de resolución", error_msg)

        finally:
            # Restaurar estado del botón principal
            self.solve_button.configure(text="🚀 Resolver Ecuación", state="normal")

    def update_status(self, message: str, is_error: bool = False, is_warning: bool = False):
        """Actualiza el mensaje de estado en la barra inferior"""
        # Determinar color según tipo de mensaje
        if is_error:
            color = "red"
        elif is_warning:
            color = "orange"  
        else:
            color = ("gray60", "gray40")

        # Actualizar texto y color del label de status
        self.status_label.configure(text=message, text_color=color)
        # Forzar actualización inmediata de la interfaz
        self.update_idletasks()
