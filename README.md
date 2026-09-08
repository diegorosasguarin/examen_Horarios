# 📅 Generador de Horarios para Estudiantes

Este es un proyecto en Python que hice para organizar y gestionar horarios de clases y actividades de forma sencilla. El programa permite agregar materias, verificar que no se crucen las horas, ver la semana completa organizada en consola y guardar reportes.

---

## 💡 ¿Qué hace la aplicación?

- **Registra materias o actividades:** Guardando día, hora de inicio, hora de fin y salón o ubicación.
- **Evita cruces de horario:** Si intentas agregar una clase a la misma hora que otra el mismo día, te avisa el choque.
- **Vista semanal:** Muestra una tabla en la terminal con las materias ordenadas por día y hora.
- **Editar y eliminar:** Modifica datos de una materia o borra las que ya no necesites.
- **Guardado automático:** Todo se guarda en `horarios.json` para que no se pierdan los datos al cerrar el programa.
- **Exportar reporte:** Genera un archivo `reporte_horario.json` con la información organizada por días.

---

## 🛠️ Estructura de archivos

- `main.py`: Menú principal e interacción con el usuario.
- `gestion_horarios.py`: Funciones para agregar, ver, modificar, eliminar y reportar.
- `validaciones.py`: Lógica para comprobar horarios, horas en minutos y evitar cruces.
- `persistencia.py`: Lectura y escritura de los archivos JSON.
- `horarios.json`: Base de datos donde se guardan los eventos.

---

## 🚀 Cómo ejecutarlo

Solo necesitas tener **Python 3** instalado en tu equipo.

1. Abre la terminal en la carpeta del proyecto.
2. Corre el siguiente comando:

```bash
python main.py
```

---

## ✒️ Autor

Desarrollado por **Diego Rosas**.
