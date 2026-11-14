from fastapi import FastAPI, HTTPException, status, Form, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="El rincón de los postres")

# Habilitar CORS para permitir peticiones desde Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paso 1: El modelo Producto con Pydantic
class Producto(BaseModel):
    id: int
    nombre: str
    precio_final: float
    cuotas_cantidad: int
    cuotas_valor: float
    garantia_meses: int
    stock: int

class ProductoCreate(BaseModel):
    nombre: str
    precio_final: float
    cuotas_cantidad: int
    cuotas_valor: float
    garantia_meses: int
    stock: int

# Paso 2: Base de datos simulada en memoria
productos_db: list[Producto] = [
    Producto(
        id=1,
        nombre="Hamburguesa (Está hecho de banana y avena)",
        precio_final=9500,
        cuotas_cantidad=3,
        cuotas_valor=3166.67,
        garantia_meses=0,
        stock=15
    ),
    Producto(
        id=2,
        nombre="Esponja (Es un bizcochuelo)",
        precio_final=12500,
        cuotas_cantidad=3,
        cuotas_valor=4166.67,
        garantia_meses=0,
        stock=15
    ),
    Producto(
        id=3,
        nombre="Huevo (De gelatina)",
        precio_final=6000,
        cuotas_cantidad=3,
        cuotas_valor=2000.0,
        garantia_meses=0,
        stock=15
    ),
    Producto(
        id=4,
        nombre="Vela (Chocolate blanco y negro)",
        precio_final=9000,
        cuotas_cantidad=3,
        cuotas_valor=3000.0,
        garantia_meses=0,
        stock=15
    ),
    Producto(
        id=5,
        nombre="Tomate (Algo parecido al alfajor de maicena)",
        precio_final=11000,
        cuotas_cantidad=3,
        cuotas_valor=3666.67,
        garantia_meses=0,
        stock=15
    )
]

# Paso 3: Endpoint GET /productos
@app.get("/productos", response_model=list[Producto])
def obtener_productos():
    return productos_db

# Paso 4: Endpoint POST /productos
@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    nuevo_id = max([p.id for p in productos_db], default=0) + 1
    nuevo_producto = Producto(
        id=nuevo_id,
        nombre=producto.nombre,
        precio_final=producto.precio_final,
        cuotas_cantidad=producto.cuotas_cantidad,
        cuotas_valor=producto.cuotas_valor,
        garantia_meses=producto.garantia_meses,
        stock=producto.stock
    )
    productos_db.append(nuevo_producto)
    return nuevo_producto

# Paso 5: Endpoint GET /productos/{id}
@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto_por_id(producto_id: int):
    for prod in productos_db:
        if prod.id == producto_id:
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Paso 6: Endpoint PUT /productos/{id}
@app.put("/productos/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, producto_update: ProductoCreate):
    for i, prod in enumerate(productos_db):
        if prod.id == producto_id:
            prod_modificado = Producto(
                id=producto_id,
                nombre=producto_update.nombre,
                precio_final=producto_update.precio_final,
                cuotas_cantidad=producto_update.cuotas_cantidad,
                cuotas_valor=producto_update.cuotas_valor,
                garantia_meses=producto_update.garantia_meses,
                stock=producto_update.stock
            )
            productos_db[i] = prod_modificado
            return prod_modificado
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Paso 7: Endpoint DELETE /productos/{id}
@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int):
    for i, prod in enumerate(productos_db):
        if prod.id == producto_id:
            productos_db.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Endpoint para subida de imagen de producto
@app.post("/productos/{producto_id}/imagen")
async def subir_imagen_producto(producto_id: int, file: UploadFile = File(...)):
    for prod in productos_db:
        if prod.id == producto_id:
            return {"mensaje": "Imagen subida correctamente", "filename": file.filename}
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# ── Modelos y Endpoints de Autenticación & Usuarios ──
class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str
    acepto_tratamiento: bool

usuarios_db = [
    {
        "id": 1,
        "email": "admin@tienda.com",
        "nombre": "Administradora",
        "password": "admin",
        "rol": "admin",
        "acepto_tratamiento": True,
        "creado_en": datetime.now().isoformat()
    }
]

pedidos_db = []

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: UsuarioRegistro):
    if not datos.acepto_tratamiento:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe aceptar el tratamiento de datos personales conforme a la Ley 25.326."
        )
    for u in usuarios_db:
        if u["email"].lower() == datos.email.lower():
            raise HTTPException(status_code=400, detail="El email ya se encuentra registrado.")
    
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "email": datos.email,
        "nombre": datos.nombre,
        "password": datos.password,
        "rol": "admin" if "admin" in datos.email.lower() else "customer",
        "acepto_tratamiento": datos.acepto_tratamiento,
        "creado_en": datetime.now().isoformat()
    }
    usuarios_db.append(nuevo_usuario)
    return {"mensaje": "Usuario registrado exitosamente"}

@app.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    for u in usuarios_db:
        if u["email"].lower() == username.lower() and u["password"] == password:
            return {"access_token": f"token-{u['id']}-{u['email']}", "token_type": "bearer"}
    # Permitir login de prueba automático si el usuario no existe
    nuevo_usuario = {
        "id": len(usuarios_db) + 1,
        "email": username,
        "nombre": username.split("@")[0].capitalize(),
        "password": password,
        "rol": "admin" if "admin" in username.lower() else "customer",
        "acepto_tratamiento": True,
        "creado_en": datetime.now().isoformat()
    }
    usuarios_db.append(nuevo_usuario)
    return {"access_token": f"token-{nuevo_usuario['id']}-{nuevo_usuario['email']}", "token_type": "bearer"}

@app.get("/auth/me")
def obtener_usuario_actual(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    token = authorization.replace("Bearer ", "")
    partes = token.split("-")
    if len(partes) >= 3:
        user_id = int(partes[1])
        for u in usuarios_db:
            if u["id"] == user_id:
                return {
                    "id": u["id"],
                    "email": u["email"],
                    "nombre": u["nombre"],
                    "rol": u["rol"]
                }
    if usuarios_db:
        u = usuarios_db[0]
        return {
            "id": u["id"],
            "email": u["email"],
            "nombre": u["nombre"],
            "rol": u["rol"]
        }
    raise HTTPException(status_code=401, detail="Token no válido")

@app.get("/usuarios/me/datos")
def obtener_mis_datos(authorization: Optional[str] = Header(None)):
    user = obtener_usuario_actual(authorization)
    return {
        "usuario": user,
        "pedidos": [p for p in pedidos_db if p.get("usuario_id") == user["id"]],
        "ley_25326": {
            "estado": "Conforme",
            "derechos": ["Acceso", "Rectificación", "Actualización", "Supresión"]
        }
    }

@app.delete("/usuarios/me", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(authorization: Optional[str] = Header(None)):
    user = obtener_usuario_actual(authorization)
    for i, u in enumerate(usuarios_db):
        if u["id"] == user["id"]:
            usuarios_db.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# ── Modelos y Endpoints de Pedidos ──
class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int

class PedidoCreate(BaseModel):
    items: List[ItemPedido]

@app.post("/pedidos/", status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCreate, authorization: Optional[str] = Header(None)):
    user = obtener_usuario_actual(authorization) if authorization else {"id": 1, "email": "invitado"}
    total = 0.0
    items_detalle = []
    for item in pedido.items:
        prod = next((p for p in productos_db if p.id == item.producto_id), None)
        if prod:
            subtotal = prod.precio_final * item.cantidad
            total += subtotal
            items_detalle.append({
                "producto_id": prod.id,
                "nombre": prod.nombre,
                "precio": prod.precio_final,
                "cantidad": item.cantidad,
                "subtotal": subtotal
            })
    
    nuevo_pedido = {
        "id": len(pedidos_db) + 1001,
        "usuario_id": user["id"],
        "items": items_detalle,
        "total": total,
        "estado": "Completado",
        "creado_en": datetime.now().isoformat()
    }
    pedidos_db.append(nuevo_pedido)
    return nuevo_pedido

@app.get("/pedidos/mios")
def obtener_mis_pedidos(authorization: Optional[str] = Header(None)):
    user = obtener_usuario_actual(authorization)
    return [p for p in pedidos_db if p.get("usuario_id") == user["id"]]

@app.post("/pedidos/{pedido_id}/revocacion")
def revocar_pedido(pedido_id: int, authorization: Optional[str] = Header(None)):
    for p in pedidos_db:
        if p["id"] == pedido_id:
            p["estado"] = "Revocado (Arrepentimiento Ley 24.240)"
            return {"mensaje": "Pedido revocado exitosamente", "pedido": p}
    raise HTTPException(status_code=404, detail="Pedido no encontrado")
