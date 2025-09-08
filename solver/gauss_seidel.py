import numpy as np
from typing import List, Tuple, Dict, Optional

class GaussSeidelSolver:
    """
    resolutor de sistemas de ecuaciones lineales usando el metodo de gauss-seidel
    con visualizacion paso a paso del proceso iterativo.
    
    este solver implementa el metodo iterativo de gauss-seidel que actualiza
    cada variable usando los valores mas recientes de las otras variables.
    """
    
    def __init__(self):
        # historial de todas las iteraciones del proceso
        self.iteration_history = []
        # historial de convergencia para cada iteracion
        self.convergence_history = []
        # historial de errores entre iteraciones consecutivas
        self.error_history = []
        # numero maximo de iteraciones permitidas
        self.max_iterations = 100
        # tolerancia para determinar convergencia
        self.tolerance = 1e-6
    
    def solve(self, A: np.ndarray, b: np.ndarray, x0: Optional[np.ndarray] = None) -> Dict:
        """
        resuelve el sistema ax = b usando gauss-seidel
        
        args:
            a: matriz de coeficientes (n x n)
            b: vector de terminos independientes (n x 1)
            x0: vector inicial (opcional, por defecto vector de ceros)
        
        returns:
            dict con solucion, iteraciones, convergencia y errores
        """
        # obtener dimension del sistema
        n = len(A)
        
        # validar si la matriz es diagonalmente dominante
        if not self._is_diagonally_dominant(A):
            print("advertencia: la matriz no es diagonalmente dominante. la convergencia no esta garantizada.")
        
        # inicializar vector solucion
        if x0 is None:
            # usar vector de ceros como punto inicial
            x = np.zeros(n)
        else:
            # usar vector inicial proporcionado
            x = x0.copy()
        
        # limpiar historiales de iteraciones anteriores
        self.iteration_history = []
        self.convergence_history = []
        self.error_history = []
        
        # guardar estado inicial en el historial
        self.iteration_history.append(x.copy())
        
        # ejecutar iteraciones de gauss-seidel
        for iteration in range(self.max_iterations):
            # guardar estado anterior para calcular error
            x_old = x.copy()
            
            # actualizar cada componente del vector solucion
            for i in range(n):
                # suma de elementos ya actualizados (indices < i)
                sum1 = sum(A[i][j] * x[j] for j in range(i))
                # suma de elementos no actualizados (indices > i)
                sum2 = sum(A[i][j] * x_old[j] for j in range(i + 1, n))
                # calcular nuevo valor de x[i]
                x[i] = (b[i] - sum1 - sum2) / A[i][i]
            
            # calcular error entre iteraciones usando norma infinito
            error = np.linalg.norm(x - x_old, np.inf)
            self.error_history.append(error)
            
            # guardar estado actual en historial
            self.iteration_history.append(x.copy())
            self.convergence_history.append(self._check_convergence(A, x, b))
            
            # verificar si se alcanzo la convergencia
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
        
        # si no convergio en max_iterations, retornar resultado actual
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
        """verifica si la matriz es diagonalmente dominante"""
        n = len(A)
        # verificar cada fila de la matriz
        for i in range(n):
            # elemento diagonal de la fila i
            diagonal = abs(A[i][i])
            # suma de elementos fuera de la diagonal en la fila i
            off_diagonal_sum = sum(abs(A[i][j]) for j in range(n) if i != j)
            # para ser diagonalmente dominante: |a_ii| > suma(|a_ij|) para j!=i
            if diagonal <= off_diagonal_sum:
                return False
        return True
    
    def _check_convergence(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
        """calcula el residuo para verificar convergencia"""
        # calcular residuo: |Ax - b|
        # esto mide que tan bien la solucion actual satisface el sistema
        residuo = np.linalg.norm(A.dot(x) - b)
        return residuo
    
    def get_iteration_details(self, iteration: int) -> Dict:
        """obtiene detalles de una iteracion especifica"""
        # verificar que el indice de iteracion sea valido
        if 0 <= iteration < len(self.iteration_history):
            return {
                'iteration': iteration,
                'solution': self.iteration_history[iteration],
                # error respecto a la iteracion anterior (0 para la primera)
                'error': self.error_history[iteration - 1] if iteration > 0 else 0,
                # convergencia respecto a la iteracion anterior
                'convergence': self.convergence_history[iteration - 1] if iteration > 0 else float('inf')
            }
        # retornar diccionario vacio si el indice no es valido
        return {}
    
    def generate_step_by_step(self, A: np.ndarray, b: np.ndarray) -> List[Dict]:
        """
        genera explicacion paso a paso del metodo
        """
        # resolver el sistema para obtener el historial completo
        result = self.solve(A, b)
        steps = []
        n = len(A)
        
        # paso inicial: mostrar sistema original
        steps.append({
            'type': 'system',
            'title': 'sistema original',
            'content': f'resolver el sistema de {n} ecuaciones con {n} incognitas',
            'matrix_A': A.copy(),
            'vector_b': b.copy()
        })
        
        # explicar el metodo
        steps.append({
            'type': 'method',
            'title': 'metodo de gauss-seidel',
            'content': 'formula iterativa: x_i^(k+1) = (b_i - suma(a_ij * x_j^(k+1)) - suma(a_ij * x_j^(k))) / a_ii'
        })
        
        # generar pasos para las iteraciones (maximo 10 para evitar sobrecarga)
        for i in range(min(len(self.iteration_history) - 1, 10)):
            step_data = {
                'type': 'iteration',
                'title': f'iteracion {i + 1}',
                'iteration': i + 1,
                'solution': self.iteration_history[i + 1],
                'previous_solution': self.iteration_history[i] if i > 0 else np.zeros(n),
                'error': self.error_history[i] if i < len(self.error_history) else 0,
                'calculations': []
            }
            
            # generar calculos detallados para cada variable
            x_old = self.iteration_history[i].copy()  # valores anteriores
            x_new = self.iteration_history[i + 1].copy()  # valores actualizados
            
            # calcular cada componente del vector solucion
            for j in range(n):
                # suma de elementos ya actualizados
                sum1 = sum(A[j][k] * x_new[k] for k in range(j))
                # suma de elementos no actualizados
                sum2 = sum(A[j][k] * x_old[k] for k in range(j + 1, n))
                
                # crear informacion del calculo para esta variable
                calculation = {
                    'variable': j,
                    'formula': f'x{j+1} = ({b[j]:.3f}',
                    'sum1': sum1,
                    'sum2': sum2,
                    'result': x_new[j]
                }
                
                # agregar terminos de la formula si son diferentes de cero
                if sum1 != 0:
                    calculation['formula'] += f' - {sum1:.3f}'
                if sum2 != 0:
                    calculation['formula'] += f' - {sum2:.3f}'
                calculation['formula'] += f') / {A[j][j]:.3f} = {x_new[j]:.6f}'
                
                step_data['calculations'].append(calculation)
            
            steps.append(step_data)
        
        # agregar resultado final
        steps.append({
            'type': 'result',
            'title': 'resultado final',
            'converged': result['converged'],
            'solution': result['solution'],
            'iterations': result['iterations'],
            'final_error': result['final_error']
        })
        
        return steps