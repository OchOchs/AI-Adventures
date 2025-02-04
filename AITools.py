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
from openai import OpenAI

class AITools(object):
    """ A class to handle the interaction with the OpenAI API """
    def __init__(self):
        """ Initialize the class with the OpenAI API key and the model name """
        # Load the OpenAI API key and model name from the .env file
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL")
        self.session_id = None
        self.store = {}
        with open("./resources/prompts.json", "r") as file:
            self.prompts = json.load(file)

    def get_session_history(self) -> InMemoryChatMessageHistory:
        """ Get the chat history for the current session """
        # Create a new session history if it doesn't exist
        if self.session_id not in self.store:
            print(f"Creating new session history")
            self.store[self.session_id] = InMemoryChatMessageHistory()
        return self.store[self.session_id]


    def chat_call(
        self, 
        prompt, 
        schema = None,
        history = True,
        new_history = False
    ):
        """ Call the OpenAI API with the given prompt """
        # Create a new instance of the ChatOpenAI class
        llm = ChatOpenAI(api_key=self.OPENAI_API_KEY, model_name=self.OPENAI_MODEL)

        # Set the schema for the structured output
        if schema:
            llm = llm.with_structured_output(schema)

        # Get the chat history for the current session
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

            # Create a chain of runnables to handle the chat prompt
            chain = chat_prompt | llm

            chain_with_history = RunnableWithMessageHistory(
                chain, 
                lambda: self.get_session_history(),
                role_messages_key="role",
                input_messages_key="input",
                history_messages_key="history"
                )
            
            # Invoke the chain with the chat prompt and add history
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
        """ Call the OpenAI API to generate images based on the given prompt """
        # Create a new instance of the OpenAI class
        client = OpenAI(api_key=self.OPENAI_API_KEY)

        # Generate images based on the given prompt for each information
        data = []
        for info in informations:
            title = info["title"]
            description = info["description"]
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