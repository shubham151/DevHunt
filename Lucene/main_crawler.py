import sys
import praw
import json
import time
import os

output_file_path = "reddit_posts.json"
def is_file_size_under_limit(file_path, limit):
    #Check if the file size is under a specific limit.
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
        print(f"Current file size: {file_size:.2f} MB") 
        return file_size < limit
    return True  

def initialize_reddit():
    #Initialize the Reddit instance.
    reddit = praw.Reddit(client_id='YcksQt_ndZA_AhGIaCMF8g',
                         client_secret='ukz9yiZs2iyYjxdk4y3VBU0rvD4yKw',
                         user_agent='spydermines')
    return reddit

def open_or_create_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

def append_to_json_file(data, file_path):
    with open(file_path, 'r+') as file:
        file.seek(0, os.SEEK_END)
        position = file.tell() - 1
        while position >= 0:
            file.seek(position)
            if file.read(1) == "]":
                file.seek(position)
                if position != 0:
                    file.write(',')
                else:
                    file.write(' ')  # Avoid syntax error in empty file
                break
            position -= 1
        json.dump(data, file)
        file.write(']')

def fetch_and_append_posts(subreddit, output_file_path, limit_fs):
    #Fetch and append reddit posts
    for post in subreddit.hot(limit=None): 
        post_dict = {
            "Title": post.title,
            "Score": post.score,
            "URL": post.url,
            "CreatedAt": post.created_utc,
            "Full Content": post.selftext,
            "CntComments": post.num_comments,
            "Comments": []
        }

        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comment_dict = {
                "Comment": comment.body,
                "Score": comment.score,
                "Replies": []
            }

            for reply in comment.replies:
                reply_dict = {
                    "Reply": reply.body,
                    "Reply Score": reply.score
                }
                comment_dict["Replies"].append(reply_dict)
            
            post_dict["Comments"].append(comment_dict)

        append_to_json_file(post_dict, output_file_path)
        
        if not is_file_size_under_limit(output_file_path, limit_fs):
            print("File size limit reached. Stopping.")
            break

        time.sleep(1)

def main():
    if len(sys.argv) > 2:
        i_path = sys.argv[1]
        subreddit_name = sys.argv[2]
        print(f"Subreddit name: {subreddit_name}")

        output_file_path = i_path+"reddit_posts.json"

        reddit = initialize_reddit()
        subreddit = reddit.subreddit(subreddit_name)
        open_or_create_json_file(output_file_path)
        fetch_and_append_posts(subreddit, output_file_path, limit_fs=500)

        print(f"Data has been written to: {output_file_path}")
    else:
        print("No subreddit name provided.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

