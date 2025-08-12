# Brute Force Demo - Web Deployment

This is the web version of the Brute Force Attack Simulator, converted from CustomTkinter to Streamlit for easy team sharing.

## 🚀 Quick Start (Local Testing)

1. Install dependencies:
```bash
pip install streamlit
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## 🌐 Deploy to Streamlit Community Cloud (Free)

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Steps:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Streamlit brute force demo"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   `https://your-repo-name-yourusername.streamlit.app`

## 📁 File Structure
```
your-project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── secret_user_info/
│   └── secret_password.txt
├── small-password-list/
│   └── smallpasswordlist.txt
└── README_DEPLOYMENT.md   # This file
```

## 🔧 Features Preserved from Desktop Version

✅ **All core logic preserved:**
- `read_passwords_from_file()` function
- `get_target()` function  
- `perform_2fa()` function
- Main attack simulation logic

✅ **Enhanced for web:**
- Real-time progress updates
- Professional web interface
- Mobile-friendly design
- Live statistics
- Better error handling

## 🎯 Sharing with Your Team

Once deployed, simply share the URL with your team members:
- No installation required
- Works on any device with a browser
- Real-time updates
- Professional appearance

## 🔒 Security Notes

- This is for educational purposes only
- Includes appropriate disclaimers
- 2FA simulation for security demonstration
- Safe for academic presentations

## 🛠️ Troubleshooting

**File not found errors:**
- Ensure `secret_user_info/` and `small-password-list/` folders are included in your repository
- Check that file paths are correct

**Deployment issues:**
- Verify `requirements.txt` is in root directory
- Ensure `app.py` is in root directory
- Check GitHub repository is public (for free tier)

## 📊 Original vs Streamlit Version

| Feature | Original (CustomTkinter) | Streamlit Version |
|---------|-------------------------|-------------------|
| Core Logic | ✅ Preserved | ✅ Preserved |
| 2FA Function | ✅ Preserved | ✅ Enhanced |
| UI Updates | Desktop widgets | Web components |
| File Handling | ✅ Preserved | ✅ Enhanced |
| Team Sharing | Local only | Web URL |
| Mobile Support | ❌ No | ✅ Yes |
