from app import app, db, Book  # Replace 'your_app' with your actual app module

# List of New York Times bestsellers from the past 10 years
books_data = [
    {
        "title": "The Four Winds",
        "author": "Kristin Hannah",
        "description": "An epic novel of love and heroism and hope, set against the backdrop of one of America's most defining eras—the Great Depression.",
        "publish_year": 2021,
        "genre": "Historical Fiction",
        "rating": 4,
        "reviews": "A powerful portrayal of hardship and resilience during the Dust Bowl era.",
        "image_url": "https://images.squarespace-cdn.com/content/v1/63d9364fe9fbbb42b22afb61/4a5da173-0a94-4027-bed7-831a79eb2c0f/The+Four+Winds.jpeg"
    },
    {
        "title": "Where the Crawdads Sing",
        "author": "Delia Owens",
        "description": "A murder mystery, a courtroom drama, and a celebration of nature that tells the story of Kya Clark, the 'Marsh Girl'.",
        "publish_year": 2018,
        "genre": "Mystery",
        "rating": 5,
        "reviews": "A haunting and beautiful novel about isolation and prejudice.",
        "image_url": "https://m.media-amazon.com/images/I/810RZxeCZXL._UF894,1000_QL80_.jpg"
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "description": "Practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.",
        "publish_year": 2018,
        "genre": "Self Development",
        "rating": 4,
        "reviews": "A thought-provoking exploration of regret and second chances.",
        "image_url": "https://scholarmedia.africa/wp-content/uploads/2024/02/1_tQszPBlBdi522xW1DnhwgQ.jpg"
    },
    {
        "title": "Rich Dad Poor Dad",
        "author": "Robert T. Kiyosaki",
        "description": "A book that advocates the importance of financial literacy, financial independence and building wealth through investing in assets, real estate investing, starting and owning businesses, as well as increasing one's financial intelligence.",
        "publish_year": 2000,
        "genre": "Personal Finance",
        "rating": 5,
        "reviews": "A must-read for anyone looking to improve their financial literacy.",
        "image_url": "https://travismewhirter.com/wp-content/uploads/2020/04/IMG_3778-2.jpg"
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "description": "A psychological thriller about a woman who shoots her husband and then stops speaking.",
        "publish_year": 2019,
        "genre": "Thriller",
        "rating": 3,
        "reviews": "A shocking psychological thriller of a woman's act of violence against her husband.",
        "image_url": "https://images.meesho.com/images/products/137168101/wqzub_512.webp?width=512"
    },
    {
        "title": "Think and Grow Rich",
        "author": "Napoleon Hill",
        "description": "The book condenses stories of famous millionaires of his generation into principles of success that the reader can apply to their own life.",
        "publish_year": 1937,
        "genre": "Self Development",
        "rating": 5,
        "reviews": "A profound book on the power of thought and its role in personal success.",
        "image_url": "https://m.media-amazon.com/images/I/51HqycCxMRL._SY780_.jpg"
    },
    {
        "title": "The Woman in the Window",
        "author": "A.J. Finn",
        "description": "A psychological thriller about an agoraphobic woman who believes she has witnessed a crime in a neighboring house.",
        "publish_year": 2018,
        "genre": "Thriller",
        "rating": 2,
        "reviews": "A twisty, powerful Hitchcock-style thriller.",
        "image_url": "https://static01.nyt.com/images/2018/01/20/arts/20bookjp2-print/04bookfinn2-superJumbo.jpg"
    },
    {
        "title": "The Prince",
        "author": "Niccolò Machiavelli",
        "description": "A political treatise by the Italian diplomat and political theorist Niccolò Machiavelli. The book is a guide on political power, how to acquire it, and how to maintain it.",
        "publish_year": 1532,
        "genre": "Political Philosophy",
        "rating": 5,
        "reviews": "A timeless classic on political strategy and power dynamics.",
        "image_url": "https://images.pangobooks.com/book_images/fhznVvEKPlaVKOh226784NPbchB2/1651169417968_fhznVvEKPlaVKOh226784NPbchB2?width=800&quality=85&crop=1%3A1"
    },
    {
        "title": "The Art of War",
        "author": "Sun Tzu",
        "description": "An ancient Chinese military treatise dating from the Late Spring and Autumn Period. The work, which is attributed to the ancient Chinese military strategist Sun Tzu, is composed of 13 chapters.",
        "publish_year": 500,
        "genre": "Military Strategy",
        "rating": 4,
        "reviews": "A profound treatise on strategy, tactics, and leadership.",
        "image_url": "https://cdn11.bigcommerce.com/s-q39b4/images/stencil/2000x2000/products/7431/223400/9780804830805.website__94202.1567110692.jpg?c=2"
    },
    {
        "title": "Normal People",
        "author": "Sally Rooney",
        "description": "A story of the complicated relationship between two teenagers, Connell and Marianne, as they navigate adulthood.",
        "publish_year": 2018,
        "genre": "Literary Fiction",
        "rating": 4,
        "reviews": "A deeply affecting love story about how one person can change another's life.",
        "image_url": "https://www.books4people.co.uk/cdn/shop/products/718W0JbHm1L.jpg?v=1655983246"
    },
    {
        "title": "The Guest List",
        "author": "Lucy Foley",
        "description": "A wedding celebration turns dark and deadly on an isolated island off the coast of Ireland.",
        "publish_year": 2020,
        "genre": "Mystery",
        "rating": 3,
        "reviews": "A gripping, twisty murder mystery set on an isolated island.",
        "image_url": "https://images.squarespace-cdn.com/content/v1/5fed0a6a15120a7c1d180129/1695135254602-2HLYGIWVQH8OI1K9V79U/IMG_0105.jpeg"
    },
    {
        "title": "The Vanishing Half",
        "author": "Brit Bennett",
        "description": "The story of twin sisters, their divergent paths, and their daughters, whose lives reflect the different paths they chose.",
        "publish_year": 2020,
        "genre": "Literary Fiction",
        "rating": 2,
        "reviews": "A powerful exploration of race, identity, and family.",
        "image_url": "https://images.squarespace-cdn.com/content/v1/63d9364fe9fbbb42b22afb61/60996666-c862-4574-af74-c2488e1cf53e/The-Vanishing-Half.jpeg"
    }
]

def seed_books():
    with app.app_context():  # Set up application context
        # Clear existing data
        db.session.query(Book).delete()
        db.session.commit()

        # Add new books from the books_data list
        for book_data in books_data:
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                description=book_data["description"],
                publish_year=book_data["publish_year"],
                genre=book_data["genre"],
                rating=book_data["rating"],
                reviews=book_data["reviews"],
                image_url=book_data["image_url"]
            )
            db.session.add(book)
        
        db.session.commit()
        print(f"Seeded {len(books_data)} books successfully.")

if __name__ == "__main__":
    seed_books()