#!/usr/bin/env python3
"""
Script para probar sistemas de ecuaciones grandes y la responsividad 
de la nueva interfaz mejorada de Gauss-Seidel
"""

import numpy as np
import customtkinter as ctk
from gui.main_window import GaussSeidelApp
import tkinter.messagebox as messagebox

def create_diagonally_dominant_system(n):
    """Crea un sistema diagonalmente dominante de tamaño n×n"""
    # Crear matriz con elementos aleatorios
    A = np.random.rand(n, n) * 2 - 1  # Valores entre -1 y 1
    
    # Hacer la matriz diagonalmente dominante
    for i in range(n):
        row_sum = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        A[i, i] = row_sum + 1 + np.random.rand()  # Asegurar dominancia diagonal
    
    # Crear solución conocida
    x_true = np.random.rand(n) * 10 - 5  # Solución entre -5 y 5
    
    # Calcular vector b
    b = A.dot(x_true)
    
    return A, b, x_true

def load_test_system(app, size):
    """Carga un sistema de prueba en la aplicación"""
    A, b, x_true = create_diagonally_dominant_system(size)
    
    # Cambiar el tamaño del sistema en la app
    app.size_var.set(str(size))
    app.on_size_change(str(size))
    
    # Cargar la matriz
    app.matrix_input.set_values(A.tolist())
    
    # Cargar el vector
    app.vector_input.set_values(b.tolist())
    
    return x_true

class TestLargeSystemsApp(GaussSeidelApp):
    """Versión extendida de la app para pruebas de sistemas grandes"""
    
    def __init__(self):
        super().__init__()
        self.title("🧪 Prueba de Sistemas Grandes - Gauss-Seidel")
        self.add_test_menu()
    
    def add_test_menu(self):
        """Agrega menú de pruebas para sistemas grandes"""
        # Frame de pruebas en la parte superior
        test_frame = ctk.CTkFrame(self)
        test_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        test_title = ctk.CTkLabel(
            test_frame,
            text="🧪 Pruebas de Responsividad - Sistemas Grandes",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#d32f2f", "#f44336")
        )
        test_title.pack(side="left", padx=20, pady=15)
        
        # Botones de prueba
        buttons_frame = ctk.CTkFrame(test_frame)
        buttons_frame.pack(side="right", padx=20, pady=10)
        
        test_sizes = [3, 5, 7, 8, 10]
        for size in test_sizes:
            btn = ctk.CTkButton(
                buttons_frame,
                text=f"Probar {size}×{size}",
                command=lambda s=size: self.test_system_size(s),
                width=80,
                height=30,
                font=ctk.CTkFont(size=11)
            )
            btn.pack(side="left", padx=3, pady=5)
    
    def test_system_size(self, size):
        """Prueba un sistema de tamaño específico"""
        try:
            # Cargar sistema de prueba
            x_true = load_test_system(self, size)
            
            # Mostrar mensaje informativo
            message = f"""
🧪 Sistema de Prueba {size}×{size} Cargado

✅ Matriz diagonalmente dominante generada automáticamente
🎯 Solución conocida: {x_true[:3].round(3)}{"..." if size > 3 else ""}
📏 Layout optimizado: {'Maximizado automáticamente' if size >= 7 else 'Redimensionado' if size >= 5 else 'Tamaño normal'}

💡 Características probadas:
   • Campos responsivos: {self.get_field_info(size)}
   • Scroll inteligente: {'✅ Activado' if size > 4 else '❌ No necesario'}
   • Layout de 2 columnas: ✅ Términos independientes + Configuración

🚀 Presiona "RESOLVER SISTEMA" para probar la visualización paso a paso
            """
            
            messagebox.showinfo(f"Sistema {size}×{size} Cargado", message)
            
            # Forzar actualización de status
            self.update_status(f"🧪 Sistema de prueba {size}×{size} cargado exitosamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar sistema de prueba: {str(e)}")
    
    def get_field_info(self, size):
        """Obtiene información sobre los campos según el tamaño"""
        if size <= 3:
            return "85px/130px, fuente 12pt"
        elif size <= 5:
            return "70px/120px, fuente 11pt"
        elif size <= 7:
            return "58px/110px, fuente 10pt"
        else:
            return "48px/100px, fuente 9pt"

def main():
    """Ejecuta la aplicación de pruebas"""
    print("🧪 PRUEBA DE SISTEMAS GRANDES - GAUSS-SEIDEL")
    print("=" * 60)
    print()
    print("🎯 Esta aplicación te permite probar la responsividad")
    print("   de la interfaz con diferentes tamaños de sistemas.")
    print()
    print("📊 Características a probar:")
    print("   • Layout de 2 columnas (Términos independientes + Configuración)")
    print("   • Auto-redimensionado de ventana")
    print("   • Campos responsivos")
    print("   • Scroll inteligente")
    print("   • Visualización optimizada")
    print()
    print("🧪 Botones de prueba disponibles:")
    print("   • 3×3: Layout normal, campos amplios")
    print("   • 5×5: Ventana agrandada, campos medianos")  
    print("   • 7×7: Auto-maximización, scroll en matriz")
    print("   • 8×8: Scroll completo, campos compactos")
    print("   • 10×10: Ultra-compacto, todos los scrolls activos")
    print()
    print("🚀 ¡Iniciando aplicación de pruebas!")
    print("=" * 60)
    
    try:
        app = TestLargeSystemsApp()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
