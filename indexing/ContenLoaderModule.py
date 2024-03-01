from langchain_community.document_loaders import PyPDFLoader, AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

class ContentLoader:
    @staticmethod
    def loadFile(fileType, fileURL):
        if(fileType=="PDF"):
            return ContentLoader.loadPDFFilebyPath(fileURL)
        elif(fileType=="WEBURL"):
            return ContentLoader.loadContentfromWebURL(fileURL)

    @staticmethod
    def loadPDFFilebyPath(url):
        loader = PyPDFLoader(url)
        data = loader.load_and_split()
        print(f'You have {len(data)} document(s) in your data')
        print(f'You have {len(data[0].page_content)} charachters in your sample document')
        return data
    
    @staticmethod
    def loadContentfromWebURL(url):
        #Load HTML
        # loader = AsyncChromiumLoader(["https://lilianweng.github.io/posts/2023-06-23-agent/"])
        # urls = ["https://www.ninersnation.com/2024/1/31/24057432/final-observations-from-san-francisco-49ers-34-31-win-over-detroit-lions-brock-purdy-kyle-shanahan"]
        # urls = ["https://www.wsj.com/"]
        # urls = ["https://en.wikipedia.org/wiki/Brown-headed_cowbird"]
        
        loader = AsyncHtmlLoader(url)
        docs = loader.load()
        print("loadContentfromWebURL docs ->",docs)

        #Transform using Html2TextTransformer

        html2text = Html2TextTransformer()
        docs_transformed= html2text.transform_documents(docs)

        #Result
        print(len(docs_transformed))
        print(len(docs_transformed[0].page_content[0]))
        print(docs_transformed[0].page_content)

        content = docs_transformed
        return content
