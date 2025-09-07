import numpy as np
import re
from typing import List, Tuple, Optional, Dict

class EquationValidator:
    """Validador para ecuaciones lineales y matrices"""
    
    @staticmethod
    def validate_matrix(matrix_data: List[List[str]]) -> Tuple[bool, str, Optional[np.ndarray]]:
        """
        Valida una matriz de coeficientes ingresada como strings
        
        Returns:
            (es_valida, mensaje_error, matriz_numpy)
        """
        if not matrix_data or not matrix_data[0]:
            return False, "La matriz está vacía", None
        
        n_rows = len(matrix_data)
        n_cols = len(matrix_data[0])
        
        # Verificar que sea cuadrada
        if n_rows != n_cols:
            return False, f"La matriz debe ser cuadrada. Actual: {n_rows}x{n_cols}", None
        
        # Verificar que todas las filas tengan el mismo número de columnas
        for i, row in enumerate(matrix_data):
            if len(row) != n_cols:
                return False, f"Fila {i+1} tiene {len(row)} elementos, esperado {n_cols}", None
        
        # Convertir a números y validar
        try:
            matrix = np.zeros((n_rows, n_cols))
            for i in range(n_rows):
                for j in range(n_cols):
                    if matrix_data[i][j].strip() == "":
                        return False, f"Celda vacía en posición ({i+1}, {j+1})", None
                    matrix[i][j] = float(matrix_data[i][j])
            
            # Verificar que no haya ceros en la diagonal principal
            for i in range(n_rows):
                if abs(matrix[i][i]) < 1e-10:
                    return False, f"Elemento diagonal en posición ({i+1}, {i+1}) es cero o muy pequeño", None
            
            return True, "Matriz válida", matrix
            
        except ValueError as e:
            return False, f"Error al convertir a número: {str(e)}", None
    
    @staticmethod
    def validate_vector(vector_data: List[str]) -> Tuple[bool, str, Optional[np.ndarray]]:
        """
        Valida un vector de términos independientes
        
        Returns:
            (es_valido, mensaje_error, vector_numpy)
        """
        if not vector_data:
            return False, "El vector está vacío", None
        
        try:
            vector = np.zeros(len(vector_data))
            for i, value in enumerate(vector_data):
                if value.strip() == "":
                    return False, f"Elemento vacío en posición {i+1}", None
                vector[i] = float(value)
            
            return True, "Vector válido", vector
            
        except ValueError as e:
            return False, f"Error al convertir a número: {str(e)}", None
    
    @staticmethod
    def parse_equation(equation: str) -> Tuple[bool, str, Optional[Tuple[List[float], float]]]:
        """
        Parsea una ecuación lineal del formato: ax + by + cz = d
        
        Returns:
            (es_valida, mensaje_error, (coeficientes, termino_independiente))
        """
        if not equation or equation.strip() == "":
            return False, "Ecuación vacía", None
        
        # Limpiar espacios y convertir a minúsculas
        eq = equation.replace(" ", "").lower()
        
        # Verificar que tenga signo igual
        if "=" not in eq:
            return False, "La ecuación debe contener el signo '='", None
        
        try:
            # Dividir por el signo igual
            left_side, right_side = eq.split("=")
            
            # Parsear el lado derecho (término independiente)
            b_value = float(right_side)
            
            # Parsear el lado izquierdo
            # Agregar + al inicio si no empieza con signo
            if not left_side.startswith(('+', '-')):
                left_side = '+' + left_side
            
            # Encontrar términos usando regex
            pattern = r'([+-]?)([0-9]*\.?[0-9]*)\*?([a-z])'
            matches = re.findall(pattern, left_side)
            
            if not matches:
                return False, "No se encontraron variables válidas", None
            
            # Extraer coeficientes
            coefficients = {}
            for sign, coef, var in matches:
                # Determinar signo
                sign_val = -1 if sign == '-' else 1
                
                # Determinar coeficiente
                if coef == '' or coef == '+':
                    coef_val = 1.0
                elif coef == '-':
                    coef_val = -1.0
                else:
                    coef_val = float(coef)
                
                final_coef = sign_val * coef_val
                
                if var in coefficients:
                    return False, f"Variable '{var}' aparece múltiples veces", None
                
                coefficients[var] = final_coef
            
            return True, "Ecuación válida", (coefficients, b_value)
            
        except Exception as e:
            return False, f"Error al parsear la ecuación: {str(e)}", None
    
    @staticmethod
    def equations_to_matrix(equations: List[str]) -> Tuple[bool, str, Optional[Tuple[np.ndarray, np.ndarray]]]:
        """
        Convierte una lista de ecuaciones a formato matricial Ax = b
        
        Returns:
            (es_valido, mensaje_error, (matriz_A, vector_b))
        """
        if not equations:
            return False, "Lista de ecuaciones vacía", None
        
        n = len(equations)
        parsed_equations = []
        all_variables = set()
        
        # Parsear todas las ecuaciones
        for i, eq in enumerate(equations):
            is_valid, error_msg, parsed = EquationValidator.parse_equation(eq)
            if not is_valid:
                return False, f"Error en ecuación {i+1}: {error_msg}", None
            
            coeffs, b_val = parsed
            parsed_equations.append((coeffs, b_val))
            all_variables.update(coeffs.keys())
        
        # Verificar que tengamos exactamente n variables para n ecuaciones
        if len(all_variables) != n:
            return False, f"Se esperan {n} variables para {n} ecuaciones, encontradas: {len(all_variables)}", None
        
        # Ordenar variables alfabéticamente
        sorted_vars = sorted(list(all_variables))
        
        # Construir matriz A y vector b
        A = np.zeros((n, n))
        b = np.zeros(n)
        
        for i, (coeffs, b_val) in enumerate(parsed_equations):
            b[i] = b_val
            for j, var in enumerate(sorted_vars):
                A[i][j] = coeffs.get(var, 0.0)
        
        return True, "Conversión exitosa", (A, b)
    
    @staticmethod
    def make_diagonally_dominant(A: np.ndarray, b: np.ndarray) -> Dict:
        """
        Intenta hacer la matriz diagonalmente dominante intercambiando filas
        
        Returns:
            Dict con resultado de la operación:
            - success: bool - Si se logró hacer diagonalmente dominante
            - matrix: np.ndarray - Matriz reordenada (o original si no se pudo)
            - vector: np.ndarray - Vector reordenado (o original si no se pudo)
            - swaps_made: List[Tuple] - Lista de intercambios realizados
            - message: str - Mensaje explicativo
        """
        n = len(A)
        A_work = A.copy()
        b_work = b.copy()
        swaps_made = []
        
        # Verificar si ya es diagonalmente dominante
        if EquationValidator._is_diagonally_dominant_static(A_work):
            return {
                'success': True,
                'matrix': A_work,
                'vector': b_work,
                'swaps_made': [],
                'message': 'La matriz ya es diagonalmente dominante'
            }
        
        # Intentar hacer diagonalmente dominante intercambiando filas
        for i in range(n):
            # Si la fila actual no es diagonalmente dominante
            diagonal_element = abs(A_work[i, i])
            off_diagonal_sum = sum(abs(A_work[i, j]) for j in range(n) if j != i)
            
            if diagonal_element <= off_diagonal_sum:
                # Buscar una fila que pueda mejorar la dominancia diagonal
                best_row = -1
                best_ratio = 0
                
                for k in range(i + 1, n):
                    # Verificar si intercambiar con la fila k mejoraría la dominancia
                    element_ki = abs(A_work[k, i])
                    off_diag_k = sum(abs(A_work[k, j]) for j in range(n) if j != i)
                    
                    if element_ki > 0 and off_diag_k > 0:
                        ratio = element_ki / off_diag_k
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_row = k
                
                # Si encontramos una fila mejor, intercambiar
                if best_row != -1 and best_ratio > diagonal_element / off_diagonal_sum:
                    # Intercambiar filas
                    A_work[[i, best_row]] = A_work[[best_row, i]]
                    b_work[[i, best_row]] = b_work[[best_row, i]]
                    swaps_made.append((i, best_row))
        
        # Verificar si ahora es diagonalmente dominante
        is_dominant = EquationValidator._is_diagonally_dominant_static(A_work)
        
        if is_dominant:
            return {
                'success': True,
                'matrix': A_work,
                'vector': b_work,
                'swaps_made': swaps_made,
                'message': f'Matriz hecha diagonalmente dominante intercambiando {len(swaps_made)} fila(s)'
            }
        else:
            # Intentar estrategia más agresiva: buscar la mejor permutación posible
            best_A, best_b, best_swaps = EquationValidator._find_best_permutation(A, b)
            
            if EquationValidator._is_diagonally_dominant_static(best_A):
                return {
                    'success': True,
                    'matrix': best_A,
                    'vector': best_b,
                    'swaps_made': best_swaps,
                    'message': f'Matriz optimizada para dominancia diagonal con {len(best_swaps)} intercambio(s)'
                }
            else:
                return {
                    'success': False,
                    'matrix': A,  # Devolver matriz original
                    'vector': b,  # Devolver vector original
                    'swaps_made': [],
                    'message': 'No es posible hacer la matriz diagonalmente dominante intercambiando filas'
                }
    
    @staticmethod
    def _is_diagonally_dominant_static(A: np.ndarray) -> bool:
        """Verifica si la matriz es diagonalmente dominante (versión estática)"""
        n = len(A)
        for i in range(n):
            diagonal = abs(A[i, i])
            off_diagonal_sum = sum(abs(A[i, j]) for j in range(n) if i != j)
            if diagonal <= off_diagonal_sum:
                return False
        return True
    
    @staticmethod
    def _find_best_permutation(A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray, List[Tuple]]:
        """
        Encuentra la mejor permutación de filas para maximizar la dominancia diagonal
        Usa un enfoque greedy optimizado
        """
        n = len(A)
        A_best = A.copy()
        b_best = b.copy()
        used_rows = set()
        swaps_made = []
        
        # Para cada posición diagonal, encontrar la mejor fila
        for i in range(n):
            if i in used_rows:
                continue
                
            best_row = i
            best_score = abs(A_best[i, i]) / (sum(abs(A_best[i, j]) for j in range(n) if j != i) + 1e-10)
            
            # Buscar en filas no usadas
            for k in range(i + 1, n):
                if k in used_rows:
                    continue
                    
                # Calcular score si ponemos la fila k en la posición i
                diagonal_val = abs(A[k, i])
                off_diagonal_sum = sum(abs(A[k, j]) for j in range(n) if j != i)
                
                if off_diagonal_sum > 0:
                    score = diagonal_val / off_diagonal_sum
                    if score > best_score:
                        best_score = score
                        best_row = k
            
            # Si encontramos una mejor fila, intercambiar
            if best_row != i:
                A_best[[i, best_row]] = A_best[[best_row, i]]
                b_best[[i, best_row]] = b_best[[best_row, i]]
                swaps_made.append((i, best_row))
                used_rows.add(best_row)
            
            used_rows.add(i)
        
        return A_best, b_best, swaps_made
