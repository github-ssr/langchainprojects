import base64
import os
from langchain.prompts import PromptTemplate, ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

def encode_image_from_file(image_path: str):
    # Get bytes from image file
    with open(image_path, "rb") as file:
        image_bytes = file.read()

    # Get base64 encoding of image
    return base64.b64encode(image_bytes).decode("utf-8")


examples = []
example_list = [
    ("./sample_images/dog_image.jpg","dog"),
    ("./sample_images/cat_image.jpg","cat")
    ]

# Create list of examples based on images in sample_images folder.
for ex in example_list :
    image_base64 = encode_image_from_file(ex[0])
    multimodal_example = {
        "example_image_base64": f"{image_base64}",
        "example_image_answer": f"{ex[1]}",
    }
    examples.append(multimodal_example)

# Define Example Prompt
example_prompt = ChatPromptTemplate.from_messages(
    [
    ("user",[
                {"type": "text", "text": "Can you identify animal in this image?"},
                {"type":"image_url", "image_url": "data:image/jpeg;base64,{example_image_base64}"}
            ]),
    ("ai", "{example_image_answer}")
    ]
    )


few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt
)


# Define Final Prompt
final_prompt = ChatPromptTemplate.from_messages(messages=
    [
        ("system", "You are AI assistant that identify the animal in the image. You are given an image and you need to identify the animal in the image."),
        few_shot_prompt,
        ("user", [
                    {"type": "text", "text": "Can you identify animal in this image?"},
                    {"type": "image_url", "image_url": "data:image/jpeg;base64,{animal_image_data}"}
                ]
        ),
    ])
 

# Create LangChain for animal image detection
# Define Azure OpenAI endpoint and API key
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = os.getenv("AZURE_OPENAI_KEY")
ai_model = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT", "gpt-4o")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2021-10-01")

# Define the model
azure_chat_model = AzureChatOpenAI(azure_endpoint=openai_endpoint, api_key=openai_api_key, azure_deployment=ai_model, api_version=api_version)

# Define the chat function
image_detection_chain =  final_prompt | azure_chat_model | StrOutputParser()

image_to_detect = encode_image_from_file("./sample_images/pig_image.jpg")

# To debug, we can print output of final prompt
#final_prompt_format = final_prompt.format(animal_image_data="image-data")
#print(final_prompt_format)

result = image_detection_chain.invoke({"animal_image_data": image_to_detect})
print(result)








 