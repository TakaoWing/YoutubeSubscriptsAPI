from fastapi import FastAPI, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

app = FastAPI()


def get_youtube_video(video_id: str):
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return YouTube(video_url)
    except Exception:
        raise HTTPException(status_code=404, detail='Invalid video ID')


def get_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['ja'])
        return ' '.join([line['text'] for line in transcript])
    except Exception:
        raise HTTPException(status_code=404, detail='Transcript not available')


@app.get('/api/video/{video_id}')
def get_video_info(video_id: str):
    video = get_youtube_video(video_id)
    transcript = get_transcript(video_id)
    url = 'https://youtu.be/'+video_id
    return {
        'title': video.title,
        'url': url,
        'transcript': transcript
    }
