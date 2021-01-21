# CSMA
Project repository for the "Critical Social Media Analysis" seminar on FU Berlin in winter semester 20/21.

# How to
## Set up prerequisites and credentials
Follow the Google's Python Quickstart Guide [here](https://developers.google.com/youtube/v3/quickstart/python)

- Create and download your client_secret.json and paste it under `youtube_api/config/secrets.json`
- Make sure the json file containing the secrets is names `secrets.json`
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
                 [-query QUERY] [-max_results MAX_RESULTS]
                 [-related_to RELATED_TO] [--export]

Find YouTube videos.

optional arguments:
  -h, --help            show this help message and exit
  -sort_by {date,rating,relevance,title,videoCount,viewCounts}
                        The order parameter specifies the method that will be
                        used to order resources in the API response. The
                        default value is relevance.
  -query QUERY          The q parameter specifies the query term to search
                        for.
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

- Run the script with `python3 -query 'global warming'` to search for global warming related videos
- Click on the url provided by Google and authorize the application
- Copy the code from the browser and past it into the application