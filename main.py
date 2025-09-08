#Andres Monsivais Salazar4
#Luis Andres Salinas Lozano

import sys
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
            if messagebox.askokcancel("Salir", "¿Estás segurisimoo de que quieres salir de aca?"):
                app.quit()
                app.destroy()
                sys.exit(0)
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
                
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
