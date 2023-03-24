# youtube_downloader_api
FAST API + YOUTUBE_DL to get googlevideo links using "youtube api js" and "youtube android api js"

# Installation
You need [Python 3](https://www.python.org/downloads/) to run this.
Recomment you to use virtual environment to this shit)

### Install Dependencies
Install needed YTDL and FastAPI Libraries with pip by executing following command into your terminal or command line: `pip install -r requirements.txt`

### Clone the Repository
`git clone https://github.com/abrorbekuz/youtube_downloader_api.git`

### Get to the repository directory
`$ cd youtube_downloader_api/`

### Run
Execute `python3 main.py` from your terminal and the api should be running at port `10111`.

### Usage
Make requests to the api with `url` parameter
For eg: `curl http://localhost:10111?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### Play signed YouTube videos (eg: from YouTube Music & so on.)
Make request to `/stream` endpoint with `url` parameter with urlencoded googlevideo url and it will return video/audio stream
For eg: `curl http://localhost:10111/stream?url=https%3A%2F%2Frr1---sn-cvh76ner.googlevideo.com%2Fvideoplayback%3Fexpire%3D1653153965%26ei%3DTcyIYu_BNMfKgAPMkIewBw%26ip%...`


### Demo
[Ayo demo here ...)](http://167.71.26.13:10111/)
