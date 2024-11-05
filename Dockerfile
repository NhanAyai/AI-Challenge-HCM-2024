FROM python:3.10.5-slim
WORKDIR /workdir


VOLUME [ "/db","/keyframes" ]

COPY . .
RUN apt update && apt -y install wget git
RUN wget -q "https://huggingface.co/BeichenZhang/LongCLIP-L/resolve/main/longclip-L.pt" -P "./ckpt"

RUN wget -q "https://dl.fbaipublicfiles.com/MMPT/metaclip/l14_400m.pt" -P "./ckpt"

RUN wget -q "https://huggingface.co/apple/DFN5B-CLIP-ViT-H-14/resolve/main/open_clip_pytorch_model.bin?download=true" -O "./ckpt/dfn5b_vit_h_14.bin"

RUN ./first_run_docker.bash

EXPOSE 8502

CMD ["run_tunnel.bash"]
