from model import Input_classifier, LABEL_COLUMNS, tokenizer, total_training_steps, warmup_steps
import torch
import warnings
warnings.filterwarnings('ignore')

## INPUT
test_comment = input()

checkpoint = torch.load("trained_model.ckpt")
# Создание нового экземпляра модели
loaded_model = Input_classifier(n_classes=len(LABEL_COLUMNS), n_training_steps=total_training_steps, n_warmup_steps=warmup_steps)

# Загрузка весов и гиперпараметров из чекпоинта
loaded_model.load_state_dict(checkpoint["state_dict"])
loaded_model.eval()
loaded_model.freeze()
encoding = tokenizer.encode_plus(
  test_comment,
  add_special_tokens=True,
  max_length=None,
  return_token_type_ids=False,
  padding="max_length",
  truncation=True,
  return_attention_mask=True,
  return_tensors='pt',
)
_, test_prediction = loaded_model(encoding["input_ids"], encoding["attention_mask"])
test_prediction = test_prediction.flatten().numpy()

## OUTPUT
for label, prediction in zip(LABEL_COLUMNS, test_prediction):
  print(f"{label}: {prediction}")