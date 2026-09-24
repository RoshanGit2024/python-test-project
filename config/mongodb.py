from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


db = client["mydb"]  # Replace "mydatabase" with your database name