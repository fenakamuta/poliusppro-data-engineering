import pandas as pd
import praw


class ClientReddit:
    def __init__(self, client_id, client_secret, username, password, user_agent):
        """
        Inicializa o cliente do Reddit com as credenciais fornecidas.

        :param client_id: ID do cliente do aplicativo (obtido no Reddit Apps)
        :param client_secret: Segredo do cliente
        :param username: Nome de usuário do Reddit
        :param password: Senha do Reddit
        :param user_agent: Identificador do aplicativo (ex.: 'meu_app/0.1')
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent,
        )

    def get_hot_posts(self, subreddit_name, limit=10):
        """
        Retorna uma lista de posts "hot" de um subreddit especificado.

        :param subreddit_name: Nome do subreddit (ex.: 'Python')
        :param limit: Número máximo de posts a serem retornados
        :return: Lista de dicionários com informações dos posts
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append(
                {
                    "id": post.id,
                    "ups": post.ups,
                    "downs": post.downs,
                    "upvote_ratio": post.upvote_ratio,
                    "subreddit": post.subreddit.display_name,
                    "title": post.title,
                    "score": post.score,
                    "created_utc": post.created_utc,
                    "url": post.url,
                    "selfText": post.selftext,
                    "comments": [comment.body for comment in post.comments],
                }
            )
        return pd.DataFrame(posts)