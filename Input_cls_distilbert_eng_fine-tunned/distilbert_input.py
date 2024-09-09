import pytorch_lightning as pl
import torch
import torch.nn as nn
from transformers import BertTokenizerFast as BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
import pytorch_lightning as pl

RANDOM_SEED = 42
pl.seed_everything(RANDOM_SEED)
BERT_MODEL_NAME = 'distilbert/distilbert-base-uncased-finetuned-sst-2-english'
tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)

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
N_EPOCHS = 2
BATCH_SIZE = 32
LABEL_COLUMNS=['benign', 'jailbreak', 'prompt_injection']
warmup_steps=185
total_training_steps=926
checkpoint = torch.load("trained_model.ckpt")
# Создание нового экземпляра модели
loaded_model = Input_classifier(n_classes=len(LABEL_COLUMNS), n_training_steps=total_training_steps, n_warmup_steps=warmup_steps)

# Загрузка весов и гиперпараметров из чекпоинта
loaded_model.load_state_dict(checkpoint["state_dict"])
loaded_model.eval()
loaded_model.freeze()
test_comment = input()

encoding = tokenizer.encode_plus(
  test_comment,
  add_special_tokens=True,
  max_length=None,
  return_token_type_ids=False,
  padding="max_length",
  return_attention_mask=True,
  return_tensors='pt',
)

_, test_prediction = loaded_model(encoding["input_ids"], encoding["attention_mask"])
test_prediction = test_prediction.flatten().numpy()

for label, prediction in zip(LABEL_COLUMNS, test_prediction):
  print(f"{label}: {prediction}")
