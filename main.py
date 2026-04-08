from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from rembg import remove
import io
import os

# Suppress onnxruntime warnings for missing GPU
os.environ["OMP_NUM_THREADS"] = "1"

app = FastAPI(title="Viserion API")

# Setup CORS to allow React frontend (running on localhost:5173 or similar depending on Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local development simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Viserion API is running"}

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Endpoint that accepts an image, removes the background using rembg,
    and returns the processed image.
    """
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    
    # Remove background
    output_image = remove(input_image)
    
    # Save the result into a byte stream
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return StreamingResponse(img_byte_arr, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)