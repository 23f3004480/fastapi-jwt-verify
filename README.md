# FastAPI RS256 JWT Verification

## Deploy on Render
1. Push `main.py`, `requirements.txt`, and `render.yaml` to a GitHub repository.
2. In Render, create a new Web Service connected to the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy, then submit the full URL ending in `/verify`.

## Endpoint
`POST /verify`
JSON body: `{"token":"<JWT>"}`

Valid tokens return status 200 with `valid`, `email`, `sub`, and `aud`.
Invalid signature, issuer, audience, or expiration returns HTTP 401 with exactly `{"valid":false}`.
