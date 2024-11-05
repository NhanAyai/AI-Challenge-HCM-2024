#TEST? NUN HUH

# Install pip packages
Write-Host "Install pip packages"
pip install -r requirements.txt --progress-bar on 
pip install torch torchvision torchaudio

git submodule update --init --recursive
# Download LongCLIP

Write-Host "Download LongCLIP"
Invoke-WebRequest -Uri "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -OutFile "./ckpt/longclip-L.pt"

Invoke-WebRequest -Uri "https://dl.fbaipublicfiles.com/MMPT/metaclip/l14_400m.pt" -OutFile "./ckpt/l14_400m.pt"

Invoke-WebRequest -Uri "https://huggingface.co/apple/DFN5B-CLIP-ViT-H-14/resolve/main/open_clip_pytorch_model.bin?download=true" -OutFile "./ckpt/dfn5b_vit_h_14.bin"
# Install nltk
Write-Host "Install nltk"
python -c "import nltk; nltk.download('punkt_tab')"
