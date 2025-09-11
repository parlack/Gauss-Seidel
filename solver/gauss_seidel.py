import numpy as np
from typing import List, Dict


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
        # historial de errores entre iteraciones consecutivas
        self.error_history = []
        # numero maximo de iteraciones permitidas
        self.max_iterations = 100
        # tolerancia para determinar convergencia
        self.tolerance = 0.000001

    def solve(self, A: np.ndarray, b: np.ndarray) -> Dict:
        """
        resuelve el sistema ax = b usando gauss-seidel

        args:
            a: matriz de coeficientes (n x n)
            b: vector de terminos independientes (n x 1)

        returns:
            dict con solucion, iteraciones, convergencia y errores
        """
        # obtener dimension del sistema
        n = len(A)

        # validar si la matriz es diagonalmente dominante
        if not self._is_diagonally_dominant(A):
            print("advertencia: la matriz no es diagonalmente dominante. la convergencia no esta garantizada.")

        # inicializar vector solucion con vector de ceros
        x = np.zeros(n)

        # limpiar historiales de iteraciones anteriores
        self.iteration_history = []
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

            # verificar si se alcanzo la convergencia
            if error < self.tolerance:
                return {
                    'solution': x,
                    'iterations': iteration + 1,
                    'converged': True,
                    'final_error': error,
                    'history': self.iteration_history,
                    'errors': self.error_history
                }

        # si no convergio en max_iterations, retornar resultado actual
        return {
            'solution': x,
            'iterations': self.max_iterations,
            'converged': False,
            'final_error': error,
            'history': self.iteration_history,
            'errors': self.error_history
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


    def _format_equation_term(self, coeff: float, var_index: int, is_first: bool) -> str:
        """Formatea un término de la ecuación"""
        if coeff == 0:
            return ""

        if is_first:
            if coeff == 1:
                return f"x{var_index + 1}"
            elif coeff == -1:
                return f"-x{var_index + 1}"
            else:
                return f"{coeff:.3f}x{var_index + 1}"
        else:
            if coeff > 0:
                if coeff == 1:
                    return f" + x{var_index + 1}"
                else:
                    return f" + {coeff:.3f}x{var_index + 1}"
            else:
                if coeff == -1:
                    return f" - x{var_index + 1}"
                else:
                    return f" - {abs(coeff):.3f}x{var_index + 1}"

    def _format_substitution_term(self, coeff: float, value: float, var_index: int, is_first: bool) -> str:
        """Formatea un término de la sustitución"""
        if coeff == 0:
            return ""

        if is_first:
            if coeff == 1:
                return f"({value:.6f})"
            elif coeff == -1:
                return f"-({value:.6f})"
            else:
                return f"{coeff:.3f}({value:.6f})"
        else:
            if coeff > 0:
                if coeff == 1:
                    return f" + ({value:.6f})"
                else:
                    return f" + {coeff:.3f}({value:.6f})"
            else:
                if coeff == -1:
                    return f" - ({value:.6f})"
                else:
                    return f" - {abs(coeff):.3f}({value:.6f})"

    def _create_equation_string(self, A_row: np.ndarray) -> str:
        """Crea la representación string de una ecuación"""
        n = len(A_row)
        equation_parts = []

        for j in range(n):
            term = self._format_equation_term(A_row[j], j, j == 0)
            if term:
                equation_parts.append(term)

        return "".join(equation_parts)

    def _create_substitution_string(self, A_row: np.ndarray, x: np.ndarray) -> str:
        """Crea la representación string de una sustitución"""
        n = len(A_row)
        substitution_parts = []

        for j in range(n):
            term = self._format_substitution_term(A_row[j], x[j], j, j == 0)
            if term:
                substitution_parts.append(term)

        return "".join(substitution_parts)

    def _verify_equation(self, A_row: np.ndarray, b_value: float, x: np.ndarray, eq_number: int) -> Dict:
        """Verifica una ecuación individual"""
        # calcular A[i] * x (producto punto de la fila i con el vector solucion)
        ax_value = sum(A_row[j] * x[j] for j in range(len(A_row)))

        # calcular residual para esta ecuación: |A*x - b|
        residual = abs(ax_value - b_value)

        # crear strings de ecuación y sustitución
        equation_str = self._create_equation_string(A_row)
        substitution_str = self._create_substitution_string(A_row, x)

        return {
            'equation_number': eq_number,
            'original_equation': f"{equation_str} = {b_value:.3f}",
            'substitution': f"{substitution_str} = {ax_value:.6f}",
            'expected_value': b_value,
            'calculated_value': ax_value,
            'residual': residual,
            'is_accurate': residual < 1e-10  # muy pequeño indica alta precision
        }

    def _verify_solution(self, A: np.ndarray, b: np.ndarray, x: np.ndarray) -> Dict:
        """
        verifica la solucion sustituyendo en el sistema original
        retorna informacion detallada de la verificacion
        """
        n = len(A)
        verification_data = {
            'equations': [],
            'ax_values': [],  # valores de A*x para cada ecuación
            'b_values': b.copy(),
            'residuals': [],  # diferencias |A*x - b| para cada ecuación
            'total_residual': 0.0
        }

        # verificar cada ecuación del sistema
        for i in range(n):
            eq_data = self._verify_equation(A[i], b[i], x, i + 1)
            verification_data['equations'].append(eq_data)
            verification_data['ax_values'].append(eq_data['calculated_value'])
            verification_data['residuals'].append(eq_data['residual'])

        # calcular residual total del sistema
        verification_data['total_residual'] = np.linalg.norm(verification_data['residuals'])

        return verification_data

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

        # verificar la solucion final sustituyendo en el sistema original
        verification_data = self._verify_solution(A, b, result['solution'])

        # agregar resultado final con verificacion
        steps.append({
            'type': 'result',
            'title': 'resultado final',
            'converged': result['converged'],
            'solution': result['solution'],
            'iterations': result['iterations'],
            'final_error': result['final_error'],
            'verification': verification_data,  # agregar datos de verificacion
            'original_matrix': A.copy(),
            'original_vector': b.copy()
        })

        return steps
