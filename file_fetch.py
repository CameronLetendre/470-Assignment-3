import bs4
import regex as re
import json
import csv as tsv


# Cleaning the text of tags and punctuation
def clean_topics_text(item):

    full_string = item['Title'] + ' ' + item['Body'] + ' ' + item['Tags']

    full_string = bs4.BeautifulSoup(full_string, 'html.parser').text
    full_string = re.sub(r'[^a-zA-Z\s]', ' ', full_string)

    return full_string

def clean_answers_text(item): 
    full_string = bs4.BeautifulSoup(item['Text'], 'html.parser').text
    full_string = re.sub(r'[^a-zA-Z\s]', ' ', full_string)

    return full_string

def load_json_file(topic_filepath):
    # a method used to read the topic file for this year of the lab; to be passed to BERT/PyTerrier methods
    with open(topic_filepath, encoding='utf-8') as f:
        queries = json.load(f)

    result = {}
    for item in queries:
        if 'Title' in item:
            preprocessed_data = clean_topics_text(item)
        if 'Text' in item:
            preprocessed_data = clean_answers_text(item)

        result[item['Id']] = preprocessed_data
    return result

# is it better to pass to my model as a strings or a list of strings?

# a method used to read the topic file
def read_qrel_file(qrel_filepath):
    result = {}
    with open(qrel_filepath, "r") as f:
        reader = tsv.reader(f, delimiter='\t', lineterminator='\n')
        for line in reader:
            query_id = line[0]
            doc_id = line[2]
            score = int(line[3])
            if query_id in result:
                result[query_id][doc_id] = score
            else:
                result[query_id] = {doc_id: score}

    return result

