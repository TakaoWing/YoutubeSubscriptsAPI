from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import json

app = FastAPI()


def get_youtube_video(video_id: str):
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return YouTube(video_url)
    except Exception:
        raise HTTPException(status_code=404, detail='Invalid video ID')


def get_transcript_chunks(video_id: str, chunk_size: int = 2500):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['ja'])
        text = ''.join([line['text'].strip() for line in transcript])
        chunks = [text[i:i+chunk_size]
                  for i in range(0, len(text), chunk_size)]
        return [{'chunk': chunk} for chunk in chunks]
    except Exception:
        raise HTTPException(status_code=404, detail='Transcript not available')


@app.get('/api/video/{video_id}')
def get_video_info(video_id: str):
    video = get_youtube_video(video_id)
    transcript_chunks = get_transcript_chunks(video_id)
    url = 'https://youtu.be/'+video_id
    return {
        'title': video.title,
        'url': url,
        'transcript': transcript_chunks
    }
