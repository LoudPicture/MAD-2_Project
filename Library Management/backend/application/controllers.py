from flask import Flask, request, render_template, request, redirect, url_for, current_app as app, session
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from application.models import *
from flask import Flask, session
from flask_restful import Api, Resource, reqparse
from flask import jsonify
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="Username is required")
        parser.add_argument("password", type=str, required=True, help="Password is required")
        parser.add_argument("email", type=str, required=True, help="Email is required")
        args = parser.parse_args()

        user = args["username"]
        password = args["password"]
        email = args['email']
        # Check if the user already exists in the database
        user_exists = User.query.filter_by(username=user).first()
        if user_exists:
            return {"error": "User already exists"}

        # Insert the new user into the database
        new_user = User(username=user, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "SignUp successful"}

    def get(self):
        return {"message": "Please sign up"}

signup_resource = SignupResource()

class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="Username is required")
        parser.add_argument("password", type=str, required=True, help="Password is required")
        args = parser.parse_args()

        user = args["username"]
        password = args["password"]

        user_query = User.query.filter_by(username=user).first()
        if user_query is None:
            return {"error": "Invalid username or password"}

        db_password = user_query.password
        if db_password != password:
            return {"error": "Invalid username or password"}
        
        user_db = User.query.filter_by(username=user).first()
        user_db.lastAct = datetime.now().replace(microsecond=0)
        db.session.commit()

        # Generate an access token
        access_token = create_access_token(identity=user)

        response = {"message": "Login successful", "access_token": access_token}

        # Set the SameSite attribute for the access token cookie
        if 'access_token_cookie' in request.cookies:
            response = unset_jwt_cookies(response)

        return response
    def get(self):
        if "user" in session:
            return {"message": "User already logged in"}
        return {"message": "Please log in"}

user_login_resource = UserLoginResource()


class AdminLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="Username is required")
        parser.add_argument("password", type=str, required=True, help="Password is required")
        args = parser.parse_args()

        user = args["username"]
        password = args["password"]

        user_query = User.query.filter_by(username=user).first()
        if user_query is None or not user.startswith("admin"):
            return {"error": "Invalid username or password"}

        db_password = user_query.password
        if db_password != password:
            return {"error": "Invalid username or password"}

        # Generate an access token
        access_token = create_access_token(identity=user)

        response = {"message": "Login successful", "access_token": access_token}

        # Set the SameSite attribute for the access token cookie
        if 'access_token_cookie' in request.cookies:
            response = unset_jwt_cookies(response)

        return response

    def get(self):
        if "user" in session:
            return {"redirect": url_for("admin")}
        return {"message": "Please log in"}

admin_login_resource = AdminLoginResource()
































#               User Routes                           #

class UserHomeResource(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        return {"result": username}

user_home_resource = UserHomeResource()


class UserBooksResource(Resource):
    def get(self):
        # Fetch all books
        books = Book.query.all()
        # Serialize books
        serialized_books = [book.serialize() for book in books]
        return {"books": serialized_books}, 200

user_books_resource = UserBooksResource()


class BookRequestResource(Resource):
    @jwt_required()
    def post(self, book_id):
        current_user_id = get_jwt_identity()

        # Check if the book exists
        book = Book.query.get_or_404(book_id)

        # Check if the user has already requested 5 books
        user_requests = UserBook.query.filter_by(user_id=current_user_id).count()
        if user_requests >= 5:
            return {"error": "Maximum book requests reached"}, 400

        # Check if the book is already requested by the user
        user_requested_book = UserBook.query.filter_by(user_id=current_user_id, book_id=book_id).first()
        if user_requested_book:
            return {"error": "Book already requested by the user"}, 400

        # Create a new user book entry
        try:
            new_user_book = UserBook(
                user_id=current_user_id,
                book_id=book_id,
                issue_date=datetime.now().date(),
                due_date=datetime.now().date() + timedelta(days=7),
                status="requested"
            )
            db.session.add(new_user_book)
            db.session.commit()
            return {"message": "Book requested successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Failed to request book, please try again later"}, 500

    @jwt_required()
    def get(self, book_id):
        current_user_id = get_jwt_identity()

        # Check if the book exists
        book = Book.query.get_or_404(book_id)

        # Check if the user has requested this book
        user_requested_book = UserBook.query.filter_by(user_id=current_user_id, book_id=book_id).first()
        if user_requested_book:
            return {"message": "Book is requested by the user"}, 200
        else:
            return {"message": "Book is not requested by the user"}, 404




class MyBooksResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        
        # Fetch all granted books for the current user
        granted_books = GrantedBook.query.filter_by(user_id=current_user).all()
        
        # Serialize the granted books
        serialized_granted_books = []
        for granted_book in granted_books:
            book = Book.query.get(granted_book.book_id)
            if book:
                serialized_granted_book = {
                    "id": granted_book.id,
                    "book": {
                        "id": book.id,
                        "name": book.name,
                        "authors": book.authors,
                        "content": book.content,
                        "section": book.section.serialize()  # Serialize the section object
                        # Add more fields as needed
                    }
                }
                serialized_granted_books.append(serialized_granted_book)
        
        return {"grantedBooks": serialized_granted_books}, 200

    @jwt_required()
    def delete(self, book_id):
        current_user = get_jwt_identity()
        # Check if the book is granted to the current user
        granted_book = GrantedBook.query.filter_by(user_id=current_user, id=book_id).first()
        if not granted_book:
            return {"message": "Book not found or not granted to the user"}, 404
        # Delete the granted book
        db.session.delete(granted_book)
        db.session.commit()

        return {"message": "Book returned successfully"}, 200



class FeedbackResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        # Create a request parser
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', type=int, required=True)
        parser.add_argument('rating', type=int, required=True)
        parser.add_argument('comment', type=str, required=True)
        
        # Parse the request
        args = parser.parse_args()

        # Extract data from parsed arguments
        book_id = args['book_id']
        rating = args['rating']
        comment = args['comment']

        # Validate the parsed data
        if not (book_id and rating and comment):
            return {'message': 'Missing required data fields'}, 400

        # Save feedback to the database
        feedback = Feedback(user_id=current_user, book_id=book_id, rating=rating, comment=comment)
        db.session.add(feedback)
        db.session.commit()

        return {'message': 'Feedback submitted successfully'}, 201


class BookReviewsResource(Resource):
    def get(self, book_id):
        # Fetch reviews for the book by book_id
        reviews = Feedback.query.filter_by(book_id=book_id).all()
        if not reviews:
            return {'message': 'No reviews found for this book'}, 404
        
        # Convert reviews objects to list of dictionaries
        reviews_list = []
        for review in reviews:
            review_dict = {
                'id': review.id,
                'user_id': review.user_id,
                'book_id': review.book_id,
                'rating': review.rating,
                'comment': review.comment,
                # Add other review details as needed
            }
            reviews_list.append(review_dict)
        
        return reviews_list, 200


class BookSearchResource(Resource): 
    def get(self):
        search_term = request.args.get('search')
        if search_term:
            section = Section.query.filter(Section.name.ilike(f'%{search_term}%')).first()
            if section:
                books = section.books
            else:
                books = Book.query.filter(
                    (Book.name.ilike(f'%{search_term}%')) |
                    (Book.authors.ilike(f'%{search_term}%'))
                ).all()
            return {"books": [book.serialize() for book in books]}, 200

        return {"message": "Please provide a valid search term"}, 400











#                          Admin routes                      #

class AdminHomeResource(Resource):
    @jwt_required()
    def get(self):
        sections = Section.query.all()
        return {"sections": [section.serialize() for section in sections]}, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.startswith("admin"):
            return {"message": "Unauthorized access"}, 403
        
        section_name = request.json.get('sectionName')
        if section_name:
            section = Section(name=section_name)
            db.session.add(section)
            try:
                db.session.commit()
                return {"message": "Section added successfully"}, 201
            except IntegrityError:
                db.session.rollback()
                return {"message": "Section already exists"}, 409

        search_term = request.json.get('search_term')
        if search_term:
            section = Section.query.filter(Section.name.ilike(f'%{search_term}%')).first()
            if section:
                books = section.books
            else:
                books = Book.query.filter(
                    (Book.name.ilike(f'%{search_term}%')) |
                    (Book.authors.ilike(f'%{search_term}%'))
                ).all()
            return {"books": [book.serialize() for book in books]}, 200

        return {"message": "Please provide a valid search term"}, 400

    @jwt_required()
    def delete(self, section_id):
        current_user = get_jwt_identity()
        if not current_user.startswith("admin"):
            return {"message": "Unauthorized access"}, 403
        
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return {"message": "Section deleted successfully"}, 200
        else:
            return {"message": "Section not found"}, 404
    
    @jwt_required()
    def put(self, section_id):
        current_user = get_jwt_identity()
        if not current_user.startswith("admin"):
            return {"message": "Unauthorized access"}, 403
        
        section = Section.query.get(section_id)
        if section:
            data = request.json
            if 'sectionName' in data:
                section.name = data['sectionName']
                db.session.commit()
                return {"message": "Section updated successfully"}, 200
            else:
                return {"message": "Invalid request, sectionName not provided"}, 400
        else:
            return {"message": "Section not found"}, 404

admin_home_resource = AdminHomeResource()


# Resource for displaying books in a section
class SectionResource(Resource):
    def get(self, section_id):
        section = Section.query.get_or_404(section_id)
        books = section.books
        serialized_books = []
        for book in books:
            serialized_books.append(book.serialize())
        return {"section_name": section.name, "books": serialized_books}

# Resource for adding a book
class BookAddResource(Resource):
    def post(self, section_id):
        section = Section.query.get_or_404(section_id)
        
        # Parse request data
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('authors', type=str, required=True)
        args = parser.parse_args()
        
        # Create book object
        new_book = Book(
            name=args['name'],
            content=args['content'],
            authors=args['authors'],
            section=section
        )
        
        # Add book to database
        db.session.add(new_book)
        db.session.commit()
        
        return {"message": "book added successfully"}, 201
        
# Resource for updating a book
class BookUpdateResource(Resource):
    def put(self, book_id):
        # Retrieve book by id
        book = Book.query.get_or_404(book_id)
        
        # Parse request data
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('authors', type=str, required=True)
        args = parser.parse_args()
        
        # Update book attributes
        book.name = args['name']
        book.content = args['content']
        book.authors = args['authors']
        
        # Commit changes to the database
        db.session.commit()
        
        return {"message": "Book updated successfully"}, 200

# Resource for deleting a book
class BookDeleteResource(Resource):
    def delete(self, book_id):
        # Retrieve book by id
        book = Book.query.get_or_404(book_id)
        
        # Delete the book
        db.session.delete(book)
        db.session.commit()
        
        return {"message": "book deleted successfully"}, 200


class AdminDashboardResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if not current_user.startswith("admin"):
            return {"message": "Unauthorized access"}, 403
        
        # Fetch all book requests
        book_requests = UserBook.query.all()
        granted_books = GrantedBook.query.all()  # Fetch all granted books
        # Serialize book requests
        serialized_requests = []
        for request in book_requests:
            user = User.query.filter_by(username=request.user_id).first()
            book = Book.query.get(request.book_id)
            if user:
                serialized_request = {
                    "id": request.id,  # Include request ID for further processing
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "book": {
                        "id": book.id,
                        "name": book.name
                    },
                    "issue_date": request.issue_date.strftime("%Y-%m-%d"),
                    "status": request.status
                }
                serialized_requests.append(serialized_request)
        
        # Serialize granted books
        serialized_granted_books = []
        for granted_book in granted_books:
            user = User.query.filter_by(username=granted_book.user_id).first()  # Fetch user by username
            book = Book.query.get(granted_book.book_id)
            if user and book:
                serialized_granted_book = {
                    "id": granted_book.id,  # Include granted book ID for further processing
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "book": {
                        "id": book.id,
                        "name": book.name
                    }
                }
                serialized_granted_books.append(serialized_granted_book)
        return {"book_requests": serialized_requests, "granted_books": serialized_granted_books}, 200


    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('action', type=str, required=True, help="Action is required")
        parser.add_argument('request_id', type=int)
        parser.add_argument('granted_book_id', type=int)
        args = parser.parse_args()

        action = args['action']
        request_id = args.get('request_id')
        granted_book_id = args.get('granted_book_id')

        if action not in ['grant', 'reject', 'revoke']:
            return {"message": "Invalid action"}, 400

        current_user = get_jwt_identity()  # Fetch current user
        if action == 'grant':
            if request_id is None:
                return {"message": "Request ID is required for granting a book"}, 400
            request = UserBook.query.get(request_id)
            if request:
                # Create a new entry in the GrantedBook table with a granted date
                granted_book = GrantedBook(user_id=request.user_id, book_id=request.book_id, granted_date=datetime.now())
                db.session.add(granted_book)
                db.session.commit()
                # Remove the request entry
                db.session.delete(request)
                db.session.commit()
                return {"message": "Book granted successfully"}, 200
            else:
                return {"message": "Request not found"}, 404

        elif action == 'reject':
            if request_id is None:
                return {"message": "Request ID is required for rejecting a book"}, 400
            request = UserBook.query.get(request_id)
            if request:
                # Remove the request entry
                db.session.delete(request)
                db.session.commit()
                return {"message": "Request rejected successfully"}, 200
            else:
                return {"message": "Request not found"}, 404

        elif action == 'revoke':
            granted_book_id = granted_book_id
            if granted_book_id is None:
                return {"message": "Granted book ID is required for revoking a book"}, 400
            print(granted_book_id)
            # Find the granted book associated with the provided ID
            granted_book = GrantedBook.query.get(granted_book_id)
            if granted_book:
                # Remove the granted book entry
                db.session.delete(granted_book)
                db.session.commit()
                return {"message": "Book revoked successfully"}, 200
            else:
                return {"message": "Granted book not found"}, 404


class EbookStatusResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        # Fetch granted books for the current user
        granted_books = GrantedBook.query.filter_by(user_id=current_user).all()

        # Serialize the granted books
        serialized_granted_books = []
        for granted_book in granted_books:
            book = Book.query.get(granted_book.book_id)
            if book:
                serialized_granted_books.append({
                    "username": current_user,
                    "book_name": book.name,
                    "granted_date": granted_book.granted_date.strftime('%Y-%m-%d')
                })

        return serialized_granted_books, 200



















def register_resources(api):
    api.add_resource(SignupResource, "/signup")
    api.add_resource(UserLoginResource, "/userlogin")
    api.add_resource(UserHomeResource, "/user/home")
    api.add_resource(AdminLoginResource, "/adminlogin")
    api.add_resource(AdminHomeResource, "/admin/home", "/admin/home/<int:section_id>")
    api.add_resource(SectionResource, '/sections/<int:section_id>')
    api.add_resource(BookAddResource, '/sections/<int:section_id>/add_book')
    api.add_resource(BookUpdateResource, '/books/<int:book_id>/update')
    api.add_resource(BookDeleteResource, '/books/<int:book_id>/delete')
    api.add_resource(UserBooksResource, '/user/books')
    api.add_resource(BookRequestResource, '/user/request-book/<int:book_id>')
    api.add_resource(AdminDashboardResource, "/admin_dashboard/book_requests","/admin_dashboard/granted_books","/admin_dashboard/grant_book","/admin_dashboard/reject_book","/admin_dashboard","/admin_dashboard/revoke_book")
    api.add_resource(MyBooksResource, "/user/mybooks","/user/mybooks/<int:book_id>")
    api.add_resource(FeedbackResource, '/feedback')
    api.add_resource(BookReviewsResource, '/book/<int:book_id>/reviews')
    api.add_resource(BookSearchResource, '/user/search-books')
    api.add_resource(EbookStatusResource, '/e-book/stat')
    