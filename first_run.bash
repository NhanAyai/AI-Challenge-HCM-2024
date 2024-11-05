#!/bin/bash

echo "Install debian packages"
apt update 
apt -y install wget git

echo "Install pip packages"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt --progress-bar on

echo "Download LongCLIP"
git submodule update --init --recursive

wget -q --show-progress "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -P "./ckpt"

echo "Download l14_400"
wget -q --show-progress "https://dl.fbaipublicfiles.com/MMPT/metaclip/l14_400m.pt" -P "./ckpt"

echo "Download DFN5B CLIP VIT H 14"
wget -q --show-progress "https://huggingface.co/apple/DFN5B-CLIP-ViT-H-14/resolve/main/open_clip_pytorch_model.bin?download=true" -O "./ckpt/dfn5b_vit_h_14.bin"
echo "Install nltk"
echo "import nltk; nltk.download('punkt_tab')" | python
