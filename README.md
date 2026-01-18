# 🛒 UCP + AP2 Shopping Agent - Web Interface

A beautiful web interface for the UCP (Universal Commerce Protocol) and AP2 (Agent Payments Protocol) shopping agent demo.

![Demo Screenshot](screenshot.png)

## ✨ Features

- 💬 **Chat Interface** - Natural language shopping experience
- 🛒 **Visual Cart** - See your items in real-time
- 📜 **AP2 Checkout** - Full mandate approval flow with animations
- 🔐 **Verification Trail** - See cryptographic proof of authorization
- 🎨 **Modern UI** - Dark theme with smooth animations

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your API Key

Open `server.py` and replace:
```python
API_KEY = 'your-gemini-api-key-here'
```

Or set environment variable:
```bash
# Windows
set GEMINI_API_KEY=your-key-here

# Mac/Linux
export GEMINI_API_KEY=your-key-here
```

### 3. Run the Server

```bash
python server.py
```

### 4. Open in Browser

Go to: **http://localhost:5000**

## 🎮 How to Use

1. **Browse Products** - Ask "Show me running shoes under $150"
2. **Add to Cart** - Say "Add the Nike ones to my cart"
3. **View Cart** - Check the sidebar or say "Show my cart"
4. **Checkout** - Click "Checkout with AP2" button
5. **Approve** - Review the Cart Mandate and approve

## 📁 Project Structure

```
ucp-demo-web/
├── server.py           # Flask backend with AP2 logic
├── products.json       # Product catalog
├── requirements.txt    # Python dependencies
├── static/
│   └── index.html     # Frontend UI
└── README.md          # This file
```

## 🔐 AP2 Flow Explained

1. **Cart Mandate Created** - Captures purchase details
2. **User Approval** - Explicit consent required
3. **Mandate Signed** - Cryptographic signature added
4. **Payment Processed** - Tokenized payment execution
5. **Order Confirmed** - Full audit trail generated

## 🛠️ Tech Stack

- **Backend**: Python + Flask
- **Frontend**: Vanilla HTML/CSS/JS
- **AI**: Google Gemini API
- **Styling**: Custom CSS with modern design

## 📝 License

MIT License - Feel free to use and modify!

---

Built with ❤️ to demonstrate the future of AI-powered commerce.
