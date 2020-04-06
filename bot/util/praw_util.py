import praw
import re
def reddit() -> praw.Reddit:
    """
    PRAW - Python Reddit API Wrapper
    Returns the Reddit client
    """
    return praw.Reddit(client_id='<id>',
                       client_secret='<secret>',
                       user_agent='<app name> by /u/<username>')

def multi(client, redditor, multireddit):
    return client.multireddit(redditor, multireddit)

def find(obj, term, **kwargs):
    yield from obj.search(term, **kwargs)

def sub(client, subreddit):
    return client.subreddit(subreddit)

def user(client, redditor):
    return client.redditor(redditor)

def post(client, post_id):
    if re.search(r"^https?\://", post_id):
        post_id = praw.models.Submission.id_from_url(post_id)
    return client.submission(id=post_id)

