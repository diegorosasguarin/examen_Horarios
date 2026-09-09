from persistencia import cargar_horarios, guardar_horarios, guardar_reporte_balance_semanal, guardar_reporte_json
from validaciones import verificar_conflicto, DIAS_SEMANA, hora_a_minutos, normalizar_cadena

def normalizar_dia(dia_input):
    dia_ingresado = normalizar_cadena(dia_input)
    for d in DIAS_SEMANA:
        if normalizar_cadena(d) == dia_ingresado:
            return d
    return dia_input.strip().capitalize()

def registrar_materia(horarios):
    print("\n--- REGISTRAR MATERIA O ACTIVIDAD ---")
    materia = input("Ingrese el nombre de la materia o actividad: ").strip()
    if not materia:
        print("El nombre de la materia no puede estar vacío.")
        return

    dia_raw = input("Ingrese el día de la semana (Lunes, Martes, ...): ").strip()
    dia = normalizar_dia(dia_raw)

    hora_inicio = input("Ingrese la hora de inicio (Formato 24H - Ejemplo: 14:00): ").strip()
    hora_fin = input("Ingrese la hora de fin (Formato 24H - Ejemplo: 16:00): ").strip()
    ubicacion = input("Ingrese la ubicación (opcional, presione ENTER para omitir): ").strip()

    conflicto, mensaje = verificar_conflicto(horarios, dia, hora_inicio, hora_fin)
    if conflicto:
        print(f"Error: {mensaje}")
        return

    nuevo_evento = {
        "materia": materia,
        "dia": dia,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "ubicacion": ubicacion
    }

    horarios.append(nuevo_evento)
    guardar_horarios(horarios)

    ubicacion_str = f" en {ubicacion}" if ubicacion else ""
    print(f'\nMateria "{materia}" registrada exitosamente el {dia} de {hora_inicio} a {hora_fin}{ubicacion_str}.')

def ver_horario_semanal(horarios):
    print("\n--- HORARIO SEMANAL ---")
    if not horarios:
        print("No hay materias ni actividades registradas.")
        return

    dias_grid = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    # Extraer franjas horarias únicas ordenadas
    franjas = sorted(list(set([(e["hora_inicio"], e["hora_fin"]) for e in horarios])), key=lambda x: hora_a_minutos(x[0]) or 0)

    if not franjas:
        print("No hay eventos registrados con horarios válidos.")
        return

    # Encabezado formateado
    header = "| Hora     | " + " | ".join([f"{d:<12}" for d in dias_grid]) + " |"
    separador = "=" * len(header)

    print(separador)
    print(header)
    print(separador)

    for h_ini, h_fin in franjas:
        min_i = hora_a_minutos(h_ini)
        hh = min_i // 60
        mm = min_i % 60
        ampm = "AM" if hh < 12 else "PM"
        hh_12 = hh if hh <= 12 else hh - 12
        if hh_12 == 0:
            hh_12 = 12
        hora_label = f"{hh_12:02d}:{mm:02d} {ampm}"

        fila = [f"| {hora_label:<8} |"]

        for d in dias_grid:
            evento_encontrado = None
            for e in horarios:
                if normalizar_cadena(e["dia"]) == normalizar_cadena(d) and e["hora_inicio"] == h_ini:
                    evento_encontrado = e["materia"]
                    break

            if evento_encontrado:
                nombre = evento_encontrado[:12]
                fila.append(f" {nombre:<12} |")
            else:
                fila.append(f" {'Libre':<12} |")

        print("".join(fila))

    print(separador)

def modificar_materia(horarios):
    print("\n--- MODIFICAR MATERIA O ACTIVIDAD ---")
    materia = input("Ingrese el nombre de la materia o actividad a modificar: ").strip()

    coincidencias = [i for i, e in enumerate(horarios) if normalizar_cadena(e["materia"]) == normalizar_cadena(materia)]

    if not coincidencias:
        print(f'No se encontró la materia "{materia}" en el horario.')
        return

    idx_mod = coincidencias[0]
    if len(coincidencias) > 1:
        print("Se encontraron varios eventos con ese nombre:")
        for pos, idx in enumerate(coincidencias, 1):
            e = horarios[idx]
            print(f"{pos}. {e['materia']} - {e['dia']} ({e['hora_inicio']} a {e['hora_fin']})")
        opc = input("Seleccione el número del evento a modificar: ").strip()
        if opc.isdigit() and 1 <= int(opc) <= len(coincidencias):
            idx_mod = coincidencias[int(opc) - 1]
        else:
            print("Opción inválida.")
            return

    evento_actual = horarios[idx_mod]
    print(f"Modificando evento actual: {evento_actual['materia']} ({evento_actual['dia']} {evento_actual['hora_inicio']}-{evento_actual['hora_fin']})")

    nuevo_dia_raw = input("Ingrese el nuevo día de la semana (ENTER para mantener el mismo): ").strip()
    nuevo_dia = normalizar_dia(nuevo_dia_raw) if nuevo_dia_raw else evento_actual["dia"]

    nueva_hora_inicio = input("Ingrese la nueva hora de inicio (Formato 24H, ENTER para mantener): ").strip() or evento_actual["hora_inicio"]
    nueva_hora_fin = input("Ingrese la nueva hora de fin (Formato 24H, ENTER para mantener): ").strip() or evento_actual["hora_fin"]

    nueva_ubicacion_raw = input("Ingrese la nueva ubicación (ENTER para mantener la misma): ").strip()
    nueva_ubicacion = nueva_ubicacion_raw if nueva_ubicacion_raw != "" else evento_actual["ubicacion"]

    conflicto, mensaje = verificar_conflicto(horarios, nuevo_dia, nueva_hora_inicio, nueva_hora_fin, evento_ignorar_idx=idx_mod)
    if conflicto:
        print(f"Error: {mensaje}")
        return

    horarios[idx_mod] = {
        "materia": evento_actual["materia"],
        "dia": nuevo_dia,
        "hora_inicio": nueva_hora_inicio,
        "hora_fin": nueva_hora_fin,
        "ubicacion": nueva_ubicacion
    }

    guardar_horarios(horarios)
    ubicacion_str = f" en {nueva_ubicacion}" if nueva_ubicacion else ""
    print(f'\nMateria "{evento_actual["materia"]}" modificada exitosamente a {nuevo_dia} de {nueva_hora_inicio} a {nueva_hora_fin}{ubicacion_str}.')

def eliminar_materia(horarios):
    print("\n--- ELIMINAR MATERIA O ACTIVIDAD ---")
    materia = input("Ingrese el nombre de la materia o actividad que desea eliminar: ").strip()
    dia_raw = input("Ingrese el día de la semana: ").strip()

    idx_eliminar = None
    for i, e in enumerate(horarios):
        if normalizar_cadena(e["materia"]) == normalizar_cadena(materia) and normalizar_cadena(e["dia"]) == normalizar_cadena(dia_raw):
            idx_eliminar = i
            break

    if idx_eliminar is None:
        print(f'No se encontró la materia "{materia}" registrada el día {dia_raw}.')
        return

    materia_nombre = horarios[idx_eliminar]["materia"]
    dia_nombre = horarios[idx_eliminar]["dia"]
    horarios.pop(idx_eliminar)
    guardar_horarios(horarios)
    print(f'La materia "{materia_nombre}" ha sido eliminada del horario del día {dia_nombre}.')

def generar_reporte(horarios):
    print("\n==========================================")
    print("REPORTE DEL HORARIO SEMANAL")
    print("==========================================")

    if not horarios:
        print("No hay eventos registrados en el horario.")
        return

    reporte_dict = {}
    for d in DIAS_SEMANA:
        eventos_dia = [e for e in horarios if normalizar_cadena(e["dia"]) == normalizar_cadena(d)]
        if eventos_dia:
            eventos_dia.sort(key=lambda x: hora_a_minutos(x["hora_inicio"]) or 0)
            reporte_dict[d] = eventos_dia

    reporte_json_list = []
    for dia, eventos in reporte_dict.items():
        eventos_formateados = []
        for ev in eventos:
            item = {
                "materia": ev["materia"],
                "hora_inicio": ev["hora_inicio"],
                "hora_fin": ev["hora_fin"],
                "ubicacion": ev["ubicacion"]
            }
            eventos_formateados.append(item)
        reporte_json_list.append({
            "dia": dia,
            "eventos": eventos_formateados
        })

    guardar_reporte_json(reporte_json_list)

    dias_reporte = list(reporte_dict.keys())
    bloques_paginacion = 3

    for i, dia in enumerate(dias_reporte):
        print(f"\n{dia}:")
        for ev in reporte_dict[dia]:
            ubicacion_str = f" en {ev['ubicacion']}" if ev['ubicacion'] else ""
            print(f"  - {ev['materia']} ({ev['hora_inicio']}-{ev['hora_fin']}){ubicacion_str}")

        if (i + 1) % bloques_paginacion == 0 and (i + 1) < len(dias_reporte):
            input("\nPresione ENTER para continuar...")

    print("\nReporte generado y guardado exitosamente en 'reporte_horario.json'.")





def reporte_balance_semanal(horarios):
    print("\n==========================================")
    print("REPORTE Balance Semanal")
    print("==========================================")

    if not horarios:
        print("No hay eventos registrados en el horario.")
        return

    reporte_dict_balance = {}
    for d in DIAS_SEMANA:
        eventos_dia = [e for e in horarios if normalizar_cadena(e["dia"]) == normalizar_cadena(d)]
        if eventos_dia:
            eventos_dia.sort(key=lambda x: hora_a_minutos(x["hora_inicio"]) or 0)
            reporte_dict[d] = eventos_dia

    reporte_json_list_balance = []
    for dia, eventos in reporte_dict.items():
        eventos_formateados = []
        for ev in eventos:
            item = {
                "materia": ev["materia"],
                "hora_inicio": ev["hora_inicio"],
                "hora_fin": ev["hora_fin"],
                "ubicacion": ev["ubicacion"]
            }
            eventos_formateados.append(item)
        reporte_json_list_balance.append({
            "dia": dia,
            "eventos": eventos_formateados
        })

    guardar_reporte_balance_semanal(reporte_json_list_balance)

    dias_reporte = list(reporte_dict_balance.keys())
    bloques_paginacion = 3

    for i, dia in enumerate(dias_reporte):
        print(f"\n{dia}:")
        for ev in reporte_dict_balance[dia]:
            ubicacion_str = f" en {ev['ubicacion']}" if ev['ubicacion'] else ""
            print(f"  - {ev['materia']} ({ev['hora_inicio']}-{ev['hora_fin']}){ubicacion_str}")

        if (i + 1) % bloques_paginacion == 0 and (i + 1) < len(dias_reporte):
            input("\nPresione ENTER para continuar...")

    print("\nReporte generado y guardado exitosamente en 'reporte_balance_semanal.json'.")









