import math
import numpy as np
from typing import Tuple, Optional, List, Dict
import re


class FunctionValidator:
    """
    Validador para funciones matemáticas y parámetros del método de bisección
    
    Esta clase proporciona métodos estáticos para validar funciones matemáticas,
    intervalos y parámetros numéricos utilizados en el método de bisección
    """

    # Funciones matemáticas permitidas
    ALLOWED_FUNCTIONS = {
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
        'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
        'log', 'ln', 'log10', 'exp', 'sqrt', 'abs', 'pow',
        'floor', 'ceil', 'round'
    }
    
    # Constantes matemáticas permitidas
    ALLOWED_CONSTANTS = {'pi', 'e', 'x'}
    
    # Operadores permitidos
    ALLOWED_OPERATORS = {'+', '-', '*', '/', '**', '^', '(', ')'}

    @staticmethod
    def _create_safe_namespace(x: float) -> Dict:
        """
        Crea un namespace seguro para evaluación de funciones
        
        Args:
            x: valor de la variable x
            
        Returns:
            dict con funciones y constantes seguras
        """
        return {
            'x': x,
            # Constantes matemáticas
            'pi': math.pi,
            'e': math.e,
            
            # Funciones trigonométricas
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            
            # Funciones hiperbólicas
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            
            # Funciones logarítmicas y exponenciales
            'log': math.log,
            'ln': math.log,  # alias para log natural
            'log10': math.log10,
            'exp': math.exp,
            
            # Otras funciones matemáticas
            'sqrt': math.sqrt,
            'abs': abs,
            'pow': pow,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            
            # Deshabilitar builtins peligrosos
            '__builtins__': {}
        }

    @staticmethod
    def _preprocess_function(func_str: str) -> str:
        """
        Preprocesa la función para hacerla evaluable
        
        Args:
            func_str: función como string
            
        Returns:
            función preprocesada
        """
        # Remover espacios extra
        func_clean = func_str.strip()
        
        # Reemplazar notaciones comunes
        replacements = [
            ('^', '**'),  # potencias
            ('ln(', 'log('),  # logaritmo natural
            ('π', 'pi'),  # pi unicode
            ('²', '**2'),  # cuadrado unicode
            ('³', '**3'),  # cubo unicode
        ]
        
        for old, new in replacements:
            func_clean = func_clean.replace(old, new)
        
        # Agregar multiplicación implícita antes de paréntesis y variables
        # Por ejemplo: 2x -> 2*x, 3(x+1) -> 3*(x+1)
        func_clean = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', func_clean)
        func_clean = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', func_clean)
        func_clean = re.sub(r'([a-zA-Z\)])\(', r'\1*(', func_clean)
        
        return func_clean

    @staticmethod
    def validate_function_syntax(func_str: str) -> Tuple[bool, str]:
        """
        Valida la sintaxis de una función matemática
        
        Args:
            func_str: función como string
            
        Returns:
            tuple con (es_válida, mensaje)
        """
        if not func_str or not func_str.strip():
            return False, "La función no puede estar vacía"
        
        # Preprocesar función
        try:
            func_clean = FunctionValidator._preprocess_function(func_str)
        except Exception as e:
            return False, f"Error en preprocesamiento: {str(e)}"
        
        # Verificar caracteres permitidos
        allowed_chars = set('0123456789+-*/().^ abcdefghijklmnopqrstuvwxyz')
        if not set(func_clean.lower()).issubset(allowed_chars):
            invalid_chars = set(func_clean.lower()) - allowed_chars
            return False, f"Caracteres no permitidos: {', '.join(invalid_chars)}"
        
        # Verificar balance de paréntesis
        if func_clean.count('(') != func_clean.count(')'):
            return False, "Paréntesis desbalanceados"
        
        # Verificar que contiene la variable x
        if 'x' not in func_clean.lower():
            return False, "La función debe contener la variable 'x'"
        
        # Intentar parsear la función con un valor de prueba
        try:
            namespace = FunctionValidator._create_safe_namespace(1.0)
            eval(func_clean, namespace)
        except SyntaxError:
            return False, "Error de sintaxis en la función"
        except NameError as e:
            return False, f"Variable o función no reconocida: {str(e)}"
        except Exception as e:
            # No reportar errores matemáticos aquí, solo sintácticos
            pass
        
        return True, "Sintaxis válida"

    @staticmethod
    def evaluate_function_safely(func_str: str, x: float) -> Tuple[bool, float, str]:
        """
        Evalúa una función de manera segura en un punto específico
        
        Args:
            func_str: función como string
            x: valor donde evaluar
            
        Returns:
            tuple con (éxito, resultado, mensaje_error)
        """
        try:
            # Preprocesar función
            func_clean = FunctionValidator._preprocess_function(func_str)
            
            # Crear namespace seguro
            namespace = FunctionValidator._create_safe_namespace(x)
            
            # Evaluar función
            result = eval(func_clean, namespace)
            
            # Verificar que el resultado es un número válido
            if not isinstance(result, (int, float, complex)):
                return False, 0.0, f"Resultado no numérico: {type(result).__name__}"
            
            # Convertir a float si es complejo con parte imaginaria cero
            if isinstance(result, complex):
                if abs(result.imag) < 1e-10:
                    result = result.real
                else:
                    return False, 0.0, f"Resultado complejo: {result}"
            
            result = float(result)
            
            # Verificar valores especiales
            if math.isnan(result):
                return False, 0.0, f"Resultado indefinido (NaN) en x={x}"
            elif math.isinf(result):
                return False, 0.0, f"Resultado infinito en x={x}"
            
            return True, result, "Evaluación exitosa"
            
        except ZeroDivisionError:
            return False, 0.0, f"División por cero en x={x}"
        except ValueError as e:
            return False, 0.0, f"Error de valor en x={x}: {str(e)}"
        except OverflowError:
            return False, 0.0, f"Desbordamiento numérico en x={x}"
        except Exception as e:
            return False, 0.0, f"Error al evaluar en x={x}: {str(e)}"

    @staticmethod
    def validate_function_in_interval(func_str: str, a: float, b: float, 
                                    num_points: int = 10) -> Tuple[bool, str, List[float]]:
        """
        Valida que la función sea evaluable en un intervalo
        
        Args:
            func_str: función como string
            a: límite inferior
            b: límite superior  
            num_points: número de puntos de prueba
            
        Returns:
            tuple con (es_válida, mensaje, lista_de_valores)
        """
        if a >= b:
            return False, f"Intervalo inválido: a={a} debe ser menor que b={b}", []
        
        # Generar puntos de prueba en el intervalo
        test_points = np.linspace(a, b, num_points)
        values = []
        problematic_points = []
        
        for x in test_points:
            success, value, error = FunctionValidator.evaluate_function_safely(func_str, x)
            if success:
                values.append(value)
            else:
                problematic_points.append((x, error))
        
        # Si hay demasiados puntos problemáticos, la función no es válida
        if len(problematic_points) > num_points // 3:
            error_msgs = [f"x={x:.3f}: {msg}" for x, msg in problematic_points[:3]]
            return False, f"Función no evaluable en el intervalo. Errores: {'; '.join(error_msgs)}", []
        
        # Si hay algunos puntos problemáticos pero no muchos, es una advertencia
        if problematic_points:
            warning_points = [f"x={x:.3f}" for x, _ in problematic_points[:2]]
            message = f"Advertencia: función no evaluable en algunos puntos: {', '.join(warning_points)}"
        else:
            message = "Función evaluable en todo el intervalo"
        
        return True, message, values

    @staticmethod
    def validate_bisection_interval(func_str: str, a: float, b: float) -> Tuple[bool, str, float, float]:
        """
        Valida específicamente un intervalo para el método de bisección
        
        Args:
            func_str: función como string
            a: límite inferior
            b: límite superior
            
        Returns:
            tuple con (es_válido, mensaje, f(a), f(b))
        """
        # Validar que a < b
        if a >= b:
            return False, f"Intervalo inválido: a={a} debe ser menor que b={b}", 0, 0
        
        # Evaluar función en los extremos
        success_a, fa, error_a = FunctionValidator.evaluate_function_safely(func_str, a)
        if not success_a:
            return False, f"Error al evaluar f({a}): {error_a}", 0, 0
        
        success_b, fb, error_b = FunctionValidator.evaluate_function_safely(func_str, b)
        if not success_b:
            return False, f"Error al evaluar f({b}): {error_b}", 0, 0
        
        # Verificar teorema de Bolzano (cambio de signo)
        if fa * fb > 0:
            # Intentar encontrar un subintervalo con cambio de signo
            sign_change_found, new_a, new_b, new_fa, new_fb = FunctionValidator._find_sign_change(
                func_str, a, b, fa, fb
            )
            
            if sign_change_found:
                return False, (
                    f"No hay cambio de signo en [{a}, {b}], pero se encontró en [{new_a:.6f}, {new_b:.6f}]\n"
                    f"f({a}) = {fa:.6f}, f({b}) = {fb:.6f}\n"
                    f"Sugerencia: usar intervalo [{new_a:.6f}, {new_b:.6f}] donde f({new_a:.6f}) = {new_fa:.6f} y f({new_b:.6f}) = {new_fb:.6f}"
                ), fa, fb
            else:
                return False, (
                    f"No hay cambio de signo en el intervalo [{a}, {b}]\n"
                    f"f({a}) = {fa:.6f}\n"
                    f"f({b}) = {fb:.6f}\n"
                    f"El método de bisección requiere que f(a) × f(b) < 0"
                ), fa, fb
        
        elif fa * fb == 0:
            # Una de las evaluaciones es exactamente cero (raíz en el extremo)
            if fa == 0:
                return False, f"f({a}) = 0: La raíz está exactamente en x = {a}", fa, fb
            else:
                return False, f"f({b}) = 0: La raíz está exactamente en x = {b}", fa, fb
        
        # Todo está bien: hay cambio de signo
        return True, f"Intervalo válido: f({a}) = {fa:.6f}, f({b}) = {fb:.6f}", fa, fb

    @staticmethod
    def _find_sign_change(func_str: str, a: float, b: float, fa: float, fb: float, 
                         divisions: int = 20) -> Tuple[bool, float, float, float, float]:
        """
        Busca un subintervalo donde ocurra cambio de signo
        
        Args:
            func_str: función como string
            a, b: límites del intervalo
            fa, fb: valores de la función en los extremos
            divisions: número de subdivisiones a probar
            
        Returns:
            tuple con (encontrado, nuevo_a, nuevo_b, nuevo_fa, nuevo_fb)
        """
        try:
            # Dividir el intervalo y buscar cambios de signo
            points = np.linspace(a, b, divisions + 1)
            
            for i in range(len(points) - 1):
                x1, x2 = points[i], points[i + 1]
                
                # Evaluar función en los puntos
                success1, f1, _ = FunctionValidator.evaluate_function_safely(func_str, x1)
                success2, f2, _ = FunctionValidator.evaluate_function_safely(func_str, x2)
                
                # Si ambas evaluaciones fueron exitosas y hay cambio de signo
                if success1 and success2 and f1 * f2 < 0:
                    return True, x1, x2, f1, f2
            
            return False, a, b, fa, fb
            
        except Exception:
            return False, a, b, fa, fb

    @staticmethod
    def validate_numerical_parameter(value_str: str, param_name: str, 
                                   min_value: Optional[float] = None,
                                   max_value: Optional[float] = None,
                                   allow_zero: bool = True) -> Tuple[bool, str, Optional[float]]:
        """
        Valida un parámetro numérico
        
        Args:
            value_str: valor como string
            param_name: nombre del parámetro para mensajes de error
            min_value: valor mínimo permitido
            max_value: valor máximo permitido
            allow_zero: si se permite el valor cero
            
        Returns:
            tuple con (es_válido, mensaje, valor_convertido)
        """
        if not value_str or not value_str.strip():
            return False, f"{param_name} no puede estar vacío", None
        
        try:
            value = float(value_str.strip())
            
            # Verificar valores especiales
            if math.isnan(value):
                return False, f"{param_name} no puede ser NaN", None
            if math.isinf(value):
                return False, f"{param_name} no puede ser infinito", None
            
            # Verificar cero si no está permitido
            if not allow_zero and value == 0:
                return False, f"{param_name} no puede ser cero", None
            
            # Verificar rango
            if min_value is not None and value < min_value:
                return False, f"{param_name} debe ser mayor o igual a {min_value}", None
            if max_value is not None and value > max_value:
                return False, f"{param_name} debe ser menor o igual a {max_value}", None
            
            return True, f"{param_name} válido", value
            
        except ValueError:
            return False, f"{param_name} debe ser un número válido", None

    @staticmethod
    def suggest_interval_for_function(func_str: str, search_range: Tuple[float, float] = (-10, 10),
                                    divisions: int = 100) -> List[Tuple[float, float]]:
        """
        Sugiere intervalos donde la función podría tener raíces
        
        Args:
            func_str: función como string
            search_range: rango de búsqueda
            divisions: número de puntos de evaluación
            
        Returns:
            lista de intervalos sugeridos (a, b) donde f(a)*f(b) < 0
        """
        suggestions = []
        
        try:
            # Validar función primero
            is_valid, _ = FunctionValidator.validate_function_syntax(func_str)
            if not is_valid:
                return suggestions
            
            # Generar puntos de evaluación
            start, end = search_range
            points = np.linspace(start, end, divisions + 1)
            
            # Evaluar función en todos los puntos
            evaluations = []
            for x in points:
                success, fx, _ = FunctionValidator.evaluate_function_safely(func_str, x)
                if success:
                    evaluations.append((x, fx))
            
            # Buscar cambios de signo entre puntos consecutivos
            for i in range(len(evaluations) - 1):
                x1, f1 = evaluations[i]
                x2, f2 = evaluations[i + 1]
                
                # Si hay cambio de signo, es un intervalo candidato
                if f1 * f2 < 0:
                    suggestions.append((x1, x2))
            
            # Limitar número de sugerencias para no abrumar al usuario
            return suggestions[:5]
            
        except Exception:
            return suggestions

    @staticmethod
    def get_function_examples() -> List[Tuple[str, str, Tuple[float, float]]]:
        """
        Obtiene ejemplos de funciones comunes con intervalos sugeridos
        
        Returns:
            lista de tuplas (función, descripción, intervalo_sugerido)
        """
        return [
            ("x**2 - 4", "Parábola con raíces en ±2", (-3, 3)),
            ("x**3 - x", "Cúbica con múltiples raíces", (-2, 2)),
            ("sin(x)", "Función seno", (3, 4)),
            ("cos(x) - 0.5", "Coseno desplazado", (0, 2)),
            ("exp(x) - 2", "Exponencial menos constante", (0, 1)),
            ("log(x) - 1", "Logaritmo menos constante", (1, 5)),
            ("x**3 + x**2 - 1", "Polinomio cúbico", (0, 1)),
            ("sin(x) - x/2", "Seno vs línea recta", (1, 2)),
            ("sqrt(x) - 2", "Raíz cuadrada menos constante", (1, 5)),
            ("x**2 - 2*x - 3", "Parábola con raíces en -1 y 3", (-2, 4))
        ]
