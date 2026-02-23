from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI(title="Diego Aguirre - Mercado Libre 2026")

# Mount static/CSS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# DB productos
def init_db():
    conn = sqlite3.connect("mercado.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos 
                 (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL, imagen TEXT)''')
    # Datos demo
    c.execute("INSERT OR IGNORE INTO productos VALUES (1, 'iPhone 16', 4500, 'iphone.jpg')")
    c.execute("INSERT OR IGNORE INTO productos VALUES (2, 'MacBook Pro', 8500, 'macbook.jpg')")
    conn.commit()
    conn.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    init_db()
    conn = sqlite3.connect("mercado.db")
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    productos = [{"id": r[0], "nombre": r[1], "precio": r[2], "imagen": r[3]} for r in c.fetchall()]
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "productos": productos})

@app.post("/agregar")
async def agregar(nombre: str = Form(...), precio: float = Form(...), imagen : str = Form(...)):
    conn = sqlite3.connect("mercado.db")
    c = conn.cursor()
    c.execute("INSERT INTO productos (nombre, precio, imagen) VALUES (?, ?, ?)", 
              (nombre, precio, imagen))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
