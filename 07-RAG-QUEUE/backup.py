print("User Query", query)
    
    search_results = await vectors.search_query(query, k=3)  # Search for similar documents 
    #for result in search_results:
    #   print(result.page_content)  # Print the content of each result
    #    print(result.metadata)  # Print the metadata of each result

    print(search_results)

    context = "\n\n".join([f" URL : {result.metadata['url']  }, heading:   {result.heading}, content: {result.content}" for result in search_results])

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
