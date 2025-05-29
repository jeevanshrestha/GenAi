import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hello, world! I am learning tokenization with tiktoken."
tokens = enc.encode(text)
print(f"Text: {text}")
print(f"Tokens: {tokens}")

tokens = [13225, 11, 2375, 0, 357, 939, 7524, 6602, 2860, 483, 260, 8251, 2488, 13]

decoded_text = enc.decode(tokens)
print(f"Decoded Text: {decoded_text}")
