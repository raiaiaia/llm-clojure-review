import requests
import pandas as pd
import re
from time import sleep


def build_comment_url(func):
  def wrapper(row):
    print(f'iteration {row["index"]}')
    pr_url = row['pull_request_url']
    comment_id = row['comment_id']
    pattern = r'[\w+:./-]*\/'

    base_url = re.findall(pattern, pr_url)[0]

    return func(f'{base_url}comments/{comment_id}')

  return wrapper


def get_diff_hunk(func):
  def wrapper(comment_url):
    token = '<your-gh-token>'
    headers = {
      'Authorization': 'token ' + token,
    }

    r = requests.get(comment_url, headers=headers)
    if r.status_code == 200:
      return func(r.json().get('diff_hunk'))
    else:
      print(f'{comment_url} - {r.status_code}')
      return func({'status_code': r.status_code, 'url': comment_url})

  return wrapper


def remove_line_range(func):
  def wrapper(diff_hunk):
    pattern = r'@@.*?@@'
    return func(re.sub(pattern, '', diff_hunk) + '\n')

  return wrapper


def filter_only_added_lines(func):
  def wrapper(diff_hunk):
    pattern = r'\+(.*?)\n'
    lines = re.findall(pattern, diff_hunk, re.MULTILINE)

    return func('\n'.join(lines))

  return wrapper


@build_comment_url
@get_diff_hunk
@remove_line_range
@filter_only_added_lines
def clean_comments(diff_hunk):
  if isinstance(diff_hunk, str):
    pattern = r'(\""".*?\"""|\'\'\'.*?\'\'\'|"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|/\*[\s\S]*?\*/|//.*?$)'
    return re.sub(pattern, '', diff_hunk)
  else:
    return diff_hunk


def main():
  df = pd.read_csv('./data/prs_comments_u.csv').reset_index()
  df['cleaned_diff_hunk'] = df.apply(clean_comments, axis=1)
  df.to_csv('./output/cleaned_data_3.csv', index=False)


if __name__ == '__main__':
  main()
