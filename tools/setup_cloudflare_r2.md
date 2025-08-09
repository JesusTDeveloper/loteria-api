# 🎯 Configuración de Cloudflare R2 - Paso a Paso

## 🔑 PASO 1: Acceder a R2 Object Storage

1. **Ir al Dashboard de Cloudflare**
   - Abre [dash.cloudflare.com](https://dash.cloudflare.com)
   - Inicia sesión con tu cuenta

2. **Navegar a R2**
   - En el menú lateral izquierdo, busca **"R2 Object Storage"**
   - Click en **"R2 Object Storage"**

## 🪣 PASO 2: Crear el Bucket

1. **Crear nuevo bucket**
   - Click en el botón **"Create bucket"** (o "Crear bucket")
   - Aparecerá un modal/formulario

2. **Configurar bucket**
   - **Name**: `loto-static` (exactamente así, sin espacios)
   - **Location**: Selecciona `Auto` (recomendado) o la región más cercana a ti
   - Click **"Create bucket"**

3. **Verificar creación**
   - Deberías ver el bucket `loto-static` en la lista
   - Status debe mostrar "Active" o "Activo"

## 🔐 PASO 3: Crear API Token

1. **Ir a API Tokens**
   - En el menú lateral, busca **"My Profile"** (o tu nombre)
   - Click en **"API Tokens"**

2. **Crear nuevo token**
   - Click en **"Create Token"**
   - Selecciona **"Custom token"** (token personalizado)

3. **Configurar permisos**
   - **Token name**: `lotoapi-production`
   - **Permissions**: Busca y selecciona **"Object Read & Write"**
   - **Resources**: Selecciona **"Include"** → **"Specific bucket"**
   - **Bucket**: Selecciona `loto-static`

4. **Crear token**
   - Click en **"Continue to summary"**
   - Revisa la configuración
   - Click en **"Create Token"**

5. **Guardar credenciales**
   - **IMPORTANTE**: Copia y guarda en un lugar seguro:
     - **Access Key ID**
     - **Secret Access Key**
   - ⚠️ **No las compartas ni las commitees al repositorio**

## 🎯 PASO 4: Obtener Account ID

1. **Ir a R2 Dashboard**
   - Regresa a **"R2 Object Storage"**

2. **Encontrar Account ID**
   - En la esquina superior derecha, busca tu **Account ID**
   - Es una cadena de 32 caracteres hexadecimales
   - Ejemplo: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

3. **Guardar Account ID**
   - Copia este valor, lo necesitarás para la configuración

## 🔧 PASO 5: Configurar Variables de Entorno

Una vez que tengas todas las credenciales, ejecuta:

```powershell
# En PowerShell, desde el directorio del proyecto
.\tools\setup_production.ps1
```

O crea manualmente el archivo `.env`:

```bash
# Variables de entorno para producción
MIRROR_IMAGES=true
S3_ENDPOINT=https://TU_ACCOUNT_ID.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=TU_ACCESS_KEY_ID
S3_SECRET_KEY=TU_SECRET_ACCESS_KEY
CDN_BASE=https://cdn.tudominio.com
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
```

## ✅ PASO 6: Verificar Configuración

1. **Probar conexión**
   ```powershell
   python tools/test_mirror_complete.py
   ```

2. **Verificar bucket**
   - En R2 Dashboard → `loto-static` → **"Files"**
   - Debería estar vacío inicialmente

## 🚨 TROUBLESHOOTING

### Problema: "Invalid endpoint"
- ✅ Verificar que `S3_ENDPOINT` use el formato correcto: `https://ACCOUNT_ID.r2.cloudflarestorage.com`
- ✅ Verificar que `ACCOUNT_ID` sea correcto (32 caracteres)

### Problema: "Access Denied"
- ✅ Verificar que `S3_ACCESS_KEY` y `S3_SECRET_KEY` sean correctos
- ✅ Verificar que el token tenga permisos **"Object Read & Write"**
- ✅ Verificar que el bucket `loto-static` exista

### Problema: "Bucket not found"
- ✅ Verificar que el nombre del bucket sea exactamente `loto-static`
- ✅ Verificar que el bucket esté en estado "Active"

## 📞 Soporte

Si tienes problemas:
1. Verifica que hayas seguido todos los pasos
2. Revisa los logs en la consola
3. Verifica que las credenciales estén correctas
4. Contacta soporte de Cloudflare si es necesario
