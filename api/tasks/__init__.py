def load_prompt(prompt_name: str) -> str:
    with open(f"tasks/prompts/{prompt_name}.txt", "r") as prompt:
        return prompt.read().replace("\n", " ")
    