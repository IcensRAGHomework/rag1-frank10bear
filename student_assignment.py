import json
import traceback

from model_configurations import get_model_configuration

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import (ResponseSchema, StructuredOutputParser)
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain import hub

import base64
from mimetypes import guess_type

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

api_key = "0ytyPtAOKfMUoc7qzWktkswXsdkA19dg"

def get_holiday(year: int, month: int) -> int:
    
    return value

class GetHolidays(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

tool = StructuredTool.from_function(
    name="get_holiday",
    description="",
    func=get_holiday,
    args_schema=GetHolidays,
)

def generate_hw02(question):
    pass
    # llm = AzureChatOpenAI(
    #     model=gpt_config['model_name'],
    #     deployment_name=gpt_config['deployment_name'],
    #     openai_api_key=gpt_config['api_key'],
    #     openai_api_version=gpt_config['api_version'],
    #     azure_endpoint=gpt_config['api_base'],
    #     temperature=gpt_config['temperature']
    # )

    # tool = StructuredTool.from_function(
    # name="get_value",
    # description="Calculate a 🦜 b",
    # func=get_value,
    # args_schema=GetValue,
    # )

    # prompt = hub.pull("hwchase17/openai-functions-agent")
    # print(prompt.messages)

    # tools = [tool]
    # agent = create_openai_functions_agent(llm, tools, prompt)
    # agent_executor = AgentExecutor(agent=agent, tools=tools)
    # response = agent_executor.invoke({"input": "2 🦜 9"}).get('output')
    # return response
    
def generate_hw03(question2, question3):
    pass
    
# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def generate_hw04(question):
    llm = AzureChatOpenAI(
        model=gpt_config['model_name'],
        deployment_name=gpt_config['deployment_name'],
        openai_api_key=gpt_config['api_key'],
        openai_api_version=gpt_config['api_version'],
        azure_endpoint=gpt_config['api_base'],
        temperature=gpt_config['temperature']
    )

    image_path = 'baseball.png'
    data_url = local_image_to_data_url(image_path)

    response_schemas = [
        ResponseSchema(
            name="score",
            description="該隊伍的積分",
            type="integer"),
    ]
    output_parser = StructuredOutputParser(response_schemas=response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "辨識圖片中的文字表格,使用台灣語言並回答問題，答案請以JSON格式的list清單,{format_instructions}"),
                (
                    "user",
                    [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_url},
                        }
                    ],
                ),
                ("human", "{question}")
            ]
        )

    prompt = prompt.partial(format_instructions=format_instructions)
    response = llm.invoke(prompt.format_messages(question=question)).content
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = "{ \"Result\":" + response + "}"
    return response
    
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

#print(generate_hw02("2024年台灣10月紀念日有哪些?"))
print(generate_hw04("中華台北的積分"))