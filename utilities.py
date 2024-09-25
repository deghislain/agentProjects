import re
from datetime import date


def extract_sources(text, links):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    urls + re.findall(url_pattern, links)
    return urls


def store_the_content(topic, content, path):
    print("store_the_content------------------------------------ ", store_the_content)
    today = str(date.today())
    f = open(path + today + "_" + topic + ".txt", "w")
    f.write(content)
    f.close()
