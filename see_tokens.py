#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "tiktoken",
#   "transformers",
#   "sentencepiece",
#   "protobuf",
# ]
# ///
"""Visualize how different AI tokenizers break a string into tokens."""

import sys
import os

# Silence transformers/tokenizers warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import tiktoken
from transformers import AutoTokenizer


# ANSI background colors for alternating tokens
BG_A = "\033[48;5;238m"  # dark gray
BG_B = "\033[48;5;240m"  # slightly lighter gray
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


def colorize_tokens(decoded_tokens: list[str]) -> str:
    """Render tokens with alternating background colors."""
    parts = []
    for i, tok in enumerate(decoded_tokens):
        bg = BG_A if i % 2 == 0 else BG_B
        display = tok.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        parts.append(f"{bg}{display}{RESET}")
    return "".join(parts)


def tiktoken_tokens(text: str, encoding_name: str) -> list[str]:
    enc = tiktoken.get_encoding(encoding_name)
    token_ids = enc.encode(text)
    return [enc.decode([tid]) for tid in token_ids]


def hf_tokens(text: str, model_name: str) -> list[str]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    token_ids = tokenizer.encode(text, add_special_tokens=False)
    # Use convert_ids_to_tokens to preserve raw representation, then clean up
    raw_tokens = tokenizer.convert_ids_to_tokens(token_ids)
    # SentencePiece uses ▁ (U+2581) for spaces, BPE uses Ġ (U+0120)
    return [t.replace("\u2581", " ").replace("\u0120", " ") for t in raw_tokens]


TOKENIZERS = [
    ("GPT-5", "o200k_base", lambda t: tiktoken_tokens(t, "o200k_base")),
    ("GPT-4 / 3.5", "cl100k_base", lambda t: tiktoken_tokens(t, "cl100k_base")),
    ("LLaMA 3", "NousResearch/Meta-Llama-3-8B", lambda t: hf_tokens(t, "NousResearch/Meta-Llama-3-8B")),
    ("Mistral", "mistralai/Mistral-7B-v0.1", lambda t: hf_tokens(t, "mistralai/Mistral-7B-v0.1")),
]


def main():
    if len(sys.argv) < 2 and sys.stdin.isatty():
        print(f"Usage: {sys.argv[0]} <text>", file=sys.stderr)
        print(f"       {sys.argv[0]} -f <file>", file=sys.stderr)
        print(f"       cat file | {sys.argv[0]}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3 and sys.argv[1] == "-f":
        with open(sys.argv[2]) as f:
            text = f.read()
    elif len(sys.argv) >= 2:
        text = " ".join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    label = text if len(text) <= 80 else text[:77] + "..."
    print(f'{DIM}Text: "{label}"{RESET}\n')

    for name, detail, tokenize_fn in TOKENIZERS:
        try:
            tokens = tokenize_fn(text)
        except Exception as e:
            print(f"{BOLD}{name}{RESET} ({detail}) — {DIM}error: {e}{RESET}\n")
            continue

        print(f"{BOLD}{name}{RESET} ({detail}) — {len(tokens)} tokens:")
        print(colorize_tokens(tokens))
        print()


if __name__ == "__main__":
    main()
