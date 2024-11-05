import faiss
import numpy as np
import pickle


class DB():
    def __init__(self,
                 faiss_db_path: str) -> None:
        self.faiss_db = faiss.read_index(faiss_db_path)

    def query(self,
              query: np.ndarray,
              k: int = 100) -> tuple[np.ndarray, np.ndarray]:
        _, indices = self.faiss_db.search(query, k)

        return indices.flatten()


class VideoMetadata():
    def __init__(self,
                 metadata_path: str,
                 nearby_index_path: str,
                 frame_index_path: str) -> None:
        self.metadata = self.__open_metadata(metadata_path)
        self.nearby_index = self.__load_nearby_index(nearby_index_path)
        self.frame_index = self.__load_frame_index(frame_index_path)

    def __load_nearby_index(self,
                            frame_index_path: str) -> list:
        with open(frame_index_path, "rb") as f:
            return pickle.load(f)

    def __open_metadata(self,
                        path) -> dict:
        return np.load(
            path,
            allow_pickle=True
        ).item()

    def map_indices(self,
                    indices_list: np.ndarray) -> list:
        return list(
            map(
                lambda i: self.frame_index[i],
                indices_list
            )
        )

    def __load_frame_index(self,
                           path) -> np.ndarray:
        return np.load(path)

    def get_by_index(self,
                     batch: int,
                     vid: int) -> list:
        i = f"L{batch:02d}_V{vid:03d}"
        return self.metadata.get(i)

    def get_by_name(self,
                    i: str) -> list:
        return self.metadata.get(i)
