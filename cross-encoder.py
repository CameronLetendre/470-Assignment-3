from sentence_transformers import CrossEncoder
import file_fetch
import os
import json

formatted_top_100_results_path = 'formatted_top_100_results.json'
top_100_results_path = 'top_100_results.json'

if not os.path.exists('formatted_top_100_results.json'):
    file_fetch.reformat_json_file(top_100_results_path, formatted_top_100_results_path)

get_100_queries = file_fetch.get_100_queries(top_100_results_path)

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

re_ranked = {}

for query_id, query_data in get_100_queries.items():
    query_text = query_data['query_text']
    answers = query_data['answers']
    scores = cross_encoder.predict([(query_text, answer['text']) for answer in answers])
    scored_answers = [{
        'answer_id': answers[i]['answer_id'],
        'text': answers[i]['text'],
        'score': float(scores[i])
    } for i in range(len(answers))]
    re_ranked[query_id] = {
        'query_text': query_text,
        'answers': sorted(scored_answers, key=lambda x: x['score'], reverse=True)
    }
    break


# Save re_ranked dictionary to a JSON file
with open('re_ranked_results.json', 'w') as json_file:
    json.dump(re_ranked, json_file, indent=4)

print("Re-ranked results have been saved to 're_ranked_results.json'")
print(re_ranked)



