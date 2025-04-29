import aiohttp
import asyncio
import openai

openai.api_key = "TOKEN_API"

async def get_gpt_response(stroka: str, semaphore: asyncio.Semaphore):
    request_data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": stroka,
            }
        ],
        "temperature": 0.8,
        "top_p": 1.0
    }

    async with semaphore:  # Используем семафор для ограничения
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.openai.com/v1/chat/completions',
                json=request_data,
                headers={
                    'Authorization': f'Bearer {openai.api_key}',
                    'Content-Type': 'application/json'
                }
            ) as response:
                if response.status == 200:
                    response_data = await response.json(content_type=None)
                    if 'choices' in response_data:
                        return response_data['choices'][0]['message']['content']
                    else:
                        print("Error in response:", response_data)
                        return "Error: 'choices' not in response"
                else:
                    print(f"HTTP Error: {response.status}")
                    error_message = await response.text()
                    print(f"Error details: {error_message}")
                    return f"HTTP Error: {response.status}"