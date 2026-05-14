# CodeCraftHub

CodeCraftHub is a simple beginner-friendly learning platform built with **Python** and **Flask**. It helps developers track the courses they want to learn using a **REST API** and a **JSON file** for storage.

A simple REST API to track courses you want to learn, built with Python Flask.

## 🎯 What Does This Do?

MyLearnTracker helps you keep track of courses you want to take. You can:
- ✅ Add new courses with target dates
- 📋 View all your courses
- 🔄 Update course information
- ✔️ Mark courses as completed
- 🗑️ Delete courses you're no longer interested in

## 📁 Project Structure

```
mylearn-tracker/
├── app.py              # Main Flask application (API server)
├── courses.json        # Data storage (auto-created)
├── requirements.txt    # Python dependencies
├── README.md           # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```


### Step 3: Test It!

Open a new terminal and try:
```bash
curl http://localhost:5000
```

You should see a welcome message with available endpoints.

## 📚 API Endpoints

### 1. Get All Courses
**GET** `/api/courses`

```bash
curl http://localhost:5000/api/courses
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "courses": [
    {
      "id": 1,
      "name": "Python Basics",
      "description": "Learn Python fundamentals",
      "target_date": "2025-12-31",
      "status": "In Progress",
      "created_at": "2025-11-04 10:30:00"
    }
  ]
}
```

### 2. Get a Specific Course
**GET** `/api/courses/<id>`

```bash
curl http://localhost:5000/api/courses/1
```

### 3. Add a New Course
**POST** `/api/courses`

```bash
curl -X POST http://localhost:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started"
  }'
```

**Required Fields:**
- `name` - Course name (string)
- `description` - Course description (string)
- `target_date` - Target completion date in YYYY-MM-DD format
- `status` - Must be one of: "Not Started", "In Progress", "Completed"

**Response:**
```json
{
  "success": true,
  "message": "Course added successfully",
  "course": {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-11-04 10:30:00"
  }
}
```

### 4. Update a Course
**PUT** `/api/courses/<id>`

```bash
curl -X PUT http://localhost:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress"
  }'
```

You can update any of these fields:
- `name`
- `description`
- `target_date`
- `status`

### 5. Delete a Course
**DELETE** `/api/courses/<id>`

```bash
curl -X DELETE http://localhost:5000/api/courses/1
```

## 🎁 Bonus Features

### Get Statistics
**GET** `/api/courses/stats`

```bash
curl http://localhost:5000/api/courses/stats
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_courses": 5,
    "not_started": 2,
    "in_progress": 2,
    "completed": 1
  }
}
```

### Search Courses
**GET** `/api/courses/search?q=<search_term>`

```bash
curl "http://localhost:5000/api/courses/search?q=python"
```

## 🧪 Testing with Postman

1. Open Postman
2. Create a new request
3. Set the method (GET, POST, PUT, DELETE)
4. Enter the URL (e.g., `http://localhost:5000/api/courses`)
5. For POST/PUT, add JSON body in the "Body" tab (select "raw" and "JSON")
6. Click "Send"

### Example Test Sequence:

1. **Add 3 courses:**
   - POST `/api/courses` (do this 3 times with different data)

2. **View all courses:**
   - GET `/api/courses`

3. **Update one course:**
   - PUT `/api/courses/1` (change status to "In Progress")

4. **Get statistics:**
   - GET `/api/courses/stats`

5. **Delete a course:**
   - DELETE `/api/courses/2`

6. **Verify deletion:**
   - GET `/api/courses`

## 📖 Understanding the Code

### How Data is Stored

Data is stored in `courses.json` as a simple JSON array:

```json
[
  {
    "id": 1,
    "name": "Python Basics",
    "description": "Learn Python fundamentals",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-11-04 10:30:00"
  }
]
```

### How the API Works

1. **When you start the app:** Flask creates a web server on port 5000
2. **When you make a request:** Flask routes it to the right function
3. **The function:** 
   - Reads `courses.json`
   - Does the operation (add, update, delete)
   - Saves back to `courses.json`
   - Returns a JSON response
