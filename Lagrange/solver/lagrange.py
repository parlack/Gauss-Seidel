import numpy as np
import math
from typing import List, Dict, Callable


class LagrangeSolver:
    """
    Solver de interpolación polinómica usando el método de Lagrange
    
    Este solver implementa la interpolación de Lagrange que construye
    un polinomio que pasa exactamente por todos los puntos dados.
    """

    def __init__(self):
        # Puntos de interpolación (x, y)
        self.points = []
        # Polinomios base de Lagrange calculados
        self.basis_polynomials = []
        # Coeficientes del polinomio interpolador
        self.coefficients = []
        # Historial de evaluaciones
        self.evaluation_history = []

    def set_points(self, x_values: List[float], y_values: List[float]) -> bool:
        """
        Establece los puntos de interpolación
        
        Args:
            x_values: Lista de coordenadas x
            y_values: Lista de coordenadas y
            
        Returns:
            True si los puntos son válidos, False en caso contrario
        """
        if len(x_values) != len(y_values):
            raise ValueError("Las listas de x e y deben tener la misma longitud")
        
        if len(x_values) < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar")
        
        # Verificar que no haya valores x duplicados
        if len(set(x_values)) != len(x_values):
            raise ValueError("Los valores de x deben ser únicos (no puede haber x duplicados)")
        
        # Guardar puntos ordenados por x
        self.points = sorted(zip(x_values, y_values), key=lambda p: p[0])
        return True

    def calculate_basis_polynomial(self, j: int, x: float) -> float:
        """
        Calcula el j-ésimo polinomio base de Lagrange evaluado en x
        
        L_j(x) = ∏(i≠j) (x - x_i) / (x_j - x_i)
        
        Args:
            j: Índice del polinomio base
            x: Punto donde evaluar
            
        Returns:
            Valor del polinomio base L_j(x)
        """
        n = len(self.points)
        result = 1.0
        
        x_j = self.points[j][0]
        
        for i in range(n):
            if i != j:
                x_i = self.points[i][0]
                result *= (x - x_i) / (x_j - x_i)
        
        return result

    def interpolate(self, x: float) -> float:
        """
        Evalúa el polinomio interpolador de Lagrange en un punto x
        
        P(x) = ∑(j=0 to n) y_j * L_j(x)
        
        Args:
            x: Punto donde evaluar el polinomio
            
        Returns:
            Valor interpolado P(x)
        """
        if not self.points:
            raise ValueError("No hay puntos de interpolación definidos")
        
        result = 0.0
        n = len(self.points)
        
        # Calcular suma de términos de Lagrange
        for j in range(n):
            y_j = self.points[j][1]
            L_j = self.calculate_basis_polynomial(j, x)
            result += y_j * L_j
        
        return result

    def generate_step_by_step(self, x_eval: float) -> List[Dict]:
        """
        Genera explicación paso a paso del proceso de interpolación
        
        Args:
            x_eval: Punto donde evaluar el polinomio
            
        Returns:
            Lista de pasos del proceso
        """
        if not self.points:
            return [{
                'type': 'error',
                'title': 'Error',
                'content': 'No hay puntos de interpolación definidos'
            }]
        
        steps = []
        n = len(self.points)
        
        # Paso 1: Mostrar puntos de interpolación
        steps.append({
            'type': 'points',
            'title': 'Puntos de Interpolación',
            'content': f'Se tienen {n} puntos para interpolar',
            'points': self.points.copy(),
            'n': n
        })
        
        # Calcular todos los polinomios base y sus contribuciones
        basis_values = []
        contributions = []
        basis_details = []
        
        for j in range(n):
            x_j, y_j = self.points[j]
            L_j = self.calculate_basis_polynomial(j, x_eval)
            contribution = y_j * L_j
            
            # Construir la fórmula de L_j(x) con fracciones
            numerator_terms = []
            denominator_terms = []
            numerator_values = []
            denominator_values = []
            
            for i in range(n):
                if i != j:
                    x_i = self.points[i][0]
                    # Términos simbólicos
                    numerator_terms.append(f"(x - {x_i:.3g})")
                    denominator_terms.append(f"({x_j:.3g} - {x_i:.3g})")
                    # Valores numéricos
                    numerator_values.append(x_eval - x_i)
                    denominator_values.append(x_j - x_i)
            
            # Calcular productos
            numerator_product = 1.0
            for val in numerator_values:
                numerator_product *= val
            
            denominator_product = 1.0
            for val in denominator_values:
                denominator_product *= val
            
            # Construir strings
            numerator_str = " × ".join(numerator_terms)
            denominator_str = " × ".join(denominator_terms)
            numerator_eval_str = " × ".join([f"{val:.3g}" for val in numerator_values])
            denominator_eval_str = " × ".join([f"{val:.3g}" for val in denominator_values])
            
            basis_values.append(L_j)
            contributions.append(contribution)
            basis_details.append({
                'j': j,
                'x_j': x_j,
                'y_j': y_j,
                'L_j': L_j,
                'contribution': contribution,
                'numerator_formula': numerator_str,
                'denominator_formula': denominator_str,
                'numerator_eval': numerator_eval_str,
                'denominator_eval': denominator_eval_str,
                'numerator_product': numerator_product,
                'denominator_product': denominator_product
            })
        
        # Paso 2: Mostrar todos los cálculos en una sola página
        steps.append({
            'type': 'calculations',
            'title': 'Cálculos de Interpolación',
            'x_eval': x_eval,
            'basis_details': basis_details,
            'n': n
        })
        
        # Paso 3: Calcular el valor final
        result = sum(contributions)
        
        # Construir la suma final
        terms = []
        for j in range(n):
            y_j = self.points[j][1]
            L_j = basis_values[j]
            terms.append(f"{y_j:.3f} × {L_j:.6f}")
        
        sum_str = " + ".join(terms)
        
        steps.append({
            'type': 'result',
            'title': 'Resultado Final',
            'x_eval': x_eval,
            'result': result,
            'calculation': f"P({x_eval:.3f}) = {sum_str} = {result:.6f}",
            'points': self.points.copy(),
            'contributions': contributions
        })
        
        return steps

    def get_polynomial_string(self) -> str:
        """
        Genera una representación en string del polinomio interpolador
        (forma expandida aproximada)
        
        Returns:
            String con el polinomio
        """
        if not self.points:
            return "P(x) = 0"
        
        # Para mostrar el polinomio, evaluamos en varios puntos
        # y mostramos la forma de Lagrange
        n = len(self.points)
        terms = []
        
        for j in range(n):
            x_j, y_j = self.points[j]
            
            # Construir término j
            numerator = []
            denominator = 1.0
            
            for i in range(n):
                if i != j:
                    x_i = self.points[i][0]
                    numerator.append(f"(x - {x_i:.2f})")
                    denominator *= (x_j - x_i)
            
            numerator_str = "×".join(numerator)
            term = f"{y_j:.2f} × [{numerator_str}] / {denominator:.2f}"
            terms.append(term)
        
        return "P(x) = " + " + ".join(terms)

    def evaluate_multiple_points(self, x_values: List[float]) -> List[Dict]:
        """
        Evalúa el polinomio en múltiples puntos
        
        Args:
            x_values: Lista de puntos donde evaluar
            
        Returns:
            Lista de diccionarios con x y P(x)
        """
        results = []
        for x in x_values:
            try:
                y = self.interpolate(x)
                results.append({
                    'x': x,
                    'y': y,
                    'valid': math.isfinite(y)
                })
            except Exception as e:
                results.append({
                    'x': x,
                    'y': None,
                    'valid': False,
                    'error': str(e)
                })
        
        return results

    def verify_interpolation(self) -> Dict:
        """
        Verifica que el polinomio pase por todos los puntos dados
        
        Returns:
            Diccionario con información de verificación
        """
        if not self.points:
            return {
                'valid': False,
                'message': 'No hay puntos de interpolación'
            }
        
        verification_data = []
        max_error = 0.0
        
        for i, (x_i, y_i) in enumerate(self.points):
            y_interp = self.interpolate(x_i)
            error = abs(y_interp - y_i)
            max_error = max(max_error, error)
            
            verification_data.append({
                'point_index': i,
                'x': x_i,
                'y_expected': y_i,
                'y_interpolated': y_interp,
                'error': error,
                'passes': error < 1e-10
            })
        
        all_pass = all(v['passes'] for v in verification_data)
        
        return {
            'valid': all_pass,
            'max_error': max_error,
            'verifications': verification_data,
            'message': 'El polinomio pasa por todos los puntos' if all_pass 
                      else f'Error máximo: {max_error:.2e}'
        }

