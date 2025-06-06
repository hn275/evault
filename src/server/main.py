from typing import Union
import fastapi


app = fastapi.FastAPI()


@app.get("/")
async def root():
    response = fastapi.Response(
        content="Hello, World!",
        status_code=200,
        media_type="text/plain",
    )

    return response
