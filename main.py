import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError
import re

def clean_command(raw_text):
    """Clean up command output by removing markdown formatting."""
    cleaned = re.sub(r"```[\w]*\n?", "", raw_text)
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()

def main():
    # Load OpenAI API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Ask how to do something in the macOS Terminal."
    )
    parser.add_argument(
        "question", 
        nargs="+", 
        help="The terminal question you want to ask."
    )
    parser.add_argument(
        "--model",
        choices=["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "o4-mini", "o3-mini", "gpt-4o", "gpt-4o-mini"],
        default="gpt-4.1",
        help="Choose which model to use (default: gpt-4.1)"
    )
    args = parser.parse_args()

    # Construct the prompt following guide.txt best practices
    instructions = """# Identity
You are a macOS Terminal Assistant that provides only raw terminal commands.

# Instructions
* Only output the exact command(s) needed to accomplish the task
* Do not include any explanations, markdown, or formatting
* Use Zsh syntax compatible with macOS Ventura or later
* If multiple commands are needed, separate them with newlines
* Never wrap commands in code blocks or backticks

# Examples
<user_query>
How do I list files sorted by size?
</user_query>

<assistant_response>
ls -lS
</assistant_response>"""

    try:
        response = client.responses.create(
            model=args.model,
            instructions=instructions,
            input=" ".join(args.question)
        )
        
        # Get the first text output from the response
        if response.output and len(response.output) > 0:
            for item in response.output:
                if item.type == "message" and item.role == "assistant":
                    for content in item.content:
                        if content.type == "output_text":
                            command = clean_command(content.text)
                            print(command)
                            return
        
        print("Error: No command found in response")
        sys.exit(1)

    except OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
