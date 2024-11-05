import open_clip
import numpy as np
import torch

from PIL import Image


class OpenCLIP():
    def __init__(self,
                 model_name: str,
                 pretrained: str,
                 device: str = "cpu") -> None:
        self.device = self.__get_device(device)
        self.model, self.tokenizer, self.preprocess = self.__eval_model(
            model_name, pretrained)

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
                     model_name: str,
                     pretrained: str,):
        model, _, preprocess = open_clip.create_model_and_transforms(
            model_name,
            pretrained=pretrained,
            device=self.device
        )
        model.eval()

        tokenizer = open_clip.get_tokenizer(model_name)
        return model, tokenizer, preprocess

    def encode_text(self,
                    search_text: str | list[str]) -> np.ndarray:
        text_tokens = self.tokenizer(search_text)

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
