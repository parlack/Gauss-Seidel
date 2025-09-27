import unittest
import math
import sys
import os

# Agregar el directorio padre al path para poder importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from solver.biseccion import BiseccionSolver


class TestBiseccionSolver(unittest.TestCase):
    """
    Tests para el solver de bisección
    
    Verifica que el método de bisección funcione correctamente
    con diferentes tipos de funciones y parámetros
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.solver = BiseccionSolver()
        self.solver.max_iterations = 100
        self.solver.tolerance = 1e-6
    
    def test_polynomial_function(self):
        """Test con función polinomial: f(x) = x^3 - 2x - 5"""
        func_expr = "x**3 - 2*x - 5"
        func = self.solver.create_function_from_expression(func_expr)
        
        # La raíz está aproximadamente en x ≈ 2.094551
        result = self.solver.solve(func, 1.0, 3.0)
        
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['solution'], 2.094551, places=3)
        self.assertLess(result['final_error'], self.solver.tolerance)
    
    def test_exponential_function(self):
        """Test con función exponencial: f(x) = e^(-x) - x"""
        func_expr = "exp(-x) - x"
        func = self.solver.create_function_from_expression(func_expr)
        
        # La raíz está aproximadamente en x ≈ 0.567143
        result = self.solver.solve(func, 0.0, 1.0)
        
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['solution'], 0.567143, places=3)
        self.assertLess(result['final_error'], self.solver.tolerance)
    
    def test_trigonometric_function(self):
        """Test con función trigonométrica: f(x) = cos(x) - x"""
        func_expr = "cos(x) - x"
        func = self.solver.create_function_from_expression(func_expr)
        
        # La raíz está aproximadamente en x ≈ 0.739085
        result = self.solver.solve(func, 0.0, 1.0)
        
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['solution'], 0.739085, places=3)
        self.assertLess(result['final_error'], self.solver.tolerance)
    
    def test_linear_function(self):
        """Test con función lineal: f(x) = 2x - 6"""
        func_expr = "2*x - 6"
        func = self.solver.create_function_from_expression(func_expr)
        
        # La raíz exacta es x = 3
        result = self.solver.solve(func, 0.0, 5.0)
        
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['solution'], 3.0, places=5)
    
    def test_quadratic_function(self):
        """Test con función cuadrática: f(x) = x^2 - 4"""
        func_expr = "x**2 - 4"
        func = self.solver.create_function_from_expression(func_expr)
        
        # Configurar tolerancia más alta para este test
        self.solver.tolerance = 0.01  # 0.01%
        
        # Las raíces exactas son x = ±2
        # Probar con raíz positiva
        result = self.solver.solve(func, 1.0, 3.0)
        
        self.assertTrue(result['converged'])
        # Verificar que esté cerca de 2.0, pero permitir más tolerancia
        self.assertAlmostEqual(result['solution'], 2.0, places=2)
    
    def test_invalid_interval_same_sign(self):
        """Test con intervalo inválido (mismo signo en extremos)"""
        func_expr = "x**2 - 4"
        func = self.solver.create_function_from_expression(func_expr)
        
        # f(3) = 5 > 0, f(5) = 21 > 0 (mismo signo)
        with self.assertRaises(ValueError) as context:
            self.solver.solve(func, 3.0, 5.0)
        
        self.assertIn("signos opuestos", str(context.exception))
    
    def test_invalid_interval_order(self):
        """Test con intervalo inválido (xl >= xu)"""
        func_expr = "x**2 - 4"
        func = self.solver.create_function_from_expression(func_expr)
        
        with self.assertRaises(ValueError) as context:
            self.solver.solve(func, 3.0, 1.0)  # xl > xu
        
        self.assertIn("menor que el superior", str(context.exception))
    
    def test_convergence_with_high_tolerance(self):
        """Test de convergencia con tolerancia alta"""
        func_expr = "x**3 - 2*x - 5"
        func = self.solver.create_function_from_expression(func_expr)
        
        # Configurar tolerancia alta
        self.solver.tolerance = 1.0  # 1%
        
        result = self.solver.solve(func, 1.0, 3.0)
        
        self.assertTrue(result['converged'])
        self.assertLess(result['iterations'], 10)  # Debería converger rápido
    
    def test_max_iterations_reached(self):
        """Test cuando se alcanza el máximo de iteraciones"""
        func_expr = "x**3 - 2*x - 5"
        func = self.solver.create_function_from_expression(func_expr)
        
        # Configurar muy pocas iteraciones y tolerancia muy baja
        self.solver.max_iterations = 3
        self.solver.tolerance = 1e-12
        
        result = self.solver.solve(func, 1.0, 3.0)
        
        self.assertFalse(result['converged'])
        self.assertEqual(result['iterations'], 3)
    
    def test_function_validation(self):
        """Test de validación de función e intervalo"""
        func_expr = "x**2 - 4"
        func = self.solver.create_function_from_expression(func_expr)
        
        # Intervalo válido
        validation = self.solver.validate_function_and_interval(func, 1.0, 3.0)
        self.assertTrue(validation['valid'])
        
        # Intervalo inválido (mismo signo)
        validation = self.solver.validate_function_and_interval(func, 3.0, 5.0)
        self.assertFalse(validation['valid'])
    
    def test_function_creation_from_expression(self):
        """Test de creación de función desde expresión string"""
        # Test expresiones válidas
        valid_expressions = [
            "x**2",
            "sin(x)",
            "exp(x) - 1",
            "log(x + 1)",
            "sqrt(x)",
            "2*x + 3"
        ]
        
        for expr in valid_expressions:
            func = self.solver.create_function_from_expression(expr)
            # Verificar que la función se puede evaluar
            try:
                result = func(1.0)
                self.assertTrue(math.isfinite(result))
            except:
                self.fail(f"No se pudo evaluar la expresión: {expr}")
    
    def test_step_by_step_generation(self):
        """Test de generación paso a paso"""
        func_expr = "x**2 - 4"
        steps = self.solver.generate_step_by_step(func_expr, 1.0, 3.0)
        
        # Verificar que se generaron pasos
        self.assertGreater(len(steps), 0)
        
        # Verificar tipos de pasos
        step_types = [step['type'] for step in steps]
        self.assertIn('function', step_types)
        self.assertIn('method', step_types)
        self.assertIn('iteration', step_types)
        self.assertIn('result', step_types)
    
    def test_evaluation_at_points(self):
        """Test de evaluación en puntos específicos"""
        func_expr = "x**2 - 4"
        points = [0, 1, 2, 3, 4]
        
        result = self.solver.evaluate_at_points(func_expr, points)
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['evaluations']), len(points))
        
        # Verificar valores conocidos
        evaluations = {eval_data['x']: eval_data['y'] for eval_data in result['evaluations']}
        self.assertEqual(evaluations[0], -4)  # 0^2 - 4 = -4
        self.assertEqual(evaluations[2], 0)   # 2^2 - 4 = 0


class TestFunctionExpressions(unittest.TestCase):
    """
    Tests específicos para expresiones de funciones
    """
    
    def setUp(self):
        self.solver = BiseccionSolver()
    
    def test_basic_math_functions(self):
        """Test de funciones matemáticas básicas"""
        test_cases = [
            ("x", 2.0, 2.0),
            ("x**2", 3.0, 9.0),
            ("2*x + 1", 2.0, 5.0),
            ("abs(-x)", -3.0, 3.0),
        ]
        
        for expr, x_val, expected in test_cases:
            func = self.solver.create_function_from_expression(expr)
            result = func(x_val)
            self.assertAlmostEqual(result, expected, places=10)
    
    def test_trigonometric_functions(self):
        """Test de funciones trigonométricas"""
        func_sin = self.solver.create_function_from_expression("sin(x)")
        func_cos = self.solver.create_function_from_expression("cos(x)")
        
        self.assertAlmostEqual(func_sin(0), 0, places=10)
        self.assertAlmostEqual(func_sin(math.pi/2), 1, places=10)
        self.assertAlmostEqual(func_cos(0), 1, places=10)
        self.assertAlmostEqual(func_cos(math.pi), -1, places=10)
    
    def test_exponential_and_logarithmic(self):
        """Test de funciones exponenciales y logarítmicas"""
        func_exp = self.solver.create_function_from_expression("exp(x)")
        func_log = self.solver.create_function_from_expression("log(x)")
        
        self.assertAlmostEqual(func_exp(0), 1, places=10)
        self.assertAlmostEqual(func_exp(1), math.e, places=10)
        self.assertAlmostEqual(func_log(1), 0, places=10)
        self.assertAlmostEqual(func_log(math.e), 1, places=10)


if __name__ == '__main__':
    unittest.main()
