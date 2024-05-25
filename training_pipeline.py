import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
from peft import get_peft_model, LoraConfig, TaskType

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


train_data = [] # A compléter

train_dataset = Dataset.from_dict(train_data)


lora_config = LoraConfig(
    r=8,  
    lora_alpha=32,  
    target_modules=["q_proj", "v_proj"],  
    lora_dropout=0.1,
    task_type=TaskType.CAUSAL_LM
)

model = get_peft_model(model, lora_config)


training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=10,
    evaluation_strategy="epoch",
    save_total_limit=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

if __name__=='main':
    trainer.train()
