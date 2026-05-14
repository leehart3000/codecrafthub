from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# File where course data will be stored
DATA_FILE = "courses.json"

# Allowed status values
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]


def ensure_data_file():
    """
    Create the JSON file automatically if it does not exist.
    The file will start as an empty list: []
    """
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as file:
                json.dump([], file, indent=4)
        except Exception as e:
            print(f"Error creating {DATA_FILE}: {e}")


def load_courses():
    """
    Read course data from the JSON file.
    Returns a list of courses.
    """
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file is missing, create it and return an empty list
        ensure_data_file()
        return []
    except json.JSONDecodeError:
        # If the file is empty or corrupted, return empty list
        return []
    except Exception as e:
        # Any other file-related error
        print(f"Error reading {DATA_FILE}: {e}")
        return None


def save_courses(courses):
    """
    Save course data back to the JSON file.
    Returns True if successful, False otherwise.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(courses, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing to {DATA_FILE}: {e}")
        return False


def get_next_id(courses):
    """
    Generate the next course ID.
    IDs start at 1 and increase by 1.
    """
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


def find_course_by_id(courses, course_id):
    """
    Search for a course by its ID.
    Returns the course object if found, otherwise None.
    """
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def validate_course_data(data, require_all_fields=True):
    """
    Validate incoming course data.

    Parameters:
    - data: request JSON payload
    - require_all_fields: if True, all required fields must be present
      if False, partial updates are allowed

    Returns:
    - (is_valid, error_message)
    """
    required_fields = ["name", "description", "target_date", "status"]

    # Check required fields
    if require_all_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

    # Validate status if provided
    if "status" in data and data["status"] not in VALID_STATUSES:
        return False, f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"

    # Validate target_date if provided
    if "target_date" in data:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
        except ValueError:
            return False, "Invalid target_date format. Use YYYY-MM-DD"

    return True, None


@app.route("/api/courses", methods=["POST"])
def add_course():
    """
    Add a new course.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    is_valid, error_message = validate_course_data(data, require_all_fields=True)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    courses = load_courses()
    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    new_course = {
        "id": get_next_id(courses),
        "name": data["name"],
        "description": data["description"],
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    courses.append(new_course)

    if not save_courses(courses):
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    Return all courses.
    """
    courses = load_courses()
    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    return jsonify(courses), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Return one course by ID.
    """
    courses = load_courses()
    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    course = find_course_by_id(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Update an existing course.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Allow partial updates, but validate any provided fields
    is_valid, error_message = validate_course_data(data, require_all_fields=False)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    courses = load_courses()
    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    course = find_course_by_id(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Update only the fields provided in the request
    if "name" in data:
        course["name"] = data["name"]
    if "description" in data:
        course["description"] = data["description"]
    if "target_date" in data:
        course["target_date"] = data["target_date"]
    if "status" in data:
        course["status"] = data["status"]

    if not save_courses(courses):
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.
    """
    courses = load_courses()
    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    course = find_course_by_id(courses, course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    updated_courses = [c for c in courses if c["id"] != course_id]

    if not save_courses(updated_courses):
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify({"message": "Course deleted successfully"}), 200


@app.route("/", methods=["GET"])
def home():
    """
    Simple welcome route.
    """
    return jsonify({
        "message": "Welcome to CodeCraftHub API",
        "available_endpoints": [
            "POST /api/courses",
            "GET /api/courses",
            "GET /api/courses/<id>",
            "PUT /api/courses/<id>",
            "DELETE /api/courses/<id>"
        ]
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Return JSON for unknown routes.
    """
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Return JSON when HTTP method is not allowed.
    """
    return jsonify({"error": "Method not allowed"}), 405


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    Return statistics about all courses:
    - Total number of courses
    - Number of courses by status
    """
    courses = load_courses()

    if courses is None:
        return jsonify({"error": "Failed to read course data"}), 500

    # Initialize status counters
    status_counts = {
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0
    }

    # Count total courses and courses by status
    for course in courses:
        status = course.get("status")
        if status in status_counts:
            status_counts[status] += 1

    return jsonify({
        "total_courses": len(courses),
        "status_counts": status_counts
    }), 200

# Create courses.json automatically when the app starts
ensure_data_file()

if __name__ == "__main__":
    app.run(debug=True)