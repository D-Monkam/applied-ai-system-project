import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, List
# We need to import the Owner class definition from the other file
from pawpal_system import Owner

class PetCareAdvisor:
    """
    An AI assistant that provides pet care advice using Google's Gemini model,
    retrieving information from a knowledge base and injecting pet-specific context.
    """

    def __init__(self, knowledge_base_path: str, owner: Owner):
        self.knowledge_base_path = knowledge_base_path
        self.owner = owner
        # Initialize the Gemini model
        # This requires the GOOGLE_API_KEY environment variable to be set
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
        self.knowledge_docs = self._load_knowledge()

    def _load_knowledge(self) -> Dict[str, str]:
        """Loads the content of all .txt files in the knowledge base."""
        docs = {}
        if not os.path.exists(self.knowledge_base_path):
            os.makedirs(self.knowledge_base_path)
        
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.knowledge_base_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    docs[filename] = f.read()
        return docs

    def _retrieve_context(self, question: str) -> (str, List[str]):
        """
        Retrieves context from the knowledge base using keyword matching
        and injects pet-specific information.
        """
        question_lower = question.lower()
        retrieved_texts = []
        source_files = []

        # 1. Keyword-based retrieval from knowledge base
        for filename, content in self.knowledge_docs.items():
            if any(word in content.lower() for word in question_lower.split()):
                retrieved_texts.append(content)
                source_files.append(filename)

        # 2. Pet-specific context injection
        for pet in self.owner.pets:
            if pet.name.lower() in question_lower:
                pet_info = (
                    f"Here is information about the pet being discussed: "
                    f"Name: {pet.name}, Breed: {pet.breed}, Age: {pet.age}."
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
                "You are a helpful pet care assistant. Use the following context to answer the question. "
                "If the context doesn't contain the answer, say you don't have enough information.\n\n"
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
