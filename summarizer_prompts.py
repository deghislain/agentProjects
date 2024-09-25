
def get_search_prompt(topic):
    return f"""
               You are a researcher. Your task is to use the tools at your disposal to search
               and return the latest development in {topic}.
           """


def get_write_prompt(topic, sources):
    return f"""
                 Write an exceptional research paper on {topic} using {sources}. 
                 Apply expert copywriting and content creation skills to produce a well-structured, 
                 engaging, and thoroughly referenced document, using the tools at your disposal.
                 
                 Make sure it is easy to read and understand for a non-technical audience. 
                 ENSURE THAT ALL INFORMATION ARE ACCURATE AND UP-TO-DATE. 

           """