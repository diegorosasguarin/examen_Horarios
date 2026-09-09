from persistencia import cargar_horarios
from gestion_horarios import (
    registrar_materia,
    ver_horario_semanal,
    modificar_materia,
    eliminar_materia,
    generar_reporte
)

def mostrar_menu():
    print("\n==========================================")
    print("  GENERADOR DE HORARIOS PARA ESTUDIANTES  ")
    print("==========================================")
    print("1. Registrar una materia o actividad")
    print("2. Ver horario semanal")
    print("3. Modificar una materia o actividad")
    print("4. Eliminar una materia o actividad")
    print("5. Generar reporte del horario")
    print("6. Reporte balance semanal")
    print("7. Salir")
    print("==========================================")

def main():
    horarios = cargar_horarios()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_materia(horarios)
        elif opcion == "2":
            ver_horario_semanal(horarios)
        elif opcion == "3":
            modificar_materia(horarios)
        elif opcion == "4":
            eliminar_materia(horarios)
        elif opcion == "5":
            generar_reporte(horarios)
        elif opcion == "6":
            reporte_balance_semanal(horarios)
        elif opcion == "7":
        
            print("\n¡Gracias por utilizar el Generador de Horarios!")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione un número del 1 al 6.")

if __name__ == "__main__":
    main()
