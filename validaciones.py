DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def normalizar_cadena(texto):
    """Elimina tildes y convierte a minúsculas para comparaciones seguras."""
    if not texto:
        return ""
    reemplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"))
    cadena = texto.strip().lower()
    for a, b in reemplazos:
        cadena = cadena.replace(a, b)
    return cadena

def hora_a_minutos(hora_str):
    """Convierte una hora en formato HH:MM (24H) a minutos."""
    try:
        partes = hora_str.strip().split(":")
        if len(partes) != 2:
            return None
        hh = int(partes[0])
        mm = int(partes[1])
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            return hh * 60 + mm
        return None
    except ValueError:
        return None

def hay_superposicion(inicio1, fin1, inicio2, fin2):
    """Verifica si dos rangos de tiempo se cruzan."""
    return inicio1 < fin2 and inicio2 < fin1

def verificar_conflicto(horarios, dia, hora_inicio_str, hora_fin_str, evento_ignorar_idx=None):
    """Comprueba conflictos de horarios en un mismo día."""
    min_inicio = hora_a_minutos(hora_inicio_str)
    min_fin = hora_a_minutos(hora_fin_str)

    if min_inicio is None or min_fin is None:
        return True, "Formato de hora inválido. Utilice formato 24H (HH:MM), por ejemplo '14:00'."

    if min_inicio >= min_fin:
        return True, "La hora de inicio debe ser estrictamente anterior a la hora de fin."

    dia_norm = normalizar_cadena(dia)

    for idx, evento in enumerate(horarios):
        if evento_ignorar_idx is not None and idx == evento_ignorar_idx:
            continue

        if normalizar_cadena(evento["dia"]) == dia_norm:
            ev_inicio = hora_a_minutos(evento["hora_inicio"])
            ev_fin = hora_a_minutos(evento["hora_fin"])

            if ev_inicio is None or ev_fin is None:
                continue

            if hay_superposicion(min_inicio, min_fin, ev_inicio, ev_fin):
                msg = f"Existe un choque de horario con '{evento['materia']}' ({evento['hora_inicio']} a {evento['hora_fin']})."
                return True, msg

    return False, ""
