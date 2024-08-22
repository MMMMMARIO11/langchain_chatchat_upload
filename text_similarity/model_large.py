from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

semantic_cls = pipeline(Tasks.sentence_similarity, model=r'\text_similarity\model_large\iic\nlp_structbert_sentence-similarity_chinese-large')
input=('英雄联盟什么英雄最好', '英雄联盟最好英雄是什么')
semantic_cls(input)
print(semantic_cls(input))