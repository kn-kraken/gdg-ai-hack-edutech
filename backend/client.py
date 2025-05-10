import requests

def main():
    print("Ask Gemini (type 'exit' to quit):")
    while True:
        prompt = input("You: ")
        if prompt.lower() == 'exit':
            break

        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"prompt": prompt}
        )

        if response.status_code == 200:
            data = response.json()
            print("Gemini:", data.get("response", "[No response]"))
        else:
            print("Error:", response.text)

if __name__ == "__main__":
    main()
