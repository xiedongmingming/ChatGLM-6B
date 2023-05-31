from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import uvicorn

file_path = "test.mp4"

app = FastAPI()


@app.get("/")
def main():
    #
    def iterfile():  # 这是生成器函数。它是一个"生成器函数"，因为它里面包含了YIELD语句

        with open(file_path, "rb") as file_like:  # 通过使用WITH块，确保在生成器函数完成后关闭类文件对象

            yield from file_like  # YIELD FROM告诉函数迭代名为FILE_LIKE的东西 对于迭代的每个部分，YIELD的内容作为来自这个生成器函数

    return StreamingResponse(iterfile(), media_type="video/mp4")


uvicorn.run(app, host='0.0.0.0', port=8001, workers=1)
