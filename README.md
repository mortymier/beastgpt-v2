# 🌐 Live App

🔗 Open BeastGPT v2 on Streamlit Cloud: https://beastgpt-v2.streamlit.app/

---

# 🐱 BeastGPT v2

**AI-Powered Animal Battle Simulator Chatbot**

BeastGPT is an educational and entertaining animal battle simulator chatbot.
It compares two animals and simulates a hypothetical battle based on their real life characteristics.

This app was made in fulfillment for our midterm and final requirement in the course CSIT349 - Applied AI.

___ 

# ⚙️ Features

* **Battle Mode:** Select two animals from dropdown menus and simulate a battle with dynamic visuals.
* **Chat Mode:** Describe your epic animal battle in full detail on a chat interface.
* AI generates entertaining battle stories and provides comprehensive animal stats table.
* AI responds to animal education inquiries.

---

# 🧰 Technologies Used

* Python v3.14
* Streamlit
* Groq API
* Llama 3.1 8b Instant (Chat Mode)
* Llama 3.3 70B Versatile (Battle Mode)

--- 

# 📦 Local Setup

1. Clone the repository.
```bash
git clone https://github.com/mortymier/beastgpt-v2.git
```

2. Make sure you are in the right directory.
```bash
cd beastgpt-v2
```

3. Install dependencies.
```bash
pip install streamlit
pip install groq
```

or

```bash
pip install -r requirements.txt
```

4. Create new folder named **.streamlit** inside root folder (beastgpt-v2/.streamlit).
```
beastgpt-v2/
├── .streamlit
└── main.py
└── animals.py
└── ai.py
```

5. Create new file named **secrets.toml** inside .streamlit folder.
```
beastgpt-v2/
├── .streamlit/
    └── secrets.toml
└── main.py
└── animals.py
└── ai.py
```

6. In the secrets.toml file, add your Groq API Key using this line of code:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

7. After all these steps, try running the app in your terminal.
```bash
streamlit run main.py
```

8. Streamlit will open in your browser:
```
http://localhost:8501
```

---

# 👨‍💻 Contributors

* Flores, E.J Boy Gabriel
* Gabiana, Nicolo Francis
* Oswa, Yusuf Bin Mohammad Ali
* Perales, Clint
* Saniel, Mitchel Gabrielle

---

# 📜 License

This project is developed as an academic requirement for the CSIT349 - Applied AI course at Cebu Insitute of Technology - University. All rights reserved.