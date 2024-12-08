import finnhub
finnhub_client = finnhub.Client(api_key="ct307s9r01qkff710nb0ct307s9r01qkff710nbg")

print(finnhub_client.quote('AAPL'))