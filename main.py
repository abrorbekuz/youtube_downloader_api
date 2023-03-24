import asyncio
import re, uvicorn
import aiohttp
import yt_dlp as youtube_dl
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from cachetools import TTLCache
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from starlette.responses import StreamingResponse

app = FastAPI()

origins = ["*"]
headers = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET"], allow_headers=headers)
ydl = youtube_dl.YoutubeDL({'extract_flat': True, 'ignoreerrors': True})
cache = TTLCache(maxsize=100, ttl=1800)

def extract_arguments_from_url(url):
    data = url.split('?')

    if len(data) == 1:
        return {}
    
    query_params = {}
    for query_param in data[1].split('&'):
        key, value = query_param.split('=')
        query_params[key] = value
    return query_params

def formatter(data, v: str = None, llist: str = None, channel: bool = False):
    if v is not None:
        return data
    else:
        if channel:
            if len(data.get("entries", None)) == 2:
                entries = data.get("entries", None)[0]
                return entries.get("entries", entries)
        return data.get("entries", None)

async def get_info(url: str, plain: bool) -> dict:
    
    extraction = extract_arguments_from_url(url)
    v = extraction.get('v', None)
    llist = extraction.get('list', None)
    channel = False

    if v == None and llist == None:
        channel = True

    if llist is not None: f_type = "playlist"
    if v is not None: f_type = "video"
    if channel: f_type = "channel"

    if (url in cache) and (v is not None):
        return cache[url], f_type
    
    ydl = youtube_dl.YoutubeDL({'extract_flat': True, 'ignoreerrors': True})

    if llist is not None or channel:
        ydl = youtube_dl.YoutubeDL({"extract_flat": "in_playlist", "skip_download": True})

    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, ydl.extract_info, url, False)
    if not plain:
        result = formatter(info, v, llist, channel)
    else: result = info
    
    if v is not None:
        cache[url] = result

    return result, f_type


async def search_videos(query: str, max: int) -> str:
    search_results = await run_in_threadpool(ydl.extract_info, f"ytsearch{max}:{query}", False)
    return search_results['entries']

@app.get("/")
async def root(url: str = None, plain: bool = False):
    try:
        data, f_type = await get_info(url, plain)
        return JSONResponse(content={"data": data, "data_type": f_type, "status": "success", "error": False})
    except youtube_dl.utils.DownloadError:
        return {"data": None, "status": "invalid url", "error": True}

@app.get("/search")
async def search(query: str = None, max: int = 10):
    data = await search_videos(query, max)
    return JSONResponse(content={"data": data, "data_type": "search", "status": "success", "error": False})


@app.get("/stream")
async def stream(url: str = None):
    def get_stream(url):
        with aiohttp.ClientSession() as session:
            with session.get(url) as resp:
                for data in resp.content.iter_any():
                    yield data

    regex = r"^(http|https):\/\/r([a-zA-Z]|[0-9])+---sn-([a-zA-Z]|[0-9])+.googlevideo.com.*"
    if re.search(regex, url):
        return StreamingResponse(get_stream(url), media_type="video/mp4")
    else:
        data = {
            "data": None,
            "status": "invalid googlevideo url",
            "error": True
        }
        return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10111)