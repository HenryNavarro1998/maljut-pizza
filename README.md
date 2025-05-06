# Maljut Pizzas Café - Sistema de Gestión

Sistema de gestión integral para pizzería, desarrollado en Python con Flask, almacenamiento en archivos JSON y una interfaz web moderna, minimalista y responsive.

## Características principales

- **Gestión de inventario:** Altas, bajas y modificaciones de productos e insumos.
- **Recetas:** Creación y edición de recetas de pizzas y productos.
- **Ventas:** Registro de ventas, historial y reportes.
- **Usuarios:** Control de usuarios y roles (admin y empleados).
- **Dashboard:** Estadísticas, top de recetas más vendidas y métricas clave.
- **Modo oscuro/claro:** Alternancia con guardado de preferencia.
- **Interfaz responsive:** Adaptada a móviles, tablets y escritorio.
- **Sidebar moderna:** Menú lateral fijo en escritorio y deslizable en móvil.
- **Seguridad:** Autenticación de usuarios y control de permisos.

## Tecnologías utilizadas

- Python 3.8+
- Flask
- Flask-Login
- Bootstrap 5
- FontAwesome
- Archivos JSON como base de datos

## Instalación y ejecución

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/maljut-pizzeria.git
   cd maljut-pizzeria
   ```
2. **Crea un entorno virtual y actívalo:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecuta la aplicación:**
   ```bash
   flask run
   ```
5. **Accede desde tu navegador:**
   - [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usuario administrador por defecto

- **Usuario:** `admin`
- **Contraseña:** `Admin123`

Puedes cambiar la contraseña desde el módulo de usuarios.

## Estructura del proyecto

```
maljut-pizzeria/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
├── app/data/           # Archivos JSON de datos
├── requirements.txt
├── README.md
└── ...
```

## Dependencias principales

- Flask
- Flask-Login
- Werkzeug
- Bootstrap 5 (CDN)
- FontAwesome (CDN)

## Créditos

Desarrollado por Henry y colaboradores.

Diseño, frontend y backend con ❤️ usando Python y Flask.

---

¿Dudas, sugerencias o mejoras? ¡Contribuciones y feedback son bienvenidos!
