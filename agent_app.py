from pathlib import Path
from schema import tool_schema
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
import json
from tool import get_commission_rate, get_cost, get_exchange_rate, read_filter_csv, save_to_new_file

TOOL_FUNCTIONS = {
    "get_cost": get_cost,
    "get_commission_rate": get_commission_rate,
    "get_exchange_rate": get_exchange_rate,
    "read_filter_csv": read_filter_csv,
    "save_to_new_file": save_to_new_file,
}

def excut_tool(tool_name: str, tool_args: str):
    tool_function = TOOL_FUNCTIONS[tool_name]
    return tool_function(**json.loads(tool_args))

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_API_BASE"))
agent_prompt = (Path(__file__).parent/"prompt"/"agent_prompt.md").read_text(encoding="utf-8")

def excut_tool(tool_name:str,tool_args:dict):
    try:
        tool_function = TOOL_FUNCTIONS[tool_name]
        return tool_function(**json.loads(tool_args))
    except Exception as e:
        return f"Tool {tool_name} failed to execute: {e}"

def run_agent(user_input:str, max_steps:int=5):
    messages = [
        {"role": "system", "content": agent_prompt},
        {"role": "user", "content": user_input},
    ]
    for step in range(max_steps):
        print(f"\n{'='*20} Step {step + 1} {'='*20}")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tool_schema,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        if response_message.tool_calls:
            print(f"🤔 Thought:\n{response_message.content}")
            messages.append(response_message.model_dump())

            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                
                print(f"🔧 Executing tool: {tool_name}")
                print(f"📦 Args: {tool_args}")
                tool_result =excut_tool(tool_name,tool_args)
                print(f"✅ Tool result:\n{tool_result}")

                if not isinstance(tool_result, str):
                    tool_result = json.dumps(tool_result)
                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call.id,
                })
        else:
            print("✅ Final Answer:")
            return response_message.content
    return "Agent failed to complete the task after {} steps".format(max_steps)


if __name__ == "__main__":
    user_input = "查询sku为MNB-3，成本为多少？"
    result = run_agent(user_input)
    print(result)