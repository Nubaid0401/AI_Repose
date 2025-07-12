import json
from typing import List, Dict, Union, Any

# --- 1. Student Class (Object-Oriented Programming) ---
class Student:
    """
    Represents a student in the school management system.
    Demonstrates: Classes, __init__, instance variables, methods, type hinting,
                   class variables for ID generation.
    """
    next_id = 1000 # Class variable to generate unique student IDs

    def __init__(self, name: str, age: int, grade: int, major: str):
        """
        Constructor for the Student class.
        Initializes a student with basic details and assigns a unique ID.
        """
        # Basic input validation
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty and must be a string.")
        if not isinstance(age, int) or not (5 <= age <= 18): # Assuming typical school age range
            raise ValueError("Student age must be an integer between 5 and 18.")
        if not isinstance(grade, int) or not (1 <= grade <= 12): # Assuming grades 1-12
            raise ValueError("Student grade must be an integer between 1 and 12.")
        if not isinstance(major, str) or not major.strip():
            raise ValueError("Student major/stream cannot be empty and must be a string.")

        self.student_id = Student.next_id
        Student.next_id += 1 # Increment class variable for the next student
        self.name = name.strip()
        self.age = age
        self.grade = grade
        self.major = major.strip()
        # In a real system, enrollment_date might be set from user input or current date
        self.enrollment_date = "2024-09-01" # Static for simplicity in CLI

    def get_details(self) -> str:
        """
        Returns a formatted string of the student's details.
        Demonstrates: String formatting (f-strings).
        """
        return (f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, "
                f"Grade: {self.grade}, Major: {self.major}, "
                f"Enrollment Date: {self.enrollment_date}")

    def update_grade(self, new_grade: int):
        """Updates the student's grade."""
        if not isinstance(new_grade, int) or not (1 <= new_grade <= 12):
            raise ValueError("New grade must be an integer between 1 and 12.")
        self.grade = new_grade
        print(f"Updated {self.name}'s grade to {self.grade}.")

    def update_major(self, new_major: str):
        """Updates the student's major/stream."""
        if not isinstance(new_major, str) or not new_major.strip():
            raise ValueError("New major cannot be empty.")
        self.major = new_major.strip()
        print(f"Updated {self.name}'s major to {self.major}.")

    def to_dict(self) -> Dict[str, Any]:
        """Converts student object to a dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "major": self.major,
            "enrollment_date": self.enrollment_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Creates a Student object from a dictionary (useful for loading from JSON).
        Demonstrates: Class methods.
        """
        # Create a dummy student first to satisfy __init__ requirements, then populate
        student = cls(data['name'], data['age'], data['grade'], data['major'])
        student.student_id = data['student_id']
        student.enrollment_date = data['enrollment_date']
        # Ensure next_id is updated if we load existing students, so new IDs are unique
        if data['student_id'] >= cls.next_id:
            cls.next_id = data['student_id'] + 1
        return student

# --- 2. StudentManager Class (Encapsulation and Management Logic) ---
class StudentManager:
    """
    Manages a collection of Student objects.
    Handles operations like add, view, update, remove, search, and data persistence.
    Demonstrates: Lists, methods for CRUD operations, file I/O, sorting.
    """
    def __init__(self, data_file: str = "students.json"):
        self.students: List[Student] = []
        self.data_file = data_file
        self._load_students() # Load existing data on startup

    def add_student(self, name: str, age: int, grade: int, major: str):
        """Adds a new student to the manager."""
        try:
            student = Student(name, age, grade, major)
            self.students.append(student)
            print(f"Student '{student.name}' (ID: {student.student_id}) added successfully.")
        except ValueError as e:
            print(f"Error adding student: {e}")
        self._save_students() # Save changes immediately

    def view_students(self):
        """
        Displays all students.
        Demonstrates: Iteration, conditional logic, sorting.
        """
        if not self.students:
            print("No students registered yet.")
            return

        print("\n--- Current Students ---")
        # Sort students by ID for consistent display
        sorted_students = sorted(self.students, key=lambda s: s.student_id)
        for student in sorted_students:
            print(student.get_details())
        print("------------------------\n")

    def update_student(self, student_id: int, new_grade: int = None, new_major: str = None):
        """
        Updates an existing student's details by ID.
        Demonstrates: Searching in a list, conditional updates.
        """
        found = False
        for student in self.students:
            if student.student_id == student_id:
                found = True
                try:
                    if new_grade is not None:
                        student.update_grade(new_grade)
                    if new_major:
                        student.update_major(new_major)
                    print(f"Student ID {student_id} updated.")
                except ValueError as e:
                    print(f"Error updating student: {e}")
                break
        if not found:
            print(f"Student with ID {student_id} not found.")
        self._save_students()

    def remove_student(self, student_id: int):
        """
        Removes a student by ID.
        Demonstrates: List removal using list comprehension.
        """
        original_count = len(self.students)
        # Create a new list excluding the student to be removed
        self.students = [s for s in self.students if s.student_id != student_id]

        if len(self.students) < original_count:
            print(f"Student with ID {student_id} removed successfully.")
            self._save_students()
        else:
            print(f"Student with ID {student_id} not found.")

    def search_students(self, query: str, search_by: str = "name"):
        """
        Searches for students by name, grade, or major.
        Demonstrates: String methods (lower, in), integer comparison, list comprehension for filtering.
        """
        results: List[Student] = []
        query_lower = query.lower()

        if search_by == "name":
            results = [s for s in self.students if query_lower in s.name.lower()]
        elif search_by == "grade":
            try:
                query_grade = int(query)
                results = [s for s in self.students if s.grade == query_grade]
            except ValueError:
                print("Invalid grade for search. Please enter a number.")
                return
        elif search_by == "major":
            results = [s for s in self.students if query_lower in s.major.lower()]
        else:
            print("Invalid search_by parameter. Use 'name', 'grade', or 'major'.")
            return

        if results:
            print(f"\n--- Search Results for '{query}' by {search_by} ---")
            for student in results:
                print(student.get_details())
            print("------------------------------------------\n")
        else:
            print(f"No students found matching '{query}' by {search_by}.")

    def _save_students(self):
        """
        Saves the current student data to a JSON file.
        Demonstrates: File writing, JSON serialization, error handling.
        """
        try:
            with open(self.data_file, 'w') as f:
                # Convert list of Student objects to list of dictionaries
                json.dump([s.to_dict() for s in self.students], f, indent=4)
            # print(f"Student data saved to {self.data_file}") # Keep this quiet for cleaner CLI
        except IOError as e:
            print(f"Error saving data to file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during save: {e}")

    def _load_students(self):
        """
        Loads student data from a JSON file.
        Demonstrates: File reading, JSON deserialization, error handling.
        """
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.students = [Student.from_dict(d) for d in data]
            # print(f"Student data loaded from {self.data_file}") # Keep this quiet
        except FileNotFoundError:
            # print(f"No existing data file '{self.data_file}' found. Starting with empty student list.")
            pass # Silent start if no file
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.data_file}. File might be corrupted. Starting with empty list.")
            self.students = []
        except Exception as e:
            print(f"An unexpected error occurred during load: {e}. Starting with empty list.")
            self.students = []

# --- 3. Main Application Logic (CLI) ---
def main():
    """
    Main function to run the School Student Management System CLI.
    Demonstrates: While loop for menu, input(), function calls, basic error handling for user input.
    """
    manager = StudentManager()

    while True:
        print("\n--- School Student Management System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Remove Student")
        print("5. Search Students")
        print("6. Exit")
        print("----------------------------------------")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            try:
                name = input("Enter student name: ")
                age = int(input("Enter student age (5-18): "))
                grade = int(input("Enter student grade (1-12): "))
                major = input("Enter student major/stream: ")
                manager.add_student(name, age, grade, major)
            except ValueError as e:
                print(f"Invalid input: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif choice == '2':
            manager.view_students()
        elif choice == '3':
            try:
                student_id = int(input("Enter student ID to update: "))
                print("Enter new grade or major (leave blank to keep current):")
                new_grade_str = input("New Grade (1-12): ")
                new_major = input("New Major/Stream: ")

                new_grade = int(new_grade_str) if new_grade_str else None

                manager.update_student(student_id, new_grade, new_major)
            except ValueError as e:
                print(f"Invalid input. {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif choice == '4':
            try:
                student_id = int(input("Enter student ID to remove: "))
                manager.remove_student(student_id)
            except ValueError:
                print("Invalid input. Student ID must be an integer.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        elif choice == '5':
            search_query = input("Enter search query (name, grade, or major): ")
            search_by = input("Search by 'name', 'grade', or 'major'? (default is name): ").lower()
            if search_by not in ['name', 'grade', 'major']:
                search_by = 'name' # Default if invalid input
            manager.search_students(search_query, search_by)
        elif choice == '6':
            print("Exiting School Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    # This block ensures main() runs only when the script is executed directly
    # and not when imported as a module.
    main()