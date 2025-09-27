import numpy as np
import math
from typing import List, Dict, Callable, Tuple, Any


class BiseccionSolver:
    """
    Resolutor de ecuaciones no lineales usando el método de Bisección
    con visualización paso a paso del proceso iterativo.

    Este solver implementa el método numérico de bisección que encuentra 
    raíces de funciones continuas mediante la división sucesiva de intervalos.
    """

    def __init__(self):
        # historial de todas las iteraciones del proceso
        self.iteration_history = []
        # historial de errores entre iteraciones consecutivas
        self.error_history = []
        # historial de intervalos [a, b] en cada iteración
        self.interval_history = []
        # historial de evaluaciones de función
        self.function_evaluations = []
        # número máximo de iteraciones permitidas
        self.max_iterations = 100
        # tolerancia para determinar convergencia
        self.tolerance = 0.000001

    def _safe_evaluate_function(self, func_str: str, x: float) -> Tuple[bool, float, str]:
        """
        Evalúa una función de manera segura manejando errores matemáticos
        
        Args:
            func_str: función como string (ej: "x**2 - 4")
            x: valor donde evaluar la función
            
        Returns:
            tuple con (éxito, resultado, mensaje_error)
        """
        try:
            # Crear namespace seguro para evaluación
            namespace = {
                'x': x,
                'pi': math.pi, 'e': math.e,
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'log': math.log, 'ln': math.log, 'log10': math.log10,
                'exp': math.exp, 'sqrt': math.sqrt, 'abs': abs,
                'pow': pow, '__builtins__': {}
            }
            
            # Reemplazar algunas notaciones comunes
            func_clean = func_str.replace('^', '**')
            func_clean = func_clean.replace('ln(', 'log(')
            
            # Evaluar función
            result = eval(func_clean, namespace)
            
            # Verificar resultado válido
            if math.isnan(result) or math.isinf(result):
                return False, 0.0, f"Resultado inválido para x={x}: {result}"
                
            return True, float(result), ""
            
        except ZeroDivisionError:
            return False, 0.0, f"División por cero en x={x}"
        except ValueError as e:
            return False, 0.0, f"Error de valor en x={x}: {str(e)}"
        except Exception as e:
            return False, 0.0, f"Error al evaluar función en x={x}: {str(e)}"

    def _validate_interval(self, func_str: str, a: float, b: float) -> Tuple[bool, str, float, float]:
        """
        Valida que el intervalo [a,b] sea válido para bisección
        
        Args:
            func_str: función como string
            a: límite inferior del intervalo
            b: límite superior del intervalo
            
        Returns:
            tuple con (es_válido, mensaje, f(a), f(b))
        """
        if a >= b:
            return False, f"Intervalo inválido: a={a} debe ser menor que b={b}", 0, 0
            
        # Evaluar función en los extremos
        success_a, fa, error_a = self._safe_evaluate_function(func_str, a)
        if not success_a:
            return False, f"Error al evaluar f({a}): {error_a}", 0, 0
            
        success_b, fb, error_b = self._safe_evaluate_function(func_str, b)
        if not success_b:
            return False, f"Error al evaluar f({b}): {error_b}", 0, 0
            
        # Verificar cambio de signo (teorema de Bolzano)
        if fa * fb > 0:
            return False, (
                f"No hay cambio de signo en el intervalo [{a}, {b}]\n"
                f"f({a}) = {fa:.6f}\n"
                f"f({b}) = {fb:.6f}\n"
                f"El método de bisección requiere que f(a) * f(b) < 0"
            ), fa, fb
            
        return True, "Intervalo válido", fa, fb

    def solve(self, func_str: str, a: float, b: float) -> Dict:
        """
        Resuelve f(x) = 0 usando bisección en el intervalo [a,b]
        
        Args:
            func_str: función como string (ej: "x**2 - 4")
            a: límite inferior del intervalo
            b: límite superior del intervalo
            
        Returns:
            dict con solución, iteraciones, convergencia y errores
        """
        # Validar intervalo inicial
        is_valid, message, fa, fb = self._validate_interval(func_str, a, b)
        if not is_valid:
            return {
                'success': False,
                'error': message,
                'root': None,
                'iterations': 0,
                'converged': False,
                'final_error': float('inf'),
                'history': [],
                'errors': [],
                'intervals': [],
                'evaluations': []
            }
            
        # Limpiar historiales de ejecuciones anteriores
        self.iteration_history = []
        self.error_history = []
        self.interval_history = []
        self.function_evaluations = []
        
        # Valores iniciales
        xl = a  # límite inferior actual
        xu = b  # límite superior actual
        xr_old = xl  # raíz anterior para calcular error
        
        # Guardar estado inicial
        initial_state = {
            'iteration': 0,
            'xl': xl,
            'xu': xu,
            'xr': (xl + xu) / 2,
            'fxl': fa,
            'fxu': fb,
            'fxr': None,
            'error': float('inf'),
            'interval_length': xu - xl
        }
        
        # Evaluar función en el punto medio inicial
        success, fxr, error_msg = self._safe_evaluate_function(func_str, initial_state['xr'])
        if not success:
            return {
                'success': False,
                'error': f"Error en iteración inicial: {error_msg}",
                'root': None,
                'iterations': 0,
                'converged': False,
                'final_error': float('inf'),
                'history': [],
                'errors': [],
                'intervals': [],
                'evaluations': []
            }
            
        initial_state['fxr'] = fxr
        self.iteration_history.append(initial_state)
        self.interval_history.append([xl, xu])
        self.function_evaluations.append({'x': initial_state['xr'], 'fx': fxr})
        
        # Ejecutar iteraciones de bisección
        for iteration in range(1, self.max_iterations + 1):
            # Calcular nuevo punto medio
            xr = (xl + xu) / 2
            
            # Evaluar función en el punto medio
            success, fxr, error_msg = self._safe_evaluate_function(func_str, xr)
            if not success:
                return {
                    'success': False,
                    'error': f"Error en iteración {iteration}: {error_msg}",
                    'root': xr,
                    'iterations': iteration - 1,
                    'converged': False,
                    'final_error': float('inf'),
                    'history': self.iteration_history,
                    'errors': self.error_history,
                    'intervals': self.interval_history,
                    'evaluations': self.function_evaluations
                }
            
            # Calcular error relativo aproximado
            if xr != 0:
                error = abs((xr - xr_old) / xr) * 100
            else:
                error = abs(xr - xr_old)
                
            self.error_history.append(error)
            
            # Evaluar función en límite inferior actual
            success_l, fxl, _ = self._safe_evaluate_function(func_str, xl)
            if not success_l:
                fxl = 0  # valor por defecto para continuar
                
            # Guardar estado de la iteración
            iteration_state = {
                'iteration': iteration,
                'xl': xl,
                'xu': xu, 
                'xr': xr,
                'fxl': fxl,
                'fxu': fb if iteration == 1 else self.function_evaluations[-1]['fx'],
                'fxr': fxr,
                'error': error,
                'interval_length': xu - xl
            }
            
            self.iteration_history.append(iteration_state)
            self.interval_history.append([xl, xu])
            self.function_evaluations.append({'x': xr, 'fx': fxr})
            
            # Verificar convergencia
            if error < self.tolerance:
                return {
                    'success': True,
                    'root': xr,
                    'iterations': iteration,
                    'converged': True,
                    'final_error': error,
                    'final_function_value': fxr,
                    'history': self.iteration_history,
                    'errors': self.error_history,
                    'intervals': self.interval_history,
                    'evaluations': self.function_evaluations
                }
                
            # Determinar nuevo intervalo usando el signo de f(xr)
            if fxl * fxr < 0:
                # La raíz está en [xl, xr]
                xu = xr
                fb = fxr  # actualizar f(b)
            else:
                # La raíz está en [xr, xu]  
                xl = xr
                fa = fxr  # actualizar f(a)
                
            xr_old = xr
            
        # Si llegamos aquí, no convergió en max_iterations
        return {
            'success': True,  # proceso exitoso aunque no convergió
            'root': xr,
            'iterations': self.max_iterations,
            'converged': False,
            'final_error': error,
            'final_function_value': fxr,
            'history': self.iteration_history,
            'errors': self.error_history,
            'intervals': self.interval_history,
            'evaluations': self.function_evaluations
        }

    def generate_step_by_step(self, func_str: str, a: float, b: float) -> List[Dict]:
        """
        Genera explicación paso a paso del método de bisección
        """
        # Resolver para obtener el historial completo
        result = self.solve(func_str, a, b)
        steps = []
        
        if not result['success']:
            # Si hubo error, crear step de error
            steps.append({
                'type': 'error',
                'title': 'Error en la Función',
                'content': result['error']
            })
            return steps

        # Paso inicial: mostrar función y método
        steps.append({
            'type': 'function',
            'title': 'Función a Resolver',
            'content': f'Encontrar raíz de: f(x) = {func_str}',
            'function': func_str,
            'interval': [a, b]
        })

        # Explicar el método
        steps.append({
            'type': 'method',
            'title': 'Método de Bisección',
            'content': (
                'El método de bisección encuentra raíces dividiendo sucesivamente '
                'el intervalo por la mitad y seleccionando el subintervalo '
                'donde ocurre el cambio de signo.'
            ),
            'formula': 'xr = (xl + xu) / 2'
        })

        # Validación inicial
        is_valid, validation_msg, fa, fb = self._validate_interval(func_str, a, b)
        steps.append({
            'type': 'validation',
            'title': 'Validación del Intervalo',
            'content': validation_msg,
            'interval': [a, b],
            'fa': fa,
            'fb': fb,
            'valid': is_valid
        })

        if not is_valid:
            return steps

        # Generar pasos para las iteraciones
        for i, iteration_data in enumerate(self.iteration_history):
            if iteration_data['iteration'] == 0:
                continue  # Skip initial state
                
            step_data = {
                'type': 'iteration',
                'title': f'Iteración {iteration_data["iteration"]}',
                'iteration': iteration_data['iteration'],
                'xl': iteration_data['xl'],
                'xu': iteration_data['xu'],
                'xr': iteration_data['xr'],
                'fxl': iteration_data['fxl'],
                'fxu': iteration_data['fxu'],
                'fxr': iteration_data['fxr'],
                'error': iteration_data['error'],
                'interval_length': iteration_data['interval_length'],
                'calculation_details': {
                    'midpoint_formula': f"xr = ({iteration_data['xl']:.6f} + {iteration_data['xu']:.6f}) / 2",
                    'midpoint_result': f"xr = {iteration_data['xr']:.6f}",
                    'function_eval': f"f({iteration_data['xr']:.6f}) = {iteration_data['fxr']:.6f}",
                    'sign_test': self._get_sign_test_explanation(
                        iteration_data['fxl'], iteration_data['fxr']
                    ),
                    'new_interval': self._get_new_interval_explanation(
                        iteration_data, i < len(self.iteration_history) - 1
                    )
                }
            }
            steps.append(step_data)

        # Resultado final
        steps.append({
            'type': 'result',
            'title': 'Resultado Final',
            'converged': result['converged'],
            'root': result['root'],
            'iterations': result['iterations'],
            'final_error': result['final_error'],
            'final_function_value': result.get('final_function_value', 0),
            'function': func_str,
            'original_interval': [a, b]
        })

        return steps

    def _get_sign_test_explanation(self, fxl: float, fxr: float) -> str:
        """Genera explicación del test de signos"""
        product = fxl * fxr
        if product < 0:
            return f"f(xl) × f(xr) = {fxl:.6f} × {fxr:.6f} = {product:.6f} < 0 (cambio de signo)"
        elif product > 0:
            return f"f(xl) × f(xr) = {fxl:.6f} × {fxr:.6f} = {product:.6f} > 0 (mismo signo)"
        else:
            return f"f(xl) × f(xr) = {fxl:.6f} × {fxr:.6f} = 0 (raíz encontrada)"

    def _get_new_interval_explanation(self, iteration_data: Dict, has_next: bool) -> str:
        """Genera explicación del nuevo intervalo"""
        if not has_next:
            return "Proceso terminado"
            
        fxl = iteration_data['fxl']
        fxr = iteration_data['fxr']
        
        if fxl * fxr < 0:
            return f"Como f(xl) × f(xr) < 0, la raíz está en [xl, xr] = [{iteration_data['xl']:.6f}, {iteration_data['xr']:.6f}]"
        else:
            return f"Como f(xl) × f(xr) > 0, la raíz está en [xr, xu] = [{iteration_data['xr']:.6f}, {iteration_data['xu']:.6f}]"

    def validate_function(self, func_str: str) -> Tuple[bool, str]:
        """
        Valida que la función sea válida y evaluable
        
        Args:
            func_str: función como string
            
        Returns:
            tuple con (es_válida, mensaje)
        """
        if not func_str or not func_str.strip():
            return False, "La función no puede estar vacía"
            
        # Probar evaluación en algunos puntos
        test_points = [0, 1, -1, 0.5, -0.5]
        
        for x in test_points:
            success, _, error = self._safe_evaluate_function(func_str, x)
            if not success and "división por cero" not in error.lower():
                return False, f"Error en función: {error}"
                
        return True, "Función válida"
