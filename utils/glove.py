import torch


class Glove:
    @staticmethod
    def _load_glove_vectors(glove_file):
        glove_vectors = {}
        with open(glove_file, "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = torch.tensor(
                    [float(val) for val in values[1:]], dtype=torch.float32
                )
                glove_vectors[word] = vector
        return glove_vectors
