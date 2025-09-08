import numpy as np
import re
from typing import List, Tuple, Optional, Dict

class EquationValidator:
    """
    validador para ecuaciones lineales y matrices del metodo de gauss-seidel
    
    esta clase proporciona metodos estaticos para validar matrices, vectores
    y sistemas de ecuaciones, asi como para optimizar la matriz para convergencia
    """
    
    @staticmethod
    def validate_matrix(matrix_data: List[List[str]]) -> Tuple[bool, str, Optional[np.ndarray]]:
        """
        valida una matriz de coeficientes ingresada como strings
        
        args:
            matrix_data: lista de listas con strings representando la matriz
        
        returns:
            tuple con (es_valida, mensaje_error, matriz_numpy)
        """
        # verificar que la matriz no este vacia
        if not matrix_data or not matrix_data[0]:
            return False, "la matriz esta vacia", None
        
        # obtener dimensiones de la matriz
        n_rows = len(matrix_data)
        n_cols = len(matrix_data[0])
        
        # verificar que sea cuadrada (necesario para sistemas lineales)
        if n_rows != n_cols:
            return False, f"la matriz debe ser cuadrada. actual: {n_rows}x{n_cols}", None
        
        # verificar que todas las filas tengan el mismo numero de columnas
        for i, row in enumerate(matrix_data):
            if len(row) != n_cols:
                return False, f"fila {i+1} tiene {len(row)} elementos, esperado {n_cols}", None
        
        # convertir strings a numeros y validar
        try:
            matrix = np.zeros((n_rows, n_cols))
            # procesar cada elemento de la matriz
            for i in range(n_rows):
                for j in range(n_cols):
                    # verificar que no haya celdas vacias
                    if matrix_data[i][j].strip() == "":
                        return False, f"celda vacia en posicion ({i+1}, {j+1})", None
                    # convertir string a float
                    matrix[i][j] = float(matrix_data[i][j])
            
            # verificar que no haya ceros en la diagonal principal
            # (necesario para el metodo de gauss-seidel)
            for i in range(n_rows):
                if abs(matrix[i][i]) < 1e-10:
                    return False, f"elemento diagonal en posicion ({i+1}, {i+1}) es cero o muy pequeno", None
            
            return True, "matriz valida", matrix
            
        except ValueError as e:
            return False, f"error al convertir a numero: {str(e)}", None
    
    @staticmethod
    def validate_vector(vector_data: List[str]) -> Tuple[bool, str, Optional[np.ndarray]]:
        """
        valida un vector de terminos independientes
        
        args:
            vector_data: lista de strings representando el vector
        
        returns:
            tuple con (es_valido, mensaje_error, vector_numpy)
        """
        # verificar que el vector no este vacio
        if not vector_data:
            return False, "el vector esta vacio", None
        
        try:
            # crear vector numpy del tamano correcto
            vector = np.zeros(len(vector_data))
            # convertir cada elemento string a float
            for i, value in enumerate(vector_data):
                # verificar que no haya elementos vacios
                if value.strip() == "":
                    return False, f"elemento vacio en posicion {i+1}", None
                # convertir a numero
                vector[i] = float(value)
            
            return True, "vector valido", vector
            
        except ValueError as e:
            return False, f"error al convertir a numero: {str(e)}", None
    
    @staticmethod
    def parse_equation(equation: str) -> Tuple[bool, str, Optional[Tuple[List[float], float]]]:
        """
        parsea una ecuacion lineal del formato: ax + by + cz = d
        
        args:
            equation: string con la ecuacion a parsear
        
        returns:
            tuple con (es_valida, mensaje_error, (coeficientes, termino_independiente))
        """
        # verificar que la ecuacion no este vacia
        if not equation or equation.strip() == "":
            return False, "ecuacion vacia", None
        
        # limpiar espacios y convertir a minusculas
        eq = equation.replace(" ", "").lower()
        
        # verificar que tenga signo igual
        if "=" not in eq:
            return False, "la ecuacion debe contener el signo '='", None
        
        try:
            # dividir por el signo igual
            left_side, right_side = eq.split("=")
            
            # parsear el lado derecho (termino independiente)
            b_value = float(right_side)
            
            # parsear el lado izquierdo
            # agregar + al inicio si no empieza con signo
            if not left_side.startswith(('+', '-')):
                left_side = '+' + left_side
            
            # encontrar terminos usando expresiones regulares
            pattern = r'([+-]?)([0-9]*\.?[0-9]*)\*?([a-z])'
            matches = re.findall(pattern, left_side)
            
            if not matches:
                return False, "no se encontraron variables validas", None
            
            # extraer coeficientes de cada variable
            coefficients = {}
            for sign, coef, var in matches:
                # determinar signo
                sign_val = -1 if sign == '-' else 1
                
                # determinar coeficiente
                if coef == '' or coef == '+':
                    coef_val = 1.0
                elif coef == '-':
                    coef_val = -1.0
                else:
                    coef_val = float(coef)
                
                # calcular coeficiente final con signo
                final_coef = sign_val * coef_val
                
                # verificar que la variable no aparezca repetida
                if var in coefficients:
                    return False, f"variable '{var}' aparece multiples veces", None
                
                coefficients[var] = final_coef
            
            return True, "ecuacion valida", (coefficients, b_value)
            
        except Exception as e:
            return False, f"error al parsear la ecuacion: {str(e)}", None
    
    @staticmethod
    def equations_to_matrix(equations: List[str]) -> Tuple[bool, str, Optional[Tuple[np.ndarray, np.ndarray]]]:
        """
        convierte una lista de ecuaciones a formato matricial ax = b
        
        args:
            equations: lista de strings con las ecuaciones
        
        returns:
            tuple con (es_valido, mensaje_error, (matriz_a, vector_b))
        """
        # verificar que la lista no este vacia
        if not equations:
            return False, "lista de ecuaciones vacia", None
        
        n = len(equations)
        parsed_equations = []
        all_variables = set()
        
        # parsear todas las ecuaciones
        for i, eq in enumerate(equations):
            is_valid, error_msg, parsed = EquationValidator.parse_equation(eq)
            if not is_valid:
                return False, f"error en ecuacion {i+1}: {error_msg}", None
            
            # extraer coeficientes y termino independiente
            coeffs, b_val = parsed
            parsed_equations.append((coeffs, b_val))
            # recopilar todas las variables del sistema
            all_variables.update(coeffs.keys())
        
        # verificar que tengamos exactamente n variables para n ecuaciones
        if len(all_variables) != n:
            return False, f"se esperan {n} variables para {n} ecuaciones, encontradas: {len(all_variables)}", None
        
        # ordenar variables alfabeticamente para consistencia
        sorted_vars = sorted(list(all_variables))
        
        # construir matriz a y vector b
        A = np.zeros((n, n))
        b = np.zeros(n)
        
        # llenar matriz y vector con los coeficientes parseados
        for i, (coeffs, b_val) in enumerate(parsed_equations):
            b[i] = b_val
            # para cada variable, buscar su coeficiente (0 si no existe)
            for j, var in enumerate(sorted_vars):
                A[i][j] = coeffs.get(var, 0.0)
        
        return True, "conversion exitosa", (A, b)
    
    @staticmethod
    def make_diagonally_dominant(A: np.ndarray, b: np.ndarray) -> Dict:
        """
        intenta hacer la matriz diagonalmente dominante intercambiando filas
        
        la dominancia diagonal es importante para garantizar convergencia en gauss-seidel
        una matriz es diagonalmente dominante si |a_ii| > suma(|a_ij|) para i!=j
        
        args:
            A: matriz de coeficientes
            b: vector de terminos independientes
        
        returns:
            dict con resultado de la operacion:
            - success: bool - si se logro hacer diagonalmente dominante
            - matrix: np.ndarray - matriz reordenada (o original si no se pudo)
            - vector: np.ndarray - vector reordenado (o original si no se pudo)
            - swaps_made: list[tuple] - lista de intercambios realizados
            - message: str - mensaje explicativo
        """
        n = len(A)
        # hacer copias para no modificar los originales
        A_work = A.copy()
        b_work = b.copy()
        swaps_made = []
        
        # verificar si ya es diagonalmente dominante
        if EquationValidator._is_diagonally_dominant_static(A_work):
            return {
                'success': True,
                'matrix': A_work,
                'vector': b_work,
                'swaps_made': [],
                'message': 'la matriz ya es diagonalmente dominante'
            }
        
        # intentar hacer diagonalmente dominante intercambiando filas
        for i in range(n):
            # verificar si la fila actual es diagonalmente dominante
            diagonal_element = abs(A_work[i, i])
            off_diagonal_sum = sum(abs(A_work[i, j]) for j in range(n) if j != i)
            
            # si no es dominante, buscar una mejor fila
            if diagonal_element <= off_diagonal_sum:
                # buscar una fila que pueda mejorar la dominancia diagonal
                best_row = -1
                best_ratio = 0
                
                # examinar filas restantes
                for k in range(i + 1, n):
                    # verificar si intercambiar con la fila k mejoraria la dominancia
                    element_ki = abs(A_work[k, i])
                    off_diag_k = sum(abs(A_work[k, j]) for j in range(n) if j != i)
                    
                    # calcular ratio de dominancia potencial
                    if element_ki > 0 and off_diag_k > 0:
                        ratio = element_ki / off_diag_k
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_row = k
                
                # si encontramos una fila mejor, intercambiar
                if best_row != -1 and best_ratio > diagonal_element / off_diagonal_sum:
                    # intercambiar filas en matriz y vector
                    A_work[[i, best_row]] = A_work[[best_row, i]]
                    b_work[[i, best_row]] = b_work[[best_row, i]]
                    swaps_made.append((i, best_row))
        
        # verificar si ahora es diagonalmente dominante
        is_dominant = EquationValidator._is_diagonally_dominant_static(A_work)
        
        if is_dominant:
            return {
                'success': True,
                'matrix': A_work,
                'vector': b_work,
                'swaps_made': swaps_made,
                'message': f'matriz hecha diagonalmente dominante intercambiando {len(swaps_made)} fila(s)'
            }
        else:
            # intentar estrategia mas agresiva: buscar la mejor permutacion posible
            best_A, best_b, best_swaps = EquationValidator._find_best_permutation(A, b)
            
            if EquationValidator._is_diagonally_dominant_static(best_A):
                return {
                    'success': True,
                    'matrix': best_A,
                    'vector': best_b,
                    'swaps_made': best_swaps,
                    'message': f'matriz optimizada para dominancia diagonal con {len(best_swaps)} intercambio(s)'
                }
            else:
                # no se pudo optimizar, devolver originales
                return {
                    'success': False,
                    'matrix': A,  # devolver matriz original
                    'vector': b,  # devolver vector original
                    'swaps_made': [],
                    'message': 'no es posible hacer la matriz diagonalmente dominante intercambiando filas'
                }
    
    @staticmethod
    def _is_diagonally_dominant_static(A: np.ndarray) -> bool:
        """verifica si la matriz es diagonalmente dominante (version estatica)"""
        n = len(A)
        # verificar cada fila de la matriz
        for i in range(n):
            # elemento diagonal
            diagonal = abs(A[i, i])
            # suma de elementos fuera de la diagonal
            off_diagonal_sum = sum(abs(A[i, j]) for j in range(n) if i != j)
            # verificar condicion de dominancia: |a_ii| > suma(|a_ij|)
            if diagonal <= off_diagonal_sum:
                return False
        return True
    
    @staticmethod
    def _find_best_permutation(A: np.ndarray, b: np.ndarray) -> Tuple[np.ndarray, np.ndarray, List[Tuple]]:
        """
        encuentra la mejor permutacion de filas para maximizar la dominancia diagonal
        usa un enfoque greedy optimizado
        
        este metodo intenta todas las combinaciones posibles de intercambio de filas
        para encontrar la configuracion que maximice la dominancia diagonal
        
        args:
            A: matriz original
            b: vector original
        
        returns:
            tuple con (matriz_optimizada, vector_optimizado, lista_intercambios)
        """
        n = len(A)
        # hacer copias para trabajar
        A_best = A.copy()
        b_best = b.copy()
        used_rows = set()
        swaps_made = []
        
        # para cada posicion diagonal, encontrar la mejor fila
        for i in range(n):
            # saltar si ya procesamos esta fila
            if i in used_rows:
                continue
                
            # empezar con la fila actual como la mejor
            best_row = i
            # calcular score de dominancia actual (evitar division por cero)
            best_score = abs(A_best[i, i]) / (sum(abs(A_best[i, j]) for j in range(n) if j != i) + 1e-10)
            
            # buscar en filas no usadas
            for k in range(i + 1, n):
                if k in used_rows:
                    continue
                    
                # calcular score si ponemos la fila k en la posicion i
                diagonal_val = abs(A[k, i])
                off_diagonal_sum = sum(abs(A[k, j]) for j in range(n) if j != i)
                
                # calcular ratio de dominancia
                if off_diagonal_sum > 0:
                    score = diagonal_val / off_diagonal_sum
                    # si es mejor que el actual, actualizar
                    if score > best_score:
                        best_score = score
                        best_row = k
            
            # si encontramos una mejor fila, intercambiar
            if best_row != i:
                A_best[[i, best_row]] = A_best[[best_row, i]]
                b_best[[i, best_row]] = b_best[[best_row, i]]
                swaps_made.append((i, best_row))
                used_rows.add(best_row)
            
            # marcar fila actual como usada
            used_rows.add(i)
        
        return A_best, b_best, swaps_made
