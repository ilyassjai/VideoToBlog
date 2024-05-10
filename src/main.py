from .utils import *
from .whisper import *
import pandas as pd
from langchain_openai import ChatOpenAI
import os
import glob
from tqdm import tqdm
from operator import itemgetter
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough




def videotodataframe(url) -> pd.DataFrame :
    video_path=download(url)
    asyncio.run(process_video_or_playlist(url, max_simultaneous_youtube_downloads, max_workers_transcribe))
    dict_time=extract_unique_slides_mse(video_path, mse_threshold=1000)
    dict_ocr=extract_text_from_image('./slidemse/')
    combined_json = combine_dicts(dict_time, dict_ocr)
    df=pd.read_csv('./generated_transcript_metadata_tables/pde_chapter_ii_section_22.csv')
    with open("./combined.json", "r") as file:
        data = json.load(file)
        list_of_dicts = list(data.values())
    df_slides = pd.DataFrame(list_of_dicts)
    list = []
# add an column 'text' with the text of the transcript
    for i in range(len(list_of_dicts)):
        start=df_slides['start'][i]
        
        end=df_slides['end'][i]
        print(start,end)
        transcript=""
        for i in range(len(df['text'])):
            if df['start'][i]>=start and df['end'][i]<=end:
                transcript+=df['text'][i]
        list.append(transcript)
    df_slides['text'] = list

    return df_slides



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




if __name__ == "__main__":

    load_dotenv()

    url = 'https://www.youtube.com/watch?v=gSYGOZVugtw'
    openai_api_key = os.getenv('OPENAI_KEY')

    image_paths = [os.path.join('./slidemse', file) for file in glob.glob(os.path.join('./slidemse', '*.png'))]
    md_paths = [f"output{i}.md" for i in range(len(image_paths))]

    #start
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    df_slides=videotodataframe(url)
    chat(llm,df_slides)
    merged_md = merge_markdown_with_images(md_paths, image_paths)

    with open("merged_output.md", "w") as f:
        f.write(merged_md)