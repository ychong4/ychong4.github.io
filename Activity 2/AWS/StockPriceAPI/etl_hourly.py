import finnhub
finnhub_client = finnhub.Client(api_key="crvli3hr01qkji45lrj0crvli3hr01qkji45lrjg")

print(finnhub_client.quote('AAPL'))