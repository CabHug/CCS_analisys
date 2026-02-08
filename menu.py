import os
import sys
import subprocess
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado():
    print("=" * 60)
    print("      🚀  Centro de Capacitación del Sur (CCS)  🚀      ")
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

def flujo_procesamiento_archivos():
    """
    OPCIÓN 1: Ejecuta la secuencia de limpieza y generación de CSV.
    """
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    scripts_a_ejecutar = ["etl.py", "table_etl.py", "transform_to_csv.py"]

    limpiar_pantalla()
    mostrar_encabezado()
    print(f"\n🔄 INICIANDO TRANSFORMACIÓN DE ARCHIVOS (Excel -> CSV)")
    
    start_time_total = time.time()
    for script in scripts_a_ejecutar:
        if not ejecutar_script(script, directorio_actual):
            print(f"\n🛑 EL PROCESO SE DETUVO debido a un error en: {script}")
            break
        time.sleep(0.5)

    print(f"\n✨ Transformación completada en {time.time() - start_time_total:.2f}s")
    input("\nPresiona ENTER para volver al menú...")

def flujo_actualizar_base_datos():
    """
    OPCIÓN 2: Ejecuta el script de carga a PostgreSQL.
    """
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    limpiar_pantalla()
    mostrar_encabezado()
    print(f"\n📤 INICIANDO CARGA A BASE DE DATOS POSTGRESQL")
    
    start_time = time.time()
    # Asegúrate de que tu script se llame exactamente 'update_db.py'
    exito = ejecutar_script("update_db.py", directorio_actual)
    
    if exito:
        print(f"\n✅ BASE DE DATOS ACTUALIZADA EXITOSAMENTE en {time.time() - start_time:.2f}s")
    else:
        print(f"\n❌ FALLÓ LA CARGA a la base de datos.")
    
    input("\nPresiona ENTER para volver al menú...")

def main():
    while True:
        limpiar_pantalla()
        mostrar_encabezado()
        print("\nSeleccione una acción:")
        print(" [1] ⚡ Procesar Archivos (ETL -> Tablas -> CSV)")
        print(" [2] 🗄️  Actualizar Base de Datos (CSV -> PostgreSQL)")
        print(" [3] ❌ Salir")
        
        opcion = input("\n>> Su elección: ").strip()

        if opcion == '1':
            flujo_procesamiento_archivos()
        elif opcion == '2':
            flujo_actualizar_base_datos()
        elif opcion == '3':
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("\n⚠️ Opción no válida.")
            time.sleep(1)

if __name__ == "__main__":
    main()