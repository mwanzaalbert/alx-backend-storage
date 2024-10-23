#!/usr/bin/env python3
"""
101-students.py

This module contains a function to retrieve and sort student documents
from a MongoDB collection based on their average scores.

Functions:
-----------
- top_students(mongo_collection):
    Returns a list of students sorted by their average score. Each student
    document includes an 'averageScore' key indicating their average score
    calculated from their associated topics.

Usage:
------
To use the function, import this module and call `top_students` with
a pymongo collection object as the argument. The function will return
a list of student documents sorted in descending order by average score.

Example:
---------
from pymongo import MongoClient
from students import top_students

client = MongoClient('mongodb://127.0.0.1:27017')
students_collection = client.my_db.students
sorted_students = top_students(students_collection)

for student in sorted_students:
    print(f"[{student['_id']}] {student['name']} => {student['averageScore']}")
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    students = list(mongo_collection.find())

    for student in students:
        # Calculate the average score
        scores = [topic['score'] for topic in student.get('topics', [])]
        student['averageScore'] = sum(scores) / len(scores) if scores else 0

    # Sort students by average score in descending order
    return sorted(students, key=lambda x: x['averageScore'], reverse=True)
