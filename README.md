# 🛒 UCP + AP2 Shopping Agent - Web Interface

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://your-app.onrender.com)
[![GitHub](https://img.shields.io/badge/github-repo-blue)](https://github.com/YOUR_USERNAME/ucp-shopping-demo)

> **🌐 [Try the Live Demo!](https://your-app.onrender.com)** ← Click here to see it in action!

A beautiful web interface demonstrating Google's Universal Commerce Protocol (UCP) and Agent Payments Protocol (AP2) with an AI-powered shopping agent.

![Demo Screenshot](screenshot.png)

## ✨ Features

- 💬 **AI Chat Interface** - Natural language shopping powered by Google Gemini
- 🛒 **Real-time Cart** - Visual shopping cart with live updates
- 📜 **AP2 Checkout Flow** - Complete mandate approval system with cryptographic signatures
- 🔐 **Verification Trail** - Transparent proof of authorization
- 🎨 **Modern UI** - Beautiful dark theme with smooth animations
- 🤖 **Smart Product Discovery** - AI understands queries like "show me affordable running shoes"

## 🎥 Demo

Try these commands in the chat:
- "Show me running shoes under $150"
- "Add the Nike ones to my cart"
- "What's in my cart?"
- "Checkout"

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ucp-shopping-demo.git
cd ucp-shopping-demo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows
set GEMINI_API_KEY=your-key-here

# Mac/Linux
export GEMINI_API_KEY=your-key-here
```

**Option B: Edit server.py**
Open `server.py` and uncomment line 28:
```python
API_KEY = 'your-key-here'
```

### 4. Run the Server

```bash
python server.py
```

### 5. Open in Browser

Navigate to: **http://localhost:5000**

## 📁 Project Structure

```
ucp-shopping-demo/
├── server.py              # Flask backend with AP2 logic
├── products.json          # Product catalog (10 demo products)
├── requirements.txt       # Python dependencies
├── static/
│   └── index.html        # Frontend UI (chat, cart, checkout)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔐 AP2 Protocol Flow

The Agent Payments Protocol (AP2) ensures secure, transparent, and verifiable transactions:

1. **Cart Mandate Creation** 🛒
   - Agent captures purchase intent with product details, prices, and user info
   - Creates cryptographic signature of cart state

2. **User Approval** ✅
   - User explicitly reviews and approves the mandate
   - Can see all items, total, shipping address, and payment method

3. **Mandate Signing** 🔏
   - System generates digital signature proving user consent
   - Timestamp and user signature added to mandate

4. **Payment Processing** 💳
   - Tokenized payment execution using approved mandate
   - No direct exposure of payment credentials

5. **Order Confirmation** 📦
   - Complete audit trail generated
   - Includes all mandate IDs, signatures, and verification data

### Why AP2 Matters

Traditional e-commerce requires manual clicks through checkout flows. With AP2:
- ✅ **AI agents can complete purchases** on your behalf
- ✅ **You maintain full control** through explicit approval
- ✅ **Cryptographic proof** of every transaction
- ✅ **Transparent audit trail** for compliance

## 🤖 AI-Powered Shopping

The agent uses Google Gemini to understand natural language:

```
User: "I need some good running shoes but I'm on a budget"
Agent: "I found several great options under $150:
        - Nike Air Zoom Pegasus 40 ($130) - Responsive cushioning
        - Brooks Ghost 15 ($140) - Smooth transitions
        Would you like to add either to your cart?"
```

The agent can:
- Browse and filter products
- Compare options
- Add items to cart
- Process checkout
- Handle follow-up questions

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python + Flask |
| **AI Model** | Google Gemini 2.0 Flash |
| **Frontend** | Vanilla HTML/CSS/JavaScript |
| **Styling** | Custom CSS with animations |
| **Protocols** | UCP (Universal Commerce), AP2 (Agent Payments) |

## 🌐 Deployment

This project is deployed on [Render](https://render.com) (free tier).

### Deploy Your Own

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Fork this repository
2. Sign up on Render
3. Create a new Web Service
4. Connect your GitHub repo
5. Add `GEMINI_API_KEY` environment variable
6. Deploy!

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📊 Product Catalog

The demo includes 10 products across categories:
- Running Shoes (Nike, Adidas, New Balance, ASICS, Brooks)
- Headphones (Sony, Apple)
- Smartwatch (Samsung)
- E-reader (Kindle)
- Portable Charger (Anker)

Edit `products.json` to add your own products!

## 🎨 Screenshots

### Chat Interface
![Chat](docs/chat.png)

### Cart & Checkout
![Cart](docs/cart.png)

### AP2 Mandate Approval
![Mandate](docs/mandate.png)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Google for the UCP and AP2 protocol concepts
- Google Gemini API for powering the AI agent
- The open-source community

## 📧 Contact

**Your Name** - [@yourhandle](https://twitter.com/yourhandle)

Project Link: [https://github.com/YOUR_USERNAME/ucp-shopping-demo](https://github.com/YOUR_USERNAME/ucp-shopping-demo)

---

⭐ **Star this repo if you found it helpful!**

Built with ❤️ to demonstrate the future of AI-powered commerce
