from pathlib import Path 
from config.db import Vectors 
from config.loader import load_pdf, load_json 
from openai import OpenAI 
import multiprocessing 
multiprocessing.set_start_method("spawn", force=True)
 


async def  process_query(query: str):
    
    client = OpenAI() 

    vectors = Vectors()
    
    print("User Query", query)
    
    search_results = await vectors.search_query(query=query)  # Search for similar documents 
    #for result in search_results:
    #   print(result.page_content)  # Print the content of each result
    #    print(result.metadata)  # Print the metadata of each result

    print(search_results)

    context = "\n\n".join([f" URL : {result.metadata['url']}, heading: {result.metadata.get('heading', '')}, content: {result.page_content}" for result in search_results])

    print (context)

    #print(context)
    SYSTEM_PROMPT = """
    You are a helpful AI assistant that answers user questions based on the provided context retrieved from web scraped json file along with content , URL and Headings.

    You should only answer the user based on the following context and navigate the user to open the right page URL about the topic. If the context does not provide enough information, you should politely inform the user that you cannot answer the question based on the provided context.
    Your response should be concise and directly related to the user's query. 

    Important: All your responses must be formatted as a JSON object.

    Context:
    {context}

    Output:
     summary: output summary,
     url : the url of the page
     heading: the heading of the page


    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
        {"role": "user", "content": query}
    ]

    chat_completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=1000,
        temperature=0.2
    )
    response = chat_completion.choices[0].message.content
    print(response, '\n\n')
    messages.append({"role": "assistant", "content": response})

    
async def load_data(filepath: str):   
    
    vectors = Vectors()
    
    print('File received', filepath, __name__)
    try:
        # check file type: if pdf load load_pdf, if json load load_json from loader
        file_ext = Path(filepath).suffix.lower() 
        if file_ext == ".pdf":
            split_docs = await load_pdf(filepath)
        elif file_ext == ".json":
            split_docs = await load_json(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        results = await vectors.save_to_database(split_docs)
        return results
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None
    
    # Make sure to call load_data using 'await' in your async context, for example:
    # results = await load_data(filepath)