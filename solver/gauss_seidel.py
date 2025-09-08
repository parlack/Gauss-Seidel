import numpy as np
from typing import List, Tuple, Dict, Optional

class GaussSeidelSolver:
    """
    Resolutor de sistemas de ecuaciones lineales usando el método de Gauss-Seidel
    con visualización paso a paso del proceso iterativo.
    """
    
    def __init__(self):
        self.iteration_history = []
        self.convergence_history = []
        self.error_history = []
        self.max_iterations = 100
        self.tolerance = 1e-6
    
    def solve(self, A: np.ndarray, b: np.ndarray, x0: Optional[np.ndarray] = None) -> Dict:
        """
        Resuelve el sistema Ax = b usando Gauss-Seidel
        
        Args:
            A: Matriz de coeficientes (n x n)
            b: Vector de términos independientes (n x 1)
            x0: Vector inicial (opcional, por defecto vector de ceros)
        
        Returns:
            Dict con solución, iteraciones, convergencia y errores
        """
        n = len(A)
        
        # Validar matriz
        if not self._is_diagonally_dominant(A):
            print("Advertencia: La matriz no es diagonalmente dominante. La convergencia no está garantizada.")
        
        # Inicializar vector solución
        if x0 is None:
            x = np.zeros(n)
        else:
            x = x0.copy()
        
        # Limpiar historiales
        self.iteration_history = []
        self.convergence_history = []
        self.error_history = []
        
        # Agregar estado inicial
        self.iteration_history.append(x.copy())
        
        # Iteraciones de Gauss-Seidel
        for iteration in range(self.max_iterations):
            x_old = x.copy()
            
            # Actualizar cada componente
            for i in range(n):
                sum1 = sum(A[i][j] * x[j] for j in range(i))
                sum2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
                x[i] = (b[i] - sum1 - sum2) / A[i][i]
            
            # Calcular error
            error = np.linalg.norm(x - x_old, np.inf)
            self.error_history.append(error)
            
            # Guardar iteración
            self.iteration_history.append(x.copy())
            self.convergence_history.append(self._check_convergence(A, x, b))
            
            # Verificar convergencia
            if error < self.tolerance:
                return {
                    'solution': x,
                    'iterations': iteration + 1,
                    'converged': True,
                    'final_error': error,
                    'history': self.iteration_history,
                    'errors': self.error_history,
                    'convergence': self.convergence_history
                }
        
        return {
            'solution': x,
            'iterations': self.max_iterations,
            'converged': False,
            'final_error': error,
            'history': self.iteration_history,
            'errors': self.error_history,
            'convergence': self.convergence_history
        }
    
    def _is_diagonally_dominant(self, A: np.ndarray) -> bool:
        """Verifica si la matriz es diagonalmente dominante"""
        n = len(A)
        for i in range(n):
            diagonal = abs(A[i][i])
            off_diagonal_sum = sum(abs(A[i][j]) for j in range(n) if i != j)
            if diagonal <= off_diagonal_sum:
                return False
        return True
    
    def _check_convergence(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
        """Calcula el residuo para verificar convergencia"""
        residuo = np.linalg.norm(A.dot(x) - b)
        return residuo
    
    def get_iteration_details(self, iteration: int) -> Dict:
        """Obtiene detalles de una iteración específica"""
        if 0 <= iteration < len(self.iteration_history):
            return {
                'iteration': iteration,
                'solution': self.iteration_history[iteration],
                'error': self.error_history[iteration - 1] if iteration > 0 else 0,
                'convergence': self.convergence_history[iteration - 1] if iteration > 0 else float('inf')
            }
        return {}
    
    def generate_step_by_step(self, A: np.ndarray, b: np.ndarray) -> List[Dict]:
        """
        Genera explicación paso a paso del método
        """
        result = self.solve(A, b)
        steps = []
        n = len(A)
        
        # Paso inicial: Mostrar sistema original
        steps.append({
            'type': 'system',
            'title': 'Sistema Original',
            'content': f'Resolver el sistema de {n} ecuaciones con {n} incógnitas',
            'matrix_A': A.copy(),
            'vector_b': b.copy()
        })
        
        # Explicar el método
        steps.append({
            'type': 'method',
            'title': 'Método de Gauss-Seidel',
            'content': 'Formula iterativa: x_i^(k+1) = (b_i - Σ(a_ij * x_j^(k+1)) - Σ(a_ij * x_j^(k))) / a_ii'
        })
        
        # Iteraciones
        for i in range(min(len(self.iteration_history) - 1, 10)):  # Mostrar máximo 10 iteraciones
            step_data = {
                'type': 'iteration',
                'title': f'Iteración {i + 1}',
                'iteration': i + 1,
                'solution': self.iteration_history[i + 1],
                'previous_solution': self.iteration_history[i] if i > 0 else np.zeros(n),
                'error': self.error_history[i] if i < len(self.error_history) else 0,
                'calculations': []
            }
            
            # Mostrar cálculos para cada variable
            x_old = self.iteration_history[i].copy()
            x_new = self.iteration_history[i + 1].copy()
            
            for j in range(n):
                sum1 = sum(A[j][k] * x_new[k] for k in range(j))
                sum2 = sum(A[j][k] * x_old[k] for k in range(j + 1, n))
                calculation = {
                    'variable': j,
                    'formula': f'x{j+1} = ({b[j]:.3f}',
                    'sum1': sum1,
                    'sum2': sum2,
                    'result': x_new[j]
                }
                
                if sum1 != 0:
                    calculation['formula'] += f' - {sum1:.3f}'
                if sum2 != 0:
                    calculation['formula'] += f' - {sum2:.3f}'
                calculation['formula'] += f') / {A[j][j]:.3f} = {x_new[j]:.6f}'
                
                step_data['calculations'].append(calculation)
            
            steps.append(step_data)
        
        # Resultado final
        steps.append({
            'type': 'result',
            'title': 'Resultado Final',
            'converged': result['converged'],
            'solution': result['solution'],
            'iterations': result['iterations'],
            'final_error': result['final_error']
        })
        
        return steps


