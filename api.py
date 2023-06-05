from fastapi import FastAPI, Request

from fastapi.responses import StreamingResponse

from transformers import AutoTokenizer, AutoModel

import uvicorn, json, datetime

import torch

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    #
    if torch.cuda.is_available():
        #
        with torch.cuda.device(CUDA_DEVICE):
            #
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()


@app.post("/v1/completions")
async def completions(request: Request):
    #
    global model, tokenizer

    json_post_raw = await request.json()

    json_post = json.dumps(json_post_raw)

    json_post_list = json.loads(json_post)

    prompt = json_post_list.get('prompt')[0]
    modelname = json_post_list.get('model')
    temperature = json_post_list.get('temperature')
    max_tokens = json_post_list.get('max_tokens')
    top_p = json_post_list.get('top_p')
    frequency_penalty = json_post_list.get('frequency_penalty')
    presence_penalty = json_post_list.get('presence_penalty')
    n = json_post_list.get('n')
    logit_bias = json_post_list.get('logit_bias')
    stream = json_post_list.get('stream')

    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')

    # {
    #     "prompt": [
    #         "Write me a song about sparkling water."
    #     ],
    #     "model": "text-davinci-003",
    #     "temperature": 0,
    #     "max_tokens": 256,
    #     "top_p": 1,
    #     "frequency_penalty": 0,
    #     "presence_penalty": 0,
    #     "n": 1,
    #     "logit_bias": {
    #
    #     },
    #     "stream": true
    # }

    if stream:

        def stream_chat(history):

            for response, history in model.stream_chat(
                    tokenizer,
                    prompt,
                    history=history,
                    max_length=max_length if max_length else 2048,
                    top_p=top_p if top_p else 0.7,
                    temperature=temperature if temperature else 0.95
            ):
                #
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                answer = {
                    "response": response,
                    "history": history,
                    "status": 200,
                    "time": time
                }

                log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'

                print(log)

                yield json.dumps(answer, ensure_ascii=False)

        return StreamingResponse(stream_chat(history), media_type="application/json")

        torch_gc()

    else:

        response, history = model.chat(
            tokenizer,
            prompt,
            history=history,
            max_length=max_length if max_length else 2048,
            top_p=top_p if top_p else 0.7,
            temperature=temperature if temperature else 0.95
        )

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        answer = {
            "response": response,
            "history": history,
            "status": 200,
            "time": time
        }

        log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'

        print(log)

        torch_gc()

        return json.dumps(answer, ensure_ascii=False)


@app.post("/chat")
async def chat(request: Request):
    #
    global model, tokenizer

    json_post_raw = await request.json()

    json_post = json.dumps(json_post_raw)

    json_post_list = json.loads(json_post)

    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    stream = json_post_list.get('stream')

    if stream:

        def stream_chat(history):

            for response, history in model.stream_chat(
                    tokenizer,
                    prompt,
                    history=history,
                    max_length=max_length if max_length else 2048,
                    top_p=top_p if top_p else 0.7,
                    temperature=temperature if temperature else 0.95
            ):
                #
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                answer = {
                    "response": response,
                    "history": history,
                    "status": 200,
                    "time": time
                }

                log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'

                print(log)

                yield json.dumps(answer, ensure_ascii=False)

        return StreamingResponse(stream_chat(history), media_type="application/json")

        torch_gc()

    else:

        response, history = model.chat(
            tokenizer,
            prompt,
            history=history,
            max_length=max_length if max_length else 2048,
            top_p=top_p if top_p else 0.7,
            temperature=temperature if temperature else 0.95
        )

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        answer = {
            "response": response,
            "history": history,
            "status": 200,
            "time": time
        }

        log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'

        print(log)

        torch_gc()

        return json.dumps(answer, ensure_ascii=False)


if __name__ == '__main__':
    #
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)

    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(8).half().cuda()

    model.eval()

    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
