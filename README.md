# 📝 Blog en Django - "Grupo XIV noche"

Proyecto **Blog en Django** desplegado en un **VPS con Docker** para produccion y **pythonanywhere** para desarrollo.  
Este blog forma parte de los proyectos de **Informatorio chaco** comision 2, grupo:"Grupo XIV noche" y se encuentra disponible en:

**🌐 Producción:** [http://esencialtic.com.ar:8000/blog](http://esencialtic.com.ar:8000/blog)
**🌐 Desarrollo:** [https://serggiors.pythonanywhere.com/blog/](https://serggiors.pythonanywhere.com/blog/g)

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
http://esencialtic.com.ar:8000/blog
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

## 🐳 Comandos Docker Útiles

Levantar el proyecto:

```bash
docker-compose up -d --build
```

Ver logs del contenedor web:

```bash
docker logs -f web
```

Ver logs de la base de datos:

```bash
docker logs -f db
```

Crear superusuario de Django:

```bash
docker exec -it web python manage.py createsuperuser
```

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

### 1️⃣ Levantar el proyecto en local

```bash
git clone git@github.com:sergiorioscomar/blog.git
cd blog
docker-compose up -d --build
```

El proyecto quedará disponible en:

```
http://localhost:8000/blog
```

### 2️⃣ Conectarse a la base de datos MySQL del contenedor

```bash
docker exec -it db mysql -u root -p
# Contraseña: passroot
#Recordar agregar la configuracion en blog/django_project/config/settings/local o en .env con variables de entorno privadas.
```

### 3️⃣ Ejecutar migraciones

```bash
docker exec -it web python manage.py migrate
```

### 4️⃣ Crear superusuario

```bash
docker exec -it web python manage.py createsuperuser
```

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

---

## ✅ Próximos pasos

- [ ] Configurar Nginx para acceder sin el puerto 8000.  
- [ ] Implementar HTTPS con Certbot.  
- [ ] Automatizar despliegue de ramas `main` y `dev` con GitHub Actions.  
- [ ] Mejorar documentación interna en `/docs`.
