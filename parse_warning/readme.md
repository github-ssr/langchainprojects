# Introduction
This sample project showcases the utilization of GPT-4o and langchain to parse layout and extract text from PDF document. By combining the image processing capabilities of GPT-4o with langchain, you can efficiently extract meaningful text from complex documents.

## Getting Started
To get started with this project, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`
2. Ensure that you have created an Azure Open AI service and deployed the GPT-4o model. For more information, refer to the documentation on Azure Open AI and GPT-4o model deployment at [Azure Open AI Concepts](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models) and [Azure Open AI Resource Creation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal)
3. Retrieve the Azure Open AI Service URL and Azure Open AI Service Key, and update the .env file.

```plaintext
AZURE_OPENAI_ENDPOINT="https://<AZURE-OPEN-AI-ENDPOINT>.openai.azure.com/"
AZURE_OPENAI_KEY="<AZURE OPEN AI KEY>"
AZURE_OPENAI_MODEL_DEPLOYMENT="gpt-4o"
AZURE_OPENAI_API_VERSION="2023-05-15"
```

## Usage
To execute the `parse_warning.py` Python script, run the following command:

```bash
python parse_warning.py
```
Ensure that you have the necessary permissions and dependencies installed before running the script.

This Python script will perform the following tasks:
1. Download the LG Dishwasher Manual from "https://gscs-b2c.lge.com/downloadFile?fileId=iCJYYWLtKIuRqa94Yi8vQ" and save it as `sample_manual.pdf`.
2. Generate image files for each page of the sample manual.
3. Utilize LangChain and GPT-4o to analyze the layout of the images and extract the warning, caution, and note sections of the document.
4. Output the extracted warning, caution, and note text.

## Disclaimer
This project is provided as a sample and is intended for educational and demonstration purposes only. It is not intended for production use. The code and techniques used in this project may not be optimized or secure for real-world scenarios. Use at your own risk.
Please note that the extraction of text from complex documents using GPT-4o and langchain may not always be accurate or complete. It is recommended to thoroughly test and validate the results before relying on them for any critical applications.
This project is not associated with or endorsed by LG Electronics. The LG Dishwasher manual used for demonstration purposes is solely for illustrative purposes and does not imply any affiliation with or endorsement by LG Electronics.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more information.

## Acknowledgements
- langchain: [Link to langchain](https://langchain.io)

