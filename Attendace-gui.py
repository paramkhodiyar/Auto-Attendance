import qrcode
import customtkinter
from PIL import Image
import mysql.connector
from customtkinter import *
from mysql.connector import Error

app = customtkinter.CTk()
app.title("QR Code Generator")
app.geometry("350x500")

img = None
tcode = None
qr_data = None
date_of_class = None  

def generate_qr(data, filename):
    global img
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{filename}.png")

    
    my_image = customtkinter.CTkImage(light_image=Image.open(f"{filename}.png"),
                                      dark_image=Image.open(f"{filename}.png"),
                                      size=(200, 200))
    image_label.configure(image=my_image)

def start_class():
    global tcode, qr_data
    tcode = tcode_entry.get()

    if not tcode:
        message_label.configure(text="Please enter a TCODE!", text_color="red")
        return

    global date_of_class
    qr_data = f"TCODE: {tcode}, Date: {date_of_class}, Start Time: -"
    generate_qr(qr_data, "start_class")
    end_button.configure(state=NORMAL)

def end_class():
    global tcode, qr_data
    if not tcode:
        message_label.configure(text="Please enter a TCODE!", text_color="red")
        return

    if not qr_data:
        message_label.configure(text="Please press Start Class first!", text_color="red")
        return

    qr_data = f"TCODE: {tcode}, Date: {date_of_class}, End Time: -"
    generate_qr(qr_data, "end_class")

    
    tcode_entry.delete(0, END)
    tcode = None
    qr_data = None

    
    end_button.configure(state=DISABLED)
    start_button.configure(state=DISABLED)

def enable_start_button():
    if tcode_entry.get():
        start_button.configure(state=NORMAL)
    else:
        start_button.configure(state=DISABLED)

def check_tcode():
    global tcode
    tcode = tcode_entry.get()

    if not tcode:
        message_label.configure(text="Please enter a TCODE!", text_color="red")
        return

    connection = None  

    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='UNIV_EX',
            user='root')

        cursor = connection.cursor()
        query = "SELECT Tname FROM teachers WHERE Tcode = %s"
        cursor.execute(query, (tcode,))
        result = cursor.fetchone()

        if result:
            tname = result[0]
            message_label.configure(text=f"Welcome, {tname}!", text_color="green")
            start_button.configure(state=NORMAL)
        else:
            message_label.configure(text="Invalid TCODE!", text_color="red")
            start_button.configure(state=DISABLED)

    except Error as e:
        message_label.configure(text=f"Error: {e}", text_color="red")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def create_table():
    global date_of_class
    date_of_class = table_name_entry.get()

    if not date_of_class:
        message_label.configure(text="Please enter a valid date (dd/mm/yyyy)!", text_color="red")
        return

    date_parts = date_of_class.split('/')
    if len(date_parts) != 3 or not all(part.isdigit() for part in date_parts):
        message_label.configure(text="Invalid date format. Please use dd/mm/yyyy!", text_color="red")
        return

    day, month, year = date_parts
    date_of_class = f"{year}-{month}-{day}"  

    connection = None  

    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='UNIV_EX',
            user='root')

        cursor = connection.cursor()
        create_table_query = f"CREATE TABLE IF NOT EXISTS attendance_{day}_{month}_{year} (id INT AUTO_INCREMENT PRIMARY KEY, Tcode VARCHAR(10), Tname VARCHAR(50), Subject VARCHAR(50), Department VARCHAR(50), A_P VARCHAR(10))"
        cursor.execute(create_table_query)
        message_label.configure(text=f"Table attendance_{day}_{month}_{year} created successfully!", text_color="green")

    except Error as e:
        message_label.configure(text=f"Error: {e}", text_color="red")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



header_label = customtkinter.CTkLabel(app, text="Anti Proxy Software", font=("Helvetica", 18, "bold"))
header_label.grid(row=0, column=0, padx=20, pady=10)


tcode_entry = customtkinter.CTkEntry(app, width=300)
tcode_entry.grid(row=1, column=0, padx=20, pady=10)
tcode_entry.configure(placeholder_text="TCODE")

enter_button = customtkinter.CTkButton(app, text="Enter", command=check_tcode, width=300)
enter_button.grid(row=2, column=0, padx=20, pady=10)


table_name_label = customtkinter.CTkLabel(app, text="Enter Date (dd/mm/yyyy):")
table_name_label.grid(row=3, column=0, padx=20, pady=10)

table_name_entry = customtkinter.CTkEntry(app, width=300)
table_name_entry.grid(row=4, column=0, padx=20, pady=10)
table_name_entry.configure(placeholder_text="dd/mm/yyyy")

create_table_button = customtkinter.CTkButton(app, text="Create Table", command=create_table, width=300)
create_table_button.grid(row=5, column=0, padx=20, pady=10)


message_label = customtkinter.CTkLabel(app, text="")
message_label.grid(row=6, column=0, padx=20, pady=10)


image_label = customtkinter.CTkLabel(app, image=None, text="") 
image_label.grid(row=7, column=0, padx=20, pady=20)


start_button = customtkinter.CTkButton(app, text="Start Class", command=start_class, width=300, state=DISABLED)
start_button.grid(row=8, column=0, padx=20, pady=10)

end_button = customtkinter.CTkButton(app, text="End Class", command=end_class, width=300, state=DISABLED)
end_button.grid(row=9, column=0, padx=20, pady=10)

app.mainloop()
