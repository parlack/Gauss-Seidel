#!/usr/bin/env python3
"""
Script de demostración para mostrar las capacidades
mejoradas de visualización de la aplicación Gauss-Seidel
"""

from gui.main_window import GaussSeidelApp
import customtkinter as ctk

def demo_message():
    """Muestra un mensaje de demostración"""
    print("🚀 DEMO - Aplicación Mejorada de Gauss-Seidel")
    print("=" * 50)
    print()
    print("🎨 NUEVAS CARACTERÍSTICAS VISUALES:")
    print("   • Cards visuales para cada iteración (no más texto de terminal)")
    print("   • Barra de progreso animada")
    print("   • Comparación visual entre iteraciones")
    print("   • Gráficos mejorados de convergencia")
    print("   • Métricas en tiempo real")
    print("   • Botones de navegación avanzados")
    print("   • Solución mostrada en tarjetas coloridas")
    print()
    print("💡 CÓMO USAR:")
    print("   1. Ingresa un sistema de ecuaciones")
    print("   2. Presiona 'RESOLVER SISTEMA'")
    print("   3. Ve a la pestaña 'Proceso de Solución'")
    print("   4. Navega entre iteraciones con los botones")
    print("   5. Revisa convergencia y resultado final")
    print()
    print("📊 EJEMPLO RECOMENDADO (3x3):")
    print("   Matriz A:")
    print("   10  -1   2")
    print("   -1  11  -1") 
    print("    2  -1  10")
    print()
    print("   Vector b:")
    print("   6, 25, -11")
    print()
    print("   Solución esperada: x1=1, x2=2, x3=-1")
    print()
    print("🎯 ¡Disfruta la nueva experiencia visual!")
    print("=" * 50)

if __name__ == "__main__":
    demo_message()
    
    # Crear y ejecutar la aplicación
    app = GaussSeidelApp()
    
    # Configurar cierre
    def on_closing():
        print("\n👋 ¡Gracias por probar la demo!")
        app.quit()
        app.destroy()
    
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

