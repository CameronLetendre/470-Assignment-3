from sentence_transformers import CrossEncoder
import file_fetch

top_100_results_path = 'top_100_results.json'

cross_encoder = CrossEncoder('cross-encoder/nli-deberta-v3-base')

topics = file_fetch.load_json_file(top_100_results_path)

