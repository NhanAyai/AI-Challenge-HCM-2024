from longclip.model import longclip
from PIL import Image
import numpy as np
import torch


class LongCLIPModel():
    def __init__(self,
                 ckpt_path: str,
                 device: str = "cpu") -> None:
        self.device = self.__get_device(device)
        self.model, self.preprocess = self.__eval_model(ckpt_path)

    def __get_device(self,
                     device: str):
        match device:
            case "cpu":
                return torch.device("cpu")
            case "cuda":
                if torch.cuda.is_available():
                    return torch.device("cuda")

                print("CUDA is not available, fallback to cpu")
                return torch.device("cpu")
            case "_":
                raise Exception(f"Unknow device:{device}")

    def __eval_model(self,
                     path: str):
        model, preprocess = longclip.load(path, device=self.device)
        model.eval()
        return model, preprocess

    def encode_text(self,
                    search_text: str | list[str]) -> np.ndarray:
        text_tokens = longclip\
            .tokenize(search_text)\
            .to(self.device)

        with torch.no_grad():
            text_features = self.model\
                .encode_text(text_tokens)\
                .float()

        text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.numpy()

    def encode_image(self,
                     image_path: str) -> np.ndarray:
        image = self.preprocess(Image.open(image_path)).unsqueeze(0)

        with torch.no_grad():
            image_features = self.model\
                .encode_image(image)\
                .float()

        image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.numpy()
