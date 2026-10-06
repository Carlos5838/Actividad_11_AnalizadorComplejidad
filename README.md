# API Analizador de Complejidad

API en FastAPI que recibe un archivo de código fuente y utiliza Ollama con `llama3.2` para generar una copia comentada con el análisis de complejidad.

## Endpoints

- `POST /complejidad/peor-caso`: análisis del peor caso en notación Big-O.
- `POST /complejidad/mejor-caso`: análisis del mejor caso en notación Big-Omega (Ω).

Ambos endpoints reciben un archivo mediante el campo `file` y devuelven un archivo de código con comentarios línea por línea y un bloque final con la suma de complejidades, la de mayor grado y la complejidad total.

## Instalación

```bash
pip install -r requirements.txt
```

También debes tener Ollama instalado y el modelo disponible:

```bash
ollama pull llama3.2
```

## Ejecución

```bash
uvicorn main:app --reload
```

Después abre:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger puedes seleccionar cualquiera de los dos endpoints, presionar **Try it out**, cargar un archivo de código y ejecutar la petición.
