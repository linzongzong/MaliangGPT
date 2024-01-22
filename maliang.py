from pystray import Icon, Menu, MenuItem
from PIL import Image
from os import path
import sys
import pyperclip
from pynput.keyboard import Key, Controller
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
import configparser

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
img_path = path.join(bundle_dir, 'icon.png')
# 创建任务栏图标
image = Image.open(img_path)  # 你需要提供一个图标文件

class azure_chatgpt:
    def __init__(self) -> None:
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.model = AzureChatOpenAI(
            openai_api_base=config.get('azure','openai_api_base'),
            openai_api_version=config.get('azure','openai_api_version'),
            deployment_name=config.get('azure','deployment_name'),
            openai_api_key=config.get('azure','openai_api_key'),
            openai_api_type="azure",
        )

    def get_clip(self):
        self.clipboard_content = pyperclip.paste()

    def write(self,text):
        pyperclip.copy(' '+text)
        keyboard = Controller()
        keyboard.press(Key.cmd)
        keyboard.press('v')

    def template(self,prompt,head):
        prompt=ChatPromptTemplate.from_template(template=head+prompt)
        messages = prompt.format_messages(text=prompt)
        return self.model(messages).content

    def translate(self):
        prompt_head = "translate the following content to english, just return translated result. "  
        self.get_clip()   
        result=self.template(self.clipboard_content,prompt_head)
        print(result)
        self.write(result)
    
    def rewrite(self):
        prompt_head = "rewriet the following content to aviod plagiarizing, only return rewrite result, use same language as content: "  
        self.get_clip()   
        result=self.template(self.clipboard_content,prompt_head)
        print(result)
        self.write(result)

    def extension(self):
        prompt_head = "extend the following content without hallucination, use truth knowledge, use same language as content: "  
        self.get_clip()   
        result=self.template(self.clipboard_content,prompt_head)
        print(result)
        self.write(result)
    
server=azure_chatgpt()
menu = Menu(MenuItem('Translate', lambda: server.translate()),
            MenuItem('Rewrite', lambda: server.rewrite()),
            MenuItem('Extension', lambda: server.extension()),
            MenuItem('Exit', lambda: icon.stop()))
icon = Icon("mytool", image, "AI工具", menu)
icon.run()
