import os
from enum import Enum
from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse, JSONResponse

from app.process_invoice_file import ProcessInvoiceFile
from app.upload_invoice_file import UploadInvoiceFile


class TargetType(str, Enum):
    xml = "xml"
    csv = "csv"


BASE_DIR = "./processed_files"


TAGS_METADATA = [
    {
        "name": "Upload invoice",
        "description": "Upload invoice file.",
    },
{
        "name": "Get invoice",
        "description": "Get invoice file by buyer",
    },
]

app = FastAPI(title="InvoiceApp", openapi_tags=TAGS_METADATA)


@app.post("/invoice", tags=["Upload invoice"], response_class=JSONResponse)
async def post_invoice(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """This endpoint sends the csv file to the server.
    Uploads the file and in the another process creates new files based on buyer.
    Returns unique timestamp part of invoice directory"""
    if file.content_type == "text/csv":
        invoice_file = UploadInvoiceFile(file, BASE_DIR).save_upload_file()
        # process the file in background task
        process = ProcessInvoiceFile(invoice_file)
        background_tasks.add_task(process.process_file)
    else:
        # throws an exception if the file is not csv
        raise HTTPException(status_code=422, detail="Invalid file type")

    return {"upload_id": invoice_file.timestamp}


@app.get("/invoice/{upload_id}/{buyer}", tags=["Get invoice"], response_class=FileResponse)
def get_invoice(upload_id: int, buyer: str, target_type: TargetType = TargetType.csv):
    """This endpoint returns xml or csv file by specific upload id, buyer and target type."""

    if target_type != TargetType.csv and target_type != TargetType.xml:
        raise HTTPException(status_code=422, detail="Target type not found")

    file = f"{BASE_DIR}/invoices_{upload_id}/{buyer}.{target_type}"
    if os.path.isfile(file):
        return FileResponse(file)
    else:
        raise HTTPException(status_code=404, detail="File not found. Upload id or buyer invalid.")


