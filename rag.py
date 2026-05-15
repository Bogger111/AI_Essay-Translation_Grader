import os

def load_knowledge():
    base_path = 'knowledge_base'
    texts = []

    for filename in os.listdir(base_path):
        file_path = os.path.join(base_path,filename)

        with open(file_path,'r',encoding='utf-8') as f:
            texts.append(f.read())

    return '\n\n'.join(texts)

def retrieve_knowledge(query):
    knowledge = load_knowledge()
    return knowledge