import numpy as np
import math
from typing import List, Dict, Callable


class BiseccionSolver:

    def __init__(self):
        # Historial de todas las iteraciones del proceso
        self.iteration_history = []
        # Historial de errores entre iteraciones consecutivas
        self.error_history = []
        # Número máximo de iteraciones permitidas
        self.max_iterations = 100
        # Tolerancia para determinar convergencia (en porcentaje)
        self.tolerance = 0.000001

    def solve(self, func: Callable[[float], float], xl: float, xu: float) -> Dict:
        # Verificar que el intervalo sea válido
        if xl >= xu:
            raise ValueError("El límite inferior debe ser menor que el superior")

        # Evaluar función en los extremos
        f_xl = func(xl)
        f_xu = func(xu)

        # Verificar que la función tenga signos opuestos en los extremos
        try:
            if f_xl is not None and f_xu is not None and f_xl * f_xu > 0:
                raise ValueError("f(xl) y f(xu) deben tener signos opuestos")
        except TypeError:
            raise ValueError("Error en evaluación de función en extremos del intervalo")

        # Limpiar historiales de iteraciones anteriores
        self.iteration_history = []
        self.error_history = []

        # Variables de trabajo
        xl_curr = xl
        xu_curr = xu
        xr_prev = None

        # Ejecutar iteraciones de bisección
        for iteration in range(self.max_iterations):
            # Calcular punto medio
            xr = (xl_curr + xu_curr) / 2.0

            # Evaluar función en los puntos con validación
            try:
                f_xl = func(xl_curr)
                if not math.isfinite(f_xl):
                    raise ValueError(f"La función no está definida en xl = {xl_curr}")
            except Exception as e:
                raise ValueError(f"Error evaluando función en xl = {xl_curr}: {str(e)}")
            
            try:
                f_xu = func(xu_curr)
                if not math.isfinite(f_xu):
                    raise ValueError(f"La función no está definida en xu = {xu_curr}")
            except Exception as e:
                raise ValueError(f"Error evaluando función en xu = {xu_curr}: {str(e)}")
            
            try:
                f_xr = func(xr)
                if not math.isfinite(f_xr):
                    raise ValueError(f"La función no está definida en xr = {xr}")
            except Exception as e:
                raise ValueError(f"Error evaluando función en xr = {xr}: {str(e)}")

            # Calcular error relativo si no es la primera iteración
            error = 0.0
            if xr_prev is not None and xr != 0 and isinstance(xr, (int, float)) and isinstance(xr_prev, (int, float)):
                try:
                    error = abs((xr - xr_prev) / xr) * 100
                except (TypeError, ZeroDivisionError):
                    error = 0.0

            # Calcular producto con validación adicional (protegido contra TypeError)
            try:
                if all(isinstance(val, (int, float)) and math.isfinite(val) for val in [f_xl, f_xr]):
                    f_xl_times_f_xr = float(f_xl) * float(f_xr)
                else:
                    raise ValueError("Valores no válidos para calcular producto")
            except TypeError as e:
                raise ValueError(
                    f"Operación inválida al calcular f(xl)×f(xr) en la iteración {iteration+1}: {e}"
                )
            except Exception as e:
                raise ValueError(f"Error calculando f(xl) × f(xr): {str(e)}")
            
            # Guardar estado de la iteración
            iteration_data = {
                'iteration': iteration + 1,
                'xl': xl_curr,
                'xu': xu_curr,
                'xr': xr,
                'f_xl': f_xl,
                'f_xu': f_xu,
                'f_xr': f_xr,
                'f_xl_times_f_xr': f_xl_times_f_xr,
                'error_percent': error,
                'converged': False
            }

            # Agregar al historial
            self.iteration_history.append(iteration_data)
            if iteration > 0:
                self.error_history.append(error)

            # Verificar convergencia por tolerancia
            if iteration > 0 and error < self.tolerance:
                iteration_data['converged'] = True
                return {
                    'solution': xr,
                    'iterations': iteration + 1,
                    'converged': True,
                    'final_error': error,
                    'history': self.iteration_history,
                    'errors': self.error_history
                }

            # También verificar si f(xr) está muy cerca de cero
            if f_xr is not None and math.isfinite(f_xr) and abs(f_xr) < 1e-12:
                iteration_data['converged'] = True
                return {
                    'solution': xr,
                    'iterations': iteration + 1,
                    'converged': True,
                    'final_error': error,
                    'history': self.iteration_history,
                    'errors': self.error_history
                }

            # Determinar nuevo intervalo basado en el signo del producto
            if f_xl_times_f_xr < 0:
                # La raíz está en [xl, xr]
                xu_curr = xr
                iteration_data['new_interval'] = 'xl a xr'
            else:
                # La raíz está en [xr, xu]
                xl_curr = xr
                iteration_data['new_interval'] = 'xr a xu'

            # Guardar xr actual como xr previo para próxima iteración
            xr_prev = xr

        # Si no convergió en max_iterations, retornar último resultado
        final_xr = (xl_curr + xu_curr) / 2.0
        # Calcular error final de manera segura
        final_error = 0.0
        if (xr_prev is not None and final_xr != 0 and 
            isinstance(final_xr, (int, float)) and isinstance(xr_prev, (int, float))):
            try:
                final_error = abs((final_xr - xr_prev) / final_xr) * 100
            except (TypeError, ZeroDivisionError):
                final_error = 0.0

        return {
            'solution': final_xr,
            'iterations': self.max_iterations,
            'converged': False,
            'final_error': final_error,
            'history': self.iteration_history,
            'errors': self.error_history
        }

    def create_function_from_expression(self, expression: str) -> Callable[[float], float]:
        # Normalizar la expresión de forma segura
        # Reemplazos ordenados por prioridad para evitar conflictos
        replacements = {
            '^': '**',
            'sen(': 'sin(',
            'cos(': 'cos(',
            'tan(': 'tan(',
            'ln(': 'log(',
            'log10(': 'log10(',
            'sqrt(': 'sqrt(',
            'exp(': 'exp(',
        }
        for src, dst in replacements.items():
            expression = expression.replace(src, dst)

        def func(x):
            """Función generada dinámicamente"""
            # Validar que x sea un número válido
            if x is None:
                raise ValueError("El valor de x no puede ser None")
            if not isinstance(x, (int, float)):
                try:
                    x = float(x)
                except:
                    raise ValueError(f"El valor de x debe ser numérico, recibido: {type(x)}")
            if not math.isfinite(x):
                raise ValueError(f"El valor de x debe ser finito, recibido: {x}")
            
            # Namespace con funciones matemáticas y variables
            namespace = {
                'x': float(x),
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'sqrt': math.sqrt,
                'exp': math.exp,
                'pi': math.pi,
                'e': math.e,
                'abs': abs,
                'pow': pow,
                'asin': math.asin,
                'acos': math.acos,
                'atan': math.atan,
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
            }
            
            try:
                # Validar que la expresión no esté vacía
                if not expression or not expression.strip():
                    raise ValueError("La expresión no puede estar vacía")
                
                result = eval(expression, {"__builtins__": {}}, namespace)
                
                # Verificar que el resultado sea un número válido
                if result is None:
                    raise ValueError(f"La función retornó None para x = {x}. Verifica la expresión: '{expression}'")
                
                if not isinstance(result, (int, float)):
                    # Intentar convertir a float (por ejemplo numpy.float64)
                    try:
                        result = float(result)
                    except Exception:
                        raise ValueError(f"La función retornó un tipo inválido: {type(result)} para x = {x}")
                
                if not math.isfinite(result):
                    raise ValueError(f"La función retornó un valor no finito: {result} para x = {x}")
                
                return float(result)
                
            except ZeroDivisionError:
                raise ValueError(f"División por cero en x = {x}. Verifica la función para evitar divisiones por cero.")
            except ValueError as ve:
                # Re-lanzar errores de ValueError ya manejados
                raise ve
            except Exception as e:
                raise ValueError(f"Error evaluando función en x = {x}: {str(e)}\nExpresión: '{expression}'")
        
        return func

    def validate_function_and_interval(self, func: Callable[[float], float], xl: float, xu: float) -> Dict:
        try:
            # Evaluar función en los extremos
            f_xl = func(xl)
            f_xu = func(xu)
            
            # Verificar que los valores sean finitos
            if not (math.isfinite(f_xl) and math.isfinite(f_xu)):
                return {
                    'valid': False,
                    'message': 'La función no está definida en uno o ambos extremos del intervalo',
                    'f_xl': None,
                    'f_xu': None
                }
            
            # Verificar signos opuestos
            try:
                product = f_xl * f_xu if f_xl is not None and f_xu is not None else None
                if product is not None and product > 0:
                    return {
                        'valid': False,
                        'message': 'f(xl) y f(xu) deben tener signos opuestos para garantizar una raíz',
                        'f_xl': f_xl,
                        'f_xu': f_xu
                    }
            except TypeError:
                return {
                    'valid': False,
                    'message': 'Error en evaluación de función en extremos del intervalo',
                    'f_xl': f_xl,
                    'f_xu': f_xu
                }
            
            # Verificar que xl < xu
            if xl >= xu:
                return {
                    'valid': False,
                    'message': 'xl debe ser menor que xu',
                    'f_xl': f_xl,
                    'f_xu': f_xu
                }
            
            return {
                'valid': True,
                'message': 'Función e intervalo válidos para bisección',
                'f_xl': f_xl,
                'f_xu': f_xu
            }
            
        except Exception as e:
            return {
                'valid': False,
                'message': f'Error evaluando función: {str(e)}',
                'f_xl': None,
                'f_xu': None
            }

    def generate_step_by_step(self, func_expression: str, xl: float, xu: float) -> List[Dict]:
        try:
            # Crear función desde expresión
            func = self.create_function_from_expression(func_expression)

            # Validar función e intervalo
            validation = self.validate_function_and_interval(func, xl, xu)
            if not validation['valid']:
                return [{
                    'type': 'error',
                    'title': 'Error de Validación',
                    'content': validation['message'],
                    'f_xl': validation.get('f_xl'),
                    'f_xu': validation.get('f_xu')
                }]

            # Resolver usando bisección (con manejo explícito de TypeError)
            # Ejecutar solución (si algo falla, se propagará como ValueError por las validaciones previas)
            result = self.solve(func, xl, xu)
            steps = []

            # Paso inicial: mostrar función y método
            steps.append({
                'type': 'function',
                'title': 'Función a resolver',
                'content': f'Encontrar las raíces de: f(x) = {func_expression}',
                'expression': func_expression,
                'xl_initial': xl,
                'xu_initial': xu,
                'f_xl_initial': validation['f_xl'],
                'f_xu_initial': validation['f_xu']
            })

            # Explicar el método
            steps.append({
                'type': 'method',
                'title': 'Método de Bisección',
                'content': 'El método divide el intervalo por la mitad y selecciona el subintervalo que contiene la raíz'
            })

            # Generar pasos para las iteraciones (máximo 20 para evitar sobrecarga)
            max_shown_iterations = min(len(self.iteration_history), 20)
            for i in range(max_shown_iterations):
                iteration_data = self.iteration_history[i]
                
                step_data = {
                    'type': 'iteration',
                    'title': f'Iteración {iteration_data["iteration"]}',
                    **iteration_data
                }
                
                steps.append(step_data)
                
                # Si ya convergió, no mostrar más iteraciones
                if iteration_data['converged']:
                    break

            # Agregar resultado final
            steps.append({
                'type': 'result',
                'title': 'Resultado Final',
                'converged': result['converged'],
                'solution': result['solution'],
                'iterations': result['iterations'],
                'final_error': result['final_error'],
                'expression': func_expression
            })

            return steps
            
        except Exception as e:
            return [{
                'type': 'error',
                'title': 'Error en el Proceso',
                'content': f'Error inesperado: {str(e)}'
            }]

    def evaluate_at_points(self, func_expression: str, points: List[float]) -> Dict:
        """
        Evalúa la función en una lista de puntos para verificación
        """
        try:
            func = self.create_function_from_expression(func_expression)
            evaluations = []
            
            for x in points:
                try:
                    y = func(x)
                    evaluations.append({
                        'x': x,
                        'y': y,
                        'valid': math.isfinite(y)
                    })
                except:
                    evaluations.append({
                        'x': x,
                        'y': None,
                        'valid': False
                    })
            
            return {
                'success': True,
                'evaluations': evaluations
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
