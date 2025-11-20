import uvicorn


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("app.app:app", host="0.0.0.0", port=8383, reload=True)
