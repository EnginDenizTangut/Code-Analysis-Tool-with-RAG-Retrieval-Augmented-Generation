# Code Analysis Tool with RAG (Retrieval-Augmented Generation)

A powerful Python tool that analyzes code files and answers questions about them using a combination of similarity search and Large Language Model (LLM) integration. This tool helps developers understand codebases by finding relevant code snippets and providing intelligent explanations.

## 🚀 Features

- **Automatic Code Parsing**: Automatically scans and parses Python files from a directory
- **Intelligent Similarity Search**: Uses advanced similarity algorithms to find relevant code snippets
- **LLM Integration**: Integrates with Ollama's Llama3.1 model for intelligent code analysis
- **Interactive Q&A**: Interactive command-line interface for asking questions about your code
- **Multi-algorithm Matching**: Combines word matching, substring matching, and sequence similarity
- **Error Handling**: Robust error handling for file operations and LLM interactions

## 📋 Requirements

- Python 3.7+
- Ollama (with Llama3.1 model)
- Required Python packages (see requirements.txt)

## 🛠️ Installation

1. **Clone or download the project**

   ```bash
   git clone <your-repo-url>
   cd LLM/RAG
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   # Install Ollama (visit https://ollama.ai for installation instructions)
   # Pull the Llama3.1 model
   ollama pull llama3.1:latest
   ```

## 🎯 Usage

### Basic Usage

```bash
python3 kodyorumlama_simple.py
```

### Interactive Mode

Once the tool starts, you'll see:

```
Kod dosyaları yükleniyor...
Toplam 30 kod parçası bulundu.

Kod analiz sistemi hazır!
Sorgularınızı yazın (çıkmak için 'quit' yazın)

Sorgunuz:
```

### Example Queries

- `neural network` - Find code related to neural networks
- `machine learning` - Search for ML-related code
- `data processing` - Find data processing functions
- `class definition` - Look for class definitions
- `function implementation` - Find function implementations

### Example Output

```
🔎 Benzer Kod Parçaları:

--- rnntabanli.py_part1 (Benzerlik: 0.06) ---
class RNNLanguageModel(nn.Module):


🤖 Llama3.1 Cevabı:
This code defines a Recurrent Neural Network (RNN) language model using PyTorch's nn.Module as the base class. The RNNLanguageModel class inherits from nn.Module, which provides the foundation for building neural network architectures in PyTorch.

Key points:
- This is a custom neural network class for language modeling
- It uses PyTorch's nn.Module as the base class
- RNN (Recurrent Neural Network) is specifically designed for sequential data processing
- This class would typically contain methods for forward propagation and model training
```

## 🔧 Configuration

### Directory Configuration

By default, the tool scans the `LLM` directory. To change this, modify the `CODE_DIR` variable:

```python
CODE_DIR = "your_code_directory"  # Change this to your desired directory
```

### Similarity Threshold

Adjust the similarity threshold to control how strict the matching is:

```python
# In find_similar_code function
filtered = [(score, key, code) for score, key, code in similarities if score > 0.05]
```

- **Lower values (0.01-0.05)**: More permissive, returns more results
- **Higher values (0.1-0.3)**: More strict, returns only highly relevant results

### Number of Results

Control how many similar code snippets to return:

```python
similar_codes = find_similar_code(query, code_snippets, top_k=3)  # Change 3 to desired number
```

## 🏗️ Architecture

### Core Components

1. **Code Loader** (`load_code_files()`)

   - Recursively scans directories for Python files
   - Parses code into functions and classes
   - Handles file encoding and error cases

2. **Similarity Engine** (`find_similar_code()`)

   - **Word Matching**: Direct word overlap between query and code
   - **Substring Matching**: Partial word matches for flexibility
   - **Sequence Similarity**: Uses difflib.SequenceMatcher for overall similarity
   - **Weighted Scoring**: Combines all methods with configurable weights

3. **LLM Integration** (`ollama.chat()`)
   - Sends context and query to Llama3.1
   - Receives intelligent analysis and explanations
   - Handles API errors gracefully

### Algorithm Details

The similarity scoring uses a weighted combination:

```python
final_score = (word_score * 0.4) + (substring_score * 0.3) + (sequence_score * 0.3)
```

- **Word Score (40%)**: Exact word matches
- **Substring Score (30%)**: Partial word matches
- **Sequence Score (30%)**: Overall text similarity

## 📁 File Structure

```
LLM/RAG/
├── kodyorumlama_simple.py    # Main application file
├── kodyorumlama.py           # Original FAISS-based version
├── requirements.txt          # Python dependencies
└── README.md                # This documentation
```

## 🔍 Supported File Types

Currently supports:

- **Python files** (`.py`)

The tool automatically:

- Extracts functions (starting with `def `)
- Extracts classes (starting with `class `)
- Handles nested structures
- Preserves code formatting

## 🐛 Troubleshooting

### Common Issues

1. **"No similar code found"**

   - Lower the similarity threshold
   - Try more specific or general queries
   - Check if your code directory contains relevant files

2. **Ollama connection errors**

   - Ensure Ollama is running: `ollama serve`
   - Verify Llama3.1 is installed: `ollama list`
   - Check network connectivity

3. **File encoding errors**

   - The tool automatically handles UTF-8 encoding
   - For other encodings, modify the `open()` function

4. **Memory issues with large codebases**
   - The tool loads all code into memory
   - For very large codebases, consider filtering file types or directories

### Debug Mode

To see loaded code snippets, uncomment the debug section in `main()`:

```python
# Debug: Show loaded code snippets
print("\nYüklenen kod parçaları:")
for i, (key, code) in enumerate(list(code_snippets.items())[:3]):
    print(f"\n{i+1}. {key}:")
    print(code[:200] + "..." if len(code) > 200 else code)
```

## 🚀 Performance Tips

1. **Optimize directory scanning**

   - Use specific directories instead of scanning entire projects
   - Exclude test files, documentation, or generated code

2. **Adjust similarity parameters**

   - Higher thresholds for more relevant results
   - Lower thresholds for broader search coverage

3. **Batch processing**
   - The tool processes all files at startup
   - Consider caching embeddings for large codebases

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- **Ollama** for providing the Llama3.1 model
- **PyTorch** for neural network capabilities
- **Python difflib** for sequence matching algorithms

## 📞 Support

For issues, questions, or contributions:

- Create an issue in the repository
- Check the troubleshooting section above
- Review the code comments for implementation details

---

**Happy Code Analyzing!** 🎉
