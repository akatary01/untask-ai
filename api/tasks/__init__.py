def load_prompt(prompt_name: str) -> str:
    with open(f"prompts/{prompt_name}.txt", "r") as prompt:
        return prompt.read()
    