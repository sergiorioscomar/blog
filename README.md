# 📝 Blog en Django - "Grupo XIV noche"

Proyecto **Blog en Django** desplegado en un **VPS con Docker** para produccion y **pythonanywhere** para desarrollo.  
Este blog forma parte de los proyectos de **Informatorio chaco** comision 2, grupo:"Grupo XIV" y se encuentra disponible en:

**🌐 Producción:** [https://blog.esencialtic.com.ar/blog](https://blog.esencialtic.com.ar/blog)

**🌐 Desarrollo:** [https://serggiors.pythonanywhere.com/blog/](https://serggiors.pythonanywhere.com/blog)

---

## 🚀 Despliegue

- **Framework:** Django  
- **Base de datos:** MySQL (en contenedor Docker) y en pythonanywhere.
- **Servidor:** VPS propio  
- **Servidor Desarrollo:** Pythonanywhere
- **Contenedores:** Docker Compose  
- **Puerto de acceso:** `8000`  
- **Puerto de acceso:** `3001` (Base de datos) 

Estructura de acceso:

```
https://serggiors.pythonanywhere.com/
https://blog.esencialtic.com.ar/blog/
```

> **Nota:** Actualmente el proyecto se expone en el puerto 8000.  
> Se prevé configurar Nginx para acceder sin el puerto en el futuro.

---

## 📂 Estructura del Proyecto

- `django_project/` → Código principal del proyecto Django.
- `Dockerfile` → Imagen personalizada para el contenedor web.
- `docker-compose.yml` → Orquesta los contenedores web y base de datos.
- `.env` → Variables de entorno (ignorado en Git).
- `.gitignore` → Ignora archivos sensibles, `.env`, volúmenes y datos locales.

---

## 🌿 Flujo de ramas

- **`main`** → Rama de producción (estable).  
- **`dev`** → Rama de desarrollo, donde se van incorporando cambios antes de pasar a producción.

> **Tip:** Se recomienda hacer **Pull Request** desde `dev` hacia `main` para mantener el historial limpio.

---

## 📋 Gestión de tareas y bugs

Este proyecto cuenta con un **Project en GitHub** para registrar:

- **Bugs** detectados en producción.
- **Tareas pendientes** (To-Do).
- **Mejoras** futuras.

[🔗 Acceder al Project de Gestión](https://github.com/users/sergiorioscomar/projects/13)

---

## 🛠️ Instrucciones para desarrolladores

## 🚀 Características

### 📄 Contenido & UI
- Posts con imagen destacada, categorías y destacados en portada  
- Listado con paginación y navegación entre posts (prev / next)  
- Imagen por defecto y degradados para mejorar legibilidad  
- Toolbar reducida e idioma es-ES (Español)
- Plantillas personalizadas de errores **404 / 403 / 500**   

### 👤 Cuentas & Perfiles
- Registro y login personalizados con **Bootstrap 5**  
- Perfil de usuario con avatar (imagen por defecto si no se carga)  
- Perfil público accesible por username o ID  
- Recuperación de contraseña con envío de email  

### 💬 Social & Engagement
- Sistema de **likes** por usuario  
- Sistema de **vistas** por post  
- Sistema de **comentarios** con notificación en la toolbar y por email
- Sistema de **mensajes privados internos** con notificación en la toolbar y por email  

### 🛡️ Roles & Permisos
- **Administrador**, **Autor**, **Usuario**  
- Permisos diferenciados para crear, editar y publicar contenido  

### ⚙️ Dev & Ops
- Configuración vía **.env** (DB, email, etc.)  
- **Docker** (Django + MySQL)  
- Compatible con despliegue en **PythonAnywhere**  

---

## 📡 Endpoints API

| Método | Ruta                   | Descripción                    |
|-------:|------------------------|--------------------------------|
| GET    | `/api/ultimos-posts/`  | Lista de últimos posts         | 
| GET    | `/api/mas-vistos/`     | Lista por popularidad          | 

---

## 🗃️ Modelos principales

- **Post**, **Categoria**, **Comment**  
- **Profile** (OneToOne con `User`)  
- **Message** (mensajes internos)  
- *(Opcional)* `PostView`, `PostLike` para métricas  

---

## 🛠️ Stack Técnico
- **Backend**: Django 5.x  
- **Base de datos**: MySQL 8  
- **Frontend**: Bootstrap 5
- **Entorno**: Docker / docker-compose  
- **Email**: SMTP (password reset, notificaciones)  

---

## 🔧 Instalación

### Requisitos
- Python 3.11+
- MySQL 8
- Docker (opcional)

### Variables de entorno (`.env`)
```env
DEBUG=False
SECRET_KEY=tu_clave_secreta
ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com
DATABASE_URL=mysql://usuario:clave@host:3306/nombre_bd
EMAIL_HOST=smtp.tu-dominio.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=info@tu-dominio.com
EMAIL_HOST_PASSWORD=********
DEFAULT_FROM_EMAIL=info@tu-dominio.com
```

### Instalación local
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Instalación con Docker
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## 📬 Flujo de notificaciones

- **Comentarios** → email al autor del post  
- **Mensajes privados** → badge en toolbar + email al receptor  
- **Recuperar contraseña** → email con enlace temporal  

---

## 🔑 Roles y permisos

| Acción                                       | Admin | Autor | Usuario  |
|--------------------------------------------- |:-----:|:------:|:-------:|
| Crear/editar posts propios                   | ✅    | ✅    | ❌     |
| Publicar posts                               | ✅    | ✅    | ❌     |
| Comentar                                     | ✅    | ✅    | ✅     |
| Editar y eliminar comentario                 | ✅    | ✅    | ✅     |
| Enviar mensajes privados                     | ✅    | ✅    | ❌     |
| Administrar grupos y perfiles                | ✅    | ❌    | ❌     |
| Editar y eliminar post de otro usuario       | ✅    | ❌    | ❌     |
| Editar y eliminar comentario de otro usuario | ✅    | ❌    | ❌     |

---

## 🛡️ Notas de seguridad

- Las **credenciales** y configuración sensible se almacenan en el archivo `.env` (no versionado).
- Se recomienda mantener actualizado Docker y los contenedores para evitar vulnerabilidades.
- Se puede implementar HTTPS mediante **Nginx + Certbot** en el VPS para producción.

---

## 👨‍💻 Equipo

**Grupo XIV noche** – Proyecto Informatorio Chaco Comisión 2

**Sergio Rios**

**Jose Audicio**

📧 Contacto: [info@esencialtic.com.ar](mailto:info@esencialtic.com.ar)
📧 Contacto sergio: [sergio@esencialtic.com.ar](mailto:sergio@esencialtic.com.ar)

---

## ✅ Próximos pasos

- [ ] Configurar Nginx para acceder sin el puerto 8000.  
- [ ] Implementar HTTPS con Certbot.  
- [ ] Automatizar despliegue de ramas `main` y `dev` con GitHub Actions.  
- [ ] Mejorar documentación interna en `/docs`.

## 📜 Changelog

Ver el [Historial de cambios](CHANGELOG.md) para detalles cronológicos de mejoras e implementaciones.

---
