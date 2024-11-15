# Api_Usuarios
##POST: Crear Usuario
```
{
  "email": "email@example.com",
  "nombre": "Juan Perez",
  "password": "password123"
}
```
##GET: Consultar usuario
```
Query Params (solo uno es necesario, tenantID o email):
tenantID: "202411-123e4567-e89b-12d3-a456-426614174000"
email: "email@example.com"
```
##PUT: Actualizar Usuario
```
{
  "tenantID": "202411-123e4567-e89b-12d3-a456-426614174000",
  "nombre": "Juan Perez Actualizado",
  "email": "nuevoemail@example.com"
}
```
##DELETE: Eliminar Usuario
```
{
  "tenantID": "202411-123e4567-e89b-12d3-a456-426614174000"
}
```

##GET: Listar Usuario
```
Query Params (opcional para paginación):
limit: "10" (cantidad máxima de usuarios por página)
lastEvaluatedKey: "{\"tenantID\": \"202411-123e4567-e89b-12d3-a456-426614174000\", \"fechaCreacion\": \"2024-11-10T15:30:45Z\"}" (para continuar desde el último usuario evaluado)
```

##POST: Login Usuario
```
{
  "email": "email@example.com",
  "password": "password123"
}
```

##TENER EN CUENTA:
En caso de solicitudes POST, PUT, o DELETE, selecciona la pestaña Body, elige raw y configura el tipo como JSON. Luego, pega el JSON de ejemplo para cada solicitud.
Para los endpoints GET, configura los parámetros en la pestaña Params.

##ENDPOINTS:
```
  POST - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/create
  GET - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/get
  PUT - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/update
  DELETE - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/delete
  GET - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/list
  POST - https://dcd20ifa4b.execute-api.us-east-1.amazonaws.com/dev/usuarios/login\
```
