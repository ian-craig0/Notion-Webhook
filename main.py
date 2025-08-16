from fastapi import FastAPI, Request, Header, HTTPException
from starlette.responses import JSONResponse
import hmac, hashlib, os

app = FastAPI()
NOTION_SECRET = os.getenv("NOTION_SECRET", "replace_with_your_secret")

@app.post("/")
async def notion_webhook(request: Request, notion_signature: str = Header(None)):
    body_bytes = await request.body()
    payload = await request.json()

    # Step 1: Handshake challenge
    if "challenge" in payload:
        return JSONResponse(content={"challenge": payload["challenge"]})

    # Step 2: Signature verification
    if not notion_signature:
        raise HTTPException(400, "Missing signature")

    digest = hmac.new(NOTION_SECRET.encode(), body_bytes, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, notion_signature):
        raise HTTPException(403, "Bad signature")

    # Step 3: Process the event
    print("Received Notion event:", payload)

    return JSONResponse(content={"status": "ok"})
