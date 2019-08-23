import praw
def usr() -> praw.Reddit:
    """
    PRAW - Python Reddit API Wrapper
    """
    return praw.Reddit(client_id='<PRAW ID>',
                       client_secret='<PRAW TOKEN>',
                       user_agent='<APP NAME> by /u/<REDDIT HANDLE>')
