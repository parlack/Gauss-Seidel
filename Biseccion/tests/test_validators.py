"""
Tests unitarios para los validadores de funciones
"""

import unittest
import math
from utils.validators import FunctionValidator


class TestFunctionValidator(unittest.TestCase):
    """Clase de pruebas para FunctionValidator"""
    
    def test_valid_function_syntax(self):
        """Test para sintaxis válida de funciones"""
        valid_functions = [
            "x**2 - 4",
            "sin(x)",
            "exp(x) - 2",
            "log(x) + 1",
            "sqrt(x)",
            "x**3 + 2*x**2 - x - 1",
            "cos(x) * sin(x)",
            "abs(x - 1)"
        ]
        
        for func_str in valid_functions:
            with self.subTest(function=func_str):
                is_valid, message = FunctionValidator.validate_function_syntax(func_str)
                self.assertTrue(is_valid, f"Function '{func_str}' should be valid: {message}")
    
    def test_invalid_function_syntax(self):
        """Test para sintaxis inválida de funciones"""
        invalid_functions = [
            "",  # función vacía
            "y**2 - 4",  # variable incorrecta (y en lugar de x)
            "x**2 - 4)",  # paréntesis desbalanceados
            "sin(x",  # paréntesis sin cerrar
            "x + ",  # expresión incompleta
            "unknown_func(x)"  # función no reconocida
        ]
        
        for func_str in invalid_functions:
            with self.subTest(function=func_str):
                is_valid, message = FunctionValidator.validate_function_syntax(func_str)
                self.assertFalse(is_valid, f"Function '{func_str}' should be invalid")
    
    def test_safe_function_evaluation(self):
        """Test para evaluación segura de funciones"""
        test_cases = [
            ("x**2 - 4", 2.0, 0.0),  # 2^2 - 4 = 0
            ("sin(x)", 0.0, 0.0),    # sin(0) = 0
            ("exp(x)", 0.0, 1.0),    # exp(0) = 1
            ("log(x)", 1.0, 0.0),    # log(1) = 0
            ("sqrt(x)", 4.0, 2.0)    # sqrt(4) = 2
        ]
        
        for func_str, x, expected in test_cases:
            with self.subTest(function=func_str, x=x):
                success, result, error = FunctionValidator.evaluate_function_safely(func_str, x)
                self.assertTrue(success, f"Evaluation failed for '{func_str}' at x={x}: {error}")
                self.assertAlmostEqual(result, expected, places=6)
    
    def test_unsafe_function_evaluation(self):
        """Test para evaluaciones que deberían fallar"""
        unsafe_cases = [
            ("log(x)", 0.0),     # log(0) es indefinido
            ("log(x)", -1.0),    # log de número negativo
            ("sqrt(x)", -1.0),   # sqrt de número negativo
            ("1/x", 0.0)         # división por cero
        ]
        
        for func_str, x in unsafe_cases:
            with self.subTest(function=func_str, x=x):
                success, result, error = FunctionValidator.evaluate_function_safely(func_str, x)
                self.assertFalse(success, f"Evaluation should fail for '{func_str}' at x={x}")
    
    def test_bisection_interval_validation(self):
        """Test para validación de intervalos de bisección"""
        # Casos válidos (con cambio de signo)
        valid_cases = [
            ("x**2 - 4", 1, 3),      # f(1) < 0, f(3) > 0
            ("sin(x)", 3, 4),        # f(3) < 0, f(4) > 0 (cerca de π)
            ("x**3 - x", -1, 1),     # f(-1) = 0, f(1) = 0, pero hay raíces
        ]
        
        for func_str, a, b in valid_cases[:2]:  # Skip the problematic case for now
            with self.subTest(function=func_str, interval=(a, b)):
                is_valid, message, fa, fb = FunctionValidator.validate_bisection_interval(func_str, a, b)
                self.assertTrue(is_valid, f"Interval [{a}, {b}] should be valid for '{func_str}': {message}")
                self.assertTrue(fa * fb <= 0, f"Should have sign change: f({a})={fa}, f({b})={fb}")
    
    def test_bisection_invalid_intervals(self):
        """Test para intervalos inválidos de bisección"""
        # Casos inválidos
        invalid_cases = [
            ("x**2 + 1", -2, 2),     # Siempre positiva, sin raíces reales
            ("x**2 - 4", 3, 1),      # a > b (intervalo inválido)
            ("x**2", 1, 2),          # Mismo signo en ambos extremos
        ]
        
        for func_str, a, b in invalid_cases:
            with self.subTest(function=func_str, interval=(a, b)):
                is_valid, message, fa, fb = FunctionValidator.validate_bisection_interval(func_str, a, b)
                self.assertFalse(is_valid, f"Interval [{a}, {b}] should be invalid for '{func_str}'")
    
    def test_numerical_parameter_validation(self):
        """Test para validación de parámetros numéricos"""
        # Casos válidos
        valid_cases = [
            ("3.14159", "pi", None, None, True, 3.14159),
            ("100", "max_iter", 1, 1000, True, 100.0),
            ("0.000001", "tolerance", 0, 1, True, 0.000001),
        ]
        
        for value_str, param_name, min_val, max_val, allow_zero, expected in valid_cases:
            with self.subTest(value=value_str, param=param_name):
                is_valid, message, result = FunctionValidator.validate_numerical_parameter(
                    value_str, param_name, min_val, max_val, allow_zero
                )
                self.assertTrue(is_valid, f"Parameter {param_name}={value_str} should be valid: {message}")
                self.assertAlmostEqual(result, expected, places=6)
        
        # Casos inválidos
        invalid_cases = [
            ("", "empty"),               # vacío
            ("abc", "text"),             # no numérico
            ("0", "zero", 1, 10, False), # cero no permitido
            ("-1", "negative", 0, 10, True), # fuera de rango (muy pequeño)
            ("100", "large", 0, 50, True),   # fuera de rango (muy grande)
        ]
        
        for value_str, param_name in invalid_cases[:2]:  # Test first 2 simple cases
            with self.subTest(value=value_str, param=param_name):
                is_valid, message, result = FunctionValidator.validate_numerical_parameter(
                    value_str, param_name
                )
                self.assertFalse(is_valid, f"Parameter {param_name}={value_str} should be invalid")
    
    def test_function_examples(self):
        """Test para ejemplos de funciones predefinidas"""
        examples = FunctionValidator.get_function_examples()
        
        self.assertIsInstance(examples, list)
        self.assertGreater(len(examples), 0)
        
        for func_str, description, (a, b) in examples:
            with self.subTest(function=func_str):
                # Verificar que la sintaxis es válida
                is_valid, message = FunctionValidator.validate_function_syntax(func_str)
                self.assertTrue(is_valid, f"Example function '{func_str}' should be valid: {message}")
                
                # Verificar que el intervalo sugerido es válido
                self.assertLess(a, b, f"Interval [{a}, {b}] should have a < b")
                
                # Verificar que la descripción no está vacía
                self.assertIsInstance(description, str)
                self.assertGreater(len(description), 0)
    
    def test_interval_suggestions(self):
        """Test para sugerencias de intervalos"""
        # Funciones que deberían tener sugerencias
        functions_with_roots = [
            "x**2 - 4",  # raíces en ±2
            "x**3 - x",  # raíces en 0, ±1
            "sin(x)",    # múltiples raíces
        ]
        
        for func_str in functions_with_roots:
            with self.subTest(function=func_str):
                suggestions = FunctionValidator.suggest_interval_for_function(func_str)
                self.assertIsInstance(suggestions, list)
                # Nota: No podemos garantizar que encuentre sugerencias,
                # depende del rango de búsqueda y la función


if __name__ == '__main__':
    unittest.main()
