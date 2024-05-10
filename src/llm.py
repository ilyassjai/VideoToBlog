from .utils import *
from .whisper import *
import pandas as pd
from langchain_openai import ChatOpenAI
from tqdm import tqdm
from operator import itemgetter
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough




def chat(llm,df_slides):
    for i in range( df_slides.shape[0]):
        transcript=df_slides['text'][i]
        if transcript=="":
            output=""
        else:
            
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a helpful chatbot"),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}"),
                ]
            )
            description = df_slides['descrp'][i]

            transcript_with_name = transcript
            position = "beginning" if i==0 else "middle" if i<df_slides.shape[0]-1 else "end"
            text=f"""

            Here is a transcribed text, which is part of a larger video:
            The transcription is : {transcript_with_name}
            The transcription is at the {position} of the blog post
            The text in the slide is : {description}

            Your task is to transform it into an Markdown format suitable for a blog. Your goal is to create a clear and concise summary while following the guidelines below:
            - Use the memory to keep track of the history of your previous outputs.
            - Eliminate verbal tics.
            - Take note of the position to insert the text in the blog post.
            - Output valid Markdown.
            - Insert section headings and other formatting as needed.
            - Avoid redundancy and extraneous information.
            - Ensure the final output is suitable for inclusion in a textbook."""

            inputs = {"input" : text}

            memory = ConversationBufferMemory(return_messages=True)

            memory.load_memory_variables({})
            chain = (
                RunnablePassthrough.assign(
                    history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
                )
                | prompt
                | llm
            )


            response = chain.invoke(inputs)
            memory.save_context(inputs, {"output": response.content})

            memory.load_memory_variables({})




            
            output=response.content
            
        print(len(output))
        try:
            with open(f"output{i}.md", "w") as file:
                file.write(output)
        except:
            print("error")
            print(output)
            continue



def merge_markdown_with_images(md_paths, image_paths):
    merged_md = ""

    for i, md_path in enumerate(md_paths):
        with open(md_path, 'r') as f:
            md_content = f.read()
            # if markdown content is empty, skip it
            if not md_content:
                continue
            else:
                # Add markdown content
                merged_md += md_content
                # Add image path after each markdown file
                image_path = image_paths[i]
                merged_md += f"\n\n![Image]({image_path})\n\n"

    return merged_md


