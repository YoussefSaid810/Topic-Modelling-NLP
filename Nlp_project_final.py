import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import warnings
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics import silhouette_score
import re
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split





# Read the dataset into a pandas DataFrame
df = pd.read_csv('articles1.csv', nrows=1000)
def remove_special_characters(text):
    pattern = r'[^a-zA-Z0-9\s]'
    text = re.sub(pattern, '', text)
    return text


def remove_numbers(text):
    pattern = r'\d+'
    text = re.sub(pattern, '', text)
    return text

def remove_urls(text):
    pattern = r'http\S+|www.\S+'
    text = re.sub(pattern, '', text)
    return text

def remove_emails(text):
    pattern = r'\S+@\S+'
    text = re.sub(pattern, '', text)
    return text


# Initialize NLTK's lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to perform word tokenization, lemmatization, and stop word removal
def preprocess_text(text):
    text = remove_special_characters(text)
    text = remove_numbers(text)
    text = remove_urls(text)
    text = remove_emails(text)
    tokens = word_tokenize(text)  # Tokenize the text into words
    tokens = [lemmatizer.lemmatize(token) for token in tokens]  # Lemmatize each word
    tokens = [token for token in tokens if token.lower() not in stop_words]  # Filter out stop words
    preprocessed_text = ' '.join(tokens)  # Join the tokens back into a single string
    return preprocessed_text
def tfidf_clustering(corpus, num_clusters):
    # Vectorize the corpus using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    # Cluster the documents using K-means
    kmeans_tfidf = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    kmeans_tfidf.fit(tfidf_matrix)
    tfidf_clusters = kmeans_tfidf.labels_

    # Reduce the dimensionality of the TF-IDF matrix using PCA
    pca = PCA(n_components=2)
    tfidf_pca = pca.fit_transform(tfidf_matrix.toarray())

    # Plot the clusters
    plt.scatter(tfidf_pca[:, 0], tfidf_pca[:, 1], c=tfidf_clusters)
    plt.title("TF-IDF Clustering (PCA Visualization)")
    plt.show()

    return tfidf_clusters
def count_clustering(corpus, num_clusters):
    # Vectorize the corpus using CountVectorizer
    count_vectorizer = CountVectorizer()
    count_matrix = count_vectorizer.fit_transform(corpus)

    # Cluster the documents using K-means
    kmeans_count = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
    kmeans_count.fit(count_matrix)
    count_clusters = kmeans_count.labels_

    # Reduce the dimensionality of the count matrix using PCA
    pca = PCA(n_components=2)
    count_pca = pca.fit_transform(count_matrix.toarray())

    # Plot the clusters
    plt.scatter(count_pca[:, 0], count_pca[:, 1], c=count_clusters)
    plt.title("Count Clustering (PCA Visualization)")
    plt.show()

    return count_clusters

# Apply preprocessing to the content column
df['content'] = df['content'].apply(preprocess_text)

# Extract the preprocessed content column from the DataFrame
corpus = df['content']
num_clusters = 10
# Split into train and test sets
corpus_train, corpus_test, y_train, y_test = train_test_split(corpus, df['content'], test_size=0.2, random_state=42)

# Vectorize the train and test sets for TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_train = tfidf_vectorizer.fit_transform(corpus_train)
tfidf_test = tfidf_vectorizer.transform(corpus_test)

# Cluster the TF-IDF train set
kmeans_tfidf = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
kmeans_tfidf.fit(tfidf_train)
y_pred_train_tfidf = kmeans_tfidf.labels_

# Vectorize the train and test sets for count
count_vectorizer = CountVectorizer()
count_train = count_vectorizer.fit_transform(corpus_train)
count_test = count_vectorizer.transform(corpus_test)

# Cluster the count train set
kmeans_count = KMeans(n_clusters=num_clusters, n_init=10, random_state=42)
kmeans_count.fit(count_train)
y_pred_train_count = kmeans_count.labels_

# Get cluster labels for the count test set
y_pred_test_count = kmeans_count.predict(count_test)

# Cluster the train set
count_clusters_train = count_clustering(corpus_train, num_clusters)
tfidf_clusters_train = tfidf_clustering(corpus_train, num_clusters)

# Get the cluster labels for the test set
count_clusters_test = count_clustering(corpus_test, num_clusters)
tfidf_clusters_test = tfidf_clustering(corpus_test, num_clusters)