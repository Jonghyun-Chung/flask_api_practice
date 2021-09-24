from flask import Flask, request, jsonify, make_response
from functools import lru_cache
import json

app = Flask(__name__)

"""
comma_separtaed_params_to_list splits string when comma occurs and append splitted tokens to a list
input_str: input string
Returns: a list of tokens separated by commas
"""


def comma_separated_params_to_list(input_str: str) -> list:
    result = []
    for val in input_str.split(','):
        if val:
            result.append(val)
    return result


@app.route('/api/ping')
def get_ping():
    return make_response(jsonify({'success': True}), 200)


class Posts:
    JSON_FIlE = "data.json"

    @classmethod
    @lru_cache()
    def load(cls):
        with open(cls.JSON_FIlE, "r") as postsFile:
            return json.load(postsFile).get("posts", [])

    @classmethod
    def write(cls, posts: list):
        with open(cls.JSON_FIlE, "w") as postsFile:
            json.dump({"posts": posts}, postsFile, indent=2)

    @classmethod
    def get_by_id(cls, posts: list, post_id: str):
        return next(filter(lambda pos: pos.get("id") == post_id, posts), None)

    @classmethod
    def get_by_tag(cls, posts: list, post_tags: list) -> list:
        ret = []
        for post in posts:
            for tag in post_tags:
                if tag in post.get("tags"):
                    # print(post.get("id"), tag, ret)
                    ret.append(post)
                    break
        return ret

    @classmethod
    def sort_by_param(cls, posts: list, param: str, reverse: bool) -> list:
        return sorted(posts, key=lambda k: k[param], reverse=reverse)



@app.route('/api/posts', methods=['GET', 'POST'])
def get_post_posts():
    if request.method == "POST":
        print("POST")
        data = request.get_json()
        posts = Posts.load()
        existing_post = Posts.get_by_id(posts, data.get("id"))

        if existing_post:
            return {"error": "Post with same id already exists"}, 400

        posts.append(data)
        Posts.write(posts)
        return "", 201

    if request.method == "GET":
        print("GET")
        response = {}
        post_tag = request.args.getlist('tags') or request.form.getlist('tags')

        if len(post_tag) == 1 and ',' in post_tag[0]:
            post_tag = comma_separated_params_to_list(post_tag[0])

        sort_by = request.args.get('sortBy', default="id")
        direction = request.args.get('direction', default="asc")

        if not post_tag:
            return {"error": "Tags parameter is required"}, 400

        if sort_by not in ["id", "reads", "likes", "popularity"]:
            return {"error": "sortBy parameter is invalid"}, 400

        if direction not in ["asc", "desc"]:
            return {"error": "direction parameter is invalid"}, 400

        reverse = False if direction == "asc" else True

        posts = Posts.load()
        post = Posts.get_by_tag(posts, post_tag)
        post = Posts.sort_by_param(post, sort_by, reverse)

        if post:
            response["posts"] = post
        return response
    return None


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
