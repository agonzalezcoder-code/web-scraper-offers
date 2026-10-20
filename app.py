import csv
import io
import json
from urllib.parse import urlparse 
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    session
)
import openpyxl

from scraper.fetch_page import fetch_html
from scraper.parse_generic import parse_generic


app = Flask(__name__)
app.secret_key = "un_secreto_super_seguro_para_sesiones"


def es_url_valida_y_segura(url):
    """Verifica que la URL tenga el formato correcto y bloquea destinos locales peligrosos."""
    try:
        resultado = urlparse(url)
        if not resultado.scheme or not resultado.netloc:
            return False
        if resultado.scheme not in ("http", "https"):
            return False
        
        host_peligrosos = ("localhost", "127.0.0.1", "0.0.0.0", "::1")
        if any(hp in resultado.netloc.lower() for hp in host_peligrosos):
            return False
            
        return True
    except Exception:
        return False


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/extraer", methods=["POST"])
def extraer():
    url = request.form["url"].strip()

    if not es_url_valida_y_segura(url):
        return render_template(
            "index.html",
            error="La URL introducida no es válida o apunta a un destino no permitido. Asegúrate de incluir http:// o https://"
        )

    try:
        html = fetch_html(url)
        resultados = parse_generic(html, url)

        if len(resultados) > 500:
            resultados = resultados[:500]

        session["resultados_recientes"] = resultados
        session["url_reciente"] = url

        return render_template(
            "index.html",
            resultados=resultados,
            source_url=url
        )

    except Exception as e:
        error_msg = "No se pudo extraer la información. Comprueba la URL e inténtalo de nuevo."
        error_str = str(e).lower()
        
        if "timeout" in error_str or "time out" in error_str:
            error_msg = "El tiempo de espera ha sido agotado (La página web tardó demasiado en responder)."
        elif "404" in error_str:
            error_msg = "Error 404: La página web solicitada no existe."
        elif "403" in error_str:
            error_msg = "Error 403: El sitio web de destino denegó el acceso al extractor."

        return render_template(
            "index.html",
            error=error_msg
        )


@app.route("/exportar/<formato>", methods=["POST"])
def exportar(formato):
    if formato not in ("csv", "json", "excel"):
        return "Formato no permitido", 400

    resultados = session.get("resultados_recientes")
    
    if not resultados:
        return "No hay datos guardados para exportar. Por favor, realiza una extracción primero.", 400

    try:
        if formato == "json":
            contenido = json.dumps(resultados, ensure_ascii=False, indent=4)
            archivo = io.BytesIO(contenido.encode("utf-8"))
            return send_file(
                archivo,
                mimetype="application/json",
                as_attachment=True,
                download_name="resultados.json"
            )

        elif formato == "csv":
            salida = io.StringIO(newline="")
            campos = ["tipo", "texto", "enlace"]
            escritor = csv.DictWriter(salida, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(resultados)

            archivo = io.BytesIO(salida.getvalue().encode("utf-8-sig"))
            return send_file(
                archivo,
                mimetype="text/csv",
                as_attachment=True,
                download_name="resultados.csv"
            )

        elif formato == "excel":
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Resultados Extracción"

            ws.append(["Tipo", "Información", "Enlace"])

            for fila in resultados:
                ws.append([fila["tipo"], fila["texto"], fila["enlace"]])

            archivo_excel = io.BytesIO()
            wb.save(archivo_excel)
            archivo_excel.seek(0)

            return send_file(
                archivo_excel,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name="resultados.xlsx"
            )

    except Exception:
        return (
            "No se pudo generar el archivo. Inténtalo de nuevo.",
            400
        )


if __name__ == "__main__":
    app.run(debug=True)
