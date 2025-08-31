from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from kafka_consumer.consumer import consume_messages
import threading

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def start():
    consume_messages()
    return("Finish it already, you cunt!!!")
    
@app.get("/{url}")
async def read_item(url: str):
    print(url)
    # try:
    #     start_consumer(url)
    # except KeyboardInterrupt:
    #     pass
    
def main():
    thread = threading.Thread(target=consume_messages)
    thread.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8002)
    thread.join()
    # uvicorn.run("main:app", host="0.0.0.0", port=8002)

if __name__ == "__main__":
    main()