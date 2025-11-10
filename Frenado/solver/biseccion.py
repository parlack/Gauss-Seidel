# Andres Monsivais Salazar
# Luis Andres Salinas Lozano

import numpy as np
from typing import List, Dict, Callable
import math


class BiseccionSolver:
    """
    Solver del método de bisección para encontrar raíces de funciones
    
    Este solver implementa el método de bisección que encuentra la raíz
    de una función continua en un intervalo [a, b] donde f(a) y f(b)
    tienen signos opuestos.
    
    Aplicación: Encontrar la velocidad máxima segura dado un límite
    de distancia de frenado.
    """
    
    def __init__(self):
        self.tolerance = 0.001  # Tolerancia en km/h
        self.max_iterations = 100
        self.iteration_history = []
        self.error_history = []
    
    def solve(self, func: Callable[[float], float], a: float, b: float) -> Dict:
        """
        Resuelve f(x) = 0 usando el método de bisección
        
        Args:
            func: Función a evaluar
            a: Límite inferior del intervalo
            b: Límite superior del intervalo
            
        Returns:
            Dict con solución, iteraciones y convergencia
        """
        # Limpiar historiales
        self.iteration_history = []
        self.error_history = []
        
        # Verificar que los signos sean opuestos
        fa = func(a)
        fb = func(b)
        
        if fa * fb > 0:
            return {
                'success': False,
                'message': 'La función debe tener signos opuestos en los extremos del intervalo',
                'iterations': 0
            }
        
        # Guardar valores iniciales
        self.iteration_history.append({
            'iteration': 0,
            'a': a,
            'b': b,
            'c': (a + b) / 2,
            'fa': fa,
            'fb': fb,
            'fc': func((a + b) / 2),
            'error': abs(b - a)
        })
        
        # Proceso iterativo de bisección
        for i in range(1, self.max_iterations + 1):
            # Calcular punto medio
            c = (a + b) / 2
            fc = func(c)
            
            # Calcular error (ancho del intervalo)
            error = abs(b - a) / 2
            
            # Guardar datos de la iteración
            iter_data = {
                'iteration': i,
                'a': a,
                'b': b,
                'c': c,
                'fa': func(a),
                'fb': func(b),
                'fc': fc,
                'error': error
            }
            self.iteration_history.append(iter_data)
            self.error_history.append(error)
            
            # Verificar convergencia
            if abs(fc) < 1e-10 or error < self.tolerance:
                return {
                    'success': True,
                    'root': c,
                    'iterations': i,
                    'final_error': error,
                    'function_value': fc,
                    'converged': True,
                    'history': self.iteration_history
                }
            
            # Decidir qué mitad del intervalo mantener
            if func(a) * fc < 0:
                b = c  # La raíz está en [a, c]
            else:
                a = c  # La raíz está en [c, b]
        
        # Si llegamos aquí, no convergió en max_iterations
        c = (a + b) / 2
        return {
            'success': True,
            'root': c,
            'iterations': self.max_iterations,
            'final_error': abs(b - a) / 2,
            'function_value': func(c),
            'converged': False,
            'history': self.iteration_history
        }
    
    def generate_step_by_step(self, func: Callable[[float], float], a: float, b: float,
                             func_name: str = "f(x)", context: Dict = None) -> List[Dict]:
        """
        Genera explicación paso a paso del proceso de bisección
        
        Args:
            func: Función a evaluar
            a: Límite inferior
            b: Límite superior
            func_name: Nombre de la función para mostrar
            context: Contexto adicional (problema real)
            
        Returns:
            Lista de pasos del proceso
        """
        steps = []
        
        # Paso 1: Problema y contexto
        if context:
            steps.append({
                'type': 'context',
                'title': 'Problema a Resolver',
                'content': context.get('description', ''),
                'data': context.get('data', {})
            })
        
        # Paso 2: Método
        steps.append({
            'type': 'method',
            'title': 'Método de Bisección',
            'content': ('El método de bisección encuentra la raíz de una función en un intervalo [a, b] '
                       'dividiendo repetidamente el intervalo por la mitad y seleccionando el subintervalo '
                       'donde la función cambia de signo.'),
            'formula': 'c = (a + b) / 2',
            'requirement': 'f(a) × f(b) < 0 (signos opuestos)'
        })
        
        # Paso 3: Intervalo inicial
        fa = func(a)
        fb = func(b)
        
        steps.append({
            'type': 'initial',
            'title': 'Intervalo Inicial',
            'a': a,
            'b': b,
            'fa': fa,
            'fb': fb,
            'func_name': func_name,
            'signs_opposite': fa * fb < 0
        })
        
        # Resolver para obtener historial
        result = self.solve(func, a, b)
        
        if not result['success']:
            steps.append({
                'type': 'error',
                'title': 'Error',
                'content': result['message']
            })
            return steps
        
        # Paso 4: Mostrar TODAS las iteraciones
        history = result['history']
        
        for idx in range(len(history)):
            iter_data = history[idx]
            
            iter_step = {
                'type': 'iteration',
                'title': f'Iteración {iter_data["iteration"]}',
                'iteration': iter_data['iteration'],
                'a': iter_data['a'],
                'b': iter_data['b'],
                'c': iter_data['c'],
                'fa': iter_data['fa'],
                'fb': iter_data['fb'],
                'fc': iter_data['fc'],
                'error': iter_data['error'],
                'func_name': func_name,
                'is_last': idx == len(history) - 1
            }
            
            # Agregar dist_limit si está disponible en el contexto
            if context and 'dist_limit' in context:
                iter_step['dist_limit'] = context['dist_limit']
            
            steps.append(iter_step)
        
        # Paso 5: Resultado final
        steps.append({
            'type': 'result',
            'title': 'Resultado Final',
            'root': result['root'],
            'iterations': result['iterations'],
            'final_error': result['final_error'],
            'function_value': result['function_value'],
            'converged': result['converged'],
            'func_name': func_name,
            'context': context
        })
        
        return steps

