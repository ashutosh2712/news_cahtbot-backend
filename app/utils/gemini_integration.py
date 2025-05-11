# import google.generativeai as genai
from google import genai
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# # Configure the Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def call_gemini_api(passages, query):
    """
    Calls the Gemini API to generate a final response based on the passages and query.
    """
    try:
        # Construct the prompt by adding the query and relevant passages
        prompt = f"Answer the following query based on the passages:\n\n{query}\n\nPassages:\n" + "\n".join(passages)
        
        # Call the Gemini API to generate the response
        # response = genai.GenerativeModel(
        #     "gemini-1.5-flash"
        #     ).generate_content(
        #         prompt=prompt, 
        #         max_output_tokens=200
        #     )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        # Extract the generated text (answer)
        final_answer = response.text.strip()
        return final_answer

    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return "Error generating response."


# if __name__ == "__main__":
#     query = "What are the latest developments in AI?"
#     passages = ["AI is transforming industries like healthcare and finance.",
#                 "Recent advancements in AI include large language models and deep learning.",
#                 "AI-powered applications are now being used for predictive analytics in various fields."]

#     final_answer = call_gemini_api(passages, query)
#     print(final_answer)
    
    