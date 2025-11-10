import numpy as np
from typing import Tuple, List


class DataValidator:
    """
    Validador de datos de entrada para interpolación de Lagrange
    """

    @staticmethod
    def validate_point_data(x_values: List, y_values: List) -> Tuple[bool, str, np.ndarray, np.ndarray]:
        """
        Valida los datos de puntos de interpolación
        
        Args:
            x_values: Lista de valores x
            y_values: Lista de valores y
            
        Returns:
            Tupla (es_válido, mensaje_error, x_array, y_array)
        """
        # Verificar que las listas no estén vacías
        if not x_values or not y_values:
            return False, "Las listas de puntos no pueden estar vacías", None, None
        
        # Verificar que tengan la misma longitud
        if len(x_values) != len(y_values):
            return False, f"Las listas deben tener la misma longitud (x: {len(x_values)}, y: {len(y_values)})", None, None
        
        # Verificar que haya al menos 2 puntos
        if len(x_values) < 2:
            return False, "Se necesitan al menos 2 puntos para interpolar", None, None
        
        # Intentar convertir a arrays de numpy
        try:
            x_array = np.array([float(x) for x in x_values])
            y_array = np.array([float(y) for y in y_values])
        except (ValueError, TypeError) as e:
            return False, f"Error al convertir valores a números: {str(e)}", None, None
        
        # Verificar que no haya NaN o infinitos
        if not np.all(np.isfinite(x_array)):
            return False, "Los valores de x deben ser números finitos (no NaN ni infinito)", None, None
        
        if not np.all(np.isfinite(y_array)):
            return False, "Los valores de y deben ser números finitos (no NaN ni infinito)", None, None
        
        # Verificar que no haya valores x duplicados
        if len(np.unique(x_array)) != len(x_array):
            duplicates = []
            seen = set()
            for i, x in enumerate(x_array):
                if x in seen:
                    duplicates.append((i, x))
                seen.add(x)
            
            dup_str = ", ".join([f"índice {i}: x={x:.3f}" for i, x in duplicates])
            return False, f"Los valores de x deben ser únicos. Duplicados encontrados: {dup_str}", None, None
        
        return True, "Datos válidos", x_array, y_array

    @staticmethod
    def validate_evaluation_point(x: str) -> Tuple[bool, str, float]:
        """
        Valida un punto de evaluación
        
        Args:
            x: Valor x como string
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_float)
        """
        if not x or not x.strip():
            return False, "El punto de evaluación no puede estar vacío", None
        
        try:
            x_val = float(x)
        except (ValueError, TypeError):
            return False, f"'{x}' no es un número válido", None
        
        if not np.isfinite(x_val):
            return False, "El punto de evaluación debe ser un número finito", None
        
        return True, "Punto válido", x_val

    @staticmethod
    def validate_number_of_points(n: str) -> Tuple[bool, str, int]:
        """
        Valida el número de puntos a usar
        
        Args:
            n: Número de puntos como string
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_int)
        """
        if not n or not n.strip():
            return False, "El número de puntos no puede estar vacío", None
        
        try:
            n_val = int(n)
        except (ValueError, TypeError):
            return False, f"'{n}' no es un número entero válido", None
        
        if n_val < 2:
            return False, "Se necesitan al menos 2 puntos para interpolar", None
        
        if n_val > 100:
            return False, "El número máximo de puntos es 100", None
        
        return True, "Número válido", n_val

    @staticmethod
    def check_interpolation_range(x_eval: float, x_points: np.ndarray) -> Tuple[bool, str]:
        """
        Verifica si el punto de evaluación está dentro del rango de interpolación
        
        Args:
            x_eval: Punto donde evaluar
            x_points: Array de puntos x de interpolación
            
        Returns:
            Tupla (está_en_rango, mensaje)
        """
        x_min = np.min(x_points)
        x_max = np.max(x_points)
        
        if x_eval < x_min or x_eval > x_max:
            return False, (f"⚠️ Advertencia: El punto x={x_eval:.3f} está fuera del rango de interpolación "
                          f"[{x_min:.3f}, {x_max:.3f}]. Esto es extrapolación y puede ser imprecisa.")
        
        return True, f"El punto está dentro del rango de interpolación [{x_min:.3f}, {x_max:.3f}]"

    @staticmethod
    def format_number(value: float, decimals: int = 6) -> str:
        """
        Formatea un número para mostrar
        
        Args:
            value: Valor a formatear
            decimals: Número de decimales
            
        Returns:
            String formateado
        """
        if not np.isfinite(value):
            return str(value)
        
        # Si el número es muy grande o muy pequeño, usar notación científica
        if abs(value) > 1e6 or (abs(value) < 1e-4 and value != 0):
            return f"{value:.{decimals}e}"
        
        return f"{value:.{decimals}f}"


