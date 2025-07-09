from pydantic import BaseModel

class Dossier(BaseModel):
    product_name: str
    notification_no: str
    files: dict
