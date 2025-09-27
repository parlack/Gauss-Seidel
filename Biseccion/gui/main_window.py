import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math

from .components import (
    ModernButton, ModernEntry, FunctionInputPanel,
    IntervalInputPanel, VisualizationPanel
)
from solver.biseccion import BiseccionSolver


class BiseccionApp(ctk.CTk):
    """
    Aplicación principal para resolver ecuaciones con bisección

    Interfaz gráfica principal que integra todos los componentes
    para resolver ecuaciones no lineales usando el método
    de bisección con visualización paso a paso
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Resolver Ecuaciones No Lineales - Método de Bisección")
        self.geometry("1280x720")
        self.minsize(1024, 500)

        # Variables de estado de la aplicación
        self.solver = BiseccionSolver()  # Instancia del solver

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

        # Crear header con título y información
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
            text="Método de bisección con visualización paso a paso",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="left", padx=(0, 30), pady=(45, 5))

        # Información del método
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="right", padx=30, pady=20)

        # Etiqueta que muestra información del método
        self.method_info_label = ctk.CTkLabel(
            info_frame,
            text="f(x) = 0",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.method_info_label.pack(padx=15, pady=10)

    def setup_input_tab(self):
        """Configura la pestaña de entrada de datos"""
        input_tab = self.main_notebook.add("Entrada de Datos")

        # Frame de controles superiores
        controls_frame = ctk.CTkFrame(input_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)

        # Botones de control
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)

        # Botón para limpiar todo
        ModernButton(
            buttons_frame,
            text="Limpiar Todo",
            command=self.clear_all_inputs,
            fg_color="gray50",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón para cargar ejemplo
        ModernButton(
            buttons_frame,
            text="Ejemplo",
            command=self.load_example,
            fg_color="orange",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón para validar entrada
        ModernButton(
            buttons_frame,
            text="Validar",
            command=self.validate_input,
            fg_color="green",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón principal de resolver
        self.solve_button = ModernButton(
            buttons_frame,
            text="Resolver Ecuación",
            command=self.solve_equation,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f538d"
        )
        self.solve_button.pack(fill="x", padx=10, pady=(10, 15), side="bottom")

        # Frame principal para entrada de datos
        input_main_frame = ctk.CTkFrame(input_tab)
        input_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo para la función
        left_frame = ctk.CTkFrame(input_main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Widget para ingresar función
        self.function_input = FunctionInputPanel(
            left_frame,
            on_change=self.on_input_change
        )
        self.function_input.pack(fill="both", expand=True)

        # Frame derecho para configuración con scroll
        right_frame = ctk.CTkFrame(input_main_frame)
        right_frame.pack(side="right", fill="both", padx=(5, 10), pady=10)

        # Contenedor con scroll para las configuraciones
        config_container = ctk.CTkScrollableFrame(right_frame, width=300, height=400)
        config_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel para intervalo inicial
        self.interval_input = IntervalInputPanel(
            config_container,
            on_change=self.on_input_change
        )
        self.interval_input.pack(fill="x", padx=10, pady=(0, 10))

        # Configuración del solver
        solver_config_frame = ctk.CTkFrame(config_container)
        solver_config_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Título de configuración
        config_title = ctk.CTkLabel(
            solver_config_frame,
            text="Configuración del Solver",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        config_title.pack(pady=(15, 20))

        # Configuración de tolerancia
        tol_frame = ctk.CTkFrame(solver_config_frame)
        tol_frame.pack(fill="x", padx=15, pady=10)

        # Etiqueta para tolerancia
        ctk.CTkLabel(
            tol_frame,
            text="Tolerancia (%):",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))

        # Campo para ingresar tolerancia
        self.tolerance_var = tk.StringVar(value="0.000001")
        self.tolerance_entry = ModernEntry(
            tol_frame,
            textvariable=self.tolerance_var,
            width=160,
            placeholder="0.000001"
        )
        self.tolerance_entry.pack(pady=(0, 10))

        # Configuración de máximo de iteraciones
        max_iter_frame = ctk.CTkFrame(solver_config_frame)
        max_iter_frame.pack(fill="x", padx=15, pady=10)

        # Etiqueta para máximo de iteraciones
        ctk.CTkLabel(
            max_iter_frame,
            text="Máx. Iteraciones:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))

        # Campo para ingresar máximo de iteraciones
        self.max_iter_var = tk.StringVar(value="100")
        self.max_iter_entry = ModernEntry(
            max_iter_frame,
            textvariable=self.max_iter_var,
            width=160,
            placeholder="100"
        )
        self.max_iter_entry.pack(pady=(0, 10))

        # Barra de estado para mostrar mensajes al usuario
        self.status_label = ctk.CTkLabel(
            input_tab,
            text="Introduce la función f(x) y el intervalo [xl, xu]",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)

    def setup_solution_tab(self):
        """Configura la pestaña de solución"""
        solution_tab = self.main_notebook.add("Proceso de Solución")

        # Panel principal de visualización del proceso
        self.visualization_panel = VisualizationPanel(solution_tab)
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
        # Aquí se podría implementar validación en tiempo real
        # Por ahora solo es un placeholder para futuras funcionalidades
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

    def load_example(self):
        """Carga un ejemplo predefinido"""
        examples = [
            {
                'name': 'Polinomio Cúbico',
                'function': 'x**3 - 2*x - 5',
                'xl': 1,
                'xu': 3,
                'description': 'Ecuación cúbica simple'
            },
            {
                'name': 'Exponencial',
                'function': 'exp(-x) - x',
                'xl': 0,
                'xu': 1,
                'description': 'Función exponencial vs lineal'
            },
            {
                'name': 'Trigonométrica',
                'function': 'cos(x) - x',
                'xl': 0,
                'xu': 1,
                'description': 'Coseno vs función lineal'
            }
        ]

        # Seleccionar ejemplo aleatoriamente o permitir al usuario elegir
        import random
        example = random.choice(examples)

        # Cargar valores del ejemplo
        self.function_input.set_function(example['function'])
        self.interval_input.set_values(example['xl'], example['xu'])

        self.update_status(f"Ejemplo cargado: {example['name']} - {example['description']}")

    def validate_input(self):
        """Valida la entrada actual del usuario"""
        try:
            # Obtener valores ingresados por el usuario
            function_expr = self.function_input.get_function()
            xl, xu = self.interval_input.get_values()

            # Validar que la función no esté vacía
            if not function_expr.strip():
                self.update_status("Error: La función no puede estar vacía", is_error=True)
                messagebox.showerror("Error de Validación", "Debe ingresar una función f(x)")
                return False

            # Validar intervalo
            if xl >= xu:
                self.update_status("Error: xl debe ser menor que xu", is_error=True)
                messagebox.showerror("Error de Validación", "El límite inferior debe ser menor que el superior")
                return False

            # Validar función e intervalo usando el solver
            validation = self.solver.validate_function_and_interval(
                self.solver.create_function_from_expression(function_expr), xl, xu
            )

            if not validation['valid']:
                self.update_status(f"Error: {validation['message']}", is_error=True)
                messagebox.showerror("Error de Validación", validation['message'])
                return False

            # Mostrar información de validación exitosa
            f_xl = validation['f_xl']
            f_xu = validation['f_xu']
            
            success_msg = (
                f"Validación exitosa:\n\n"
                f"f({xl}) = {f_xl:.6f}\n"
                f"f({xu}) = {f_xu:.6f}\n"
                f"f(xl) × f(xu) = {f_xl * f_xu:.6f} < 0 ✓\n\n"
                f"Se garantiza la existencia de al menos una raíz en [{xl}, {xu}]"
            )

            messagebox.showinfo("Validación Exitosa", success_msg)
            self.update_status("Validación exitosa. Función y intervalo listos para resolver")
            return True

        except ValueError as e:
            error_msg = str(e)
            self.update_status(f"Error: {error_msg}", is_error=True)
            messagebox.showerror("Error de Validación", f"Error en la función:\n\n{error_msg}\n\nVerifica que la función esté correctamente escrita.")
            return False
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            return False

    def solve_equation(self):
        """Resuelve la ecuación usando bisección"""
        # Validar entrada primero antes de proceder
        if not self.validate_input():
            return

        try:
            # Obtener valores ingresados por el usuario
            function_expr = self.function_input.get_function()
            xl, xu = self.interval_input.get_values()

            # Configurar parámetros del solver
            try:
                # Configurar tolerancia
                self.solver.tolerance = float(self.tolerance_var.get())
                # Configurar máximo número de iteraciones
                self.solver.max_iterations = int(self.max_iter_var.get())
            except ValueError:
                messagebox.showerror("Error", "Valores de configuración inválidos")
                return

            # Iniciar proceso de resolución
            self.update_status("Resolviendo ecuación...")
            self.solve_button.configure(text="Resolviendo...", state="disabled")
            self.update_idletasks()

            # Generar pasos detallados del proceso
            steps_data = self.solver.generate_step_by_step(function_expr, xl, xu)

            # Verificar si hubo errores en el proceso
            if steps_data and steps_data[0].get('type') == 'error':
                error_msg = steps_data[0].get('content', 'Error desconocido')
                self.update_status(f"Error: {error_msg}", is_error=True)
                messagebox.showerror("Error en el Proceso", error_msg)
                return

            # Actualizar panel de visualización con los resultados
            self.visualization_panel.update_visualization(steps_data)

            # Cambiar a la pestaña de solución para mostrar resultados
            self.main_notebook.set("Proceso de Solución")

            # Actualizar status basado en el resultado
            result_step = next((step for step in steps_data if step.get('type') == 'result'), None)
            if result_step:
                if result_step.get('converged'):
                    root = result_step.get('solution')
                    iterations = result_step.get('iterations')
                    self.update_status(f"Ecuación resuelta: raíz ≈ {root:.6f} en {iterations} iteraciones")
                else:
                    self.update_status("Proceso completado (convergencia no alcanzada)", is_warning=True)
            else:
                self.update_status("Proceso completado")

        except ValueError as e:
            error_msg = str(e)
            self.update_status(f"Error: {error_msg}", is_error=True)
            messagebox.showerror("Error de Resolución", f"Error en la evaluación de la función:\n\n{error_msg}\n\nVerifica que:\n• La función esté bien escrita\n• No haya divisiones por cero\n• No haya logaritmos de números negativos\n• El intervalo sea apropiado")
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error de Resolución", error_msg)

        finally:
            # Restaurar estado del botón principal
            self.solve_button.configure(text="Resolver Ecuación", state="normal")

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
