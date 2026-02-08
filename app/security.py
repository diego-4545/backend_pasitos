from fastapi import Header, HTTPException

from app.config import API_KEY

def verificar_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

