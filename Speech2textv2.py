#coded in PyCharm
#.env file OPENAI_API_KEY="YOUR KEY"
#run code using the command from command line / terminal "streamlit run Speechetextv2.py"
import streamlit as st
import pdfkit
from docx import Document
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to convert audio file to text
def audio_to_text(audio_file):
    audio_file1=audio_file.name
    audio_file2 = open(audio_file1, "rb")
    # to transcribe
    #transcript = openai.Audio.transcribe("whisper-1", audio_file2)
    # to translate
    transcript = openai.Audio.translate("whisper-1", audio_file2)
    text = transcript.popitem()[1]
    return text

# Function to convert text to PDF
def text_to_pdf(text, filename="output.pdf"):
    print("pdf")
    pdfkit.from_string(text, filename)
    return filename

# Function to convert text to Word document
def text_to_word(text, filename="output.docx"):
    print("doc")
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)
    return filename

st.title("Speech to Text Converter")

# sidebar contents
with st.sidebar:
    st.title('OpenAI LLM based Speech to Text Converter')
    st.markdown('''
    ## The application is created using:
    
    - **streamlit**: For the web app interface. [Link](https://www.streamlit.io/)
    - **Open AI API whisper-1 Model**: For converting speech to text. [Link](https://platform.openai.com/docs/guides/speech-to-text)
    - **python-docx**: For creating Word documents. [Link](https://python-docx.readthedocs.io/)
    - **wkhtmltopdf**: converting HTML to PDF. [Link](https://wkhtmltopdf.org/downloads.html)
    - **pdfkit**: provides a Pythonic interface to wkhtmltopdf [Link](https://pypi.org/project/pdfkit/)

    ## About me:
    - [Linkedin](https://www.linkedin.com/in/vkrisvasan/)

    ''', unsafe_allow_html=True)

# Initialize session state
if 'text' not in st.session_state:
    st.session_state.text = ""

option = st.radio("Choose an option", ["Upload Audio File", "Record Audio (Not Implemented)"])

if option == "Upload Audio File":
    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm", "flac", "ogg"])

    if uploaded_file is not None:
        file_type = uploaded_file.type
        st.audio(uploaded_file, format=file_type)
        if st.button("Convert to Text"):
            try:
                # Convert audio to text
                st.session_state.text = audio_to_text(uploaded_file)
                st.text_area("Text:", value=st.session_state.text, height=200)

            except Exception as e:
                st.write("Error:", e)

    # Convert text to PDF/DOC
    if st.session_state.text and st.button("Convert Text to PDF and DOC"):
        pdf_file = text_to_pdf(st.session_state.text)
        doc_file = text_to_word(st.session_state.text)
        st.write("Completed generating PDF and DOCX in folder")

elif option == "Record Audio":
    st.write("Recording feature is not implemented in this example.")

