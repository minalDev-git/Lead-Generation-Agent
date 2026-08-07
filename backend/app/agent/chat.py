import json
import inspect
from config import CONSOLE
from agent.memory import init_history,add_user,add_assistant
from agent.prompt import build_system_prompt
from agent.llm import chat
from agent.tool_registry import get_handler
from pydantic import BaseModel

def format_observation(observation) -> str:
    if isinstance(observation, BaseModel):
        return json.dumps(observation.model_dump(), indent=2)

    if isinstance(observation, (dict, list)):
        return json.dumps(observation, indent=2)

    return str(observation)

def truncate_text(text: str, max_chars: int = 1000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "... [truncated]"

console = CONSOLE

async def run():
    system_p = build_system_prompt()
    history = init_history()
    while True:
        user_input = input("You: ")

        user_input= user_input.strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "q", "exit"):
            print("\nBye")
            return

        add_user(history,user_input)
        # Iterate LLM <-> tools until final answer
        MAX_TOOL_STEPS = 10
        # ───────────────────── LLM think ──────────────────────
        for _ in range(MAX_TOOL_STEPS):
            try:
                raw = chat(history, system=system_p)

                action = json.loads(raw) # type: ignore
                add_assistant(history, json.dumps(action))
            except json.JSONDecodeError as e:
                print(e)
                break
            
            act_type = action.get("action")
            
            if act_type == "tool_call":
                tool_name = action.get("tool","")
                tool_args = action.get("args",{}) or {}
            
                handler= get_handler(tool_name)
                if handler is None:
                    observation = f"[error] Unknown tool: {tool_name}"
                else:
                    try:
                        with console.status(f"[bold green]Executing tool:[/] [yellow]{tool_name}[/]", spinner="dots") as status:
                            status.update(f"[bold cyan]Running {tool_name}[/]")
                            if inspect.iscoroutinefunction(handler):
                                observation = await handler(**tool_args)
                            else:
                                observation = handler(**tool_args)
                    except Exception as e:
                            observation = f"[error] {type(e).__name__}: {e}"
                # Pretty-print for the user
                console.print(f"⏳ [bold yellow]Processing[/] 🔧 [bold]{tool_name}[/]")
                console.print(f"🔧 [cyan]{tool_name}[/] [dim]{truncate_text(str(tool_args))}[/]")

                observation_text = format_observation(observation)
            
                tool_result = (
                    f"[Tool Result for {tool_name}]\n\n"
                    f"{observation_text}"
                )

                add_user(history, tool_result)
                continue
            
            elif act_type == "final":
                answer = action.get("answer","")
                print(f"Agent: {answer}")
                add_assistant(history, answer)
                break
            else:
                print("Unknown action")
                break
        else:
            print("Agent stopped: exceeded maximum tool steps.")