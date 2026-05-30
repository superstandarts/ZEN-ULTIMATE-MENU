def generate_readme(name, description, author):
    return f"""<div align="center">

# 🔴 {name}

### {description}

![Python](https://img.shields.io/badge/Python-3.10+-red?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-active-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows-black?style=for-the-badge&logo=windows&logoColor=white)

</div>

---

## 📌 About

**{name}** is a ZEN-style project created to be useful, clean and easy to use.

---

## ✨ Features

- Modern dark/red interface
- Simple setup
- Lightweight project structure
- Easy customization

---

## 📦 Installation

```bash
pip install -r requirements.txt
python main.py
```

---

## 👤 Author

Made by [{author}](https://github.com/{author})

---

<div align="center">

```txt
SYSTEM STATUS: ONLINE
ACCESS: GRANTED
```

</div>
"""
