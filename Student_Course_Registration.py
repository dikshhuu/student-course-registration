import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector



def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="your_password_here",
        database="student_course_db",
        port=3306
    )



class StudentCourseRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Course Registration System")
        self.root.geometry("1200x750")
        self.root.minsize(1100, 650)
        self.root.resizable(True, True)
        self.selected_registration_id = None
        self.root.configure(bg="#eef2f7")

        title = tk.Label(
            root,
            text="Student Course Registration System",
            font=("Segoe UI", 22, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=18
        )
        title.pack(fill=tk.X)

        main_frame = tk.Frame(root, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_student_section(left_frame)
        self.create_course_section(left_frame)
        self.create_registration_section(left_frame)
        self.create_table_section(right_frame)

        self.load_students()
        self.load_courses()
        self.load_registrations()

    def create_student_section(self, parent):
        frame = tk.Frame(parent, bg="#ffffff", bd=0, highlightthickness=0)
        frame.pack(fill=tk.X, pady=10)

        title = tk.Label(
        frame,
        text="Add Student",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff",
        fg="#2f3640"
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0,10))

        tk.Label(frame, text="Student Name").grid(row=1, column=0, sticky="w",pady=5)
        self.student_name = tk.Entry(frame, width=35)
        self.student_name.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Email").grid(row=2, column=0, sticky="w", pady=5)
        self.student_email = tk.Entry(frame, width=35)
        self.student_email.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Phone").grid(row=3, column=0, sticky="w", pady=5)
        self.student_phone = tk.Entry(frame, width=35)
        self.student_phone.grid(row=3, column=1, pady=5)

        tk.Button(
            frame,
            text="Add Student",
            width=18,
            bg="#27ae60",
            fg="white",
            command=self.add_student
    ).grid(row=4, column=1, sticky="e", pady=10)
    

    def add_student(self):
        name = self.student_name.get().strip()
        email = self.student_email.get().strip()
        phone = self.student_phone.get().strip()

        if name == "" or email == "" or phone == "":
            messagebox.showwarning("Input Error", "Please fill all student fields.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Input Error", "Please enter a valid email address.")
            return

        if not phone.isdigit() or len(phone) < 7:
            messagebox.showwarning("Input Error", "Please enter a valid phone number.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)"
            values = (name, email, phone)

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Student added successfully.")

            self.student_name.delete(0, tk.END)
            self.student_email.delete(0, tk.END)
            self.student_phone.delete(0, tk.END)

            self.load_students()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

    

    def create_course_section(self, parent):
        frame = tk.LabelFrame(parent, text="Add Course", font=("Arial", 12, "bold"), padx=15, pady=10)
        frame.pack(fill=tk.X, pady=8)

        tk.Label(frame, text="Course Name").grid(row=0, column=0, sticky="w", pady=5)
        self.course_name = tk.Entry(frame, width=35)
        self.course_name.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Course Code").grid(row=1, column=0, sticky="w", pady=5)
        self.course_code = tk.Entry(frame, width=35)
        self.course_code.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Credit Hour").grid(row=2, column=0, sticky="w", pady=5)
        self.credit_hour = tk.Entry(frame, width=35)
        self.credit_hour.grid(row=2, column=1, pady=5)

        tk.Button(
            frame,
            text="Add Course",
            width=18,
            bg="#2980b9",
            fg="white",
            command=self.add_course
        ).grid(row=3, column=1, sticky="e", pady=10)

    def add_course(self):
        course_name = self.course_name.get().strip()
        course_code = self.course_code.get().strip()
        credit_hour = self.credit_hour.get().strip()

        if course_name == "" or course_code == "" or credit_hour == "":
            messagebox.showwarning("Input Error", "Please fill all course fields.")
            return

        if not credit_hour.isdigit():
            messagebox.showwarning("Input Error", "Credit hour must be a number.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "INSERT INTO courses (course_name, course_code, credit_hour) VALUES (%s, %s, %s)"
            values = (course_name, course_code, int(credit_hour))

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Course added successfully.")

            self.course_name.delete(0, tk.END)
            self.course_code.delete(0, tk.END)
            self.credit_hour.delete(0, tk.END)

            self.load_courses()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

   

    def create_registration_section(self, parent):
        frame = tk.LabelFrame(parent, text="Register Student to Course", font=("Arial", 12, "bold"), padx=15, pady=10)
        frame.pack(fill=tk.X, pady=8)

        tk.Label(frame, text="Select Student").grid(row=0, column=0, sticky="w", pady=5)
        self.student_combo = ttk.Combobox(frame, width=32, state="readonly")
        self.student_combo.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Select Course").grid(row=1, column=0, sticky="w", pady=5)
        self.course_combo = ttk.Combobox(frame, width=32, state="readonly")
        self.course_combo.grid(row=1, column=1, pady=5)

        tk.Button(
            frame,
            text="Register",
            width=18,
            bg="#8e44ad",
            fg="white",
            command=self.register_course
        ).grid(row=2, column=1, sticky="e", pady=10)

    def load_students(self):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT id, name FROM students ORDER BY name")
            students = cursor.fetchall()

            self.students_data = students
            self.student_combo["values"] = [f"{student[0]} - {student[1]}" for student in students]

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def load_courses(self):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name")
            courses = cursor.fetchall()

            self.courses_data = courses
            self.course_combo["values"] = [f"{course[0]} - {course[1]}" for course in courses]

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def register_course(self):
        selected_student = self.student_combo.get()
        selected_course = self.course_combo.get()

        if selected_student == "" or selected_course == "":
            messagebox.showwarning("Input Error", "Please select both student and course.")
            return

        student_id = selected_student.split(" - ")[0]
        course_id = selected_course.split(" - ")[0]

        try:
            connection = get_connection()
            cursor = connection.cursor()

            check_query = """
            SELECT * FROM registrations 
            WHERE student_id = %s AND course_id = %s
            """
            cursor.execute(check_query, (student_id, course_id))
            existing = cursor.fetchone()

            if existing:
                messagebox.showwarning("Duplicate", "This student is already registered for this course.")
                return

            query = "INSERT INTO registrations (student_id, course_id) VALUES (%s, %s)"
            values = (student_id, course_id)

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Student registered to course successfully.")

            self.student_combo.set("")
            self.course_combo.set("")

            self.load_registrations()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

   

    def create_table_section(self, parent):
        table_title = tk.Label(
            parent,
            text="Registered Students and Courses",
            font=("Arial", 14, "bold")
        )
        table_title.pack(anchor="w", pady=(0, 10))

        columns = ("id", "student_name", "email", "phone", "course_name", "course_code", "credit_hour", "date")

        self.registration_table = ttk.Treeview(parent, columns=columns, show="headings", height=18)

        self.registration_table.heading("id", text="ID")
        self.registration_table.heading("student_name", text="Student Name")
        self.registration_table.heading("email", text="Email")
        self.registration_table.heading("phone", text="Phone")
        self.registration_table.heading("course_name", text="Course")
        self.registration_table.heading("course_code", text="Code")
        self.registration_table.heading("credit_hour", text="Credit")
        self.registration_table.heading("date", text="Date")

        self.registration_table.column("id", width=40)
        self.registration_table.column("student_name", width=130)
        self.registration_table.column("email", width=150)
        self.registration_table.column("phone", width=100)
        self.registration_table.column("course_name", width=130)
        self.registration_table.column("course_code", width=80)
        self.registration_table.column("credit_hour", width=60)
        self.registration_table.column("date", width=140)

        self.registration_table.pack(fill=tk.BOTH, expand=True)

        self.registration_table.bind("<<TreeviewSelect>>", self.select_registration)

        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=15)

        tk.Button(
            button_frame,
            text="Refresh",
            width=18,
            bg="#16a085",
            fg="white",
            command=self.load_registrations
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Delete Selected Registration",
            width=25,
            bg="#c0392b",
            fg="white",
            command=self.delete_registration
        ).pack(side=tk.LEFT, padx=5)

    def load_registrations(self):
        for row in self.registration_table.get_children():
            self.registration_table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

        
            query = """
            SELECT 
                registrations.id,
                students.name,
                students.email,
                students.phone,
                courses.course_name,
                courses.course_code,
                courses.credit_hour,
                registrations.registration_date
            FROM registrations
            JOIN students ON registrations.student_id = students.id
            JOIN courses ON registrations.course_id = courses.id
            ORDER BY registrations.id DESC
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                self.registration_table.insert("", tk.END, values=row)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

        finally:
            cursor.close()
            connection.close()

    def select_registration(self, event):
        selected = self.registration_table.focus()

        if selected:
            values = self.registration_table.item(selected, "values")
            self.selected_registration_id = values[0]

    def delete_registration(self):
        if self.selected_registration_id is None:
            messagebox.showwarning("Selection Error", "Please select a registration to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this registration?")

        if confirm:
            try:
                connection = get_connection()
                cursor = connection.cursor()

                query = "DELETE FROM registrations WHERE id = %s"
                cursor.execute(query, (self.selected_registration_id,))
                connection.commit()

                messagebox.showinfo("Deleted", "Registration deleted successfully.")

                self.selected_registration_id = None
                self.load_registrations()

            except mysql.connector.Error as error:
                messagebox.showerror("Database Error", str(error))

            finally:
                cursor.close()
                connection.close()




if __name__ == "__main__":
    root = tk.Tk()
    app = StudentCourseRegistrationApp(root)
    root.mainloop()