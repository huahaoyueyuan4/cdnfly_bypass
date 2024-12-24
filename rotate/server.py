import os
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import imagehash

app = FastAPI()

hash_cache = {}

IMAGES_FOLDER = "img/rotate-origin"

@app.on_event("startup")
def preload_images():
    global hash_cache
    hash_cache = {}

    if not os.path.exists(IMAGES_FOLDER):
        print(f"文件夹 {IMAGES_FOLDER} 不存在，无法预加载图片。")
        return

    for filename in os.listdir(IMAGES_FOLDER):
        file_path = os.path.join(IMAGES_FOLDER, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    hash_cache[filename] = imagehash.phash(img)
            except Exception as e:
                print(f"跳过无法处理的文件：{filename}，原因：{e}")

@app.post("/similar")
async def find_most_similar_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_stream = BytesIO(contents)
        with Image.open(image_stream) as ref_img:
            reference_hash = imagehash.phash(ref_img)
    except Exception as e:
        return {
            "error": f"无法打开上传的图片: {e}"
        }

    if not hash_cache:
        return {
            "error": "哈希缓存为空，请检查服务启动时是否已加载图片或文件夹为空。"
        }

    min_diff = float('inf')
    most_similar_image_name = None

    for filename, candidate_hash in hash_cache.items():
        diff = reference_hash - candidate_hash
        if diff < min_diff:
            min_diff = diff
            most_similar_image_name = filename

    return {
        "most_similar_image": most_similar_image_name,
        "hash_difference": min_diff
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)