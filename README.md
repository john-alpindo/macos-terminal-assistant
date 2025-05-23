<p align="center">
  <img src="assets/logo.svg" width="400" alt="macOS Terminal Assistant Logo">
</p>

<p align="center">
Ask natural-language questions about macOS Terminal commands.<br />
Get clean, copy-paste-ready CLI output instantly.
</p>

<p align="center">
  <a href="LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-blue">
  </a>
  <a href="https://astral.sh/uv">
    <img alt="Built with UV" src="https://img.shields.io/badge/Built%20With-Astral%20UV-9370DB">
  </a>
  <a href="https://platform.openai.com/docs">
    <img alt="Powered by OpenAI" src="https://img.shields.io/badge/Powered%20By-OpenAI-ff69b4">
  </a>
</p>

---

## 🧰 Requirements

- Python 3.8+
- [`uv`](https://astral.sh/uv/install) (for Python dependency management)
- OpenAI API key
- macOS (Zsh shell assumed)

---

## ⚡ Quick Start

```bash
git clone https://github.com/yourusername/macos-terminal-assistant.git
cd macos-terminal-assistant
uv sync
cp .env.example .env
# Edit .env and add your OpenAI API Key
```

---

## 📦 Installation (using `uv`)

1. Clone the project:

   ```bash
   git clone https://github.com/yourusername/macos-terminal-assistant.git
   cd macos-terminal-assistant
   ```

2. Sync dependencies using `uv`:

   ```bash
   uv sync
   ```

3. Create a `.env` file by copying the example file:

   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```

---

## 🧠 Setup: `ai` Command in Zsh

To easily call the assistant from anywhere, add the following function to your `~/.zshrc`:

1. Add the following function to your `~/.zshrc`:

   ```zsh
   function ai() {
     if [ $# -eq 0 ]; then
       echo "Usage: ai 'your terminal question here'"
       return 1
     fi

     (
       cd /Users/YOUR_USERNAME/macos-terminal-assistant || exit 1
       uv run main.py "$@"
     )
   }
   ```

   > Replace `/Users/YOUR_USERNAME/macos-terminal-assistant` with your actual full path.

2. Reload your terminal:

   ```bash
   source ~/.zshrc
   ```

---

## 🚀 Usage

Ask terminal-related questions like this:

```bash
$ ai "How do I list all files including hidden ones?"
ls -la
```

```bash
$ ai "output the contents of a text file and save it to clipboard"
cat filename.txt | pbcopy
```

To specify a different GPT model:
```bash
$ ai --model gpt-4o-mini "Show disk usage for current directory"
df -h
```
> Note: The `--model` flag lets you choose from supported models listed in `main.py` (default: gpt-4.1)

✅ GPT responses are automatically cleaned — plain terminal commands without markdown or extra formatting.

---

## 🧠 Prompt Structure (in `main.py`)

The assistant uses OpenAI's Responses API with a structured prompt containing:

1. **Identity**: Defines the assistant's role
2. **Instructions**: Rules for command output format
3. **Examples**: Few-shot learning examples

Key behaviors:
- Outputs only raw terminal commands
- Uses Zsh syntax for macOS Ventura+
- Never includes explanations or formatting
- Handles multi-command responses

---

## 🛠 Project Structure

```
macos-terminal-assistant/
├── main.py        # Entry point script
├── .env           # Stores your OpenAI key
├── pyproject.toml # UV-managed project config
└── README.md      # You're here
```

---

## 🧠 Customization

### 🔄 Change the Model

You can change the OpenAI model used in `main.py` by modifying the `model` parameter (default is `"gpt-4o"`). Supported text models include:

- `gpt-4.1` (default)
- `gpt-4.1-mini`
- `gpt-4.1-nano` 
- `o4-mini`
- `o3-mini`
- `gpt-4o`
- `gpt-4o-mini`

All models use the new [Responses API](https://platform.openai.com/docs/api-reference/responses) format.

Edit the line in `main.py`:

```python
model="gpt-4o"  # change this to another supported model if needed
```

### 🛠 Modify the Prompt

To adjust the assistant's behavior:
1. Edit the `instructions` string in `main.py`
2. Update examples in the `# Examples` section
3. Change identity/behavior rules in `# Identity` and `# Instructions`

---

## ❓ Troubleshooting

- **Command not found?**  
  Ensure the `ai()` function is added to `.zshrc` and sourced.

- **Doesn't work outside the project folder?**  
  The `ai` function uses `cd` into the project directory so it works globally.

- **Missing packages?**  
  Run `uv sync` again to install dependencies.

--- 
