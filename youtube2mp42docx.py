"""
pip3 install pytube
pip3 install jiwer
/Applications/Python\ 3.9/Install\ Certificates.command
pip3 install -U openai-whisper
install ffmpeg
https://www.ffmpeg.org/download.html#build-mac > static FFmpeg binaries for macOS 64-bit > download and unzip >
https://www.hostinger.in/tutorials/how-to-install-ffmpeg#How_to_Install_FFmpeg_on_macOS
"""

from pytube import YouTube
import whisper
import openai
import os
from dotenv import load_dotenv
from docx import Document
import torch

#Load api key from env file
def load_api_key():
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

# load input output parameters - URL of the YouTube video
def toload_input_output_parameters():
    global link, outputformat, outputaufilename, outputdocfilename, outputdocfilenamefromffmpeg, outputdocfilenamefromopenai
    link = "https://www.youtube.com/watch?v=it0l6lx3qI0&t"
    outputformat = 'mp4'
    outputdocfilename=''
    outputaufilename = 'kvutube2mp4filename.mp4'
    outputdocfilenamefromffmpeg = 'kvutube2docffmpegfilename.docx'
    outputdocfilenamefromopenai = 'kvutube2docopenaifilename.docx'

# Function to convert text to Word document
def text_to_word(text, filename=outputdocfilename):
    print("doc")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    return filename

# Create a YouTube object
def create_utube_object_download(link):
    try:
        yt=YouTube(link)
    except:
        print("Connection error while trying YouTube command")
    # Get the stream of the video
    yt.streams.filter(file_extension=outputformat)
    stream = yt.streams.get_audio_only()
    # Download the video
    stream.download('',outputfilename)

#to transcribe using whisper transcribe
def to_transcribe_using_whisper_ffmpeg(outputfilename):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = whisper.load_model("base").to(device)
    result = model.transcribe(outputfilename, fp16=False)
    print(result['text'])
    doc_file = text_to_word(result['text'],outputfilename)

#to transcribe using openai Audio transcribe
def to_transcribe_using_openai_whisper(outputfilename):
    audio_file= open(outputfilename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text=transcript.popitem()[1]
    print(text)
    doc_file = text_to_word(text,outputfilename)


load_api_key()
toload_input_output_parameters()
create_utube_object_download(link)
to_transcribe_using_whisper_ffmpeg(outputdocfilenamefromffmpeg)
to_transcribe_using_openai_whisper(outputdocfilenamefromopenai)
