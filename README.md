# Prueba tecnica Gendra - Backend

Este es el backend para la prueba tecnica que consiste en un backoffice KYC, una API robusta y asíncrona construida con **FastAPI**. Gestiona procesos transaccionales de alta integridad en **PostgreSQL** y mantiene un sistema de auditoría flexible en **MongoDB**.

URL Productiva documentacion: <https://backend-prueba-tecnica-7cu9.onrender.com/docs>

## Tecnologías Utilizadas

* **FastAPI:** Framework moderno de alto rendimiento para APIs con Python.
* **PostgreSQL (Neon):** Base de datos relacional para la gestión de solicitudes KYC.
* **MongoDB (Atlas):** Almacenamiento no relacional para logs de auditoría detallados.
* **SQLAlchemy & Motor:** Herramientas para comunicación asíncrona con bases de datos SQL y NoSQL.
* **Pydantic:** Validación estricta de esquemas y tipos de datos.
* **Docker:** Containerización completa para asegurar un despliegue consistente.

## Decisiones Técnicas Clave

1. **Persistencia Híbrida (SQL + NoSQL):** - Se eligió **PostgreSQL** para el core de las solicitudes debido a la necesidad de transaccionalidad e integridad referencial.
   - Se optó por **MongoDB** para la auditoría, permitiendo que el historial de eventos crezca sin afectar el rendimiento de la base de datos operativa principal.
2. **Programación Asíncrona:** - El uso de `async/await` en todos los endpoints permite que el servidor maneje múltiples conexiones simultáneas de forma eficiente, algo vital para el escalado en la nube.

## Configuración y Ejecución

### **1. Requisitos Previos**
* Python
* Docker.
* Variables de entorno configuradas (`DATABASE_URL`, `MONGO_URI`, `MONGO_DB_NAME`, `API_PREFIX`, `PROJECT_NAME`).

### **2. Instalación Local**
```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requeriments.txt

# 4. Ejecutar servidor
uvicorn src.main:app --reload

# Construir imagen
docker build -t kyc-backend .

# Ejecutar contenedor
docker run -p 8080:8080 --env-file .env kyc-backend

# Pruebas unitarias
pytest -v 