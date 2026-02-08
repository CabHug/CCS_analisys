import os
import sys
import subprocess
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado():
    print("=" * 60)
    print("      🚀  Centro de Capacitacion del Sur   🚀     ")
    print("=" * 60)

def ejecutar_script(nombre_script, directorio):
    """
    Ejecuta un script individual y maneja errores.
    """
    ruta_script = os.path.join(directorio, nombre_script)
    
    if not os.path.exists(ruta_script):
        print(f"\n❌ ERROR: No se encontró '{nombre_script}' en {directorio}")
        return False

    print(f"\n⚙️  Ejecutando: {nombre_script}...")
    print("-" * 40)
    
    try:
        # Ejecutamos el script asegurando que use el mismo interprete de python
        subprocess.run(
            [sys.executable, ruta_script], 
            check=True, 
            cwd=directorio 
        )
        print(f"✅ {nombre_script} finalizado correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error crítico en {nombre_script} (Código {e.returncode}).")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

def flujo_completo_procesamiento():
    """
    Ejecuta la secuencia completa de procesamiento de datos.
    """
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Definimos el orden lógico de ejecución
    scripts_a_ejecutar = [
        "etl.py",
        "table_etl.py",
        "transform_to_csv.py"
    ]

    limpiar_pantalla()
    mostrar_encabezado()
    print(f"\n🔄 INICIANDO FLUJO DE TRABAJO COMPLETO")
    start_time_total = time.time()

    for script in scripts_a_ejecutar:
        exito = ejecutar_script(script, directorio_actual)
        if not exito:
            print(f"\n🛑 EL PROCESO SE DETUVO debido a un error en: {script}")
            break
        time.sleep(1) # Pequeña pausa estética entre scripts

    end_time_total = time.time()
    print("\n" + "=" * 60)
    print(f"✨ ¡TODO EL PROCESO COMPLETADO! Duración: {end_time_total - start_time_total:.2f}s")
    print("=" * 60)
    
    input("\nPresiona ENTER para volver al menú...")

def main():
    while True:
        limpiar_pantalla()
        mostrar_encabezado()
        print("\nSeleccione una acción:")
        print(" [1] ⚡ Procesar Datos (ETL -> Tablas -> CSV)")
        print(" [2] 📝 (Espacio para futuro script...)")
        print(" [3] ❌ Salir")
        
        opcion = input("\n>> Su elección: ").strip()

        if opcion == '1':
            flujo_completo_procesamiento()
        elif opcion == '2':
            print("\n💡 Opción reservada para el nuevo script en desarrollo.")
            time.sleep(2)
        elif opcion == '3':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n⚠️ Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    main()