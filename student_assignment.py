import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import (ResponseSchema, StructuredOutputParser)

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):
    llm = AzureChatOpenAI(
        model=gpt_config['model_name'],
        deployment_name=gpt_config['deployment_name'],
        openai_api_key=gpt_config['api_key'],
        openai_api_version=gpt_config['api_version'],
        azure_endpoint=gpt_config['api_base'],
        temperature=gpt_config['temperature']
    )

    response_schemas = [
        ResponseSchema(
            name="date",
            description="該紀念日的日期",
            type="YYYY-MM-DD"),
        ResponseSchema(
            name="name",
            description="該紀念日的名稱")
    ]
    output_parser = StructuredOutputParser(response_schemas=response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_messages([
        ("system","使用台灣語言並回答問題，答案請以JSON格式的list清單,{format_instructions}"),
        ("human","{question}")])
    prompt = prompt.partial(format_instructions=format_instructions)
    response = llm.invoke(prompt.format(question=question)).content
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = "{ \"Result\":" + response + "}"
    return response
    
def generate_hw02(question):
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
def demo(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    
    return response

print(generate_hw01("2024年台灣10月紀念日有哪些?"))