#!/usr/bin/env python3
"""
Demostración específica de la funcionalidad de dominancia diagonal automática
en la aplicación Gauss-Seidel
"""

import numpy as np
from utils.validators import EquationValidator
from gui.main_window import GaussSeidelApp
import customtkinter as ctk

def demo_diagonal_dominance():
    """Demuestra la funcionalidad de hacer matrices diagonalmente dominantes"""
    print("🔧 DEMOSTRACIÓN: DOMINANCIA DIAGONAL AUTOMÁTICA")
    print("=" * 60)
    print()
    
    # Ejemplo 1: Sistema que puede hacerse diagonalmente dominante
    print("📋 Ejemplo 1: Sistema que PUEDE hacerse diagonalmente dominante")
    A1 = np.array([
        [1, 8, 2],   # 1 < 8+2 = 10, NO dominante
        [2, 1, 9],   # 1 < 2+9 = 11, NO dominante  
        [15, -1, 2]  # 15 > 1+2 = 3, SÍ dominante
    ])
    b1 = np.array([11, 12, 16])
    
    print("Matriz original:")
    print(A1)
    print("Vector b:", b1)
    print()
    
    result1 = EquationValidator.make_diagonally_dominant(A1, b1)
    print(f"Resultado: {result1['message']}")
    if result1['success']:
        print("Matriz optimizada:")
        print(result1['matrix'])
        print("Vector optimizado:", result1['vector'])
        print("Intercambios realizados:", result1['swaps_made'])
    print()
    print("-" * 60)
    print()
    
    # Ejemplo 2: Sistema que NO puede hacerse diagonalmente dominante
    print("📋 Ejemplo 2: Sistema que NO puede hacerse diagonalmente dominante")
    A2 = np.array([
        [1, 5, 3],   # 1 < 5+3 = 8
        [2, 1, 4],   # 1 < 2+4 = 6
        [3, 2, 1]    # 1 < 3+2 = 5
    ])
    b2 = np.array([9, 7, 6])
    
    print("Matriz original:")
    print(A2)
    print("Vector b:", b2)
    print()
    
    result2 = EquationValidator.make_diagonally_dominant(A2, b2)
    print(f"Resultado: {result2['message']}")
    print()
    print("-" * 60)
    print()
    
    # Ejemplo 3: Sistema ya diagonalmente dominante
    print("📋 Ejemplo 3: Sistema YA diagonalmente dominante")
    A3 = np.array([
        [10, -1, 2],   # 10 > 1+2 = 3, SÍ dominante
        [-1, 11, -1],  # 11 > 1+1 = 2, SÍ dominante
        [2, -1, 10]    # 10 > 2+1 = 3, SÍ dominante
    ])
    b3 = np.array([6, 25, -11])
    
    print("Matriz original:")
    print(A3)
    print("Vector b:", b3)
    print()
    
    result3 = EquationValidator.make_diagonally_dominant(A3, b3)
    print(f"Resultado: {result3['message']}")
    print()
    print("=" * 60)
    print()
    
    return [(A1, b1, result1), (A2, b2, result2), (A3, b3, result3)]

class DiagonalDominanceTestApp(GaussSeidelApp):
    """App extendida para demostrar dominancia diagonal"""
    
    def __init__(self):
        super().__init__()
        self.title("🔧 Demo: Dominancia Diagonal Automática - Gauss-Seidel")
        self.add_demo_controls()
        
        # Ejecutar demo al iniciar
        self.after(500, self.show_demo_info)
    
    def add_demo_controls(self):
        """Agrega controles específicos para la demo"""
        # Frame de demo en la parte superior
        demo_frame = ctk.CTkFrame(self)
        demo_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        demo_title = ctk.CTkLabel(
            demo_frame,
            text="🔧 DEMO: Dominancia Diagonal Automática",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        demo_title.pack(side="left", padx=20, pady=15)
        
        # Botones de demo
        buttons_frame = ctk.CTkFrame(demo_frame)
        buttons_frame.pack(side="right", padx=20, pady=10)
        
        demo_examples = [
            ("Ejemplo 1: Necesita reordenamiento", self.load_demo_1),
            ("Ejemplo 2: No se puede optimizar", self.load_demo_2),
            ("Ejemplo 3: Ya es dominante", self.load_demo_3)
        ]
        
        for text, command in demo_examples:
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                width=180,
                height=30,
                font=ctk.CTkFont(size=10)
            )
            btn.pack(side="left", padx=3, pady=5)
    
    def show_demo_info(self):
        """Muestra información inicial de la demo"""
        info_message = """
🔧 DEMOSTRACIÓN: DOMINANCIA DIAGONAL AUTOMÁTICA

🎯 Esta aplicación detecta automáticamente si un sistema de ecuaciones
   puede hacerse diagonalmente dominante intercambiando filas.

✨ FUNCIONALIDADES DEMOSTRADAS:

🔄 Auto-reordenamiento: Si es posible hacer la matriz diagonalmente dominante
   intercambiando filas, se hace automáticamente.

✅ Garantía de convergencia: Una matriz diagonalmente dominante asegura
   que el método de Gauss-Seidel converja.

⚠️ Advertencia inteligente: Si no se puede optimizar, se muestra una
   advertencia clara al usuario.

🧪 EJEMPLOS DISPONIBLES:
   • Ejemplo 1: Sistema que PUEDE optimizarse
   • Ejemplo 2: Sistema que NO puede optimizarse  
   • Ejemplo 3: Sistema YA optimizado

💡 INSTRUCCIONES:
   1. Haz clic en cualquier botón de ejemplo
   2. Presiona "✅ Validar" para ver la optimización automática
   3. O directamente "🚀 RESOLVER SISTEMA"

¡Prueba todos los ejemplos para ver diferentes comportamientos!
        """
        
        from tkinter import messagebox
        messagebox.showinfo("Bienvenido a la Demo", info_message)
    
    def load_demo_1(self):
        """Carga ejemplo que necesita reordenamiento"""
        self.size_var.set("3")
        self.on_size_change("3")
        
        matrix_values = [
            [1, 8, 2],     # NO dominante: 1 < 8+2
            [2, 1, 9],     # NO dominante: 1 < 2+9
            [15, -1, 2]    # SÍ dominante: 15 > 1+2
        ]
        vector_values = [11, 12, 16]
        
        self.matrix_input.set_values(matrix_values)
        self.vector_input.set_values(vector_values)
        self.update_status("🔧 Demo 1: Sistema que PUEDE hacerse diagonalmente dominante")
    
    def load_demo_2(self):
        """Carga ejemplo que NO puede optimizarse"""
        self.size_var.set("3")
        self.on_size_change("3")
        
        matrix_values = [
            [1, 5, 3],     # 1 < 5+3 = 8
            [2, 1, 4],     # 1 < 2+4 = 6
            [3, 2, 1]      # 1 < 3+2 = 5
        ]
        vector_values = [9, 7, 6]
        
        self.matrix_input.set_values(matrix_values)
        self.vector_input.set_values(vector_values)
        self.update_status("⚠️ Demo 2: Sistema que NO puede hacerse diagonalmente dominante")
    
    def load_demo_3(self):
        """Carga ejemplo ya dominante"""
        self.size_var.set("3")
        self.on_size_change("3")
        
        matrix_values = [
            [10, -1, 2],   # 10 > 1+2 = 3 ✅
            [-1, 11, -1],  # 11 > 1+1 = 2 ✅
            [2, -1, 10]    # 10 > 2+1 = 3 ✅
        ]
        vector_values = [6, 25, -11]
        
        self.matrix_input.set_values(matrix_values)
        self.vector_input.set_values(vector_values)
        self.update_status("✅ Demo 3: Sistema YA diagonalmente dominante")

def main():
    """Ejecuta la demostración"""
    print("🚀 Iniciando demostración de dominancia diagonal...")
    
    # Primero ejecutar demo en consola
    demo_examples = demo_diagonal_dominance()
    
    print("🎨 Ahora iniciando interfaz gráfica interactiva...")
    print("💡 Prueba los diferentes ejemplos con los botones de la interfaz")
    print()
    
    try:
        app = DiagonalDominanceTestApp()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

