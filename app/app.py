import chainlit as cl


# Decorator to Handle Incoming Messages
@cl.on_message
# whenever chainlit receives this message main function is called.
async def main(message: cl.Message):
    # Log the received message for debugging purposes
    print(f"Received message: {message.content}")
    # echoing back the ocntent of the message back to the user. this completes the scaffold.
    await cl.Message(message.content).send()

    # Log the response has been sent
    print(f"Sent message: {message.content}")
