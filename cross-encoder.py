from sentence_transformers import CrossEncoder
import file_fetch
import os

formatted_top_100_results_path = 'formatted_top_100_results.json'
top_100_results_path = 'top_100_results.json'

if not os.path.exists('formatted_top_100_results.json'):
    file_fetch.reformat_json_file()

get_100_queries = file_fetch.get_100_queries(top_100_results_path)

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

re_ranked = {}

