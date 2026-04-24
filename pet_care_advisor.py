import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, List
# We need to import the Owner class definition from the other file
from pawpal_system import Owner
# NEW IMPORTS for TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PetCareAdvisor:
    """
    An AI assistant that provides pet care advice using Google's Gemini model,
    retrieving information from a knowledge base and injecting pet-specific context.
    """

    def __init__(self, knowledge_base_path: str, owner: Owner):
        self.knowledge_base_path = knowledge_base_path
        self.owner = owner
        # Initialize the Gemini model
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        
        # Load documents first
        self.knowledge_docs = self._load_knowledge()

        # --- NEW: Setup TF-IDF Vectorizer ---
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        if self.knowledge_docs:
            # Create a list of document contents and corresponding filenames
            self.doc_contents = list(self.knowledge_docs.values())
            self.doc_filenames = list(self.knowledge_docs.keys())
            # Fit the vectorizer on our document collection
            self.tfidf_matrix = self.vectorizer.fit_transform(self.doc_contents)
        else:
            self.doc_contents = []
            self.doc_filenames = []
            self.tfidf_matrix = None

    def _load_knowledge(self) -> Dict[str, str]:
        """Loads the content of all .txt files from all knowledge base paths."""
        docs = {}
        # The knowledge_base_path can now be a list of paths
        paths = self.knowledge_base_path if isinstance(self.knowledge_base_path, list) else [self.knowledge_base_path]
        
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
            
            for filename in os.listdir(path):
                if filename.endswith(".txt"):
                    filepath = os.path.join(path, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        docs[filename] = f.read()
        return docs

    def _retrieve_context(self, question: str) -> (str, List[str]):
        """
        Retrieves context from the knowledge base using TF-IDF similarity
        and injects pet-specific information.
        """
        question_lower = question.lower()
        retrieved_texts = []
        source_files = []

        # --- NEW: TF-IDF based retrieval ---
        if self.tfidf_matrix is not None and self.doc_contents:
            # Transform the user's question into a TF-IDF vector
            question_vector = self.vectorizer.transform([question_lower])
            
            # Calculate the cosine similarity between the question and all documents
            cosine_similarities = cosine_similarity(question_vector, self.tfidf_matrix).flatten()
            
            # Get the indices of the top 2 most relevant documents
            # We use argpartition to be efficient, getting the top 2 without a full sort
            top_doc_indices = np.argpartition(cosine_similarities, -2)[-2:]
            
            # Add the most relevant documents to the context if their score is > 0
            for i in top_doc_indices:
                if cosine_similarities[i] > 0.0: # Only include if there's some relevance
                    retrieved_texts.append(self.doc_contents[i])
                    source_files.append(self.doc_filenames[i])

        # 2. Pet-specific context injection (remains the same)
        for pet in self.owner.pets:
            if f" {pet.name.lower()} " in f" {question_lower} ":
                pet_info = (
                    f"Here is information about the pet being discussed: "
                    f"Name: {pet.name}, Breed: {pet.breed}, Age: {pet.age}. "
                    f"Additional Info: {pet.general_info}"
                )
                retrieved_texts.insert(0, pet_info)

        return "\n---\n".join(retrieved_texts), list(set(source_files))
    def ask(self, question: str) -> Dict:
        """
        Asks a question, retrieves context, and generates an answer using the Gemini LLM.
        """
        context, sources = self._retrieve_context(question)

        if not context:
            final_prompt = (
                "You are a helpful pet care assistant. Please answer the following question based on your general knowledge.\n"
                f"Question: {question}\n"
                "Answer:"
            )
        else:
            final_prompt = (
                "You are a friendly and knowledgeable pet care expert. Your goal is to provide a helpful, conversational answer to the user's question. "
                "Use the information from the 'CONTEXT' section below to form your answer. "
                "Do not simply copy the text. Instead, synthesize the key points and present them in a natural, easy-to-understand way. "
                "Address the user and their pet directly if their names are known.\n\n"
                "If the context does not contain the answer, state that you don't have specific information on that topic and recommend consulting a veterinarian or uploading a relevant file.\n\n"
                "--- CONTEXT ---\n"
                f"{context}\n"
                "--- END CONTEXT ---\n\n"
                f"Question: {question}\n"
                "Answer:"
            )
        try:
            # Use .invoke() for the chat model
            response = self.llm.invoke(final_prompt)
            return {
                "answer": response.content,
                "source_documents": sources
            }
        except Exception as e:
            return {"error": f"An error occurred while querying the Gemini model: {e}"}
