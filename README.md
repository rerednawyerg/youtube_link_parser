# YouTube Link Parser
Script to query YouTube API and parse the results

## Setup

```
python3 -m venv env
source env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Run

```bash
./query_youtube_api.py
```

## Output

Script will output two files:
  - yt_api_verbose.txt
    - A text file containing video URL, channel ID, channel title, video description, and any associated URLs extracted
  - expanded_links.txt
    - A text file containing all links, with shortened URL expansion performed. Also includes functionality to parse all links from telegra.ph sites.
  
