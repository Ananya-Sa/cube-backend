from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO


app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket('/ws')
async def videoFrame(websocket: WebSocket):
    await websocket.accept()

    frame_count = 0

    while True:
        data = await websocket.receive()
        print(f'data: {data}')
        binary_stream = BytesIO(data.get('bytes'))

        # Open the image using PIL
        image = Image.open(binary_stream)

        # Save the image to a file
        image.save(f"frame-{frame_count}.png")


        frame_count += 1


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
