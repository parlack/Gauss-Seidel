import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import traceback

from .components import (
    ModernButton, PointsTableInput, EvaluationPanel, VisualizationPanel
)
from solver.lagrange import LagrangeSolver
from utils.validators import DataValidator


class LagrangeApp(ctk.CTk):
    """
    Aplicación principal para interpolación de Lagrange
    
    Interfaz gráfica principal que integra todos los componentes
    para realizar interpolación polinómica usando el método de Lagrange
    con visualización paso a paso
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Predictor de Crecimiento de Plantas - Método de Lagrange")
        self.geometry("1280x720")
        self.minsize(1024, 600)

        # Variables de estado de la aplicación
        self.solver = LagrangeSolver()

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
            text="Predictor de Crecimiento de Plantas",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(side="left", padx=30, pady=25)

        # Subtítulo explicativo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Predice la altura de tu planta en cualquier día usando interpolación de Lagrange",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="left", padx=(0, 30), pady=(45, 5))

        # Información del método
        info_frame = ctk.CTkFrame(header_frame)
        info_frame.pack(side="right", padx=30, pady=20)

        self.method_info_label = ctk.CTkLabel(
            info_frame,
            text="P(x) = Σ y_j × L_j(x)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.method_info_label.pack(padx=15, pady=10)

    def setup_input_tab(self):
        """Configura la pestaña de entrada de datos"""
        input_tab = self.main_notebook.add("Mis Mediciones")

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

        # Frame principal para entrada de datos
        input_main_frame = ctk.CTkFrame(input_tab)
        input_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo para la tabla de puntos
        left_frame = ctk.CTkFrame(input_main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Widget para ingresar tabla de puntos
        self.points_table = PointsTableInput(
            left_frame,
            initial_size=5,
            on_change=self.on_input_change
        )
        self.points_table.pack(fill="both", expand=True)

        # Frame derecho para evaluación
        right_frame = ctk.CTkFrame(input_main_frame)
        right_frame.pack(side="right", fill="both", padx=(5, 10), pady=10)

        # Panel de evaluación
        self.evaluation_panel = EvaluationPanel(
            right_frame,
            on_evaluate=self.evaluate_polynomial
        )
        self.evaluation_panel.pack(fill="x", padx=10, pady=10)

        # Información adicional
        info_frame = ctk.CTkFrame(right_frame)
        info_frame.pack(fill="both", expand=True, padx=10, pady=(10, 10))

        info_title = ctk.CTkLabel(
            info_frame,
            text="Información",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info_title.pack(pady=(15, 10))
        
        info_text = """¿Cómo funciona?

Esta aplicación usa el método de Lagrange para predecir la altura de tu planta en cualquier día, basándose en mediciones reales que hayas tomado.

Cómo usarlo:
1. Mide tu planta varios días (ej: día 0, 7, 14, 21)
2. Anota el día y la altura en cm
3. Ingresa los datos en la tabla (Día, Altura)
4. Escribe el día que quieres predecir
5. ¡Obtén la altura estimada!

Ejemplo práctico:
Si mediste tu tomate los días 0, 7, 14 y 21, puedes predecir su altura el día 10 o el día 25.

Nota: Funciona mejor dentro del rango de días que mediste."""

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=11),
            text_color="gray60",
            justify="left",
            wraplength=280
        )
        info_label.pack(padx=15, pady=(0, 15))

        # Barra de estado para mostrar mensajes al usuario
        self.status_label = ctk.CTkLabel(
            input_tab,
            text="Introduce tus mediciones: Día (número) y Altura en cm",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)

    def setup_solution_tab(self):
        """Configura la pestaña de solución"""
        solution_tab = self.main_notebook.add("Predicción y Análisis")

        # Panel principal de visualización del proceso
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

    def on_input_change(self):
        """Callback cuando cambian los datos de entrada"""
        pass

    def clear_all_inputs(self):
        """Limpia todas las entradas de la interfaz"""
        self.points_table.clear_all()
        self.evaluation_panel.clear()
        self.visualization_panel.clear()
        self.update_status("Todas las entradas han sido limpiadas")

    def load_example(self):
        """Carga un ejemplo predefinido"""
        examples = [
            {
                'name': 'Tomate Cherry',
                'points': [(0, 5), (7, 12), (14, 22), (21, 35), (28, 48)],
                'description': 'Crecimiento de planta de tomate durante 4 semanas (días vs cm)'
            },
            {
                'name': 'Girasol',
                'points': [(0, 8), (5, 18), (10, 35), (15, 58), (20, 85), (25, 115)],
                'description': 'Crecimiento rápido de girasol (días vs cm)'
            },
            {
                'name': 'Suculenta',
                'points': [(0, 3), (30, 4.5), (60, 6), (90, 7.2)],
                'description': 'Crecimiento lento de suculenta (días vs cm)'
            },
            {
                'name': 'Frijol',
                'points': [(0, 0), (3, 5), (6, 15), (9, 28), (12, 42)],
                'description': 'Germinación y crecimiento de frijol (días vs cm)'
            }
        ]

        # Seleccionar ejemplo aleatoriamente
        import random
        example = random.choice(examples)

        # Cargar valores del ejemplo
        self.points_table.set_values(example['points'])

        self.update_status(f"Ejemplo cargado: {example['name']} - {example['description']}")

    def validate_input(self):
        """Valida la entrada actual del usuario"""
        try:
            # Obtener valores ingresados por el usuario
            x_values, y_values = self.points_table.get_values()

            # Validar datos
            is_valid, error_msg, x_array, y_array = DataValidator.validate_point_data(x_values, y_values)

            if not is_valid:
                self.update_status(f"Error: {error_msg}", is_error=True)
                messagebox.showerror("Error de Validación", error_msg)
                return False

            # Establecer puntos en el solver
            try:
                self.solver.set_points(x_array.tolist(), y_array.tolist())
            except ValueError as e:
                self.update_status(f"Error: {str(e)}", is_error=True)
                messagebox.showerror("Error de Validación", str(e))
                return False

            # Verificar interpolación
            verification = self.solver.verify_interpolation()

            success_msg = (
                f"Mediciones válidas:\n\n"
                f"Número de mediciones: {len(x_array)}\n"
                f"Período de seguimiento: Día {min(x_array):.0f} al día {max(x_array):.0f}\n"
                f"Altura registrada: {min(y_array):.1f} cm a {max(y_array):.1f} cm\n"
                f"Precisión del modelo: Grado {len(x_array) - 1}\n\n"
                f"¡Listo para hacer predicciones!"
            )

            messagebox.showinfo("Mediciones Validadas", success_msg)
            self.update_status("Mediciones validadas. Ahora puedes predecir la altura en cualquier día")
            return True

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            return False

    def evaluate_polynomial(self):
        """Evalúa el polinomio en un punto específico"""
        # Validar entrada primero
        if not self.validate_input():
            return

        try:
            # Obtener punto de evaluación
            x_str = self.evaluation_panel.get_x_value()

            # Validar punto de evaluación
            is_valid, error_msg, x_eval = DataValidator.validate_evaluation_point(x_str)

            if not is_valid:
                self.update_status(f"Error: {error_msg}", is_error=True)
                messagebox.showerror("Error", error_msg)
                return

            # Verificar si está en rango de interpolación
            x_values, _ = self.points_table.get_values()
            _, _, x_array, _ = DataValidator.validate_point_data(x_values, [0] * len(x_values))

            in_range, range_msg = DataValidator.check_interpolation_range(x_eval, x_array)

            if not in_range:
                result = messagebox.askyesno(
                    "Advertencia - Extrapolación",
                    f"{range_msg}\n\n¿Deseas continuar de todos modos?"
                )
                if not result:
                    return
                self.update_status(range_msg, is_warning=True)

            # Iniciar proceso de evaluación
            self.update_status("Calculando interpolación...")
            self.update_idletasks()

            # Generar pasos detallados del proceso
            steps_data = self.solver.generate_step_by_step(x_eval)

            # Verificar si hubo errores
            if steps_data and steps_data[0].get('type') == 'error':
                error_msg = steps_data[0].get('content', 'Error desconocido')
                self.update_status(f"Error: {error_msg}", is_error=True)
                messagebox.showerror("Error", error_msg)
                return

            # Actualizar panel de visualización con los resultados
            self.visualization_panel.update_visualization(steps_data)

            # Cambiar a la pestaña de solución para mostrar resultados
            self.main_notebook.set("Predicción y Análisis")

            # Obtener resultado final
            result_step = next((step for step in steps_data if step.get('type') == 'result'), None)
            if result_step:
                result_value = result_step.get('result')
                self.update_status(f"Predicción: En el día {x_eval:.1f}, tu planta medirá aproximadamente {result_value:.2f} cm de altura")
            else:
                self.update_status("Proceso completado")

        except Exception as e:
            error_msg = f"Error al evaluar: {str(e)}"
            tb = traceback.format_exc()
            print(f"Error completo:\n{tb}")
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)

    def update_status(self, message: str, is_error: bool = False, is_warning: bool = False):
        """Actualiza el mensaje de estado en la barra inferior"""
        if is_error:
            color = "red"
        elif is_warning:
            color = "orange"
        else:
            color = ("gray60", "gray40")

        self.status_label.configure(text=message, text_color=color)
        self.update_idletasks()





