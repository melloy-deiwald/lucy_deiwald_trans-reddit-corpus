import json, sys
from datetime import datetime

TIME_FORMAT='%Y-%m-%d %H:%M:%S'

field = "subreddit"
values = ["trans", "mtf", "ftm", "NonBinary", "truscum", "transgender"]
#!!!!!!
location = ""
#!!!!!!
year = sys.argv[1] + "/"

posts = {
    "trans": [],
    "MtF": [],
    "ftm": [],
    "NonBinary": [],
    "truscum": [],
    "transgender": []
}

unfiltered_data = []

for month in range(12):
    month_string = str(month+1) + ".json"
    if month < 9: month_string = "0" + month_string
    try:
        with open(location+year+month_string, 'r') as raw_data:
            unfiltered_data = json.load(raw_data)
        raw_data.close()
        submission_index = 0
        for submission in unfiltered_data["data"]:
            if submission["is_self"] or not submission["is_self"]:
                timestamp = datetime.utcfromtimestamp(submission["created_utc"]).strftime(TIME_FORMAT)
                date = str(datetime.strptime(timestamp, TIME_FORMAT))
                submission_data = {
                    "title": submission["title"],
                    "text": submission["selftext"],
                    "date": date,
                    "subreddit": submission["subreddit"],
                    "permalink": submission["permalink"],
                    "author": submission["author"],
                    "reference": submission_index
                }
                posts[submission_data["subreddit"]].append(submission_data)
                submission_index += 1
    except: print("File for month " + str(month+1) + " not found.")

for subreddit in posts:
    with open(location+year+"subreddit_view/"+subreddit+".json", 'w') as file:
        json.dump(posts[subreddit], file)
    file.close()