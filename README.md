# 🌟 AI-Challenge-HCM-2024 🌟

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10.5-blue?style=for-the-badge" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Docker-Supported-green?style=for-the-badge" alt="Docker Badge"/>
</p>

---

## 📚 Dataset

<p align="center">
  The project uses the following datasets:
</p>

1. **[Set 1](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-keyframe-extract-1-kf)**  
2. **[Set 2](https://www.kaggle.com/datasets/huynhmy1/hcm-ai-keyframe-extract-2-kf)**  
3. **[Set 3](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-keyframe-extract-l25-30)**  
4. **[DB](https://www.kaggle.com/datasets/letruonggiangk17ct/hcm-ai-db)**  

---

## 🔧 Instructions

### Step 1: Prepare Directories
Extract all keyframes into the `./keyframes` directory and extract the database into the `./db` directory.

> [!IMPORTANT]  
> 📦 **3 CLIP models are about 15GB in size**  
> ⚠️ For some reason, the progress bar for the OpenCLIP downloading process no longer shows up.

---

### 🖥️ Local Setup

> [!WARNING]  
> ❌ **DO NOT RUN ON WINDOWS**, use Docker instead.

1. **Create a Python 3.10.5 Environment**  
   Make sure you have Python 3.10.5 installed.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/potasium142/hcm_ai_2024_dashboard
   cd hcm_ai_2024_dashboard
   
3. **Run the Setup Script**
- On Linux/MacOS: Run first_run.bash
- On Windows (PowerShell): Run first_run.ps1

4. **Start the Dashboard**
After the setup script finishes, run:
```bash
streamlit run dashboard.py
```

🐳 Docker Setup
1. Build the Docker Image

```bash
docker build . --tag hcmai_c2024:dashboard
```
2. Run the Docker Container

```bash
docker run --name hcm_ai_dashboard -p 8502:8502 -v ./keyframes:/keyframes -v ./db:/db potasium142/hcm_ai_dashboard:main
```

🙏 Acknowledgements
<p align="center">
Thank you for checking out this project! If you find it helpful, please give it a star ⭐.
Good luck with your AI journey! 🚀
</p>

<p align="center">
Made with ❤️ by Our Team
</p>
