from abc import ABC, abstractmethod

class BackgroundRemover(ABC):
    @abstractmethod
    def remove_background(self, input_path: str, output_path: str) -> None:
        pass