# Andres Monsivais Salazar
# Luis Andres Salinas Lozano

import sys
import tkinter as tk
from tkinter import messagebox


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_deps = []

    try:
        import customtkinter  # noqa: F401
    except ImportError:
        missing_deps.append("customtkinter")

    try:
        import numpy  # noqa: F401
    except ImportError:
        missing_deps.append("numpy")

    if missing_deps:
        deps_str = ", ".join(missing_deps)
        error_msg = f"Faltan dependencias: {deps_str}\n\n"
        error_msg += "Por favor, instala las dependencias ejecutando:\n"
        error_msg += "pip install -r requirements.txt"

        # Mostrar error usando tkinter básico si customtkinter no está
        # disponible
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Dependencias Faltantes", error_msg)
        root.destroy()
        return False

    return True


def show_error_dialog(title: str, message: str):
    """Muestra un diálogo de error usando tkinter"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        pass


def setup_closing_protocol(app):
    """Configura el protocolo de cierre de la aplicación"""
    def on_closing():
        """Maneja el cierre de la aplicación"""
        question = "¿Estás segurisimoo de que quieres salir de aca?"
        if messagebox.askokcancel("Salir", question):
            app.quit()
            app.destroy()
            sys.exit(0)

    app.protocol("WM_DELETE_WINDOW", on_closing)


def run_application():
    """Ejecuta la aplicación principal"""
    from gui.main_window import BiseccionApp

    app = BiseccionApp()
    setup_closing_protocol(app)
    app.mainloop()


def main():
    """Función principal de la aplicación"""
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    try:
        run_application()

    except ImportError as e:
        error_msg = f"Error al importar módulos: {str(e)}\n"
        error_msg += ("Verifica que todos los archivos estén en sus "
                      "carpetas correctas.")
        print(f"❌ {error_msg}")
        show_error_dialog("Error de Importación", error_msg)
        sys.exit(1)

    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"❌ {error_msg}")
        show_error_dialog("Error", error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()

