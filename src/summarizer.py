from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="models/mistral-7b-instruct-v0.1.Q3_K_S.gguf",
    n_ctx=2048,
    temperature=0.7,
    max_tokens=512,
    verbose=False
)

def summarize(text):
    prompt = f"Summarize the following research content in plain English with bullet points:\n\n{text}"
    return llm.invoke(prompt[:3000])
