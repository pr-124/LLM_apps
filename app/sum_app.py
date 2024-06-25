import chainlit as cl
import openai
import PyPDF2


def text_from_pdf(path):
    reader = PyPDF2.PdfFileReader(path)
    text = ""
    for page in range(reader.numPages):
        page_con = reader.getPage(page)
        text += page_con.extract_text()
    return text


async def summarize_text(text):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"},
        ],
        max_tokens=200,
        temperature=0.5,
    )
    return response.choices[0].message["content"].strip()


async def chat_with_gpt(prompt):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()


@cl.on_message
async def main(message: cl.Message):
    if message.content.startswith("summarize pdf "):
        pdf_path = message.content[len("summarize pdf ") :].strip()
        try:
            text = text_from_pdf(pdf_path)
            summary = await summarize_text(text)
            await cl.Message(summary).send()
        except Exception as e:
            await cl.Message(f"Error summarizing PDF: {e}").send()
    else:
        response = await chat_with_gpt(message.content)
        await cl.Message(response).send()
