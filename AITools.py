import os
import uuid
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks import LangChainTracer
from openai import OpenAI

class AITools(object):
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL")
        self.session_id = None
        self.store = {}
        with open("./resources/prompts.json", "r") as file:
            self.prompts = json.load(file)

    def get_session_history(self) -> InMemoryChatMessageHistory:
        if self.session_id not in self.store:
            print(f"Creating new session history for {self.session_id}")
            self.store[self.session_id] = InMemoryChatMessageHistory()
        return self.store[self.session_id]


    def chat_call(
        self, 
        prompt, 
        schema = None,
        history = True,
        new_history = False
    ):
        tracer = LangChainTracer(project_name="AI-Adevnetures")
        callback_manager = CallbackManager([tracer])

        llm = ChatOpenAI(api_key=self.OPENAI_API_KEY, model_name=self.OPENAI_MODEL, callback_manager=callback_manager)

        if schema:
            llm = llm.with_structured_output(schema)

        if history:
            if new_history:
                self.store = {}

            if self.session_id:
                # Use history for repeated conversations
                chat_prompt = ChatPromptTemplate.from_messages([
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}")
                ])
            else:
                self.session_id = str(uuid.uuid4())
                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", "{role}"),
                    ("human", "{input}")
                ])
            session_id = self.session_id

            chain = chat_prompt | llm

            chain_with_history = RunnableWithMessageHistory(
                chain, 
                lambda: self.get_session_history(),
                role_messages_key="role",
                input_messages_key="input",
                history_messages_key="history",
                callback_manager=callback_manager
                )
            
            response = chain_with_history.invoke(
                {"role": self.prompts["chatbot"],
                 "input": prompt},
                config={"configurable": {"session_id": session_id}}
            )
            history = self.get_session_history()
            history.add_user_message(prompt)
            history.add_ai_message(str(response))
        else:
            response = llm.invoke(prompt)

        return response
    
    def image_call(
        self,
        informations
    ):
        # Initialisiere OpenAI-Client für die Bildgenerierung
        client = OpenAI(api_key=self.OPENAI_API_KEY)

        # Liste für die Rückgabe der Themen mit Bild-URLs
        data = []
        for info in informations:
            title = info["title"]
            description = info["description"]
            # Generiere das Bild basierend auf dem Thema
            prompt=self.prompts["image"].format(title=title, description=description)

            while True:
                try: 
                    theme_image = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    break
                except Exception as e:
                    print("recreating image with new prompt")
                    prompt = self.chat_call(self.prompts["rewrite_prompt"], history=False)

            data.append(theme_image.data[0].url)

        return data