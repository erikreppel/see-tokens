# see-tokens

Compare how different AI tokenizers break text into tokens. Tokens are displayed with alternating background colors so boundaries are easy to spot.

**Tokenizers compared:**
- GPT-5 (`o200k_base`)
- GPT-4 / GPT-3.5 (`cl100k_base`)
- LLaMA 3
- Mistral

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
# Option 1: run directly
uv run see_tokens.py "some text"

# Option 2: symlink to PATH for global use
ln -s $(pwd)/see_tokens.py ~/.local/bin/see-tokens
chmod +x see_tokens.py
see-tokens "some text"
```

## Usage

```bash
# Inline text
see-tokens "The quick brown fox jumps over the lazy dog"

# From a file
see-tokens -f prompt.txt

# Piped via stdin
cat prompt.txt | see-tokens
```

Example output:

```
Text: "The quick brown fox jumps over the lazy dog"

GPT-5 (o200k_base) — 9 tokens:
|The| quick| brown| fox| jumps| over| the| lazy| dog|

GPT-4 / 3.5 (cl100k_base) — 9 tokens:
|The| quick| brown| fox| jumps| over| the| lazy| dog|

LLaMA 3 (NousResearch/Meta-Llama-3-8B) — 9 tokens:
|The| quick| brown| fox| jumps| over| the| lazy| dog|

Mistral (mistralai/Mistral-7B-v0.1) — 11 tokens:
| The| quick| brown| f|ox| j|umps| over| the| lazy| dog|
```

(In the terminal, tokens are shown with alternating background colors instead of `|` delimiters.)
