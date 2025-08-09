# 🚀 Guía de Despliegue en Railway

## 📋 Checklist Pre-Despliegue

### ✅ Requisitos
- [ ] Cuenta en Railway (gratuita)
- [ ] Repositorio en GitHub
- [ ] Cuenta en Cloudflare (para R2 - opcional)
- [ ] Dominio personalizado (opcional)

### ✅ Configuración Local
- [ ] FASE 1 completada (local básico)
- [ ] FASE 2 completada (mirror local)
- [ ] Tests funcionando

---

## 🎯 **PASO 1: Crear cuenta en Railway**

### 1.1 Registrarse
1. Ir a [railway.app](https://railway.app)
2. Click **"Start a Project"**
3. Seleccionar **"Deploy from GitHub repo"**
4. Conectar cuenta de GitHub
5. Autorizar acceso al repositorio

### 1.2 Crear proyecto
1. Seleccionar tu repositorio `lotoapi`
2. Click **"Deploy Now"**
3. Railway detectará automáticamente que es Python
4. Se iniciará el build automáticamente

---

## 🎯 **PASO 2: Configurar Variables de Entorno**

### 2.1 Variables básicas
En Railway Dashboard → **Variables** → Agregar:

```bash
# Configuración básica
MIRROR_IMAGES=false
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"

# Cache (opcional)
CACHE_TTL_SECONDS=300
```

### 2.2 Variables para mirror (opcional)
Si quieres usar R2 más adelante:

```bash
# Mirror de imágenes (R2)
MIRROR_IMAGES=true
S3_ENDPOINT=https://TU_ACCOUNT_ID.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=TU_ACCESS_KEY_ID
S3_SECRET_KEY=TU_SECRET_ACCESS_KEY
CDN_BASE=https://cdn.tudominio.com
```

---

## 🎯 **PASO 3: Configurar Dominio**

### 3.1 Dominio de Railway
1. Railway Dashboard → **Settings** → **Domains**
2. Click **"Generate Domain"**
3. Anotar la URL generada (ej: `lotoapi-production-1234.up.railway.app`)

### 3.2 Dominio personalizado (opcional)
1. Click **"Add Domain"**
2. Agregar tu dominio: `api.tudominio.com`
3. Configurar DNS:
   - Tipo: `CNAME`
   - Nombre: `api`
   - Destino: `tu-app.up.railway.app`

---

## 🎯 **PASO 4: Verificar Despliegue**

### 4.1 Health check
```bash
curl https://tu-app.up.railway.app/health
```

### 4.2 Test endpoints
```bash
# Animalitos
curl "https://tu-app.up.railway.app/animalitos?date=$(date +%Y-%m-%d)"

# Loterías
curl "https://tu-app.up.railway.app/loterias?date=$(date +%Y-%m-%d)"
```

### 4.3 Verificar logs
1. Railway Dashboard → **Deployments** → **Latest**
2. Click **"View Logs"**
3. Verificar que no hay errores

---

## 🎯 **PASO 5: Configurar Auto-Deploy**

### 5.1 GitHub Actions (opcional)
Railway se conecta automáticamente a GitHub, pero puedes configurar:

1. Repository → **Settings** → **Webhooks**
2. Verificar que Railway esté conectado
3. Cada push a `main` desplegará automáticamente

### 5.2 Monitoreo
1. Railway Dashboard → **Metrics**
2. Verificar:
   - **CPU Usage**: <80%
   - **Memory Usage**: <512MB
   - **Response Time**: <500ms

---

## 🎯 **PASO 6: Optimización**

### 6.1 Configurar build cache
Railway automáticamente cachea dependencias, pero puedes optimizar:

1. **requirements.txt** - Ya está optimizado
2. **Runtime.txt** - Crear si necesitas Python específico
3. **Procfile** - No necesario (Railway detecta Python)

### 6.2 Variables de entorno optimizadas
```bash
# Para producción
PYTHON_VERSION=3.11
PYTHONUNBUFFERED=1
PORT=8000
```

---

## 🔧 **Troubleshooting Railway**

### Problema: Build falla
- ✅ Verificar `requirements.txt`
- ✅ Verificar que `app/main.py` existe
- ✅ Verificar logs de build

### Problema: App no responde
- ✅ Verificar variables de entorno
- ✅ Verificar que `uvicorn` esté en requirements.txt
- ✅ Verificar logs de runtime

### Problema: Timeout
- ✅ Verificar que la app se inicie en <30s
- ✅ Optimizar imports
- ✅ Verificar que `--host 0.0.0.0` esté configurado

---

## 📊 **Post-Despliegue**

### ✅ Checklist Final
- [ ] App respondiendo en `https://tu-app.up.railway.app`
- [ ] Health check OK
- [ ] Endpoints funcionando
- [ ] Logs sin errores
- [ ] Métricas estables

### 🎯 Monitoreo
1. **Railway Dashboard**: Métricas y logs
2. **GitHub**: Actions y commits
3. **Uptime**: Monitoreo externo (opcional)

---

## 💰 **Costos y Límites**

### Plan Gratuito
- **$5 creditos/mes** (suficiente para desarrollo)
- **512MB RAM** (suficiente para la API)
- **1GB storage** (suficiente para logs)
- **Sin límite de requests**

### Plan Pro ($20/mes)
- **500GB storage**
- **8GB RAM**
- **Monitoreo avanzado**
- **Dominios personalizados**

---

## 🚀 **Próximos Pasos**

1. **Desplegar en Railway** (este documento)
2. **Configurar R2** (opcional - para imágenes)
3. **Dominio personalizado** (opcional)
4. **Monitoreo** (opcional)
5. **CDN** (opcional)

---

## 📞 **Soporte**

- **Railway Docs**: [railway.app/docs](https://railway.app/docs)
- **Discord**: [discord.gg/railway](https://discord.gg/railway)
- **GitHub Issues**: [github.com/railwayapp/railway](https://github.com/railwayapp/railway)
