# 📜 Changelog — Blog Esencial TIC

Historial cronológico de implementaciones y mejoras.

---

## **Julio 2025**

### 📆 28 de julio
- Inicio del proyecto: creación del entorno Django y configuración inicial para desarrollo (pythonanywhere) y producción (VPS).
- Configuración MySQL en Docker.
- Creación de apps base: `blog`, `accounts`, `core`.
- Integración de Bootstrap 5 en `base.html`.
- Configuración de MySQL y carga de modelos `Post`, `Categoria`, `Comentario`.
- Configuración de media y archivos estáticos.
- Creación de API para ultimos posts.

### 📆 29 de julio
- Implementación de paginación en el listado de posts.
- Imagen por defecto en posts sin imagen destacada.
- Vista inicial de `post_detail`.
- Configuración de Docker para desarrollo.

---

## **Agosto 2025**

### 📆 1 de agosto
- Sistema de comentarios vinculado a usuario autenticado.
- Avatar en comentarios (sin imagen por defecto).
- Notificación visual tras comentar.

### 📆 2 de agosto
- Modelo `Profile` vinculado a `User` (OneToOne).
- Formulario básico de edición de perfil.
- Creación de API para posts mas vistos.

### 📆 5 de agosto
- Posts destacados en la página principal.
- Tarjetas de post en 3 columnas.
- Navegación entre posts (prev/next).
- Configuración de categorías y filtrado.

### 📆 9 de agosto
- Enlaces a perfil público desde autor/comentarios.
- Tags personalizados para mostrar avatar/datos de perfil.
- Diseño inicial de perfil público.
- Implementación inicial del sistema de mensajes privados entre usuarios.
- Notificación por email al recibir un mensaje.
- Notificación por email al recibir un comentario en el post.

### 📆 10 de agosto
- Efecto de imagen tenue/degradado en login.
- Corrección de estilos en tarjetas de post para vista en 3 columnas.
- Imagen por defecto para posts sin imagen.
- Configuración `.env` para email y DB.

### 📆 11 de agosto
- Plantillas personalizadas para errores 404/403/500.
- Traducción de validaciones al español.
- Ajustes de `DEBUG=False` para static/media.
- Footer con redes sociales.

### 📆 12 de agosto
- Mejora de login con imagen lateral responsiva.
- Avatar por defecto para usuarios sin imagen.
- Integración de `django-summernote`.
- Ajuste de barra de navegación según autenticación.
- Ajuste de tamaños de títulos y fechas.
- Corrección de acceso a perfil público por username
- Corrección de barra de navegación para mostrar autenticación real.

### 📆 13 de agosto
- Toolbar reducido, idioma español django.
- Ajuste de tamaños de letra para títulos y fechas en navegación de posts.