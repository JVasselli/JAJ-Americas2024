import random
from typing import Any, Dict, List


def replace_placeholders(text: str, instance: Dict[str, Any], prefix: str = "") -> str:
    """
    Replaces placeholders in a string with values from a dictionary.
    Args:
        text: string with placeholders
        instance: dictionary with values to fill in
        prefix: prefix for the keys in the dictionary (used for examples)
    """
    if not isinstance(instance, dict):
        print(instance)
        raise TypeError("instance must be a dictionary")
    for key, value in instance.items():
        if type(value) == list and len(value) > 0 and type(value[0]) == str:
            value = ", ".join(value)
        if type(value) != str:
            value = str(value)
        text = text.replace(f"[{prefix}{key}]", value)
    return text


def process_examples(
    lines: List[str], examples: List[Dict[str, Any]], num_shots: int = -1
) -> str:
    """
    Processes the examples section of a template file.
    Args:
        lines: list of lines in the template file
        examples: list of dictionaries with information to fill in
        num_shots: number of examples to include in the output, -1 for all
    """
    example_template = ""
    for line in lines:
        if not line.startswith("#"):
            example_template += line.strip() + "\n"

    if num_shots > -1:
        num_examples = min(num_shots, len(examples))
        # randomly select num_examplse
        examples = random.sample(examples, num_examples)
    example_text = ""
    for i, example in enumerate(examples):
        example_text += replace_placeholders(
            example_template, example, prefix="example_"
        ).replace("[$index]", str(i + 1))
    return example_text


def fill_template_file(
    template_file: str,
    question: Dict[str, Any],
    examples: List[Dict[str, Any]],
    num_shots: int = -1,
):
    """
    Reads a template file and fills in placeholders with values from a dictionary.
    Args:
        template_file: path to the template file
        question: dictionary with values to fill in to the general prompt
        examples: list of dictionarys for the examples section
        num_shots: number of examples to include, -1 for all
    """
    messages = []
    lines = [line for line in open(template_file, "r").readlines()]
    examples_start = -1
    for i, line in enumerate(lines):
        # add blank lines to the message
        if line.strip() == "" and len(messages) > 0 and examples_start == -1:
            messages[-1]["content"] += line
            continue

        if line.strip() == "# system":
            messages.append({"role": "system", "content": ""})
        elif line.strip() == "# user":
            messages.append({"role": "user", "content": ""})
        elif line.strip() == "# assistant":
            messages.append({"role": "assistant", "content": ""})
        elif line.strip() == "# start examples":
            examples_start = i + 1
        elif line.strip() == "# end examples":
            example_text = process_examples(
                lines[examples_start:i], examples, num_shots
            )
            if len(messages) > 0:
                messages[-1]["content"] += example_text
            else:
                messages.append({"role": "user", "content": example_text})
            examples_start = -1
        elif examples_start == -1 and (line.startswith("\t") or line.startswith(" ")):
            # append line to the last message
            messages[-1]["content"] += line.strip() + "\n"

    for message in messages:
        message["content"] = replace_placeholders(message["content"], question)
    return messages
