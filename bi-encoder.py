from sentence_transformers import SentenceTransformer, util
import file_fetch


# paths to the files
topic_filepath = 'topics_1.json'
answer_filepath = 'answers.json'

# Load the model
bi_encoder = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# Get the data 
topics = file_fetch.load_json_file(topic_filepath)
answers = file_fetch.load_json_file(answer_filepath)

# Encode the data

topic_embeddings = bi_encoder.encode(list(topics.values()), convert_to_tensor=True)
answer_embeddings = bi_encoder.encode(list(answers.values()), convert_to_tensor=True)

cos_sim = util.cos_sim(topic_embeddings, answer_embeddings)


