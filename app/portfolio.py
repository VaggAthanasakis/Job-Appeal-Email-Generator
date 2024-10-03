import pandas as pd
import chromadb
import uuid
import pdfplumber
import os

current_dir = os.path.dirname(__file__)
resource_dir = os.path.join(current_dir, '..', 'resource')

class Portfolio:
    def __init__(self,portfolio_file_path = os.path.join(resource_dir,'Vaggelis_portfolio.csv'), cv_file = os.path.join(resource_dir,'CV.pdf')): 
        self.file_path = portfolio_file_path
        self.data = pd.read_csv(portfolio_file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        self.cv_file = cv_file

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                #print(row["Links"])
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self,skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
    
    def insert_cv(self):
        with pdfplumber.open(self.cv_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text()
        return full_text