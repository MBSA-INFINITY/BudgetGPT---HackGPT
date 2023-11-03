import os
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

llm = OpenAI(openai_api_key=OPENAI_API_KEY)


template = """
I am the subject. If this statement "{statement}" is a transaction and
If the statement has multiple transaction return me a list of JSON in which each JSON object will be a single transaction. JSON will be in the following format:-
JSON(
"cumulative_transaction_amount" :

"cumulative_transaction_reason" : 
"type" : was this a credit to bank or a debit from my bank account
)
Do remember that if I borrow money that is a credit to my bank account and if someone borrows from me thats a debit from  my account.
"""
prompt = PromptTemplate(template=template, input_variables=["statement"])

llm_chain = LLMChain(prompt=prompt, llm=llm)
