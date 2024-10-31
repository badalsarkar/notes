# Gen AI

## Evolution of NLP

- Rule based systems ERA
  - hand crafted rules
  - syntax tagging, parts of speech tagging
  - Challenged with the complexity of NLP
  -
- Statistical ERA

- Machine Learning ERA

- Embeddings ERA

- Transformer ERA

## Transformer model

- main components
  - Encoder
    - processes input text and generate continuous vector representation
  - Decoder
    - Generate output text from encoder generated vector representation
- Training mechanism
  - two phases of training: pre-training and fine tuning
    - pre-training
      - initial learning process to grasp language structure, semantics and context from vast dataset.
      - very expensive. Requires vast text data and compute power
    - fine tuning
      - training the model on a specific task
  - supervised learning: training using input text and target output text
- Types of transformer model
  - BERT (Bidirectional Encoder R)
    - Encoder only. So doesn't have ability to generate text
    - Pre-training
      - on Wikipedia and book corpus
      - objectives
        - Mask...
        - Next sentence prediction
  - GPT
    - Decoder only model
  - T5
    - Encoder decoder model
- Building blocks
  - Tokenizer
    - Tokens are the vocabulary of a model
    - The more tokens the better
  - Embeddings
    - Transforming word to meaningful numbers

## Large language model

- based on transformer architecture
- most LLMs are decoder only model like GPT4, LLama, Mistral, Gemma
- Phi family of model are popular in smaller size model
-
-

## Resources

- Udemy course (Generative AI, ChatGPT, GPT4, Llama3, Decoders, T5, BERT, LoRA, FSDP, 4bit, Machine Learning, Data Science by The Fuzzy Scienties)
