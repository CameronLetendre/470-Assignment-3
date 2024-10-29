from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder('cross-encoder/nli-deberta-v3-base')
tuned_cross_encoder = CrossEncoder('output/cross-encoder')