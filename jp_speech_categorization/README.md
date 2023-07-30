# About this project

In this project I created my own dataset from the speech records in the Japanese diet. It classifies the 1500+ speech segments into factual, question, descriptive, opinion based and other sentences.

Then I finetuned the `cl-tohoku/bert-base-japanese-v3` model to classify these correctly. The model is available [here](https://huggingface.co/kkatodus/jp-speech-classifier?text=%E3%83%90%E3%83%8A%E3%83%8A%E3%81%AF%E3%81%8A%E3%82%84%E3%81%A4%E3%81%AB%E5%85%A5%E3%82%8A%E3%81%BE%E3%81%99%E3%81%8B) for anyone to use.