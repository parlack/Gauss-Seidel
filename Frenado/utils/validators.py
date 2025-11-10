# Andres Monsivais Salazar
# Luis Andres Salinas Lozano

import numpy as np
from typing import Tuple, List


class FrenadoValidator:
    """
    Validador de datos de entrada para el sistema de análisis de frenado
    
    Valida datos de velocidad, distancia de frenado y límites de seguridad
    """

    @staticmethod
    def validate_point_data(velocidades: List, distancias: List) -> Tuple[bool, str, np.ndarray, np.ndarray]:
        """
        Valida los datos de velocidad y distancia de frenado
        
        Args:
            velocidades: Lista de velocidades (km/h)
            distancias: Lista de distancias de frenado (metros)
            
        Returns:
            Tupla (es_válido, mensaje_error, velocidades_array, distancias_array)
        """
        # Verificar que las listas no estén vacías
        if not velocidades or not distancias:
            return False, "Las listas de datos no pueden estar vacías", None, None
        
        # Verificar que tengan la misma longitud
        if len(velocidades) != len(distancias):
            return False, f"Las listas deben tener la misma longitud (velocidades: {len(velocidades)}, distancias: {len(distancias)})", None, None
        
        # Verificar que haya al menos 2 puntos
        if len(velocidades) < 2:
            return False, "Se necesitan al menos 2 puntos de datos experimentales", None, None
        
        # Intentar convertir a arrays de numpy
        try:
            vel_array = np.array([float(v) for v in velocidades])
            dist_array = np.array([float(d) for d in distancias])
        except (ValueError, TypeError) as e:
            return False, f"Error al convertir valores a números: {str(e)}", None, None
        
        # Verificar que no haya NaN o infinitos
        if not np.all(np.isfinite(vel_array)):
            return False, "Las velocidades deben ser números finitos (no NaN ni infinito)", None, None
        
        if not np.all(np.isfinite(dist_array)):
            return False, "Las distancias deben ser números finitos (no NaN ni infinito)", None, None
        
        # Verificar que las velocidades sean positivas
        if np.any(vel_array <= 0):
            return False, "Las velocidades deben ser mayores que cero", None, None
        
        # Verificar que las distancias sean no negativas
        if np.any(dist_array < 0):
            return False, "Las distancias de frenado no pueden ser negativas", None, None
        
        # Verificar que no haya velocidades duplicadas
        if len(np.unique(vel_array)) != len(vel_array):
            duplicates = []
            seen = set()
            for i, v in enumerate(vel_array):
                if v in seen:
                    duplicates.append((i, v))
                seen.add(v)
            
            dup_str = ", ".join([f"índice {i}: {v:.1f} km/h" for i, v in duplicates])
            return False, f"Las velocidades deben ser únicas. Duplicados: {dup_str}", None, None
        
        # Verificar rangos razonables
        if np.any(vel_array > 300):
            return False, "Las velocidades deben ser menores a 300 km/h (rango realista)", None, None
        
        if np.any(dist_array > 500):
            return False, "Las distancias de frenado deben ser menores a 500 metros (rango realista)", None, None
        
        return True, "Datos válidos", vel_array, dist_array

    @staticmethod
    def validate_velocity(v: str) -> Tuple[bool, str, float]:
        """
        Valida una velocidad de entrada
        
        Args:
            v: Velocidad como string (km/h)
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_float)
        """
        if not v or not v.strip():
            return False, "La velocidad no puede estar vacía", None
        
        try:
            v_val = float(v)
        except (ValueError, TypeError):
            return False, f"'{v}' no es un número válido", None
        
        if not np.isfinite(v_val):
            return False, "La velocidad debe ser un número finito", None
        
        if v_val <= 0:
            return False, "La velocidad debe ser mayor que cero", None
        
        if v_val > 300:
            return False, "La velocidad debe ser menor a 300 km/h (rango realista)", None
        
        return True, "Velocidad válida", v_val

    @staticmethod
    def validate_distance(d: str) -> Tuple[bool, str, float]:
        """
        Valida una distancia de frenado
        
        Args:
            d: Distancia como string (metros)
            
        Returns:
            Tupla (es_válido, mensaje_error, valor_float)
        """
        if not d or not d.strip():
            return False, "La distancia no puede estar vacía", None
        
        try:
            d_val = float(d)
        except (ValueError, TypeError):
            return False, f"'{d}' no es un número válido", None
        
        if not np.isfinite(d_val):
            return False, "La distancia debe ser un número finito", None
        
        if d_val < 0:
            return False, "La distancia de frenado no puede ser negativa", None
        
        if d_val > 500:
            return False, "La distancia debe ser menor a 500 metros (rango realista)", None
        
        return True, "Distancia válida", d_val

    @staticmethod
    def validate_interval(a: str, b: str) -> Tuple[bool, str, float, float]:
        """
        Valida un intervalo de búsqueda para bisección
        
        Args:
            a: Límite inferior como string
            b: Límite superior como string
            
        Returns:
            Tupla (es_válido, mensaje_error, a_float, b_float)
        """
        # Validar límite inferior
        is_valid_a, msg_a, a_val = FrenadoValidator.validate_velocity(a)
        if not is_valid_a:
            return False, f"Límite inferior: {msg_a}", None, None
        
        # Validar límite superior
        is_valid_b, msg_b, b_val = FrenadoValidator.validate_velocity(b)
        if not is_valid_b:
            return False, f"Límite superior: {msg_b}", None, None
        
        # Verificar que a < b
        if a_val >= b_val:
            return False, f"El límite inferior ({a_val:.1f}) debe ser menor que el superior ({b_val:.1f})", None, None
        
        # Verificar que el intervalo no sea demasiado pequeño
        if b_val - a_val < 1.0:
            return False, "El intervalo debe ser al menos de 1 km/h de ancho", None, None
        
        return True, "Intervalo válido", a_val, b_val

    @staticmethod
    def validate_number_of_points(n: str) -> Tuple[bool, str, int]:
        """
        Valida el número de puntos experimentales
        
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
            return False, "Se necesitan al menos 2 puntos de datos", None
        
        if n_val > 20:
            return False, "El número máximo de puntos es 20", None
        
        return True, "Número válido", n_val

    @staticmethod
    def check_interpolation_range(v_eval: float, v_points: np.ndarray) -> Tuple[bool, str]:
        """
        Verifica si la velocidad de evaluación está dentro del rango de interpolación
        
        Args:
            v_eval: Velocidad donde evaluar
            v_points: Array de velocidades de datos experimentales
            
        Returns:
            Tupla (está_en_rango, mensaje)
        """
        v_min = np.min(v_points)
        v_max = np.max(v_points)
        
        if v_eval < v_min or v_eval > v_max:
            return False, (f"⚠️ Advertencia: La velocidad {v_eval:.1f} km/h está fuera del rango experimental "
                          f"[{v_min:.1f}, {v_max:.1f}] km/h. Esto es extrapolación y puede ser imprecisa.")
        
        return True, f"La velocidad está dentro del rango experimental [{v_min:.1f}, {v_max:.1f}] km/h"

    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
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

