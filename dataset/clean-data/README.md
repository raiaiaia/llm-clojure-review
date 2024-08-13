## Clean Data

This script intends to clean teh diff hunks extracted from github pull requests.

To run it you need `python3` and `virtualenv`. Once you have it installed, you can run it with the following commands to create the virtual enviroment and install dependencies:

```sh
python3 -m venv venv

. ./venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt
```

You need to place a csv file with the name `prs_comments_u.csv` in teh directory `data`, and the csv must have a column `pull_request_url` and `comment_id` for the script to work.

You also need to create a `github personal access token` and place it in the function `get_diff_hunk` in order to work.

OBS: I had to run the script in three separted executions due to a limitation of the Github API that only allows 5000 requests per hour, once I had 12000 requests to make, I ran it in three parts:
from 0 to 5000, from 5001 to 10000 and from 10001 to the end.
