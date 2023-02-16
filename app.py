from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/api/data')
def get_data():
    data = {"name": "John", "age": 30, "city": "New York"}
    return data


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
