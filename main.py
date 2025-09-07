#!/usr/bin/env python3
"""
Aplicación para resolver sistemas de ecuaciones lineales usando el método de Gauss-Seidel
con interfaz gráfica moderna y visualización paso a paso.

Autor: AI Assistant
Fecha: 2024
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_deps = []
    
    try:
        import customtkinter
    except ImportError:
        missing_deps.append("customtkinter")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    if missing_deps:
        deps_str = ", ".join(missing_deps)
        error_msg = f"Faltan dependencias: {deps_str}\n\n"
        error_msg += "Por favor, instala las dependencias ejecutando:\n"
        error_msg += "pip install -r requirements.txt"
        
        # Mostrar error usando tkinter básico si customtkinter no está disponible
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Dependencias Faltantes", error_msg)
        root.destroy()
        return False
    
    return True

def main():
    """Función principal de la aplicación"""
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Importar después de verificar dependencias
        from gui.main_window import GaussSeidelApp
        
        # Crear y ejecutar la aplicación
        app = GaussSeidelApp()
        
        # Configurar el protocolo de cierre
        def on_closing():
            """Maneja el cierre de la aplicación"""
            if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
                app.quit()
                app.destroy()
                sys.exit(0)
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Mostrar mensaje de bienvenida
        print("="*60)
        print("🔢 RESOLVER SISTEMAS DE ECUACIONES - GAUSS-SEIDEL")
        print("="*60)
        print("✨ Interfaz gráfica moderna cargada exitosamente")
        print("📊 Visualización paso a paso habilitada")
        print("🚀 ¡La aplicación está lista para usar!")
        print("="*60)
        print()
        print("💡 Consejos de uso:")
        print("   • Para mejor convergencia, usa matrices diagonalmente dominantes")
        print("   • Ajusta la tolerancia según la precisión requerida")
        print("   • Usa el botón 'Ejemplo' para cargar sistemas de prueba")
        print("   • Navega entre iteraciones en la pestaña 'Proceso de Solución'")
        print()
        
        # Iniciar la aplicación
        app.mainloop()
        
    except ImportError as e:
        error_msg = f"Error al importar módulos: {str(e)}\n"
        error_msg += "Verifica que todos los archivos estén en sus carpetas correctas."
        print(f"❌ {error_msg}")
        
        # Mostrar también en GUI si es posible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error de Importación", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)
    
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"❌ {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()

