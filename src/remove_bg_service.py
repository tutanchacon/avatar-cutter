from src.background_remover import BackgroundRemover
import requests

class RemoveBgService(BackgroundRemover):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def remove_background(self, input_path: str, output_path: str) -> None:
        
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(input_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': self.api_key}
        )
        
        if response.status_code == requests.codes.ok:
            with open(output_path, 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
        