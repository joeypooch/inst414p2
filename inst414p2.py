import requests
import networkx as nx
import matplotlib.pyplot as plt

# API endpoint and parameters
url = "https://api.nytimes.com/svc/archive/v1/{year}/{month}.json"
api_key = "AOMXHSzPCHEphhXLPMk7hkI17VutWpZe"
year = 2023
month = 3

# Request articles from the NYTimes API
response = requests.get(url.format(year=year, month=month), params={"api-key": api_key})

if response.status_code == 200:
    data = response.json()
    articles = data["response"]["docs"][:250]

   
    graph = nx.DiGraph()

   
    for article in articles:
        article_id = article["_id"]
        article_headline = article["headline"]["main"]
        article_keywords = [keyword["value"] for keyword in article["keywords"]]

        # Add the article as a node to the graph
        graph.add_node(article_id, headline=article_headline)

        # Check for related articles within the same month
        for related_article in articles:
            if related_article["_id"] != article_id:
                related_article_id = related_article["_id"]
                related_article_keywords = [keyword["value"] for keyword in related_article["keywords"]]
                
            shared_keywords = set(article_keywords).intersection(related_article_keywords)

            # Add an edge between the current article and the related article if there are shared keywords
            if shared_keywords:
                graph.add_edge(article_id, related_article_id)

# Filter out articles with no connections
filtered_articles = [node for node in graph.nodes() if graph.degree(node) > 0]

# Create a subgraph with filtered articles
filtered_graph = graph.subgraph(filtered_articles)

# Generate a layout for the filtered graph
layout = nx.spring_layout(filtered_graph, scale=2.0)

# Draw the filtered graph
plt.figure(figsize=(12, 8))
nx.draw_networkx(
    filtered_graph,
    pos=layout,
    node_size=300,
    alpha=0.8,
    font_size=8,
    edge_color='gray',
    width=0.5,
    with_labels=False  # Remove node labels
)
plt.axis("off")
plt.title("Keyword-based Network of Articles from March 2023")
plt.tight_layout()
plt.show()

# Rank articles by number of connections
article_ranks = sorted(filtered_graph.degree, key=lambda x: x[1], reverse=True)


top_articles = article_ranks[:10]

print("Top 10 articles by number of connections:")
for rank, (index, connections) in enumerate(top_articles, start=1):
    print(f"Rank: {rank}, Article ID: {index}, Connections: {connections}")s