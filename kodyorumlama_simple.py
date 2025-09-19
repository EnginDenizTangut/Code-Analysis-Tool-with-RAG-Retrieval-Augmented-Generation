import os
import re
import ollama
from difflib import SequenceMatcher

CODE_DIR = "LLM"  # tüm .py dosyalarının bulunduğu klasör

def similarity(a, b):
    """İki string arasındaki benzerliği hesapla"""
    return SequenceMatcher(None, a, b).ratio()

def extract_code_parts(code):
    """Kod parçalarını çıkar"""
    parts = re.split(r"(def |class )", code)
    snippets = []
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            snippets.append(parts[i] + parts[i+1])
    return snippets

def load_code_files():
    code_snippets = {}
    
    for root, dirs, files in os.walk(CODE_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()
                        snippets = extract_code_parts(code)
                        for idx, snippet in enumerate(snippets):
                            key = f"{file}_part{idx}"
                            code_snippets[key] = snippet
                except Exception as e:
                    print(f"Dosya okunamadı {path}: {e}")
                    continue
    
    return code_snippets

def find_similar_code(query, code_snippets, top_k=3):
    """Sorguya benzer kod parçalarını bul"""
    similarities = []
    query_lower = query.lower()
    
    for key, code in code_snippets.items():
        code_lower = code.lower()
        
        # 1. Doğrudan kelime eşleştirme
        query_words = set(query_lower.split())
        code_words = set(code_lower.split())
        common_words = query_words.intersection(code_words)
        
        # 2. Alt string eşleştirme (daha esnek)
        substring_score = 0
        for word in query_words:
            if word in code_lower:
                substring_score += 1
        
        # 3. SequenceMatcher ile genel benzerlik
        sequence_score = SequenceMatcher(None, query_lower, code_lower).ratio()
        
        # 4. Ağırlıklı skor hesaplama
        word_score = len(common_words) / max(len(query_words), 1) if query_words else 0
        substring_score = substring_score / max(len(query_words), 1) if query_words else 0
        
        # Final skor (kelime eşleştirme + alt string + sequence)
        final_score = (word_score * 0.4) + (substring_score * 0.3) + (sequence_score * 0.3)
        
        similarities.append((final_score, key, code))
    
    # En yüksek skorları sırala
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Minimum eşik değeri (0.05)
    filtered = [(score, key, code) for score, key, code in similarities if score > 0.05]
    
    return filtered[:top_k]

def main():
    print("Kod dosyaları yükleniyor...")
    code_snippets = load_code_files()
    print(f"Toplam {len(code_snippets)} kod parçası bulundu.")
    
    print("\nKod analiz sistemi hazır!")
    print("Sorgularınızı yazın (çıkmak için 'quit' yazın)")
    
    while True:
        try:
            query = input("\nSorgunuz: ")
            if query.lower() == 'quit':
                break
            
            if not query.strip():
                continue
        except (EOFError, KeyboardInterrupt):
            print("\nProgram sonlandırılıyor...")
            break
            
        print("\n🔎 Benzer Kod Parçaları:")
        similar_codes = find_similar_code(query, code_snippets)
        
        if not similar_codes or similar_codes[0][0] == 0:
            print("Benzer kod parçası bulunamadı.")
            continue
            
        # En iyi kod parçalarını göster
        context_parts = []
        for i, (score, key, code) in enumerate(similar_codes):
            print(f"\n--- {key} (Benzerlik: {score:.2f}) ---")
            print(code)
            context_parts.append(f"Kod Parçası {i+1} ({key}):\n{code}")
        
        # Llama ile analiz
        context = "\n\n".join(context_parts)
        prompt = f"""
Kullanıcı sorusu: {query}

Aşağıdaki kod parçalarına göre cevap ver. Her kod parçasını referans göstererek açıkla:

{context}
"""
        
        try:
            response = ollama.chat(
                model="llama3.1:latest",
                messages=[{"role": "user", "content": prompt}],
            )
            
            print("\n🤖 Llama3.1 Cevabı:")
            print(response["message"]["content"])
            
        except Exception as e:
            print(f"Llama hatası: {e}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
