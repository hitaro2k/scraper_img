import os
import aiohttp
import asyncio
import aiofiles
from bs4 import BeautifulSoup
from dialogWindow import get_word_from_user
from tkinter import filedialog

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.bbc.com/news',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'DNT': '1',
}


class Connection:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch(self, url):
        async with self.session.get(url, headers=headers) as response:
            return await response.text()

    async def close(self):
        await self.session.close()

async def save_image(session, url, folder, index):
    if not url.startswith(('http:', 'https:')):
        url = 'http:' + url
    async with session.get(url) as response:
        if response.status == 200:
            file_path = os.path.join(folder, f'image_{index}.jpg')
            async with aiofiles.open(file_path, 'wb') as file:
                await file.write(await response.read())
            print(f'Img {file_path} download access.')
        else:
            print(f'Error in download {url}: status code {response.status}')

async def download_images(arrImg, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    async with aiohttp.ClientSession() as session:
        tasks = [save_image(session, url, folder, index) for index, url in enumerate(arrImg)]
        await asyncio.gather(*tasks)

async def main(word, folder='images'):
    fetcher = Connection()
    URL = f'https://www.flickr.com/search/?text={word}'
    try:
        html = await fetcher.fetch(URL)
        soup = BeautifulSoup(html, 'html.parser')
        main_div = soup.find("div", class_="main search-photos-results")
        img = main_div.find_all("img") if main_div else []
        arrImg = [image.get("src") for image in img if image.get("src")]
        await download_images(arrImg, folder)
    finally:
        await fetcher.close()


def on_word_received(word):
    chosen_folder = filedialog.askdirectory()
    if chosen_folder:
        asyncio.run(main(word, chosen_folder))

if __name__ == "__main__":
    get_word_from_user(on_word_received)