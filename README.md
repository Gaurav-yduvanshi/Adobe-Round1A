# PDF Heading Extraction System

A machine learning-powered system that automatically extracts document titles and heading structures from PDF files. This project uses a RandomForest classifier trained on text formatting features to identify and classify headings at different hierarchical levels.

## 🚀 Features

- **Automatic Title Extraction**: Identifies document titles from the first page
- **Hierarchical Heading Detection**: Classifies headings into H1, H2, H3, and H4 levels
- **Batch Processing**: Process multiple PDF files at once
- **JSON Output**: Structured output format for easy integration
- **Machine Learning Based**: Uses trained RandomForest model for accurate classification

## 📋 Requirements

- Python 3.10+
- PyMuPDF (fitz)
- scikit-learn
- joblib
- pandas

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install pymupdf scikit-learn joblib pandas
   ```

3. **Ensure you have the required files**:
   - `train_model.py` - Model training script
   - `extract_headings.py` - Main extraction script
   - `data.csv` - Training dataset (1M labeled text samples)
   - `input/` - Directory for input PDF files
   - `output/` - Directory for output JSON files

## 📊 Training Data

The system is trained on a dataset (`data.csv`) containing 1,000,000 labeled text samples with the following features:

- **text**: The actual text content
- **font_size**: Font size of the text
- **bold**: Whether the text is bold (1/0)
- **x, y**: Position coordinates on the page
- **page**: Page number
- **label**: Classification label (Title, H1, H2, H3, Body)

## 🎯 Usage

### Train the Model

First, train the machine learning model using your labeled dataset:

```bash
python train_model.py
```

This will create:
- `heading_classifier.pkl` - Trained RandomForest model
- `label_encoder.pkl` - Label encoder for classification labels

### Extract Headings from PDFs

#### Process All PDFs in Input Directory

```bash
python extract_headings.py
```

This will process all PDF files in the `input/` directory and save JSON results in the `output/` directory.

#### Process a Single PDF

```bash
python extract_headings.py input/document.pdf output/document.json
```

### Example Output

The system generates JSON files with the following structure:

```json
{
  "title": "Document Title Here",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "1.1 Overview",
      "page": 1
    },
    {
      "level": "H2",
      "text": "1.2 Objectives", 
      "page": 2
    }
  ]
}
```

## 🔧 How It Works

1. **PDF Text Extraction**: Uses PyMuPDF to extract text and formatting information from PDF files
2. **Feature Engineering**: Extracts font size, bold formatting, position coordinates, and page numbers
3. **ML Classification**: Uses a trained RandomForest model to classify each text element
4. **Title Detection**: Identifies the document title using font size heuristics on the first page
5. **Outline Generation**: Filters and organizes headings into a hierarchical structure

## 📁 Project Structure

```
├── README.md
├── train_model.py          # Model training script
├── extract_headings.py     # Main extraction script
├── requiremnts.txt         # Dependencies list
├── data.csv               # Training dataset (1M samples)
├── heading_classifier.pkl # Trained model (generated)
├── label_encoder.pkl      # Label encoder (generated)
├── input/                 # Input PDF files
│   ├── file01.pdf
│   ├── file02.pdf
│   └── ...
└── output/                # Output JSON files
    ├── file01.json
    ├── file02.json
    └── ...
```

## 🎛️ Configuration

### Model Parameters

The RandomForest classifier uses the following default parameters:
- `n_estimators=100`
- `random_state=42`

### Feature Set

The model uses these 5 features for classification:
- `font_size`: Text font size
- `bold`: Bold formatting (binary)
- `x`: Horizontal position
- `y`: Vertical position  
- `page`: Page number

### Title Extraction

Title detection uses the following logic:
- Analyzes first page only
- Selects text with font size ≥ 85% of maximum font size on page
- Combines multiple title parts if found
- Falls back to first line if no large text found

## 🔍 Model Performance

The system classifies text into 5 categories:
- **Title**: Document titles
- **H1**: Major headings
- **H2**: Sub-headings
- **H3**: Sub-sub-headings
- **Body**: Regular body text

Only H1-H4 headings are included in the final outline output.

## 🐛 Troubleshooting

### Common Issues

1. **sklearn warnings about feature names**: This is expected and doesn't affect functionality
2. **Empty outline results**: Check if PDFs have clear heading formatting differences
3. **Missing model files**: Run `train_model.py` first to generate the required .pkl files

### File Requirements

- Ensure `data.csv` exists and contains the training data
- PDF files should be placed in the `input/` directory
- The `output/` directory will be created automatically

## 📈 Performance Notes

- Processing time depends on PDF size and complexity
- The model works best with PDFs that have clear formatting distinctions for headings
- Large PDFs may take longer to process due to text extraction overhead

## 🤝 Contributing

To improve the model:
1. Add more training data to `data.csv`
2. Experiment with additional features (font family, color, etc.)
3. Try different ML algorithms
4. Enhance the title detection logic

## 📄 License

This project is provided as-is for educational and development purposes.
