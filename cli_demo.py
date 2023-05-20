import os
import platform
import signal

from transformers import AutoTokenizer, AutoModel

import readline


tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)

model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).quantize(8).half().cuda()

model = model.eval()

os_name = platform.system()

clear_command = 'cls' if os_name == 'Windows' else 'clear'

stop_stream = False


def build_prompt(history):
    #
    prompt = "欢迎使用CHATGLM-6B模型，输入内容即可进行对话，CLEAR清空对话历史，STOP终止程序"

    for query, response in history:
        #
        prompt += f"\n\n用户：{query}"
        prompt += f"\n\nCHATGLM-6B：{response}"

    return prompt


def signal_handler(signal, frame):
    #
    global stop_stream

    stop_stream = True


def main():
    #
    history = []

    global stop_stream

    print("欢迎使用CHATGLM-6B模型，输入内容即可进行对话，CLEAR清空对话历史，STOP终止程序")

    while True:

        query = input("\n用户：")

        if query.strip() == "stop":
            #
            break

        if query.strip() == "clear":
            #
            history = []

            os.system(clear_command)  # 执行清屏命令

            print("欢迎使用CHATGLM-6B模型，输入内容即可进行对话，CLEAR清空对话历史，STOP终止程序")

            continue

        count = 0

        for response, history in model.stream_chat(tokenizer, query, history=history):

            if stop_stream:

                stop_stream = False

                break

            else:

                count += 1

                if count % 8 == 0:
                    #
                    os.system(clear_command)

                    print(build_prompt(history), flush=True)  # ？？？刷新

                    signal.signal(signal.SIGINT, signal_handler)  # 每次都要重新设置

        os.system(clear_command)

        print(build_prompt(history), flush=True)


if __name__ == "__main__":
    #
    main()
