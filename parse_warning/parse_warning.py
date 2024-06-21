import base64
import os
import pymupdf
import requests
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

def encode_image_from_bytes(image_bytes: bytes):
        return base64.b64encode(image_bytes).decode("utf-8")

def download_pdf_file(*,
                      pdf_url : str,
                      pdf_file_path : str):
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(requests.get(pdf_url).content)
    return pdf_file_path

def get_pdf_page_images(*, pdf_file : str, is_save_images : bool = False, image_dir : str = None):
    if not os.path.exists(pdf_file):
        raise FileNotFoundError(f"PDF file {pdf_file} not found.")
    
    if is_save_images and not image_dir:
        raise ValueError("Please provide a directory to save the images.")
    
    if is_save_images and not os.path.exists(image_dir):
        os.makedirs(image_dir)

    docs = pymupdf.open(pdf_file)
    for page in docs.pages():
        page_img = page.get_pixmap()
        if is_save_images and image_dir:
            page_img.save(f"{image_dir}/page_{page.number}.png")
        yield { "page_number" : page.number, "page_img_bytes" : page_img.tobytes() }


def warning_extraction_langchain() :
    # Define Azure OpenAI endpoint
    ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    ai_api_key = os.getenv("AZURE_OPENAI_KEY")
    ai_model = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT", "gpt-4o")  
    ai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2021-10-01")

    # Define the prompt template
    return


pdf_file_path = "sample_manual.pdf"

# Download LG Diswasher Manual
lg_manual_url = "https://gscs-b2c.lge.com/downloadFile?fileId=iCJYYWLtKIuRqa94Yi8vQ"

# Download the PDF file. If there is problem with downloading the file, you can download it manually and provide the path to the file in pdf_file_path variable.
# If the file is already downloaded, comment out the line below.
download_pdf_file(lg_manual_url, pdf_file_path)

# Create LanguageChain warning extraction
# Define Azure OpenAI endpoint and API key
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
ai_model = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT", "gpt-4o")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2021-10-01")
        
# Define the prompt template
warning_extract_prompt = ChatPromptTemplate.from_messages([
    ("system", """              
                You are an AI assistant designed to identify warning sections from an image of a document page.
                Your task is to locate and extract the caution, warning, and note sections from the image and output the text contained within each section
                in JSON format as follows: [{{"section_type":"note", "text": "section text"}}].
                If the image does not contain any sections that meet the provided criteria. Please output empty JSON array.

                A section is considered as Caution, Note, or Warning if it meets all the following layout criteria:
                1. Header Text:
                - The words "CAUTION", "NOTE", and "WARNING" must be in bold and all capital letters to signify the importance of the sections.
                - The header text must be located at the top left corner of the section.
                2 Icon:
                - For the "WARNING" section, a triangle with an exclamation mark inside, placed to the left of the word "WARNING".
                - For the "CAUTION" section, a triangle with an exclamation mark inside, placed to the left of the word "CAUTION".
                - For the "NOTE" section, there is no icon placed to the left of the word "NOTE".
                3. Horizontal Lines:
                - A thick horizontal line at the top to demarcate the beginning of each section.
                - Thinner horizontal lines may separate the "CAUTION" text from the "NOTE" text for clarity.
                The use of horizontal lines, bold text, and icons helps ensure that each part is easily identifiable and readable. Make sure the section text contains all the text within the horizontal lines.
                Before outputting the section text, please ensure that it meets all the criteria.
            """
    ),
    ("user", [
                {"type": "text", "text": "Please identify and extract caution, warning and note section text from the image."},
                {"type": "image_url", "image_url": "data:image/jpeg;base64,{page_image_data}"}
            ]
    ),
    ]
)

# Define the model
azure_chat_model = AzureChatOpenAI(azure_endpoint=openai_endpoint, api_key=openai_api_key, azure_deployment=ai_model, api_version=api_version)

# Define the chat function
chat_chain =  warning_extract_prompt | azure_chat_model | StrOutputParser()

# Get the images from the PDF file
for page in get_pdf_page_images(pdf_file=pdf_file_path, is_save_images=True, image_dir="./images"):
    # Page numbers start with 0
    page_no = page.get("page_number")
    print(f"Processing {page_no}")
    encoded_img = encode_image_from_bytes(page.get("page_img_bytes"))
    # invoke the chat chain
    result = chat_chain.invoke({"page_image_data": encoded_img})
    print(result)



             





        
    