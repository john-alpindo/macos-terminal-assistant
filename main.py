import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError
import re

def clean_command(raw_text):
    # Remove triple backticks and any language label like ```zsh, ```bash, etc
    cleaned = re.sub(r"```[\w]*\n?", "", raw_text)
    cleaned = cleaned.replace("```", "")  # Remove any closing ```
    cleaned = cleaned.strip()  # Remove leading/trailing whitespace
    return cleaned

def main():
    # Load OpenAI API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Ask how to do something in the macOS Terminal.")
    parser.add_argument("question", nargs="+", help="The terminal question you want to ask.")
    parser.add_argument(
        "--model",
        choices=["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o4-mini", "o3-mini", "gpt-4o", "gpt-4o-mini"],
        default="gpt-4o",
        help="Choose which model to use: 'gpt-4o' for GPT-4o (default: gpt-4o)."
    )
    args = parser.parse_args()

    # Combine multiple words into a full question string
    user_question = " ".join(args.question)

    # Select model
    model = "gpt-4o"

    # System prompt
    system_prompt = (
        "You are a macOS Terminal Assistant.\n\n"
        "The user will ask how to perform specific tasks using the macOS Terminal.\n\n"
        "Your response must be only a plain terminal command or a concise set of commands, without any explanations, formatting, markdown syntax, or code blocks.\n\n"
        "Do not wrap the output in backticks, triple backticks, or label it like zsh, bash, shell, etc.\n\n"
        "Simply return the raw command(s) as plain text.\n\n"
        "Assume the user is using the Zsh shell on a recent version of macOS (e.g., Ventura or later).\n\n"
        "If multiple steps are absolutely necessary, separate them with newlines."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0
        )
    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        sys.exit(1)

    raw_command = response.choices[0].message.content
    command = clean_command(raw_command)
    print(command)

if __name__ == "__main__":
    main()
