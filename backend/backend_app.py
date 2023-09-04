from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    # Function to implement the validation of json data.
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Function to implement Get opoeration.
    return jsonify(POSTS)


@app.route('/api/posts', methods=["POST"])
def add_post():
    # Function to  implement the add post in POSTS.
    post = {}
    post = request.get_json()
    post["id"] = max([pos["id"] for pos in POSTS]) + 1
    if not validate_post_data(post):
        return jsonify({"error": "Invalid blog data"}), 400
    POSTS.append(post)
    return jsonify(post), 201


def find_blog_by_id(post_id):
    """ Find the post with the id `post_id`.
      If there is no post with this id, return None. """
    # TODO: implement this
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Function to implement the Delete in POSTS.

    post = find_blog_by_id(int(id))
    if post is None:
        return 'message: post not found', 404

    # TODO: implement this
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}, post)


@app.route('/api/posts/<int:id>', methods=['PUT'])
def handle_post(id):
    """Function to implement the Updation of data in
       particular post in POSTS. """

    post = find_blog_by_id(id)
    if post is None:
        return 'message: post not found', 404

    new_data = request.get_json()
    if not validate_post_data(new_data):
        return jsonify({"error": "Invalid post data"}), 400
    post.update(new_data)

    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def handle_posts_query():
    """Function to implement the Searching the post by
       its title or content keywords . """

    title = request.args.get('title')
    content = request.args.get('content')

    if title:
        filtered_posts = [post for post in POSTS if
                          str(title) in post.get('title') or str(content) in post.get('content')]
        return jsonify(filtered_posts)
    else:
        return jsonify(POSTS)


@app.route('/api/posts/sorting', methods=['GET'])
def handle_post_sorting():
    """Function to implement the sorting on the basis of title
      and content in ascending and descending order. """

    sort = request.args.get('sort')
    direction = request.args.get('direction')
    titles_list = [post["title"] for post in POSTS]
    content_list = [post["content"] for post in POSTS]

    sorted_title_descending = sorted(POSTS, key=lambda pair: pair["title"], reverse=True)
    sorted_content_descending = sorted(POSTS, key=lambda pair: pair["content"], reverse=True)

    sorted_title_ascending = sorted(POSTS, key=lambda pair: pair["title"])
    sorted_content_ascending = sorted(POSTS, key=lambda pair: pair["content"])

    if sort == "title" and direction == "asc":
        return jsonify(sorted_title_ascending)
    elif sort == "title" and direction == "desc":
        return jsonify(sorted_content_descending)
    elif sort == "content" and direction == "asc":
        return jsonify(sorted_content_ascending)
    elif sort == "content" and direction == "desc":
        return jsonify(sorted_content_descending)


@app.route('/api/posts/pagination', methods=['GET'])
def handle_blogs():
    """ Function to implement Pagination """

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_posts = POSTS[start_index:end_index]
    return jsonify(paginated_posts)


@app.errorhandler(404)
def not_found_error(error):
    """Function to implement 404 error handling. """
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
