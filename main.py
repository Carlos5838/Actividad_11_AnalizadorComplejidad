from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import Response
import requests

app = FastAPI(
    title="API Analizador de Complejidad",
    description="Analiza archivos de código en peor caso (Big-O) y mejor caso (Big-Omega)",
    version="1.0"
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2"


def generate_response(prompt, model=MODELO):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error al conectar con Ollama: {e}")


template_big_o = """Eres un experto en análisis de complejidad algorítmica.
Analiza el siguiente código considerando el PEOR CASO y utiliza notación Big-O.

Código:
{code}

Devuelve SOLAMENTE el código fuente modificado, sin Markdown y sin bloques ```.
Conserva el código original y agrega comentarios usando la sintaxis correspondiente al lenguaje.
Añade comentarios con la complejidad Big-O línea por línea cuando corresponda.
Al final del archivo agrega un bloque de comentarios con:
- Suma de las complejidades individuales.
- Complejidad de mayor grado.
- Complejidad total del programa en Big-O.
La suma puede mostrarse, por ejemplo, como O(1) + O(n) + O(n^2), y después debe simplificarse identificando el término dominante.
"""


template_big_omega = """Eres un experto en análisis de complejidad algorítmica.
Analiza el siguiente código considerando el MEJOR CASO y utiliza notación Big-Omega (Ω).

Código:
{code}

Devuelve SOLAMENTE el código fuente modificado, sin Markdown y sin bloques ```.
Conserva el código original y agrega comentarios usando la sintaxis correspondiente al lenguaje.
Añade comentarios con la complejidad Big-Omega línea por línea cuando corresponda.
Al final del archivo agrega un bloque de comentarios con:
- Suma de las complejidades individuales.
- Complejidad de mayor grado.
- Complejidad total del programa en Big-Omega.
La suma puede mostrarse, por ejemplo, como Ω(1) + Ω(n) + Ω(n^2), y después debe simplificarse identificando el término dominante.
"""


def analizar_big_o(codigo):
    return generate_response(template_big_o.format(code=codigo))


def analizar_big_omega(codigo):
    return generate_response(template_big_omega.format(code=codigo))


async def leer_archivo(file: UploadFile):
    contenido = await file.read()
    try:
        return contenido.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="El archivo debe contener código fuente en formato de texto UTF-8.")


def nombre_resultado(nombre, tipo):
    nombre = nombre or "codigo.txt"
    if "." in nombre:
        base, extension = nombre.rsplit(".", 1)
        return f"{base}_{tipo}.{extension}"
    return f"{nombre}_{tipo}.txt"


@app.get("/")
def inicio():
    return {"mensaje": "API de análisis de complejidad activa", "documentacion": "/docs"}


@app.post("/complejidad/peor-caso")
async def peor_caso(file: UploadFile = File(...)):
    codigo = await leer_archivo(file)
    resultado = analizar_big_o(codigo)
    nombre = nombre_resultado(file.filename, "big_o")
    return Response(
        content=resultado,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'}
    )


@app.post("/complejidad/mejor-caso")
async def mejor_caso(file: UploadFile = File(...)):
    codigo = await leer_archivo(file)
    resultado = analizar_big_omega(codigo)
    nombre = nombre_resultado(file.filename, "big_omega")
    return Response(
        content=resultado,
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{nombre}"'}
    )
