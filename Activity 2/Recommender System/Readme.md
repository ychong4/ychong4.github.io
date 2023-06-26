## Recommender System

Recommender systems are the algorithms that aimed at suggesting relevant products/services to users to boost your sales.

**Benefits of using recommender system:**
1. Link the users to the right products.
2. Increase user engagement.
3. Make personalized contents/ads.

**Types of recommendations:**
1. Popularity based recommender system: Recommend items based on ratings from most people.
2. Classification model based recommender system: Using classification model to determine if user will like the product.
3. Content based recommender system: Assume that user would like items that are similar to other items.  
4. Collaborative filtering: Assume that people likes things similar to other things they like, and things that are liked by other people with similar taste. i) User-user, ii) item-item
5. Hybrid approach: Combination of collaborative filtering, content-based filtering, and other approaches.
6. Association rule mining: Association rules capture the relationships between items based on their patterns of co-occurrence across transactions.

**Components of Recommendation System**
1. Candidate Generation: The system generates smaller subset of candidates from a huge corpus of items.The model needs to evaluate quickly given the enormous size of the corpus. A given model may provide multiple candidate generators, each nominating different subset of candidates.
2. Scoring: Then, another model scores and ranks the candidates in order to select the set of items to display to the user. This model evaluates a relatively small subset of items and can use a more precise model relying on additonal queries.
3. Re-ranking: The system will take into account additional constraints for the final tanking. For example, remove items that the user explicitly disliked or boosts the score of fresher content. Re-ranking can help ensure diversity, freshness, and fairness.

**Embedding Types**
1. Matrix Factorization: Matrix factorization involves factorizing the user-item iteraction matrix into two lower-rank matrices, which can be used to generate embeddings for the users and items.
2. Autoencoder: Autoencoders are neural networks that learn to compress and decompress data, and can be used to generate embeddings for users or items by training the network to reconstruct the input data. 
3. GNN: GNNs are a more recent approach to embedding that leverages graph structures to capture the relationships between items and users. GNNs are message passing algorithms to propagade information across the graph and generate embeddings for the nodes in the graph. It is effective for capturing complex dependencies between items and users, as well as for handling heterogeneous types of data.


**Similarity Measures**
1. Cosine: The cosine of the angle between the two vectors.
2. Dot product: The dot product of two vectors.
3. Euclidean distance: The usual distance in Euclidean space. A smaller distance means higher similarity.

**Notebooks Information:**
1. **Recommender system for Amazon product:** This notebook introduces the use of popularity-based recommendation system and collaborative filtering recommendation. Popularity-based recommendation is the engine to recommend items to customers based on the hot trend in the item database, which means more ratings counts from users. Collaborative filtering recommends items to customer based on the item they rated previously. The recommender engine lookup for items that have similar ratings from users and recommend them to the specific user based on his/her activity.
2. **Recommender-System-movies:** In this notebook, the deep learning libraries for recommendation system, Tensorflow Recommender System (TFRS) is explored and used to build a recommendation system. This notebook only includes the shallow model, while deeper model can be added into future research list.
