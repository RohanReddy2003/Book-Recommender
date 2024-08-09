from django.shortcuts import render
import numpy as np
import os
import pickle

current_path = os.path.dirname(os.path.abspath(__file__))
popular_df_path = os.path.join(current_path, 'popular.pkl')
similarity_scores_path = os.path.join(current_path, 'similarity_scores.pkl')
books_path = os.path.join(current_path, 'books.pkl')
pt_path = os.path.join(current_path, 'pt.pkl')

# Helper function to load pickle files
def load_pickle(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} pickle file not found.")
        return None

# Load the data from pickle files
popular_df = load_pickle(popular_df_path)
books = load_pickle(books_path)
similarity_scores = load_pickle(similarity_scores_path)
pt = load_pickle(pt_path)

# View for the home page
def home(request):
    book_name = list(popular_df['Book-Title'].values)
    author = list(popular_df['Book-Author'].values)
    image = list(popular_df['Image-URL-M'].values)
    votes = list(popular_df['num_ratings'].values)
    rating = list(popular_df['avg_rating'].values)
    num_books = len(book_name)  # Calculate the number of books
    
    context = {
        'book_data': zip(book_name, author, image, votes, rating),
        'num_books': num_books  # Pass the number of books to the template
    }
    return render(request, 'index.html', context)

# View for the recommend UI page
def recommend_ui(request):
    return render(request, 'recommend.html')

# View for handling book recommendations
def recommend_books(request):
    data = []  # Initialize an empty list to hold the recommended books
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        print(user_input)
        
        # Check if user_input exists in pt.index
        if user_input not in pt.index:
            # If the book is not found, display an error message on the recommend page
            return render(request, 'recommend.html', {'message': "The book you're looking for is not in our dataset."})
        
        # Find the index of the book in pt
        index_array = np.where(pt.index == user_input)[0]
        
        # Handle the case where the book is not found in the index
        if index_array.size == 0:
            return render(request, 'recommend.html', {'message': "No recommendations available for the given book."})
        
        index = index_array[0]
        
        # Calculate similarity scores and sort them
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]
        
        # Collect data for the recommended books
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

    # Render the recommend.html template with the recommended books
    return render(request, 'recommend.html', {'data': data})
