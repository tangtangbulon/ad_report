import os
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_API_BASE"))
input_price_per_m = 1.0
output_price_per_m = 2.0


def generate_listing(product_info):
    prompt = f"""
    你是一个电商助手。请根据以下产品信息生成Listing。
    严格输出以下JSON格式，不要包含任何其他解释文字、不要用markdown代码块包裹：
    {{
        "product_name": "产品名称",
        "product_description": "产品描述",
        "product_price": "产品价格"
    }}
    产品信息：
    {product_info}
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        json_data = json.loads(content)
        usage=response.usage
        prompt_tokens=usage.prompt_tokens
        completion_tokens=usage.completion_tokens
        return json_data, prompt_tokens, completion_tokens,True
    except Exception as e:
        print(f"Error generating listing: {e}")
        return None, 0, 0, False

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="生成电商Listing")
    parser.add_argument("--info", type=str, required=True, help="产品信息")
    args=parser.parse_args()
    print(f"产品信息: {args.info}")
    data, prompt_tokens, completion_tokens, is_success = generate_listing(args.info)
    if is_success:
        print("✅ 生成成功！输出如下：")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"本次消耗 -> 输入Token: {prompt_tokens}, 输出Token: {completion_tokens}")
    
    
    