import gradio as gr
import onnxruntime as rt
from transformers import AutoTokenizer
import torch, json

tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

with open("genre_types_encoded.json", "r") as fp:
  encode_genre_types = json.load(fp)

genres = list(encode_genre_types.keys())

inf_session = rt.InferenceSession('genre-classifier-quantized.onnx')
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name

def classify_movie_genre(summary):
  input_ids = tokenizer(summary)['input_ids'][:512]
  logits = inf_session.run([output_name], {input_name: [input_ids]})[0]
  logits = torch.FloatTensor(logits)
  probs = torch.sigmoid(logits)[0]
  return dict(zip(genres, map(float, probs))) 

label = gr.Label(num_top_classes=5)
iface = gr.Interface(fn=classify_movie_genre, inputs="text", outputs=label)
iface.launch(inline=False, share=True)