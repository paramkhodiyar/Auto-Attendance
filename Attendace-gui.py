import qrcode
import sqlite3
import customtkinter
from PIL import Image
from customtkinter import *
from tkinter import NORMAL, DISABLED  # Import constants here


# Initialize the database
def init_db():
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("DROP TABLE IF EXISTS teachers")
    cursor.execute("DROP TABLE IF EXISTS attendance")

    # Create tables with the correct schema
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS students (
                        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS teachers (
                        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tcode TEXT UNIQUE NOT NULL,
                        tname TEXT NOT NULL,
                        password TEXT NOT NULL)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        tcode TEXT,
                        date TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        FOREIGN KEY(student_id) REFERENCES students(student_id))"""
    )
    connection.commit()
    connection.close()


init_db()

# Login window setup
login_window = customtkinter.CTk()
login_window.title("Attendance App")
login_window.geometry("350x500")
customtkinter.set_appearance_mode("dark")

title = customtkinter.CTkLabel(
    login_window, text="Login", font=("Helvetica", 18, "bold")
)
title.grid(row=0, column=0, padx=20, pady=10)

username_entry = customtkinter.CTkEntry(
    login_window, width=300, placeholder_text="Username"
)
username_entry.grid(row=1, column=0, padx=20, pady=10)

password_entry = customtkinter.CTkEntry(
    login_window, width=300, show="*", placeholder_text="Password"
)
password_entry.grid(row=2, column=0, padx=20, pady=10)

message_label = customtkinter.CTkLabel(login_window, text="")
message_label.grid(row=3, column=0, padx=20, pady=10)


def login_user():
    username = username_entry.get()
    password = password_entry.get()
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE username=? AND password=?", (username, password)
    )
    user = cursor.fetchone()
    connection.close()

    if user:
        message_label.configure(text="Login successful!", text_color="green")
        login_window.destroy()
        open_student_app(user[0])
    else:
        message_label.configure(text="Invalid username or password!", text_color="red")


def login_teacher():
    tcode = username_entry.get()
    password = password_entry.get()
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM teachers WHERE tcode=? AND password=?", (tcode, password)
    )
    teacher = cursor.fetchone()
    connection.close()

    if teacher:
        message_label.configure(text="Login successful!", text_color="green")
        login_window.destroy()
        open_teacher_app(teacher[0])
    else:
        message_label.configure(text="Invalid TCODE or password!", text_color="red")


student_login_button = customtkinter.CTkButton(
    login_window, text="Student Login", command=login_user, width=300
)
student_login_button.grid(row=4, column=0, padx=20, pady=10)

teacher_login_button = customtkinter.CTkButton(
    login_window, text="Teacher Login", command=login_teacher, width=300
)
teacher_login_button.grid(row=5, column=0, padx=20, pady=10)


def open_register_window(user_type):
    register_window = customtkinter.CTk()
    register_window.title(f"Register {user_type.capitalize()}")
    register_window.geometry("350x500")
    customtkinter.set_appearance_mode("dark")

    title = customtkinter.CTkLabel(
        register_window,
        text=f"Register {user_type.capitalize()}",
        font=("Helvetica", 18, "bold"),
    )
    title.grid(row=0, column=0, padx=20, pady=10)

    if user_type == "student":
        username_entry = customtkinter.CTkEntry(
            register_window, width=300, placeholder_text="Username"
        )
        username_entry.grid(row=1, column=0, padx=20, pady=10)

        password_entry = customtkinter.CTkEntry(
            register_window, width=300, show="*", placeholder_text="Password"
        )
        password_entry.grid(row=2, column=0, padx=20, pady=10)

        def register():
            username = username_entry.get()
            password = password_entry.get()
            connection = sqlite3.connect("attendance.db")
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO students (username, password) VALUES (?, ?)",
                    (username, password),
                )
                connection.commit()
                message_label.configure(
                    text="Registration successful!", text_color="green"
                )
                register_window.destroy()
            except sqlite3.IntegrityError:
                message_label.configure(
                    text="Username already exists!", text_color="red"
                )
            connection.close()

    elif user_type == "teacher":
        tcode_entry = customtkinter.CTkEntry(
            register_window, width=300, placeholder_text="TCODE"
        )
        tcode_entry.grid(row=1, column=0, padx=20, pady=10)

        tname_entry = customtkinter.CTkEntry(
            register_window, width=300, placeholder_text="Name"
        )
        tname_entry.grid(row=2, column=0, padx=20, pady=10)

        password_entry = customtkinter.CTkEntry(
            register_window, width=300, show="*", placeholder_text="Password"
        )
        password_entry.grid(row=3, column=0, padx=20, pady=10)

        def register():
            tcode = tcode_entry.get()
            tname = tname_entry.get()
            password = password_entry.get()
            connection = sqlite3.connect("attendance.db")
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "INSERT INTO teachers (tcode, tname, password) VALUES (?, ?, ?)",
                    (tcode, tname, password),
                )
                connection.commit()
                message_label.configure(
                    text="Registration successful!", text_color="green"
                )
                register_window.destroy()
            except sqlite3.IntegrityError:
                message_label.configure(text="TCODE already exists!", text_color="red")
            connection.close()

    message_label = customtkinter.CTkLabel(register_window, text="")
    message_label.grid(row=4, column=0, padx=20, pady=10)

    register_button = customtkinter.CTkButton(
        register_window, text="Register", command=register, width=300
    )
    register_button.grid(row=5, column=0, padx=20, pady=10)

    register_window.mainloop()


register_student_button = customtkinter.CTkButton(
    login_window,
    text="Register Student",
    command=lambda: open_register_window("student"),
    width=300,
)
register_student_button.grid(row=6, column=0, padx=20, pady=10)

register_teacher_button = customtkinter.CTkButton(
    login_window,
    text="Register Teacher",
    command=lambda: open_register_window("teacher"),
    width=300,
)
register_teacher_button.grid(row=7, column=0, padx=20, pady=10)


# Student app
def open_student_app(student_id):
    student_app = customtkinter.CTk()
    student_app.title("Student Attendance App")
    student_app.geometry("350x500")

    def scan_qr():
        # QR code scanning logic goes here
        pass

    scan_button = customtkinter.CTkButton(
        student_app, text="Scan QR Code", command=scan_qr, width=300
    )
    scan_button.grid(row=0, column=0, padx=20, pady=10)

    student_app.mainloop()


# Teacher app
def open_teacher_app(teacher_id):
    teacher_app = customtkinter.CTk()
    teacher_app.title("Teacher Attendance App")
    teacher_app.geometry("350x500")

    def generate_qr(data, filename):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{filename}.png")

        my_image = customtkinter.CTkImage(
            light_image=Image.open(f"{filename}.png"),
            dark_image=Image.open(f"{filename}.png"),
            size=(200, 200),
        )
        image_label.configure(image=my_image)
        image_label.image = my_image  # Keep a reference to avoid garbage collection

    def start_class():
        tcode = tcode_entry.get()
        if not tcode:
            message_label.configure(text="Please enter a TCODE!", text_color="red")
            return

        date_of_class = date_entry.get()
        if not date_of_class:
            message_label.configure(
                text="Please enter a valid date (dd/mm/yyyy)!", text_color="red"
            )
            return

        qr_data = f"TCODE: {tcode}, Date: {date_of_class}, Start Time: -"
        generate_qr(qr_data, "start_class")
        end_button.configure(state=NORMAL)

    def end_class():
        tcode = tcode_entry.get()
        if not tcode:
            message_label.configure(text="Please enter a TCODE!", text_color="red")
            return

        date_of_class = date_entry.get()
        if not date_of_class:
            message_label.configure(
                text="Please enter a valid date (dd/mm/yyyy)!", text_color="red"
            )
            return

        qr_data = f"TCODE: {tcode}, Date: {date_of_class}, End Time: -"
        generate_qr(qr_data, "end_class")

    header_label = customtkinter.CTkLabel(
        teacher_app, text="Anti Proxy Software", font=("Helvetica", 18, "bold")
    )
    header_label.grid(row=0, column=0, padx=20, pady=10)

    tcode_entry = customtkinter.CTkEntry(
        teacher_app, width=300, placeholder_text="TCODE"
    )
    tcode_entry.grid(row=1, column=0, padx=20, pady=10)

    date_entry = customtkinter.CTkEntry(
        teacher_app, width=300, placeholder_text="dd/mm/yyyy"
    )
    date_entry.grid(row=2, column=0, padx=20, pady=10)

    message_label = customtkinter.CTkLabel(teacher_app, text="")
    message_label.grid(row=3, column=0, padx=20, pady=10)

    image_label = customtkinter.CTkLabel(teacher_app, image=None, text="")
    image_label.grid(row=4, column=0, padx=20, pady=20)

    start_button = customtkinter.CTkButton(
        teacher_app, text="Start Class", command=start_class, width=300, state=NORMAL
    )
    start_button.grid(row=5, column=0, padx=20, pady=10)

    end_button = customtkinter.CTkButton(
        teacher_app, text="End Class", command=end_class, width=300, state=DISABLED
    )
    end_button.grid(row=6, column=0, padx=20, pady=10)

    teacher_app.mainloop()


login_window.mainloop()
