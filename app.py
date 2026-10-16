
import csv
import io
import json

from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from scraper.fetch_page import fetch_html
from scraper.parse_generic import parse_generic


app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/extraer", methods=["POST"])
def extraer():
    url = request.form["url"].strip()

    try:
        html = fetch_html(url)
        resultados = parse_generic(html, url)

        return render_template(
            "index.html",
            resultados=resultados,
            source_url=url
        )

    except Exception:
        return render_template(
            "index.html",
            error=(
                "No se pudo extraer la información. "
                "Comprueba la URL e inténtalo de nuevo."
            )
        )


@app.route("/exportar/<formato>", methods=["POST"])
def exportar(formato):
    if formato not in ("csv", "json"):
        return "Formato no permitido", 400

    url = request.form["url"].strip()

    try:
        html = fetch_html(url)
        resultados = parse_generic(html, url)

        if formato == "json":
            contenido = json.dumps(
                resultados,
                ensure_ascii=False,
                indent=4
            )

            archivo = io.BytesIO(
                contenido.encode("utf-8")
            )

            return send_file(
                archivo,
                mimetype="application/json",
                as_attachment=True,
                download_name="resultados.json"
            )

        salida = io.StringIO(newline="")
        campos = ["tipo", "texto", "enlace"]

        escritor = csv.DictWriter(
            salida,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resultados)

        archivo = io.BytesIO(
            salida.getvalue().encode("utf-8-sig")
        )

        return send_file(
            archivo,
            mimetype="text/csv",
            as_attachment=True,
            download_name="resultados.csv"
        )

    except Exception:
        return (
            "No se pudo generar el archivo. "
            "Comprueba la URL e inténtalo de nuevo.",
            400
        )


if __name__ == "__main__":
    app.run(debug=True)