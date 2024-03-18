import subprocess
import time
import sys

i_path="./"
if len(sys.argv) > 1:
        i_path = sys.argv[1]
print(i_path)

script = 'main_crawler.py'

# Open the file containing the list of subreddits
with open(i_path+"subreddits.txt", "r") as file:
    
    for subreddit_name in file:
        
        subreddit_name = subreddit_name.strip()
        print(f'Crawling Subreddit: {subreddit_name}')

        command = ['python3', i_path+script,i_path, subreddit_name]

        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Output:", result.stdout)
            if result.stderr:
                print("Error:", result.stderr)
            time.sleep(60)
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")

