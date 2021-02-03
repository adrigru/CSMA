# CSMA
Project repository for the "Critical Social Media Analysis" seminar on FU Berlin in winter semester 20/21.

# How to
## Set up prerequisites and credentials
Follow the Google's Python Quickstart Guide [here](https://developers.google.com/youtube/v3/quickstart/python)

- Create an API_KEY within the Google developer console https://console.developers.google.com/
- Create a python virtual environment by running `python3 -m venv venv`
- Make sure you use the virtual environment by running `source venv/bin/activate`
- Install the necessary dependencies `pip3 install -r requirements.txt`

## Use
- Head ove to the youtube_api by running `cd youtube_api`
- Make sure you use the virtual environment by running `source venv/bin/activate`
- Run the script with `python3 search.py -h` to see help
```
usage: search.py [-h]
                 [-sort_by {date,rating,relevance,title,videoCount,viewCounts}]
                 [-max_results MAX_RESULTS] [-related_to RELATED_TO]
                 [--export]
                 api_key query

Find YouTube videos.

positional arguments:
  api_key               YouTube API is required. Check:
                        https://console.developers.google.com/
  query                 The q parameter specifies the query term to search
                        for.

optional arguments:
  -h, --help            show this help message and exit
  -sort_by {date,rating,relevance,title,videoCount,viewCounts}
                        The order parameter specifies the method that will be
                        used to order resources in the API response. The
                        default value is relevance.
  -max_results MAX_RESULTS
                        The maxResults parameter specifies the maximum number
                        of items that should be returned in the result set.
                        Acceptable values are 0 to 50, inclusive. The default
                        value is 25.
  -related_to RELATED_TO
                        The relatedToVideoId parameter retrieves a list of
                        videos that are related to the video that the
                        parameter value identifies.
  --export              The export parameter specifies if the results should
                        be exported as .csv file
```

## Example usage

- Run the script with `python3 API_KEY "chemtrails"` to search for global warming related videos
- You can export search results in to a `.csv` file with `python3 API_KEY "chemtrails" --export` 
- Look into the csv file and find a relevant video's id
- Put the videoId as an argument for `-related_to` flag, for instance `python3 API_KEY "chemtrails" -related_to=uOMRF7t5Vn0 --export`
- The script will search for 25 and allow you to select the videos you are interested in
- Be patient it might take a couple of minutes depending on number of results