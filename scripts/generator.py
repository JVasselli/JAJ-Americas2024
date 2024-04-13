import json
import os
import random
from typing import Any, Dict, List

import torch
from openai import OpenAI, OpenAIError
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    LlamaForCausalLM,
    LlamaTokenizer,
)

from prompt_utils import fill_template_file


class Generator:
    def __init__(self, model_name, show_progress: bool = True, verbose: bool = False):
        self.model_name = model_name
        self.show_progress = show_progress
        self.verbose = verbose
        self.tokenizer = None
        self.model = None
        self.system_message = False
        self.is_debug = False
        random.seed(42)

        if "gpt" in self.model_name:
            self.setup_gpt_evaluator()
        elif "Mixtral" in self.model_name:
            self.setup_mixtral_evaluator()
        elif "Llama" in self.model_name:
            self.setup_llama_evaluator()
        else:
            self.is_debug = True

        if self.tokenizer:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        if self.model:
            self.model.eval()

    def setup_gpt_evaluator(self):
        assert os.environ["OPENAI_API_KEY"] is not None, "OPENAI_API_KEY not set"
        if "OPENAI_API_ORG" not in os.environ:
            print("OPENAI_API_ORG not set")
            self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        else:
            self.client = OpenAI(
                api_key=os.environ["OPENAI_API_KEY"],
                organization=os.environ["OPENAI_API_ORG"],
            )
        self.system_message = True

    def setup_mixtral_evaluator(self):
        # "Mixtral-8x7B-Instruct-v0.1"
        model_id = "mistralai/" + self.model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, quantization_config=config, device_map="auto"
        )
        self.system_message = False

    def setup_llama_evaluator(self):
        # "meta-llama/Llama-2-70b-chat-hf"
        model_id = "meta-llama/" + self.model_name
        config = BitsAndBytesConfig(load_in_4bit=True)

        self.model = LlamaForCausalLM.from_pretrained(
            model_id,
            quantization_config=config,
            device_map="auto",
            low_cpu_mem_usage=True,
        )
        self.tokenizer = LlamaTokenizer.from_pretrained(model_id)

    def prompt(
        self,
        questions: List[Dict[str, str]],
        template_file: str,
        examples=[],
        num_shots=-1,
        rate=0.0,
        stop=[],
    ):
        assert len(questions) > 0, "Nothing to run"
        assert os.path.exists(template_file), "Template file does not exist: {}".format(
            template_file
        )
        if self.is_debug:
            print("Debug mode, no API calls will be made")

        answers = []
        tokens = 0
        for question in tqdm(questions, disable=not self.show_progress):
            use_question_examples = False
            if (
                "examples" in question
                and type(question["examples"]) == list
                and len(examples) == 0
            ):
                use_question_examples = True

            llm_input = fill_template_file(
                template_file,
                question=question,
                examples=examples
                if use_question_examples == False
                else question["examples"],
                num_shots=num_shots,
            )
            if (
                len(llm_input[0]) > 0
                and llm_input[0]["role"] == "system"
                and self.system_message == False
            ):
                llm_input[1]["content"] = (
                    llm_input[0]["content"] + "\n" + llm_input[1]["content"]
                )
                llm_input.pop(0)

            if self.verbose:
                print(json.dumps(llm_input, indent=4, ensure_ascii=False))

            if self.is_debug:
                import tiktoken

                # answer will be the questions
                answer = "\n".join([v["content"] for v in llm_input])
                # count number of tokens
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
                tokens += len(encoding.encode(answer))
            elif "gpt" in self.model_name:
                try:
                    completion = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=llm_input,
                        temperature=0.0,
                        stop=stop,
                        #logprobs=True,
                        #top_logprobs=5
                    )
                    answer = completion.choices[0].message.content
                    """for content in completion.choices[0].logprobs.content:
                        log_prob_results = [(logprob.token, logprob.logprob) for logprob in content.top_logprobs]
                        print(log_prob_results)"""
                except OpenAIError as e:
                    print("Error with chatgpt after {} questions".format(len(answers)))
                    print(e)
                    return answers

                if self.verbose:
                    if self.model_name != completion.model:
                        print(
                            "Warning: model changed from {} to {}".format(
                                self.model_name, completion.model
                            )
                        )
                        self.model_name = completion.model
            else:
                input_ids = self.tokenizer.apply_chat_template(
                    llm_input, return_tensors="pt"
                ).to("cuda")

                outputs = self.model.generate(
                    input_ids,
                    max_new_tokens=500,
                    return_dict_in_generate=True,
                    output_scores=True,
                )
                answer = self.tokenizer.decode(
                    outputs.sequences[0], skip_special_tokens=True
                )
                answer = answer.split(" [/INST] ")[-1]

            answers.append(answer)

        if self.verbose:
            print(answer)
        if self.is_debug:
            cost = tokens / 1000 * rate
            print("{} tokens (${:0.2f})".format(tokens, cost))
        return answers
