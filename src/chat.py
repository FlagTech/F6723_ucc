import os
import sys
import asyncio
import time
from typing import Callable
from dotenv import load_dotenv, find_dotenv
from mcp import ClientSession
from google import genai
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from mcp_utils import (
    load_mcp, close_mcp, call_function, 
    tools_to_functions, sessions_to_functions
)
from google_search import google_search
from u_skills import get_skill

load_dotenv(dotenv_path=find_dotenv(usecwd=True))

client = genai.Client()
console = Console()
hist_file = "previous_interaction_id.txt"

async def chat(
    tools: list,
    sessions: list[ClientSession], 
    hooks: list[
        Callable[[genai.interactions.InteractionSSEEvent], None]
    ]
):
    functions = (
        tools_to_functions(client, tools) + 
        await sessions_to_functions(sessions)
    )

    if os.path.exists(hist_file):
        with open(hist_file, 'r') as f:
            previous_interaction_id = f.read()
            console.print(f"接續交談 {previous_interaction_id}")
    else:
        previous_interaction_id = None
    
    results = [] # 單輪交談後的函式叫用結果
    while True:
        if not results:
            prompt = console.input("請輸入訊息(按 ⏎ 結束): ")  
            if prompt.strip() == "":
                break
            contents = prompt
        else:
            contents = results
        calls = [] # 串接串流過程中的函式叫用結果
        async for event in await client.aio.interactions.create(
            model="gemini-2.5-flash",
            previous_interaction_id=previous_interaction_id,
            input=contents,
            tools=functions,
            system_instruction=(
                f"- 現在 GMT 日期與時間："
                f"{time.strftime("%c", time.gmtime())}\n"
                "- 請使用繁體中文\n"
                "以 Markdown 格式回覆\n"
                "- 以使用工具優先，不要自己亂猜\n"
                f"- 你所在的系統平台是 {sys.platform}\n"
            ),
            stream=True,
        ):
            if event.event_type == "interaction.start":
                interaction = event.interaction
                previous_interaction_id = interaction.id
            for hook in hooks:
                hook(event)
            calls.extend(await call_function(
                event, 
                tools, sessions
            ))
        results = calls

    if previous_interaction_id:
        with open(hist_file, 'w') as f:
            f.write(previous_interaction_id)

live: Live | None = None
text: str = ""

def show_text(event):
    global live, text

    if event.event_type == "interaction.start":
        live = Live(
            Markdown(""),
            console=console,
            refresh_per_second=10,
        )
        live.start()

    if event.event_type == "interaction.complete":
        live.stop()
        live = None
        text = ""

    if not (
        event.event_type == "content.delta" and
        event.delta.type == "text"
    ):
        return

    text += event.delta.text or ""
    live.update(Markdown(text))

def show_function_calls(
    event
):
    if not (
        event.event_type == "content.delta" and
        event.delta.type == "function_call"
    ):
        return
    name = event.delta.name
    args = event.delta.arguments
    console.print(f" →{name}(**{args})")

async def main():
    hooks = [show_function_calls, show_text]
    tools = [get_skill]
    try:
        sessions = await load_mcp()
        await chat(tools, sessions, hooks)
    except Exception as e:
        console.print(f"[red]錯誤: {e}[/red]")
    finally:
        await close_mcp()
        print("程式結束")

def run():
    asyncio.run(main())
