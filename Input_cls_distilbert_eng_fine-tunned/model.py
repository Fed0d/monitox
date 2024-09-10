import torch
import torch.nn as nn
from transformers import BertTokenizerFast as BertTokenizer, BertModel
import pytorch_lightning as pl

##args
RANDOM_SEED = 42
pl.seed_everything(RANDOM_SEED)
BERT_MODEL_NAME = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'
tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
LABEL_COLUMNS=['benign', 'jailbreak', 'prompt_injection']
warmup_steps=185
total_training_steps=926
MAX_TOKEN_COUNT=None


class Input_classifier(pl.LightningModule):

  def __init__(self, n_classes: int, n_training_steps=None, n_warmup_steps=None):
    super().__init__()
    self.bert = BertModel.from_pretrained(BERT_MODEL_NAME, return_dict=True)
    self.classifier = nn.Linear(self.bert.config.hidden_size, n_classes)
    self.n_training_steps = n_training_steps
    self.n_warmup_steps = n_warmup_steps
    self.criterion = nn.BCELoss()

  def forward(self, input_ids, attention_mask, labels=None):
    output = self.bert(input_ids, attention_mask=attention_mask)
    output = self.classifier(output.pooler_output)
    output = torch.sigmoid(output)
    loss = 0
    if labels is not None:
        loss = self.criterion(output, labels)
    return loss, output
