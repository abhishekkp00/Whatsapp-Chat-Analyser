# 💬 WhatsApp Chat Analyzer

A comprehensive Streamlit-based web application that analyzes WhatsApp chat exports and provides detailed insights and visualizations.

## 📊 Features

- **Message Statistics**: Get total message count, word count, media shared, and links shared
- **User Activity Analysis**: Identify most active participants in group chats
- **Word Cloud**: Visual representation of frequently used words
- **Word Frequency Analysis**: Top 20 most common words with visualization
- **Emoji Analysis**: Discover which emojis are most frequently used
- **Timeline Analysis**: 
  - Monthly trends of messaging activity
  - Daily message count tracking
- **Activity Heatmap**: See when the conversation is most active (by day and hour)
- **Per-User Analysis**: Analyze individual user statistics or overall group statistics

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or Download the Project**
```bash
cd "AIML Project"
```

2. **Run the Setup Script** (Linux/Mac)
```bash
bash setup.sh
```

Or **Manually Install Dependencies** (Windows/All Platforms)
```bash
pip install -r requirements.txt
```

3. **Verify Installation**
```bash
python --version  # Should be 3.8+
streamlit --version
```

## 🚀 Usage

### Step 1: Export Your WhatsApp Chat

1. Open WhatsApp on your phone
2. Go to the chat you want to analyze
3. Tap **Menu (⋮) → More → Export chat**
4. Select **"Without media"** (Important: Choose this option)
5. Save the **.txt** file to your computer

### Step 2: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Step 3: Analyze Your Chat

1. Use the **file uploader** in the left sidebar to upload your WhatsApp chat export (.txt file)
2. Select a specific user or **"Overall"** to analyze the entire conversation
3. Click **"Show Analysis"** button to view the dashboard

## 📁 Project Structure

```
AIML Project/
├── app.py                    # Main Streamlit application
├── preprocessor.py           # Chat data preprocessing module
├── helper.py                 # Analysis and visualization helper functions
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script for Linux/Mac
├── stop_hinglish.txt        # Stop words for text filtering (optional)
├── Readme.md                # This file
└── __pycache__/             # Python cache directory
```

## 📋 Requirements

All dependencies are listed in `requirements.txt`:

- **streamlit** - Web app framework
- **numpy** - Numerical computing
- **pandas** - Data manipulation and analysis
- **matplotlib** - Plotting library
- **seaborn** - Statistical data visualization
- **textblob** - Text processing
- **wordcloud** - Word cloud generation
- **scikit-learn** - Machine learning utilities
- **urlextract** - URL extraction from text
- **emoji** - Emoji processing

## 📊 Analysis Outputs

### Statistics Panel
- Total messages in conversation
- Total words used
- Number of media files shared
- Number of links shared

### Visualizations
- **Bar Charts**: Most active users, top words, top emojis
- **Word Cloud**: Visual representation of word frequency
- **Line Charts**: Monthly and daily message trends
- **Heatmap**: Activity intensity by day and hour

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError" when running app.py

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "stop_hinglish.txt not found" warning

**Solution**: This is optional. The app will use default stop words. You can create this file with Hindi-English stop words for better analysis.

### Issue: No emojis detected

**Solution**: The emoji detection depends on how emojis are represented in the exported chat. Some versions of WhatsApp may handle emojis differently.

### Issue: File upload doesn't work

**Solution**: 
- Make sure the file is exported as .txt format
- Choose "Without media" when exporting
- Try a smaller chat first to test

## 💡 Tips for Best Results

1. **Export without media** - Reduces file size and processing time
2. **Use recent chats** - For faster analysis
3. **Select "Overall"** first to understand the group dynamics
4. **Then analyze individual users** for specific insights

## 📝 Chat Export Format

WhatsApp chat exports use this format:
```
1/17/2024, 10:30 AM - User Name: Hello there!
1/17/2024, 10:31 AM - Another User: Hi! How are you?
1/17/2024, 10:32 AM - User Name: <Media omitted>
```

The app automatically parses this format and extracts:
- Timestamp
- User name
- Message content
- Media indicators

## 🎯 Use Cases

- Analyze group chat dynamics
- Understand communication patterns
- Identify most active participants
- Track conversation trends over time
- Find trending topics through word clouds
- Monitor peak activity times

## ⚠️ Privacy Notice

This application processes your WhatsApp chat data locally. The data is:
- Not stored permanently
- Not sent to external servers
- Only used during your analysis session

Please ensure you have the right to analyze the chat before proceeding.

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to enhance this project by:
- Adding new analysis features
- Improving visualizations
- Optimizing performance
- Adding support for more languages

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Ensure your WhatsApp export format is correct

## 🎉 Enjoy Your Analysis!

Start exploring your WhatsApp conversations and discover interesting insights about your communication patterns!
