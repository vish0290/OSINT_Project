import praw

# Reddit API credentials

# Reddit API credentials
client_id       = "13ebR3osBuMhCFhRN8NtBw"
client_secret   = "4KvI1iGAGrwhtt_2qvkqOOW09c6vCQ"
user_agent      = "extractor by u/VishwanathAS"

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def scrape_reddit_comments(post_id):
    """
    Scrape comments from a Reddit post using its post ID.
    Args:
        post_id (str): The Reddit post ID.
    Returns:
        list: A list of comments from the post.
    """
    try:
        # Get the submission object using the post ID
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=25)  # Remove "more comments"
        
        comments = []
        for comment in submission.comments.list():
            comments.append(comment.body)
        
        return comments

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    # Example Reddit post ID
    post_id = "example_post_id"  # Replace with the actual post ID
    
    comments = scrape_reddit_comments(post_id)
    
    if comments:
        print("Comments scraped successfully:")
        for i, comment in enumerate(comments[:10], 1):  # Display first 10 comments
            print(f"{i}. {comment}\n")
    else:
        print("No comments found or an error occurred.")