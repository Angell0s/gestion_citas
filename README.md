## 📍 ~Gestor de Citas

> **Estado:** 🚧 En fase de desarrollo activo (Backend funcional, implementando autenticación JWT).





## 🎯 Visión del Proyecto
**Flujo Local** nace como un gestor de citas inteligente para pequeños emprendimientos, con la mira puesta en convertirse en un **SaaS de catálogo local**. La idea es agrupar locales comerciales por rubro en un dominio web unificado, facilitando que los clientes encuentren y contacten negocios cercanos, mientras los dueños administran su agenda sin complicaciones.

## 💡 Problema que resuelve
Actualmente, muchos emprendedores locales usan agendas físicas, Excel o mensajes de WhatsApp para gestionar sus turnos. Esto genera:
- Dobles reservas.
- Pérdida de datos de contacto.
- Nula visibilidad de la jornada laboral en tiempo real.

**Flujo Local** centraliza este proceso en un panel visual e intuitivo.

## ✨ Características principales (Backend actual + Futuro)
- **Autenticación Segura:** Implementación de JWT (JSON Web Tokens) para roles de administrador y empleado.
- **CRUD de Citas:** Creación, lectura, actualización y eliminación de turnos asignando Cliente, Fecha, y datos de contacto.
- **Calendario Interactivo:** Vista mensual/semanal para visualizar la carga de trabajo (conectado al backend).
- **📺 Pantalla para Monitor Secundario:** Funcionalidad diferenciadora que muestra en tiempo real la **cita actual**, la **siguiente** y las **pasadas**. Ideal para poner en una TV en la recepción del local.

## 🛠️ Stack Tecnológico (Arquitectura)

| Capa | Tecnología |
| :--- | :--- |
| **Backend API** | Python 3.10+, FastAPI, PyJWT, SQLAlchemy |
| **Frontend** | React (o Next.js) con TypeScript |
| **Base de Datos** | PostgreSQL |
| **Contenerización** | Docker & Docker Compose |
| **Proxy/Exposición** | Cloudflare Tunnel (Zero Trust) |
| **Despliegue** | Preparado para entornos Linux auto-gestionados (Self-Hosted) |

## 🐳 Levantar el proyecto en local (Desarrollo)

Si quieres probar el backend actual:

1. Clona el repositorio:
   ```bash
   git clone [url-del-repo]
   cd gestioncitas-backend
   ```
2. Crea un archivo ```.env``` basado en ```.env.example``` con tus claves de JWT y DB.

3. Levanta todo con Docker (incluye PostgreSQL y la API):
    ```bash
    docker-compose up -d --build
    ```
4. La documentación interactiva de FastAPI estará disponible en: ```http://localhost:8000/docs``` 

(Próximamente: Frontend en React/Next disponible en la misma compose).

## Estrategia de Despliegue a Producción

El proyecto está diseñado pensando en la autonomía del emprendedor. Se conteneriza mediante Docker para garantizar que funcione igual en un servidor local, un VPS (DigitalOcean, AWS) o en la nube. La exposición segura al exterior se gestiona mediante **Cloudflare Tunnels**, evitando abrir puertos en el router y añadiendo una capa de seguridad y caché.

## Hoja de Ruta (Roadmap)

- [x] Base de datos modelada (PostgreSQL).
- [x] Autenticación JWT implementada.
- [ ] Frontend en React/Next con diseño responsivo.
- [ ] Módulo de "Pantalla de Recepción" en tiempo real (WebSockets/Socket.io).
- [ ] Migración a arquitectura multi-tenant (SaaS) para manejar múltiples locales.
- [ ] Panel de administración para dar de alta nuevos comercios.

## ¿Para quién es esto?

Si tienes un pequeño negocio (peluquería, taller, consultorio) y quieres digitalizar tus citas sin pagar costosas suscripciones mensuales, este proyecto puede ser tu punto de partida. **Actualmente estoy buscando casos de uso reales para probarlo sin costo a corto plazo.**

