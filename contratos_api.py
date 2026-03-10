"""
contratos_api.py
API FastAPI que genera contratos en .docx y .pdf
Deploy en Railway o Render junto con los machotes.

Requiere:
  pip install fastapi uvicorn python-docx
  apt install libreoffice (para PDF)
"""

import os
import uuid
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from generar_contratos import generar_arrendamiento, generar_compraventa

app = FastAPI(title="Generador de Contratos", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMP = tempfile.gettempdir()


class DatosArrendamiento(BaseModel):
    fecha_firma: str
    nombre_arrendador: str
    nombre_arrendatario: str
    nombre_obligado_solidario: str
    domicilio_inmueble: str
    domicilio_arrendador: str
    domicilio_obligado: str
    destino_uso: str
    fecha_inicio: str
    fecha_terminacion: str
    monto_renta_numeros: str
    monto_renta_letras: str
    monto_deposito_numeros: str
    monto_deposito_letras: str
    forma_pago: str
    fecha_pago_renta: str
    fecha_nuevo_contrato: str


class DatosCompraventa(BaseModel):
    fecha_contrato: str
    nombre_vendedora: str
    nombre_comprador: str
    domicilio_inmueble: str
    colonia_inmueble: str
    cp_inmueble: str
    numero_escritura: str
    nombre_notario: str
    numero_notaria: str
    tomo_rpp: str
    registro_rpp: str
    domicilio_vendedora: str
    domicilio_comprador: str
    precio_total_letras: str
    precio_total_numeros: str
    monto_arras_letras: str
    monto_arras_numeros: str
    monto_segundo_pago_letras: str
    monto_segundo_pago_numeros: str
    cuenta_bancaria_vendedora: str
    banco_vendedora: str
    fecha_limite_segundo_pago: str
    fecha_limite_escritura: str
    pena_convencional_comprador_letras: str
    pena_convencional_comprador_numeros: str
    pena_convencional_vendedora_letras: str
    pena_convencional_vendedora_numeros: str


@app.post("/contratos/arrendamiento/docx")
def contrato_arrendamiento_docx(datos: DatosArrendamiento):
    uid = uuid.uuid4().hex[:8]
    docx_path = os.path.join(TMP, f"arrendamiento_{uid}.docx")
    pdf_path  = os.path.join(TMP, f"arrendamiento_{uid}.pdf")
    try:
        generar_arrendamiento(datos.dict(), docx_path, pdf_path)
        return FileResponse(
            docx_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Contrato_Arrendamiento.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contratos/arrendamiento/pdf")
def contrato_arrendamiento_pdf(datos: DatosArrendamiento):
    uid = uuid.uuid4().hex[:8]
    docx_path = os.path.join(TMP, f"arrendamiento_{uid}.docx")
    pdf_path  = os.path.join(TMP, f"arrendamiento_{uid}.pdf")
    try:
        generar_arrendamiento(datos.dict(), docx_path, pdf_path)
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="No se pudo generar el PDF")
        return FileResponse(pdf_path, media_type="application/pdf",
                            filename="Contrato_Arrendamiento.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contratos/compraventa/docx")
def contrato_compraventa_docx(datos: DatosCompraventa):
    uid = uuid.uuid4().hex[:8]
    docx_path = os.path.join(TMP, f"compraventa_{uid}.docx")
    pdf_path  = os.path.join(TMP, f"compraventa_{uid}.pdf")
    try:
        generar_compraventa(datos.dict(), docx_path, pdf_path)
        return FileResponse(
            docx_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Promesa_Compraventa.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contratos/compraventa/pdf")
def contrato_compraventa_pdf(datos: DatosCompraventa):
    uid = uuid.uuid4().hex[:8]
    docx_path = os.path.join(TMP, f"compraventa_{uid}.docx")
    pdf_path  = os.path.join(TMP, f"compraventa_{uid}.pdf")
    try:
        generar_compraventa(datos.dict(), docx_path, pdf_path)
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="No se pudo generar el PDF")
        return FileResponse(pdf_path, media_type="application/pdf",
                            filename="Promesa_Compraventa.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("contratos_api:app", host="0.0.0.0", port=8001, reload=True)
