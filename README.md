# GeoLocator Function

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una función serverless que proporciona información de geolocalización basada en direcciones IP. La función detecta automáticamente la IP del visitante y devuelve información detallada sobre su ubicación.

## Estructura del Proyecto

```
geoLocator/
├── packages/
│   └── geoLocator/        # Nombre del paquete (debe coincidir con project.yml)
│       └── main.py        # Archivo principal con el código (nombre fijo)
└── project.yml            # Configuración del proyecto
```

### Explicación de la Estructura

1. El archivo `main.py` SIEMPRE debe llamarse así. Es el punto de entrada que Digital Ocean busca por defecto.
2. En `project.yml`, el nombre `main` en la sección de functions es el nombre del endpoint, NO el nombre del archivo:

```yaml
packages:
  - name: geoLocator       # Debe coincidir con el nombre del directorio
    functions:
      - name: main         # Nombre del endpoint en la URL
        runtime: python:3.9
        web: true
```

3. La URL final se construye así:
   - Base: `https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/[namespace]`
   - Paquete: `/geoLocator` (del name en packages)
   - Función: `/main` (del name en functions)

Por lo tanto:
- El archivo se DEBE llamar `main.py`
- El nombre `main` en `project.yml` es para la URL del endpoint
- Son dos "main" diferentes con propósitos distintos

## Requisitos

- Digital Ocean Account
- Digital Ocean CLI (`doctl`) instalado y configurado
- Python 3.9 o superior

## Configuración

1. Instalar doctl:
   ```bash
   brew install doctl  # Para macOS
   ```

2. Autenticar con Digital Ocean:
   ```bash
   doctl auth init
   ```

## Despliegue

Para desplegar la función:

```bash
doctl serverless deploy .
```

## Comandos Útiles

### Ver la URL de la función
```bash
doctl serverless fn get geoLocator/main --url
```

### Ver los logs de la función
```bash
doctl serverless activation list  # Lista todas las activaciones
doctl serverless activation get <activation-id>  # Ver logs específicos
```

### Actualizar la función
Después de hacer cambios, simplemente vuelve a ejecutar:
```bash
doctl serverless deploy .
```

## Endpoint

### URL Base
```
https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-16be738e-8723-4eac-ba2d-7da78fbd8d5f/geoLocator/main
```

### Método
- GET

### Respuesta

La función retorna un JSON con la siguiente estructura:

```json
{
    "ip": "8.8.8.8",              // IP detectada
    "range": [0, 0],              // Rango IP (simplificado)
    "country": "US",              // Código del país
    "region": "California",       // Región/Estado
    "eu": "0",                    // Si está en la UE (1) o no (0)
    "timezone": "America/Los_Angeles", // Zona horaria
    "city": "Mountain View",      // Ciudad
    "ll": [37.42301, -122.083352], // Latitud y Longitud
    "metro": 0,                   // Código metro (simplificado)
    "area": 1000                  // Código de área (simplificado)
}
```

### Códigos de Estado

- 200: Éxito
- 500: Error del servidor

### Headers de Respuesta

```
Content-Type: application/json
Access-Control-Allow-Origin: *
```

## Ejemplos de Uso

### Curl
```bash
curl -X GET "https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-16be738e-8723-4eac-ba2d-7da78fbd8d5f/geoLocator/main"
```

### JavaScript
```javascript
fetch('https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-16be738e-8723-4eac-ba2d-7da78fbd8d5f/geoLocator/main')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python
```python
import requests
response = requests.get('https://faas-sfo3-7872a1dd.doserverless.co/api/v1/web/fn-16be738e-8723-4eac-ba2d-7da78fbd8d5f/geoLocator/main')
data = response.json()
print(data)
```

## Limitaciones

- La función utiliza el servicio gratuito ipapi.co que tiene los siguientes límites:
  - 1,000 peticiones por día
  - Máximo 30 peticiones por minuto
  - Para más peticiones, se requiere una suscripción en ipapi.co
- La precisión de la geolocalización depende de la base de datos de ipapi.co
- Los campos range, metro y area están simplificados y retornan valores por defecto
- El servicio podría ser más lento en algunas regiones geográficas

## Solución de Problemas

1. Si la función retorna un error 500:
   - Verifica los logs usando `doctl serverless activation list`
   - Asegúrate de que la IP sea válida
   - Verifica que ipapi.co esté funcionando

2. Si el deploy falla:
   - Verifica que la estructura de archivos sea correcta
   - Asegúrate de que `project.yml` esté bien configurado
   - Verifica que tengas los permisos necesarios en Digital Ocean 

## Licencia

Este proyecto está bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 Cairo Resendiz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
``` 