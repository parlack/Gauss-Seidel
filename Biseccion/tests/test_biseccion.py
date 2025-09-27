"""
Tests unitarios para el solver de bisección
"""

import unittest
import math
from solver.biseccion import BiseccionSolver


class TestBiseccionSolver(unittest.TestCase):
    """Clase de pruebas para BiseccionSolver"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.solver = BiseccionSolver()
        self.solver.tolerance = 1e-6
        self.solver.max_iterations = 100
    
    def test_solve_quadratic_function(self):
        """Test para función cuadrática x^2 - 4"""
        func_str = "x**2 - 4"
        a, b = 1, 3
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['root'], 2.0, places=5)
        self.assertLess(abs(result['final_function_value']), 1e-5)
    
    def test_solve_sine_function(self):
        """Test para función seno"""
        func_str = "sin(x)"
        a, b = 3, 4
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['root'], math.pi, places=4)
    
    def test_solve_exponential_function(self):
        """Test para función exponencial exp(x) - 2"""
        func_str = "exp(x) - 2"
        a, b = 0, 1
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['root'], math.log(2), places=5)
    
    def test_solve_logarithmic_function(self):
        """Test para función logarítmica log(x) - 1"""
        func_str = "log(x) - 1"
        a, b = 2, 4
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['converged'])
        self.assertAlmostEqual(result['root'], math.e, places=4)
    
    def test_no_sign_change(self):
        """Test para intervalo sin cambio de signo"""
        func_str = "x**2 + 1"  # Siempre positiva
        a, b = -2, 2
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertFalse(result['success'])
        self.assertIn("cambio de signo", result['error'].lower())
    
    def test_invalid_interval(self):
        """Test para intervalo inválido (a >= b)"""
        func_str = "x**2 - 4"
        a, b = 3, 1  # a > b
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertFalse(result['success'])
        self.assertIn("inválido", result['error'].lower())
    
    def test_division_by_zero(self):
        """Test para función con división por cero"""
        func_str = "1/x"
        a, b = -1, 1  # Contiene x=0
        
        result = self.solver.solve(func_str, a, b)
        
        # Debería fallar debido a la división por cero en x=0
        self.assertFalse(result['success'])
    
    def test_max_iterations_reached(self):
        """Test para cuando se alcanza el máximo de iteraciones"""
        func_str = "x**2 - 4"
        a, b = 1, 3
        
        # Configurar muy pocas iteraciones
        self.solver.max_iterations = 2
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertFalse(result['converged'])
        self.assertEqual(result['iterations'], 2)
    
    def test_step_by_step_generation(self):
        """Test para generación paso a paso"""
        func_str = "x**2 - 4"
        a, b = 1, 3
        
        steps = self.solver.generate_step_by_step(func_str, a, b)
        
        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)
        
        # Verificar que hay diferentes tipos de pasos
        step_types = [step['type'] for step in steps]
        self.assertIn('function', step_types)
        self.assertIn('method', step_types)
        self.assertIn('validation', step_types)
        self.assertIn('iteration', step_types)
        self.assertIn('result', step_types)
    
    def test_history_tracking(self):
        """Test para seguimiento del historial"""
        func_str = "x**2 - 4"
        a, b = 1, 3
        
        result = self.solver.solve(func_str, a, b)
        
        self.assertTrue(result['success'])
        self.assertGreater(len(self.solver.iteration_history), 0)
        self.assertGreater(len(self.solver.error_history), 0)
        self.assertEqual(len(self.solver.iteration_history), len(self.solver.error_history) + 1)


if __name__ == '__main__':
    unittest.main()
