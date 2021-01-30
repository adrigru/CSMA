# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import argparse
import csv
import json
import os
import pprint
from datetime import datetime as dt
from io import StringIO

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd


def export(_dict, query):
    filename = f'comments_{"_".join(query.split())}_{dt.now().isoformat()}.csv'
    header = ['videoId', 'videoPublishedAt', 'videoTitle', 'commentId', 'replyCount', 'textOriginal',
              'authorDisplayName', 'likeCount', 'publishedAt', 'parentId']
    with open(os.path.join(f'{os.curdir}/results', filename), 'w+', newline='') as fp:
        writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for item in _dict:
            video_data = [item['videoId'], item['publishTime'], item['title']]
            if 'comments' in item:
                for c in item['comments']:
                    writer.writerow(
                        video_data + [c['commentId'], c['replyCount'], c['textOriginal'], c['authorDisplayName'],
                                      c['likeCount'], c['publishedAt'], None])
                    if 'replies' in c:
                        for r in c['replies']:
                            writer.writerow(
                                video_data + [r['replyId'], 0, r['textOriginal'],
                                              r['authorDisplayName'],
                                              r['likeCount'], r['publishedAt']])


class YouTubeAPI:
    def __init__(self, api_key):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

        # Get credentials and create an API client
        api_service_name = 'youtube'
        api_version = 'v3'
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

    def get_comments_for_vids(self, query, sort_by, max_results, related_to='', _export=False):
        videos = self.search(query, sort_by, max_results, related_to=related_to)

        for video in videos:
            comments = self.get_comments_by_vid_id(video['videoId'], sort_by, replies=True)
            if comments is not None:
                video['comments'] = comments

        if _export:
            return export(videos, query)

        return videos

    def get_comments_by_vid_id(self, video_id, sort_by, max_results=100, replies=False, _export=False):
        request = self.youtube.commentThreads().list(
            part='snippet',
            maxResults=max_results,
            moderationStatus='published',
            order=sort_by,
            videoId=video_id
        )
        try:
            response = request.execute()
            results = [{'commentId': c['id'],
                        'videoId': c['snippet']['videoId'],
                        'replyCount': c['snippet']['totalReplyCount'],
                        'textOriginal': c['snippet']['topLevelComment']['snippet']['textOriginal'],
                        'authorDisplayName': c['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'likeCount': c['snippet']['topLevelComment']['snippet']['likeCount'],
                        'publishedAt': c['snippet']['topLevelComment']['snippet']['publishedAt']} for c in
                       response['items']]

            if replies:
                for comment in results:
                    if comment['replyCount']:
                        replies = self.get_replies(max_results=100, parent_id=comment['commentId'])
                        comment['replies'] = replies

            if _export:
                return json.dumps(results)

            return results

        except Exception as e:
            print(f'An exception has occurred: {e}')

        return None

    def get_replies(self, max_results, parent_id):
        request = self.youtube.comments().list(
            part="snippet",
            maxResults=max_results,
            parentId=parent_id
        )
        response = request.execute()
        results = [{'replyId': r['id'],
                    'parentId': r['snippet']['parentId'],
                    'authorDisplayName': r['snippet']['authorDisplayName'],
                    'textOriginal': r['snippet']['textOriginal'],
                    'likeCount': r['snippet']['likeCount'],
                    'publishedAt': r['snippet']['publishedAt']} for r in response['items']]

        return results

    def search(self, query, sort_by, max_results, related_to='', _type='video', _export=False):
        if related_to is not '':
            request = self.youtube.search().list(
                relatedToVideoId=related_to,
                maxResults=max_results,
                order=sort_by,
                part='snippet',
                type=_type,
                q=query
            )
        else:
            request = self.youtube.search().list(
                maxResults=max_results,
                order=sort_by,
                part='snippet',
                type=_type,
                q=query
            )

        response = request.execute()
        results = [{'videoId': v['id']['videoId'],
                    'title': v['snippet']['title'],
                    'channelTitle': v['snippet']['channelTitle'],
                    # 'description': v['snippet']['description'],
                    'publishTime': v['snippet']['publishTime']} for v in response['items']]
        if _export:
            return json.dumps(results)

        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find YouTube videos.')
    parser.add_argument('-sort_by',
                        choices=['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCounts'],
                        default='relevance',
                        help='The order parameter specifies the method that will be used to order resources'
                             ' in the API response. The default value is relevance.')
    parser.add_argument('api_key',
                        type=str,
                        default='',
                        help='YouTube API is required. Check: https://console.developers.google.com/')
    parser.add_argument('query',
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

    ytb = YouTubeAPI(args.api_key)

    # Search for videos related to query
    _json = ytb.search(args.query, args.sort_by, args.max_results, related_to=args.related_to, _export=args.export)
    pprint.pprint(_json)

    # Export list of videos that YouTube returned for the given query
    if args.export:
        df = pd.read_json(StringIO(_json), orient='records')
        filename = f'videos_{"_".join(args.query.split())}_{args.sort_by}_{dt.now().isoformat()}.csv'
        df.to_csv(path_or_buf=os.path.join(f'{os.curdir}/results', filename), index=False)

    # Export comments to videos related to videoId specified in related_to argument
    if args.related_to:
        _json = ytb.get_comments_for_vids(args.query, args.sort_by, args.max_results, related_to=args.related_to,
                                          _export=args.export)
    # Export comments for videos related to query
    # Might return irrelevant comments
    # Better specify related_to or make sure the videos found by YouTube API is what you want
    else:
        _json = ytb.get_comments_for_vids(args.query, args.sort_by, args.max_results, related_to='',
                                          _export=args.export)
