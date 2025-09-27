import math
from typing import Tuple, Dict, Callable


class FunctionValidator:
    """
    Validador para funciones matemáticas y parámetros del método de bisección
    
    Proporciona métodos estáticos para validar que las funciones y intervalos
    sean apropiados para el método de bisección
    """
    
    @staticmethod
    def validate_function_expression(expression: str) -> Tuple[bool, str]:
        """
        Valida que una expresión matemática sea válida y segura
        
        Args:
            expression: expresión matemática como string
            
        Returns:
            tupla (es_valida, mensaje_error)
        """
        if not expression or not expression.strip():
            return False, "La expresión no puede estar vacía"
        
        expression = expression.strip()
        
        # Caracteres permitidos (básicos)
        allowed_chars = set("x0123456789+-*/.()^** abcdefghijklmnopqrstuvwxyz")
        
        # Verificar caracteres no permitidos
        for char in expression.lower():
            if char not in allowed_chars:
                return False, f"Carácter no permitido: '{char}'"
        
        # Verificar que contenga al menos una 'x'
        if 'x' not in expression.lower():
            return False, "La expresión debe contener la variable 'x'"
        
        # Verificar paréntesis balanceados
        if not FunctionValidator._are_parentheses_balanced(expression):
            return False, "Los paréntesis no están balanceados"
        
        # Intentar crear y evaluar la función en un punto de prueba
        try:
            # Importar solver para usar el método create_function_from_expression
            from solver.biseccion import BiseccionSolver
            solver = BiseccionSolver()
            test_func = solver.create_function_from_expression(expression)
            
            # Probar evaluación en puntos de prueba
            test_points = [0.0, 1.0, -1.0, 0.5, -0.5]
            valid_evaluations = 0
            
            for point in test_points:
                try:
                    result = test_func(point)
                    if math.isfinite(result):
                        valid_evaluations += 1
                except:
                    continue
            
            if valid_evaluations == 0:
                return False, "La función no se puede evaluar en ningún punto de prueba"
            
            return True, "Expresión válida"
            
        except Exception as e:
            return False, f"Error en la expresión: {str(e)}"
    
    @staticmethod
    def validate_interval(xl: float, xu: float) -> Tuple[bool, str]:
        """
        Valida que un intervalo sea apropiado para bisección
        
        Args:
            xl: límite inferior
            xu: límite superior
            
        Returns:
            tupla (es_valido, mensaje_error)
        """
        # Verificar que sean números finitos
        if not (math.isfinite(xl) and math.isfinite(xu)):
            return False, "Los límites del intervalo deben ser números finitos"
        
        # Verificar que xl < xu
        if xl >= xu:
            return False, "El límite inferior debe ser menor que el superior"
        
        # Verificar que el intervalo no sea demasiado pequeño
        if abs(xu - xl) < 1e-15:
            return False, "El intervalo es demasiado pequeño"
        
        # Verificar que el intervalo no sea demasiado grande
        if abs(xu - xl) > 1e10:
            return False, "El intervalo es demasiado grande"
        
        return True, "Intervalo válido"
    
    @staticmethod
    def validate_function_in_interval(func: Callable[[float], float], xl: float, xu: float) -> Tuple[bool, str, Dict]:
        """
        Valida que una función sea apropiada para bisección en un intervalo dado
        
        Args:
            func: función a validar
            xl: límite inferior
            xu: límite superior
            
        Returns:
            tupla (es_valido, mensaje, datos_adicionales)
        """
        try:
            # Evaluar función en los extremos
            f_xl = func(xl)
            f_xu = func(xu)
            
            # Verificar que los valores sean finitos
            if not (math.isfinite(f_xl) and math.isfinite(f_xu)):
                return False, "La función no está definida en uno o ambos extremos del intervalo", {
                    'f_xl': f_xl,
                    'f_xu': f_xu,
                    'product': None
                }
            
            # Verificar signos opuestos
            product = f_xl * f_xu
            
            if product > 0:
                return False, "f(xl) y f(xu) deben tener signos opuestos", {
                    'f_xl': f_xl,
                    'f_xu': f_xu,
                    'product': product
                }
            
            if product == 0:
                if f_xl == 0:
                    return True, f"Raíz exacta encontrada en xl = {xl}", {
                        'f_xl': f_xl,
                        'f_xu': f_xu,
                        'product': product,
                        'exact_root': xl
                    }
                else:
                    return True, f"Raíz exacta encontrada en xu = {xu}", {
                        'f_xl': f_xl,
                        'f_xu': f_xu,
                        'product': product,
                        'exact_root': xu
                    }
            
            # Todo está bien para bisección
            return True, "La función es apropiada para bisección en este intervalo", {
                'f_xl': f_xl,
                'f_xu': f_xu,
                'product': product
            }
            
        except Exception as e:
            return False, f"Error evaluando la función: {str(e)}", {
                'f_xl': None,
                'f_xu': None,
                'product': None
            }
    
    @staticmethod
    def validate_solver_parameters(tolerance: float, max_iterations: int) -> Tuple[bool, str]:
        """
        Valida los parámetros del solver de bisección
        
        Args:
            tolerance: tolerancia para convergencia
            max_iterations: máximo número de iteraciones
            
        Returns:
            tupla (son_validos, mensaje_error)
        """
        # Validar tolerancia
        if not math.isfinite(tolerance) or tolerance <= 0:
            return False, "La tolerancia debe ser un número positivo"
        
        if tolerance > 100:
            return False, "La tolerancia no puede ser mayor que 100%"
        
        if tolerance < 1e-15:
            return False, "La tolerancia es demasiado pequeña (puede causar problemas de precisión)"
        
        # Validar máximo de iteraciones
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            return False, "El máximo de iteraciones debe ser un entero positivo"
        
        if max_iterations > 10000:
            return False, "El máximo de iteraciones es demasiado alto (máximo: 10000)"
        
        return True, "Parámetros válidos"
    
    @staticmethod
    def suggest_better_interval(func: Callable[[float], float], initial_xl: float, initial_xu: float, 
                               num_points: int = 20) -> Dict:
        """
        Sugiere un mejor intervalo si el actual no es válido para bisección
        
        Args:
            func: función a analizar
            initial_xl: límite inferior inicial
            initial_xu: límite superior inicial
            num_points: número de puntos a evaluar
            
        Returns:
            diccionario con sugerencias
        """
        try:
            # Expandir el intervalo inicial
            expanded_xl = initial_xl - abs(initial_xu - initial_xl)
            expanded_xu = initial_xu + abs(initial_xu - initial_xl)
            
            # Evaluar función en varios puntos
            dx = (expanded_xu - expanded_xl) / (num_points - 1)
            points = []
            
            for i in range(num_points):
                x = expanded_xl + i * dx
                try:
                    y = func(x)
                    if math.isfinite(y):
                        points.append((x, y))
                except:
                    continue
            
            if len(points) < 2:
                return {
                    'success': False,
                    'message': 'No se pudo evaluar la función en suficientes puntos',
                    'suggestions': []
                }
            
            # Buscar cambios de signo
            intervals = []
            
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                if y1 * y2 < 0:  # Cambio de signo
                    intervals.append({
                        'xl': x1,
                        'xu': x2,
                        'f_xl': y1,
                        'f_xu': y2,
                        'width': x2 - x1
                    })
            
            if not intervals:
                return {
                    'success': False,
                    'message': 'No se encontraron cambios de signo en el intervalo expandido',
                    'suggestions': [],
                    'points_evaluated': points
                }
            
            # Ordenar intervalos por ancho (preferir intervalos más pequeños)
            intervals.sort(key=lambda x: x['width'])
            
            return {
                'success': True,
                'message': f'Se encontraron {len(intervals)} intervalo(s) con cambio de signo',
                'suggestions': intervals[:3],  # Máximo 3 sugerencias
                'points_evaluated': points
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error analizando la función: {str(e)}',
                'suggestions': []
            }
    
    @staticmethod
    def _are_parentheses_balanced(expression: str) -> bool:
        """Verifica que los paréntesis estén balanceados"""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:  # Más ')' que '('
                    return False
        return count == 0  # Mismo número de '(' y ')'
    
    @staticmethod
    def get_function_help() -> Dict[str, str]:
        """Retorna información de ayuda sobre funciones disponibles"""
        return {
            'operators': 'Operadores: +, -, *, /, ** (potencia), () (paréntesis)',
            'functions': 'Funciones: sin(x), cos(x), tan(x), exp(x), log(x), sqrt(x), abs(x)',
            'constants': 'Constantes: pi, e',
            'examples': [
                'x**2 - 4',
                'sin(x) - 0.5',
                'exp(x) - 2*x',
                'log(x) - 1',
                'x**3 - 2*x - 5'
            ]
        }
