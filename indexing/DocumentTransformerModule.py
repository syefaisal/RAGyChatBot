from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentTransformer:

    @staticmethod
    def text_splitter(data, chunk_size=1000, chunk_overlap=0):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(data)
        # print(f'Now you have {len(texts)} documents')
        # print(f'Now you have {texts} documents')

        return texts
    