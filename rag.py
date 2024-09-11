from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os
import sys

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def clean_text(text):
    # 替换文本中的换行符
    text = text.replace('\n', ' ')
    # 可能还需要替换其他特殊字符，比如多余的空格
    text = ' '.join(text.split())
    return text

def load_sanming():
    sanming_path = "/home/zhangjiajun/fozu/shellchat/knowledge/三命通会.pdf"
    loader = PyMuPDFLoader(sanming_path)
    sanming = loader.load()
    sanming = [clean_text(document.page_content) for document in sanming]
    sanming_str = ''.join(sanming)
    return sanming_str



class SuppressOutput:
    def __enter__(self):
        # 替换标准输出和标准错误
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        # 打开一个使用os.devnull的文件，所有写入操作将被丢弃
        self._devnull = open(os.devnull, 'w')
        sys.stdout = self._devnull
        sys.stderr = self._devnull

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 恢复标准输出和标准错误到原始状态
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        self._devnull.close()

def build_db():
    #loader = DirectoryLoader('../', glob="**/*.pdf")
    knowledge_dir = "/home/zhangjiajun/fozu/shellchat/knowledge"
    documents = []
    for dirpath, dirnames, filenames in os.walk(knowledge_dir):
        for filename in filenames:
            loader = PyMuPDFLoader(os.path.join(dirpath, filename))
            documents.extend(loader.load())
   
    # loader = TextLoader("./yijing.txt")
    # documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    with SuppressOutput():
        documents = text_splitter.split_documents(documents)
    # print("doc1",type(documents),type(documents[0]))
    # for doc in documents:
    #     print("="*50)
    #     print(len(doc.page_content),":")
   
    #print(documents)

    model_name = "moka-ai/m3e-base"
    model_kwargs = {'device': 'cuda:5'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding = HuggingFaceBgeEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs=encode_kwargs,
                    query_instruction="为文本生成向量表示用于文本检索"
                )

    db = Chroma.from_documents(documents, embedding)
    print(len(documents))
    # for index, doc in enumerate(documents):
    #     print(index ,doc.page_content)

    return db

def rag(massage, db):
    # similarity search
    results = db.similarity_search(massage, k=2) # topk=1
    # print(len(result[0].dict()['page_content']))
    #print(result)
    #rint(result[0].dict()['page_content'])
    result_list = [result.dict()["page_content"] for result in results]
    #return result[0].dict()['page_content']
    return result_list

def build_sanming():
    # sanming_path = "/home/zhangjiajun/fozu/shellchat/knowledge/三命通会.pdf"
    # sanming = extract_text_from_pdf(sanming_path)
    # documents = Document(page_content=sanming, meta={"source": "PDF"})
    # documents = [documents]

    loader = PyMuPDFLoader("/home/zhangjiajun/fozu/shellchat/三命通会-11-30.pdf")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    for i, doc in enumerate(documents):
        cleaned_text = clean_text(doc.page_content)
        documents[i].page_content = cleaned_text
    with SuppressOutput():
        documents = text_splitter.split_documents(documents)
    # print("doc2",type(documents),type(documents[0]),)
    sum = 0
    for doc in documents:
        print("="*50)
        print(len(doc.page_content),":")
        sum += len(doc.page_content)
    print(sum)
   

    model_name = "moka-ai/m3e-base"
    model_kwargs = {'device': 'cuda:5'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding = HuggingFaceBgeEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs=encode_kwargs,
                    query_instruction="为文本生成向量表示用于文本检索"
                )

    db = Chroma.from_documents(documents, embedding)

    return db

def rag_baoshi(massage):
    db = build_sanming()
    results = db.similarity_search(massage, k=3) # topk=1
    result_list = [result.dict()["page_content"] for result in results]
  
    return result_list


if __name__ == '__main__':
    # result = rag("哈哈哈哈哈哈", build_db())
    # print(result)
    db = build_db()