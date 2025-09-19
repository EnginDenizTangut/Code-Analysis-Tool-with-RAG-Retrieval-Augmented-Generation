import os
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama
import re
import warnings
from sklearn.metrics.pairwise import cosine_similarity

# Uyarıları kapat
warnings.filterwarnings("ignore", category=UserWarning)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

CODE_DIR = "LLM"  # tüm .py dosyalarının bulunduğu klasör

code_snippets = {}
for root, dirs, files in os.walk(CODE_DIR):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                    # fonksiyon ve sınıf bazında ayır (basit regex)
                    parts = re.split(r"(def |class )", code)
                    # başlıkları koru
                    snippets = []
                    for i in range(1, len(parts), 2):
                        snippets.append(parts[i] + parts[i+1])
                    for idx, s in enumerate(snippets):
                        key = f"{file}_part{idx}"
                        code_snippets[key] = s
            except Exception as e:
                print(f"Dosya okunamadı {path}: {e}")
                continue

print(f"Toplam {len(code_snippets)} kod parçası bulundu.")

texts = list(code_snippets.values())
keys = list(code_snippets.keys())

embeddings = embedder.encode(texts)
embeddings = np.array(embeddings).astype("float32")

print("Embeddings hazır.")

def ask_question():
    query = input("Sorgunu yaz (çıkmak için 'quit' yaz): ")
    if query.lower() == 'quit':
        return False
    
    try:
        query_emb = embedder.encode([query]).astype("float32")
        
        # Cosine similarity kullanarak en benzer kod parçalarını bul
        similarities = cosine_similarity(query_emb, embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:3]  # En yüksek 3 benzerlik
        
        retrieved = [texts[i] for i in top_indices]
        files = [keys[i] for i in top_indices]
        
        print("\n🔎 Bulunan Kod Parçaları:")
        for f, c in zip(files, retrieved):
            print(f"\n--- {f} ---\n{c}")
        
        context = "\n\n".join(retrieved)
        prompt = f"""
Kullanıcı sorusu: {query}

Aşağıdaki kod parçalarına göre cevap ver. Kod parçalarını referans göstererek açıkla:
{context}
"""
        
        response = ollama.chat(
            model="llama3.1:latest",
            messages=[{"role": "user", "content": prompt}],
        )
        
        print("\n🤖 Llama3.1 Cevabı:")
        print(response["message"]["content"])
        print("\n" + "="*50 + "\n")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
    
    return True

# Ana döngü
while True:
    if not ask_question():
        break
