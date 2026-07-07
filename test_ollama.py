from ollama import Client

client = Client(host="http://localhost:11434")

print("Connected!")

response = client.generate(
    model="qwen3:8b",
    prompt="Say hello in one sentence."
)

print(response)