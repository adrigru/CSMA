# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import argparse
import json
import os
import pprint
from datetime import datetime as dt
from io import StringIO

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']


def search(query, sort_by, max_results, related_to, _type='video'):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    api_service_name = 'youtube'
    api_version = 'v3'
    client_secrets_file = os.path.join(os.path.abspath(os.curdir), 'config/secrets.json')

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        relatedToVideoId=related_to,
        maxResults=max_results,
        order=sort_by,
        part='snippet',
        type=_type,
        q=query
    )

    response = request.execute()
    _json = json.dumps([{'videoId': v['id']['videoId'],
                         'title': v['snippet']['title'],
                         'channelTitle': v['snippet']['channelTitle'],
                         'description': v['snippet']['description'],
                         'publishTime': v['snippet']['publishTime']} for v in response['items']])

    pprint.pprint(_json)
    return _json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find YouTube videos.')
    parser.add_argument('-sort_by',
                        choices=['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCounts'],
                        default='relevance',
                        help='The order parameter specifies the method that will be used to order resources'
                             ' in the API response. The default value is relevance.')
    parser.add_argument('-query',
                        type=str,
                        default='',
                        help='The q parameter specifies the query term to search for.')
    parser.add_argument('-max_results',
                        type=int,
                        default=25,
                        help='The maxResults parameter specifies the maximum number of items that '
                             'should be returned in the result set. Acceptable values are 0 to 50,'
                             ' inclusive. The default value is 25.')
    parser.add_argument('-related_to',
                        type=str,
                        default='',
                        help='The relatedToVideoId parameter retrieves a list of videos that are related to the video'
                             ' that the parameter value identifies.')
    parser.add_argument('--export',
                        action='store_true',
                        help='The export parameter specifies if the results should be exported as .csv file')
    args = parser.parse_args()

    _json = search(args.query, args.sort_by, args.max_results, args.related_to)

    if args.export:
        df = pd.read_json(StringIO(_json), orient='records')
        filename = f'results_{"_".join(args.query.split())}_{args.sort_by}_{dt.now().isoformat()}.csv'
        df.to_csv(path_or_buf=os.path.join(f'{os.curdir}/results', filename), index=False)
