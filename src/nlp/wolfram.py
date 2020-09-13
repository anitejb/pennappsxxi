import requests
from urllib.parse import quote_plus

class Wolfram:
    def __init__(self):
        self.api_key = "KH3LRW-HUELER2TUL"
        self.base_api_url = f"http://api.wolframalpha.com/v1/simple?appid={self.api_key}&i="
        self.STOP_WORD = "magic"

    def get_query_url(self, query_text):
        query_str = quote_plus(query_text.lower().strip().replace(".", "").replace("!", ""))
        return f"{self.base_api_url}{query_str}"

    def query_wolfram(self, query_text):
        query_str = quote_plus(query_text.lower().strip().replace(".", "").replace("!", ""))
        resp = requests.get(f"{self.base_api_url}{query_str}")
        if resp.status_code != 200:
            print(f'Failed to fetch "{query_text}" from Wolfram. Status code {resp.status_code}')
        return resp.content

# if __name__ == "__main__":
#     w = Wolfram()
#     with open("./wolfram.png", "wb") as f:
#         f.write(w.query_wolfram("what is the capital of france"))

