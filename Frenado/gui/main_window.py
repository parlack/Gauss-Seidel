# Andres Monsivais Salazar
# Luis Andres Salinas Lozano

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from .components import (
    ModernButton, DatosExperimentalesPanel, InterpolacionPanel,
    BiseccionPanel, VisualizationPanel
)
from solver.lagrange import LagrangeSolver
from solver.biseccion import BiseccionSolver
from utils.validators import FrenadoValidator


class FrenadoApp(ctk.CTk):
    """
    Aplicación principal para análisis de distancias de frenado
    
    Integra dos métodos numéricos:
    1. Interpolación de Lagrange: Predecir distancia de frenado a cualquier velocidad
    2. Bisección: Encontrar velocidad máxima segura dado un límite de distancia
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Análisis de Distancias de Frenado - Métodos Numéricos")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Solvers para ambos métodos
        self.lagrange_solver = LagrangeSolver()
        self.biseccion_solver = BiseccionSolver()

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
        self.setup_data_tab()
        self.setup_interpolation_tab()
        self.setup_biseccion_tab()
        self.setup_visualization_tab()

    def create_header(self, parent):
        """Crea el header de la aplicación con título e información"""
        header_frame = ctk.CTkFrame(parent, height=110, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Título principal de la aplicación
        title_label = ctk.CTkLabel(
            header_frame,
            text="Análisis de Distancias de Frenado",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("gray10", "gray90")
        )
        title_label.pack(side="top", padx=30, pady=(20, 5))

        # Subtítulo explicativo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Predicción y optimización de seguridad vial usando Interpolación de Lagrange y Bisección",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray50")
        )
        subtitle_label.pack(side="top", padx=30, pady=(0, 15))

    def setup_data_tab(self):
        """Configura la pestaña de entrada de datos experimentales"""
        data_tab = self.main_notebook.add("Datos Experimentales")

        # Frame de controles superiores
        controls_frame = ctk.CTkFrame(data_tab)
        controls_frame.pack(fill="x", padx=10, pady=10)

        # Título explicativo
        title_frame = ctk.CTkFrame(controls_frame)
        title_frame.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(
            title_frame,
            text="Ingresa mediciones reales de velocidad vs distancia de frenado",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(padx=10, pady=10)

        # Botones de control
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=10, pady=10)

        # Botón para limpiar todo
        ModernButton(
            buttons_frame,
            text="Limpiar",
            command=self.clear_all_data,
            fg_color="gray50",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón para cargar ejemplo 1
        ModernButton(
            buttons_frame,
            text="Ejemplo 1",
            command=self.load_example_data_1,
            fg_color="orange",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón para cargar ejemplo 2
        ModernButton(
            buttons_frame,
            text="Ejemplo 2",
            command=self.load_example_data_2,
            fg_color="orange",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Botón para validar entrada
        ModernButton(
            buttons_frame,
            text="Validar",
            command=self.validate_data,
            fg_color="green",
            width=120
        ).pack(side="left", padx=5, pady=5)

        # Frame principal para entrada de datos
        input_main_frame = ctk.CTkFrame(data_tab)
        input_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel de datos experimentales (ocupa todo el ancho)
        self.datos_panel = DatosExperimentalesPanel(
            input_main_frame,
            initial_size=5,
            on_change=self.on_data_change
        )
        self.datos_panel.pack(fill="both", expand=True, padx=10, pady=10)

        # Barra de estado
        self.status_label = ctk.CTkLabel(
            data_tab,
            text="Ingresa los datos experimentales de velocidad y distancia de frenado",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="bottom", pady=5)

    def setup_interpolation_tab(self):
        """Configura la pestaña de interpolación (Lagrange)"""
        interp_tab = self.main_notebook.add("Interpolacion (Lagrange)")

        # Título explicativo
        title_frame = ctk.CTkFrame(interp_tab)
        title_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            title_frame,
            text="Metodo de Interpolacion de Lagrange",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        ).pack(pady=10)

        desc_text = ("Este método usa los datos experimentales para construir un polinomio interpolador "
                    "que permite predecir la distancia de frenado a cualquier velocidad dentro del rango medido.")

        ctk.CTkLabel(
            title_frame,
            text=desc_text,
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=900,
            justify="left"
        ).pack(pady=(0, 10), padx=30)

        # Panel de interpolación
        self.interpolacion_panel = InterpolacionPanel(
            interp_tab,
            on_evaluate=self.evaluate_interpolation
        )
        self.interpolacion_panel.pack(fill="x", padx=100, pady=30)


    def setup_biseccion_tab(self):
        """Configura la pestaña de bisección"""
        bisec_tab = self.main_notebook.add("Biseccion (Velocidad Segura)")

        # Título explicativo
        title_frame = ctk.CTkFrame(bisec_tab)
        title_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            title_frame,
            text="Metodo de Biseccion",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("darkorange", "orange")
        ).pack(pady=10)

        desc_text = ("Este método encuentra la velocidad máxima segura a la que un vehículo puede circular "
                    "para poder detenerse dentro de una distancia límite específica.")

        ctk.CTkLabel(
            title_frame,
            text=desc_text,
            font=ctk.CTkFont(size=12),
            text_color="gray60",
            wraplength=900,
            justify="left"
        ).pack(pady=(0, 10), padx=30)

        # Panel de bisección
        self.biseccion_panel = BiseccionPanel(
            bisec_tab,
            on_solve=self.solve_biseccion
        )
        self.biseccion_panel.pack(fill="both", expand=True, padx=20, pady=20)

        
    def setup_visualization_tab(self):
        """Configura la pestaña de visualización"""
        viz_tab = self.main_notebook.add("Visualizacion Paso a Paso")

        # Panel de visualización
        self.visualization_panel = VisualizationPanel(viz_tab)
        self.visualization_panel.pack(fill="both", expand=True, padx=10, pady=10)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_data_change(self):
        """Callback cuando cambian los datos de entrada"""
        pass

    def clear_all_data(self):
        """Limpia todos los datos ingresados"""
        self.datos_panel.clear_all()
        self.interpolacion_panel.clear()
        self.biseccion_panel.clear()
        self.visualization_panel.clear()
        self.update_status("Datos limpiados")

    def load_example_data_1(self):
        """Carga datos de ejemplo 1: Pavimento seco"""
        # Datos experimentales típicos de frenado en pavimento seco
        datos_ejemplo = [
            (20, 6.0),    # 20 km/h -> 6 metros
            (40, 16.0),   # 40 km/h -> 16 metros
            (60, 32.0),   # 60 km/h -> 32 metros
            (80, 52.0),   # 80 km/h -> 52 metros
            (100, 78.0),  # 100 km/h -> 78 metros
            (120, 110.0), # 120 km/h -> 110 metros
        ]

        self.datos_panel.set_values(datos_ejemplo)
        self.interpolacion_panel.set_velocity(75)
        self.biseccion_panel.set_values(50, 20, 150, 0.01)
        self.update_status("Ejemplo 1 cargado: Pavimento seco - Velocidad: 75 km/h, Distancia limite: 50m, Tolerancia: 0.01 km/h")

    def load_example_data_2(self):
        """Carga datos de ejemplo 2: Pavimento mojado"""
        # Datos experimentales de frenado en pavimento mojado (distancias mayores)
        datos_ejemplo = [
            (20, 9.0),    # 20 km/h -> 9 metros
            (40, 24.0),   # 40 km/h -> 24 metros
            (60, 48.0),   # 60 km/h -> 48 metros
            (80, 78.0),   # 80 km/h -> 78 metros
            (100, 117.0), # 100 km/h -> 117 metros
        ]

        self.datos_panel.set_values(datos_ejemplo)
        self.interpolacion_panel.set_velocity(70)
        self.biseccion_panel.set_values(60, 20, 120, 0.01)
        self.update_status("Ejemplo 2 cargado: Pavimento mojado - Velocidad: 70 km/h, Distancia limite: 60m, Tolerancia: 0.01 km/h")

    def validate_data(self):
        """Valida los datos experimentales ingresados"""
        try:
            # Obtener valores de la tabla
            velocidades, distancias = self.datos_panel.get_values()

            # Validar usando el validador
            is_valid, message, vel_array, dist_array = FrenadoValidator.validate_point_data(
                velocidades, distancias
            )

            if not is_valid:
                self.update_status(f"Error: {message}", is_error=True)
                messagebox.showerror("Error de Validación", message)
                return False

            # Configurar puntos en el solver de Lagrange
            self.lagrange_solver.set_points(vel_array.tolist(), dist_array.tolist())

            # Verificar interpolación
            verification = self.lagrange_solver.verify_interpolation()

            self.update_status("Datos validos y listos para usar")
            messagebox.showinfo(
                "Validacion Exitosa",
                f"Datos experimentales validos:\n\n"
                f"- {len(vel_array)} mediciones\n"
                f"- Rango de velocidad: {vel_array.min():.1f} - {vel_array.max():.1f} km/h\n"
                f"- Rango de distancia: {dist_array.min():.1f} - {dist_array.max():.1f} m\n\n"
                f"El polinomio interpolador esta listo para usar."
            )
            return True

        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            return False

    def evaluate_interpolation(self):
        """Evalúa el polinomio interpolador en una velocidad específica"""
        # Primero validar que hay datos
        if not self.lagrange_solver.points:
            messagebox.showerror(
                "Error",
                "Primero debes ingresar y validar los datos experimentales en la pestana 'Datos Experimentales'"
            )
            self.main_notebook.set("Datos Experimentales")
            return

        # Obtener velocidad ingresada
        v_str = self.interpolacion_panel.get_velocity()

        # Validar velocidad
        is_valid, message, v_val = FrenadoValidator.validate_velocity(v_str)
        if not is_valid:
            messagebox.showerror("Error", message)
            return

        # Verificar rango de interpolación
        velocidades = [p[0] for p in self.lagrange_solver.points]
        import numpy as np
        in_range, range_msg = FrenadoValidator.check_interpolation_range(
            v_val, np.array(velocidades)
        )

        if not in_range:
            result = messagebox.askyesno(
                "Advertencia - Extrapolación",
                f"{range_msg}\n\n¿Deseas continuar de todos modos?"
            )
            if not result:
                return

        try:
            # Generar pasos detallados
            self.update_status("Generando interpolación paso a paso...")
            steps = self.lagrange_solver.generate_step_by_step(v_val)

            # Actualizar visualización
            self.visualization_panel.update_visualization(steps)

            # Cambiar a pestaña de visualización
            self.main_notebook.set("Visualizacion Paso a Paso")

            # Obtener resultado
            result_step = [s for s in steps if s['type'] == 'result'][0]
            distancia = result_step['result']

            self.update_status(
                f"A {v_val:.1f} km/h, la distancia de frenado es aproximadamente {distancia:.2f} metros"
            )

        except Exception as e:
            error_msg = f"Error al interpolar: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)

    def solve_biseccion(self):
        """Resuelve el problema de bisección para encontrar velocidad segura"""
        # Primero validar que hay datos
        if not self.lagrange_solver.points:
            messagebox.showerror(
                "Error",
                "Primero debes ingresar y validar los datos experimentales en la pestana 'Datos Experimentales'"
            )
            self.main_notebook.set("Datos Experimentales")
            return

        # Obtener valores ingresados
        dist_str, a_str, b_str, tol_str = self.biseccion_panel.get_values()

        # Validar distancia límite
        is_valid, message, dist_limit = FrenadoValidator.validate_distance(dist_str)
        if not is_valid:
            messagebox.showerror("Error en distancia límite", message)
            return

        # Validar intervalo
        is_valid, message, a_val, b_val = FrenadoValidator.validate_interval(a_str, b_str)
        if not is_valid:
            messagebox.showerror("Error en intervalo", message)
            return
        
        # Validar tolerancia
        try:
            tol_val = float(tol_str)
            if tol_val <= 0:
                messagebox.showerror("Error en tolerancia", "La tolerancia debe ser mayor que cero")
                return
            if tol_val > 10:
                messagebox.showerror("Error en tolerancia", "La tolerancia debe ser menor a 10 km/h")
                return
        except (ValueError, TypeError):
            messagebox.showerror("Error en tolerancia", f"'{tol_str}' no es un numero valido")
            return

        # Verificar que el intervalo esté dentro del rango de datos
        velocidades = [p[0] for p in self.lagrange_solver.points]
        v_min, v_max = min(velocidades), max(velocidades)

        if a_val < v_min or b_val > v_max:
            result = messagebox.askyesno(
                "Advertencia",
                f"El intervalo de búsqueda [{a_val:.1f}, {b_val:.1f}] km/h está parcialmente fuera "
                f"del rango experimental [{v_min:.1f}, {v_max:.1f}] km/h.\n\n"
                f"Esto puede causar extrapolación imprecisa.\n\n¿Deseas continuar?"
            )
            if not result:
                return

        try:
            # Configurar tolerancia en el solver de bisección
            self.biseccion_solver.tolerance = tol_val
            
            # Definir función: f(v) = distancia_interpolada(v) - dist_limit
            # Buscamos v tal que f(v) = 0
            def f(v):
                return self.lagrange_solver.interpolate(v) - dist_limit

            # Verificar que los signos sean opuestos
            fa = f(a_val)
            fb = f(b_val)

            if fa * fb > 0:
                messagebox.showerror(
                    "Error",
                    f"La función no tiene signos opuestos en los extremos del intervalo:\n\n"
                    f"f({a_val:.1f}) = {fa:.2f}\n"
                    f"f({b_val:.1f}) = {fb:.2f}\n\n"
                    f"Intenta con un intervalo diferente o verifica los datos experimentales."
                )
                return

            # PASO 1: Generar contexto inicial
            self.update_status("Preparando visualización integrada de Lagrange y Bisección...")
            
            context_inicial = {
                'type': 'context',
                'title': 'Problema: Velocidad Máxima Segura',
                'content': (
                    f"Encontrar la velocidad máxima segura para frenar dentro de {dist_limit:.1f} metros.\n\n"
                    f"Estrategia:\n"
                    f"1. Usar Lagrange para calcular d(v) en cada punto\n"
                    f"2. Usar Bisección para encontrar v donde d(v) = {dist_limit:.1f}\n\n"
                    f"En cada iteración verás el cálculo completo de Lagrange."
                ),
                'data': {
                    'Distancia disponible': f"{dist_limit:.1f} metros",
                    'Intervalo inicial': f"[{a_val:.1f}, {b_val:.1f}] km/h",
                    'Tolerancia': f"{tol_val} km/h",
                    'Función objetivo': f"f(v) = d(v) - {dist_limit:.1f} = 0"
                }
            }
            
            # PASO 2: Obtener historial de bisección
            self.update_status("Ejecutando método de bisección...")
            result = self.biseccion_solver.solve(f, a_val, b_val)
            
            if not result['success']:
                messagebox.showerror("Error", result['message'])
                return
            
            # PASO 3: Construir pasos intercalando Lagrange y Bisección
            all_steps = [context_inicial]
            
            # Agregar explicación del método de bisección
            all_steps.append({
                'type': 'method',
                'title': 'Método de Bisección',
                'content': ('El método de bisección encuentra la raíz de una función en un intervalo [a, b] '
                           'dividiendo repetidamente el intervalo por la mitad y seleccionando el subintervalo '
                           'donde la función cambia de signo.'),
                'formula': 'c = (a + b) / 2',
                'requirement': 'f(a) × f(b) < 0 (signos opuestos)'
            })
            
            # Procesar cada iteración
            history = result['history']
            for idx, iter_data in enumerate(history):
                iteration_num = iter_data['iteration']
                c_val = iter_data['c']
                
                # Generar pasos de Lagrange para el punto medio de esta iteración
                # Omitir la explicación del método en iteraciones posteriores a la primera
                self.update_status(f"Generando interpolación de Lagrange para iteración {iteration_num}...")
                skip_explanation = (idx > 0)  # Solo mostrar explicación en la primera iteración
                lagrange_steps_iter = self.lagrange_solver.generate_step_by_step(c_val, skip_method_explanation=skip_explanation)
                
                # Modificar el título del primer paso de Lagrange para indicar la iteración
                if lagrange_steps_iter:
                    lagrange_steps_iter[0]['title'] = f"Iteración {iteration_num}: Calcular d({c_val:.2f}) con Lagrange"
                
                # Agregar los pasos de Lagrange
                all_steps.extend(lagrange_steps_iter)
                
                # Agregar paso de iteración de bisección
                iter_step = {
                    'type': 'iteration',
                    'title': f'Iteración {iteration_num}: Resultado de Bisección',
                    'iteration': iteration_num,
                    'a': iter_data['a'],
                    'b': iter_data['b'],
                    'c': iter_data['c'],
                    'fa': iter_data['fa'],
                    'fb': iter_data['fb'],
                    'fc': iter_data['fc'],
                    'error': iter_data['error'],
                    'func_name': f"f(v) = d(v) - {dist_limit:.1f}",
                    'is_last': idx == len(history) - 1,
                    'dist_limit': dist_limit
                }
                all_steps.append(iter_step)
            
            # Agregar resultado final
            all_steps.append({
                'type': 'result',
                'title': 'Resultado Final',
                'root': result['root'],
                'iterations': result['iterations'],
                'final_error': result['final_error'],
                'function_value': result['function_value'],
                'converged': result['converged'],
                'func_name': f"f(v) = d(v) - {dist_limit:.1f}",
                'context': {
                    'dist_limit': dist_limit
                }
            })

            # Actualizar visualización con todos los pasos
            self.visualization_panel.update_visualization(all_steps)

            # Cambiar a pestaña de visualización
            self.main_notebook.set("Visualizacion Paso a Paso")

            # Mostrar resultado
            v_max = result['root']
            
            self.update_status(
                f"Velocidad maxima segura: {v_max:.1f} km/h para frenar en {dist_limit:.1f} m"
            )

            messagebox.showinfo(
                "Resultado",
                f"Velocidad Maxima Segura\n\n"
                f"Para poder frenar dentro de {dist_limit:.1f} metros,\n"
                f"la velocidad maxima es:\n\n"
                f"      {v_max:.1f} km/h\n\n"
                f"Iteraciones: {result['iterations']}\n"
                f"Error: {result['final_error']:.6f} km/h"
            )

        except Exception as e:
            error_msg = f"Error al resolver: {str(e)}"
            self.update_status(error_msg, is_error=True)
            messagebox.showerror("Error", error_msg)
            import traceback
            traceback.print_exc()

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

