import os
import praw


def get_reddit_client():
    """
    Retorna uma instância do cliente do Reddit.

    Retorna:
        praw.Reddit: Instância do cliente do Reddit.
    """
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_KEY"),
        client_secret=os.environ.get("REDDIT_SECRET_KEY"),
        password=os.environ.get("REDDIT_PASSWORD"),
        user_agent=os.environ.get("REDDIT_USER_AGENT"),
        username=os.environ.get("REDDIT_USERNAME"),
    )
    reddit.read_only = True
    return reddit


def search_posts_by_text(search_text, n_posts=10, sort="hot"):
    """
    Retorna uma lista de posts do Reddit baseados na consulta de texto fornecida.
    Parâmetros:
        search_text (str): Texto utilizado para realizar a pesquisa dos posts no subreddit "all".
    Retorna:
        list: Uma lista de dicionários, onde cada dicionário contém os seguintes dados do post:
            - "title": Título do post.
            - "url": URL do post.
            - "score": Pontuação do post.
            - "text": Conteúdo textual do post.
            - "comments": Número de comentários do post.
    Observação:
        A função utiliza a biblioteca 'praw' para se conectar à API do Reddit em modo somente leitura.
    """
    reddit = get_reddit_client()
    subreddit = reddit.subreddit("all")
    posts_response = subreddit.search(search_text, limit=n_posts, sort=sort)

    return [
        {
            "title": post.title,
            "created_utc": post.created_utc,
            "url": post.url,
            "peurlrmalink": post.permalink,
            "score": float(post.score),
            "text": post.selftext,
            "comments": int(post.num_comments),
            "subreddit": post.subreddit.display_name,
            "upvote_ratio": float(post.upvote_ratio),

        }
        for post in posts_response
    ]