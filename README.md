# **Cocktail Recommender**

## Group: Vinicius Eller and Arthur Chieppe

Step 1: Embeddings

The dataset consists of game reviews scraped from Gamerant. The CSV file contains two columns: the title of the game and the review text. Each row represents a unique game-review pairing, forming the basis for subsequent embedding generation.

An autoencoder architecture generates embeddings. The encoder compresses the input dimension to a 200-dimensional space using two fully connected layers with ReLU activations. The decoder mirrors this structure to reconstruct the original embeddings, and the Adam optimizer adjusts weights with a learning rate of 0.0001.

![Neural network topology](img/topology.png)

The training process minimizes the Mean Squared Error (MSE) between the input and the reconstructed embeddings. MSE is preferred over Cross Entropy in this context because it effectively measures the reconstruction error in continuous values. Unlike Cross Entropy, which is designed for classification tasks and emphasizes probability distributions, MSE focuses on the exact numerical differences between input and output. This characteristic allows the model to penalize larger reconstruction errors more heavily, encouraging the autoencoder to refine its representations. The loss function is defined as follows:

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^n (x_i - \hat{x}_i)^2
$$

