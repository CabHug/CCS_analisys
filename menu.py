import os
import sys
import subprocess
import time

def limpiar_pantalla():
    # Limpia la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado():
    print("=" * 50)
    print("        SISTEMA DE GESTIÓN DE PROYECTOS CCS")
    print("=" * 50)

def ejecutar_conversion_automatica():
    """
    Ejecuta el archivo externo transform_to_csv.py asegurando las rutas correctas.
    """
    # 1. Obtener la ruta absoluta de la carpeta donde está ESTE archivo de menú
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Construir la ruta completa al script objetivo
    nombre_script = "transform_to_csv.py"
    ruta_script = os.path.join(directorio_actual, nombre_script)

    if not os.path.exists(ruta_script):
        print(f"\n❌ ERROR CRÍTICO: No se encuentra el archivo.")
        print(f"   Buscando en: {ruta_script}")
        print("   Asegúrate de que 'transform_to_csv.py' esté en la misma carpeta que este menú.")
        return

    print(f"\n🚀 Iniciando proceso de conversión...\n")
    print(f"📂 Ejecutando: {nombre_script}")
    print("-" * 50)
    
    try:
        start_time = time.time()
        
        # 3. EJECUCIÓN CLAVE: 
        # Pasamos 'cwd=directorio_actual' para que el script sepa dónde buscar sus imports (OOP_classes)
        subprocess.run(
            [sys.executable, ruta_script], 
            check=True, 
            cwd=directorio_actual 
        )
        
        end_time = time.time()
        
        print("-" * 50)
        print(f"✨ Proceso finalizado exitosamente en {end_time - start_time:.2f} segundos.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ El script falló con un error (Código {e.returncode}).")
        print("   Revisa los mensajes de error arriba ⬆️.")
    except Exception as e:
        print(f"\n❌ Error inesperado al intentar ejecutar: {e}")

    input("\nPresiona ENTER para volver al menú...")

def main():
    while True:
        limpiar_pantalla()
        mostrar_encabezado()
        print("\nSeleccione una opción:")
        print(" [1] Ejecutar Conversión XLSX a CSV (Automático)")
        print(" [2] Salir")
        
        opcion = input("\n>> Su elección: ").strip()

        if opcion == '1':
            ejecutar_conversion_automatica()
        elif opcion == '2':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n⚠️ Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    main()