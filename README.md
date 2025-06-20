# eventos
Aplicación web para venta de entradas a eventos

# Cargar base de datos
```bash
python manage.py cargar_datos
```
   >   - Contraseña clientes : `Cliente123`
# Crear admin default
```bash
python manage.py admin_default
```
   > - Un usuario admin con las siguientes credenciales:
   >   - Usuario: `admin`
   >   - Contraseña: `admin123`
# Actualizar estado de tickets ( eventos que ya se realizaron )
```bash
python manage.py tickets_expirados
```
   > - Si el evento ya se realizo, se cambia el estado de todos los tickets relacionados con ese evento a EXPIRED