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

import json

def get_100_queries(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_top_100 = {}

    # dict query_text -> answers_texts
    for query in data:
        query_text = query_id_to_text(query['topic_id'], 'topics_1.json')
        answers_results = []
        for result in query['results']:
            answer = result[0]  # Access the dictionary within the list
            cleaned_text = clean_answers_text(answer)
            answers_results.append({
                'answer_id': answer['Id'],
                'text': cleaned_text
            })
        cleaned_top_100[query['topic_id']] = {
            'query_text': query_text,
            'answers': answers_results
        }

    return cleaned_top_100

def query_id_to_text(query_id, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Assuming data is a list of dictionaries
    for item in data:
        if item.get('Id') == query_id:
            text = clean_topics_text(item)
            return text
    
    return "Query ID not found"



def reformat_json_file(input_filepath, output_filepath):
    # Read the JSON data from the input file
    with open(input_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Write the JSON data to the output file with indentation
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
