from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_community.chat_message_histories import ChatMessageHistory
from pirate_speak.chain import chain as benefits_chat_chain

app = FastAPI()
benefits_history = ChatMessageHistory()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.post('/benefits-api')
async def continue_conversation(text : str = Body(..., embed=True)):
    benefits_history.add_user_message(text)
    AI_response = benefits_chat_chain.invoke({"text": text})
    benefits_history.add_ai_message(AI_response)
    return AI_response

@app.delete('/benefits-api')
async def clear_conversation():
    benefits_history.clear()
    return


# Edit this to add the chain you want to add
add_routes(app, benefits_chat_chain, path="/benefits-api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
