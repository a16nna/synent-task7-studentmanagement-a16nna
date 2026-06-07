
import json
import csv
from pathlib import Path
from datetime import datetime

DATA_FILE = "students.json"


def load_data():
    if not Path(DATA_FILE).exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(students):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def generate_student_id(students):
    if not students:
        return 1001

    return max(student["id"] for student in students) + 1


def get_performance_category(marks):
    if marks >= 90:
        return "Excellent"
    elif marks >= 75:
        return "Good"
    elif marks >= 50:
        return "Average"
    return "Needs Improvement"


def print_separator():
    print("-" * 120)


def display_students(students):
    if not students:
        print("\nNo student records found.")
        return

    print_separator()
    print(
        f"{'ID':<8}"
        f"{'Name':<20}"
        f"{'Age':<8}"
        f"{'Course':<15}"
        f"{'Marks':<10}"
        f"{'Category':<20}"
        f"{'Registered On':<25}"
    )
    print_separator()

    for student in students:
        category = get_performance_category(student["marks"])

        print(
            f"{student['id']:<8}"
            f"{student['name']:<20}"
            f"{student['age']:<8}"
            f"{student['course']:<15}"
            f"{student['marks']:<10}"
            f"{category:<20}"
            f"{student['registered_on']:<25}"
        )

    print_separator()


def add_student(students):
    print("\nADD STUDENT")

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    for student in students:
        if student["name"].lower() == name.lower():
            print("A student with this name already exists.")
            return

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks: "))
    except ValueError:
        print("Invalid numeric input.")
        return

    course = input("Enter course: ").strip()

    new_student = {
        "id": generate_student_id(students),
        "name": name,
        "age": age,
        "course": course,
        "marks": marks,
        "registered_on": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    students.append(new_student)
    save_data(students)

    print("\nStudent added successfully.")
    print(f"Assigned Student ID: {new_student['id']}")
    print(f"Registration Time : {new_student['registered_on']}")


def search_by_id(students):
    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for student in students:
        if student["id"] == student_id:
            display_students([student])
            return

    print("Student not found.")


def search_by_name(students):
    name = input("Enter student name: ").strip().lower()

    results = [
        student
        for student in students
        if name in student["name"].lower()
    ]

    if results:
        display_students(results)
    else:
        print("No matching students found.")


def search_student(students):
    print("\n1. Search by ID")
    print("2. Search by Name")

    choice = input("Choose option: ").strip()

    if choice == "1":
        search_by_id(students)
    elif choice == "2":
        search_by_name(students)
    else:
        print("Invalid choice.")


def update_student(students):
    try:
        student_id = int(
            input("Enter student ID to update: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    for student in students:
        if student["id"] == student_id:

            print("\nLeave fields blank to keep current values.")

            name = input(
                f"Name ({student['name']}): "
            ).strip()

            age = input(
                f"Age ({student['age']}): "
            ).strip()

            course = input(
                f"Course ({student['course']}): "
            ).strip()

            marks = input(
                f"Marks ({student['marks']}): "
            ).strip()

            if name:
                student["name"] = name

            if age:
                try:
                    student["age"] = int(age)
                except ValueError:
                    print("Invalid age entered.")

            if course:
                student["course"] = course

            if marks:
                try:
                    student["marks"] = float(marks)
                except ValueError:
                    print("Invalid marks entered.")

            save_data(students)
            print("Student record updated successfully.")
            return

    print("Student not found.")


def delete_student(students):
    try:
        student_id = int(
            input("Enter student ID to delete: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    for student in students:
        if student["id"] == student_id:

            confirmation = input(
                f"Are you sure you want to delete "
                f"{student['name']}? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                students.remove(student)
                save_data(students)
                print("Student deleted successfully.")
            else:
                print("Deletion cancelled.")

            return

    print("Student not found.")


def show_statistics(students):
    if not students:
        print("No records available.")
        return

    total_students = len(students)

    average_marks = (
        sum(student["marks"] for student in students)
        / total_students
    )

    topper = max(
        students,
        key=lambda student: student["marks"]
    )

    lowest = min(
        students,
        key=lambda student: student["marks"]
    )

    print("\nSTUDENT STATISTICS")
    print_separator()

    print(f"Total Students : {total_students}")
    print(f"Average Marks  : {average_marks:.2f}")
    print(f"Highest Marks  : {topper['marks']}")
    print(f"Top Performer  : {topper['name']}")
    print(f"Lowest Marks   : {lowest['marks']}")

    print_separator()


def sort_students(students):
    if not students:
        print("No student records found.")
        return

    print("\n1. Sort by Name")
    print("2. Sort by Marks")

    choice = input("Choose option: ").strip()

    if choice == "1":
        sorted_students = sorted(
            students,
            key=lambda student: student["name"].lower()
        )

    elif choice == "2":
        sorted_students = sorted(
            students,
            key=lambda student: student["marks"],
            reverse=True
        )

    else:
        print("Invalid choice.")
        return

    display_students(sorted_students)


def export_to_csv(students):
    if not students:
        print("No data available to export.")
        return

    with open(
        "student_records.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Name",
            "Age",
            "Course",
            "Marks",
            "Registered On"
        ])

        for student in students:
            writer.writerow([
                student["id"],
                student["name"],
                student["age"],
                student["course"],
                student["marks"],
                student["registered_on"]
            ])

    print("CSV exported successfully.")
    print("File created: student_records.csv")


def show_menu():
    print("\n")
    print("=" * 40)
    print("STUDENT MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Statistics")
    print("7. Sort Students")
    print("8. Export to CSV")
    print("9. Exit")


def main():
    students = load_data()

    while True:
        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            display_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            show_statistics(students)

        elif choice == "7":
            sort_students(students)

        elif choice == "8":
            export_to_csv(students)

        elif choice == "9":
            print("Exiting application.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

