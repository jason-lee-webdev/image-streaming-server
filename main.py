from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import asyncio

app = FastAPI()

# 이미지 파일 경로
image_files = ["./jeju-island.jpg", "./bamboo-forest.jpg"]


async def image_generator():
    while True:
        for image_file in image_files:
            # OpenCV로 이미지 읽기
            image = cv2.imread(image_file)
            # 이미지를 JPEG 형식으로 인코딩
            _, jpeg = cv2.imencode('.jpg', image)
            # JPEG 이미지를 바이트로 변환
            image_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n\r\n')
            await asyncio.sleep(1)  # 1초 대기


@app.get("/stream")
async def stream_images():
    return StreamingResponse(image_generator(), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
