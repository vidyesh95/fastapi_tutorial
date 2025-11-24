from fastapi import FastAPI, HTTPException, status

app = FastAPI()

text_posts = {1: {"title":"New Post", "content":  "cool test post"}}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in text_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    return text_posts.get(post_id)

