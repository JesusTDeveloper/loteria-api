# 🚀 Guía de Despliegue a Producción

## 📋 Checklist Pre-Despliegue

### ✅ Requisitos
- [ ] Cuenta en Render/Railway/Heroku
- [ ] Cuenta en Cloudflare R2 (o AWS S3/B2)
- [ ] Dominio personalizado (opcional)
- [ ] CDN configurado (Cloudflare/CloudFront)

### ✅ Configuración Local
- [ ] FASE 1 completada (local básico)
- [ ] FASE 2 completada (mirror local)
- [ ] Variables de entorno preparadas
- [ ] Tests funcionando

---

## 🎯 **PASO 1: Configurar Cloudflare R2**

### 1.1 Crear cuenta en Cloudflare
1. Ir a [cloudflare.com](https://cloudflare.com)
2. Crear cuenta gratuita
3. Verificar email

### 1.2 Configurar R2
1. Dashboard → **R2 Object Storage**
2. Click **"Create bucket"**
3. Nombre: `loto-static`
4. Seleccionar región (recomendado: `auto`)
5. Click **"Create bucket"**

### 1.3 Crear API Token
1. Dashboard → **My Profile** → **API Tokens**
2. Click **"Create Token"**
3. Template: **"Custom token"**
4. Permissions:
   - **Object Read & Write** (para bucket `loto-static`)
5. Resources:
   - **Include** → **Specific bucket** → `loto-static`
6. Click **"Continue to summary"** → **"Create Token"**

### 1.4 Obtener credenciales
1. Dashboard → **R2 Object Storage** → **Manage R2 API tokens**
2. Click **"Create API token"**
3. Nombre: `lotoapi-production`
4. Permissions: **Object Read & Write**
5. Bucket: `loto-static`
6. Anotar:
   - **Account ID**
   - **Access Key ID**
   - **Secret Access Key**

---

## 🎯 **PASO 2: Configurar CDN**

### 2.1 Cloudflare CDN (Recomendado)
1. Dashboard → **Workers & Pages**
2. Click **"Create application"**
3. Seleccionar **"Pages"**
4. Conectar repositorio GitHub
5. Configurar:
   - **Build command**: `echo "Static site"`
   - **Build output directory**: `public`
   - **Root directory**: `/`

### 2.2 Configurar dominio
1. **Custom domains** → **Set up a custom domain**
2. Agregar: `cdn.tudominio.com`
3. Configurar DNS:
   - Tipo: `CNAME`
   - Nombre: `cdn`
   - Destino: `your-pages-app.pages.dev`

---

## 🎯 **PASO 3: Desplegar en Render**

### 3.1 Crear servicio
1. Ir a [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Conectar repositorio GitHub
4. Configurar:
   - **Name**: `lotoapi`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.2 Variables de entorno
Agregar estas variables en Render:

```bash
MIRROR_IMAGES=true
S3_ENDPOINT=https://ACCOUNT_ID.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=YOUR_ACCESS_KEY_ID
S3_SECRET_KEY=YOUR_SECRET_ACCESS_KEY
CDN_BASE=https://cdn.tudominio.com
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
```

### 3.3 Dominio personalizado
1. **Settings** → **Custom Domains**
2. Agregar: `api.tudominio.com`
3. Configurar DNS:
   - Tipo: `CNAME`
   - Nombre: `api`
   - Destino: `your-app.onrender.com`

---

## 🎯 **PASO 4: Configurar GitHub Actions**

### 4.1 Warm Cache Workflow
1. Ir a `.github/workflows/warm.yml`
2. Reemplazar `https://TU-API` con tu URL real:
   ```yaml
   curl -sS "https://api.tudominio.com/animalitos?date=$D" >/dev/null || true
   curl -sS "https://api.tudominio.com/loterias?date=$D"  >/dev/null || true
   ```

### 4.2 Activar workflow
1. Repository → **Settings** → **Actions** → **General**
2. **Actions permissions**: **Allow all actions and reusable workflows**
3. **Workflow permissions**: **Read and write permissions**

---

## 🎯 **PASO 5: Preseed de Íconos**

### 5.1 Ejecutar preseed
```bash
# En tu máquina local o en Render shell
python tools/preseed_lottery_icons.py
```

### 5.2 Verificar subida
1. Ir a Cloudflare R2 Dashboard
2. Bucket `loto-static` → **Files**
3. Verificar que existan carpetas:
   - `loterias/`
   - `animalitos/`

---

## 🎯 **PASO 6: Testing y Monitoreo**

### 6.1 Tests básicos
```bash
# Health check
curl https://api.tudominio.com/health

# Animalitos
curl "https://api.tudominio.com/animalitos?date=$(date +%Y-%m-%d)"

# Loterías
curl "https://api.tudominio.com/loterias?date=$(date +%Y-%m-%d)"
```

### 6.2 Verificar mirror
- Las imágenes deben comenzar con `https://cdn.tudominio.com/`
- Logs en Render deben mostrar `[mirror] uploaded...`

### 6.3 Monitoreo
1. **Render**: Dashboard → **Logs**
2. **Cloudflare**: Analytics → **Traffic**
3. **GitHub**: Actions → **Warm Cache**

---

## 🔧 **Troubleshooting**

### Problema: Imágenes no se suben
- ✅ Verificar credenciales R2
- ✅ Verificar permisos bucket
- ✅ Verificar `MIRROR_IMAGES=true`

### Problema: CDN no funciona
- ✅ Verificar configuración DNS
- ✅ Verificar dominio personalizado
- ✅ Verificar certificados SSL

### Problema: API no responde
- ✅ Verificar variables de entorno
- ✅ Verificar logs en Render
- ✅ Verificar dependencias

---

## 📊 **Post-Despliegue**

### ✅ Checklist Final
- [ ] API respondiendo en `https://api.tudominio.com`
- [ ] CDN funcionando en `https://cdn.tudominio.com`
- [ ] Imágenes subidas a R2
- [ ] Warm cache ejecutándose
- [ ] Logs sin errores
- [ ] Documentación actualizada

### 🎯 Métricas a monitorear
- **Uptime**: 99.9%+
- **Response time**: <500ms
- **Cache hit rate**: >80%
- **Error rate**: <1%
