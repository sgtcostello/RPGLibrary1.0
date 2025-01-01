# Import Libraries
from tkinter import Tk, Frame, Text, Label, Button, Entry, Toplevel, StringVar, END
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3

# Centering the window function
def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Database setup function
def setup_database():
    conn = sqlite3.connect('ttrpg_world.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL,
        tags TEXT,
        image_path TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to add an article to the database
def add_article(title, content, category, tags=None, image_path=None):
    conn = sqlite3.connect('ttrpg_world.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO articles (title, content, category, tags, image_path)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, content, category, tags, image_path))
    conn.commit()
    conn.close()

# Function to search the database
def search_database(query):
    conn = sqlite3.connect('ttrpg_world.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, content, category, tags, image_path FROM articles WHERE title LIKE ? OR content LIKE ?',
                   (f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results

# GUI Setup
def create_gui():
    root = Tk()
    root.title("Towermourne Knowledge Base")
    root.configure(bg="#FDF5E6")
    center_window(root, 800, 600)

    # Top Banner
    banner_frame = Frame(root, bg="#FDF5E6")
    banner_frame.pack(fill="x", pady=5)

    search_button = Button(banner_frame, text="Search", command=lambda: open_search_screen(root), bg="#FDF5E6")
    search_button.pack(side="left", padx=10)

    add_button = Button(banner_frame, text="Add Article", command=lambda: open_add_article_screen(root), bg="#FDF5E6")
    add_button.pack(side="left", padx=10)

    # Welcome Message
    welcome_frame = Frame(root, bg="#FDF5E6")
    welcome_frame.pack(expand=True)  # Center vertically and horizontally

    welcome_label = Label(
        welcome_frame,
        text="Welcome to the Library.\nWhat would you like to do?",
        bg="#FDF5E6",
        font=("Times New Roman", 16, "bold"),
        justify="center"
    )
    welcome_label.pack()

    root.mainloop()

# Function for search screen
def open_search_screen(parent):
    search_screen = Toplevel(parent)
    search_screen.title("Search Articles")
    search_screen.configure(bg="#FDF5E6")
    center_window(search_screen, 800, 600)

    # Top: Search Bar
    search_bar_frame = Frame(search_screen, bg="#FDF5E6")
    search_bar_frame.pack(fill="x", pady=10)

    search_var = StringVar()
    search_entry = Entry(search_bar_frame, textvariable=search_var, width=50, font=("Times New Roman", 14))
    search_entry.pack(side="left", padx=10)

    def execute_search():
        query = search_var.get()
        results = search_database(query)
        results_box.delete('1.0', END)
        image_label.config(image="")  # Clear the image
        tags_label.config(text="")  # Clear tags

        if results:
            for title, content, category, tags, image_path in results:
                results_box.insert(END, f"Title: {title}\n")
                results_box.insert(END, f"Content: {content}\n")
                results_box.insert(END, f"Category: {category}\n")
                results_box.insert(END, "-" * 40 + "\n")

                # Display tags
                tags_label.config(text=f"Tags: {tags if tags else 'None'}")

                if image_path:
                    try:
                        img = Image.open(image_path)
                        img = img.resize((200, 200), Image.Resampling.LANCZOS)
                        img = ImageTk.PhotoImage(img)
                        image_label.config(image=img)
                        image_label.image = img  # Prevent garbage collection
                    except Exception as e:
                        results_box.insert(END, f"Error loading image: {e}\n")
        else:
            results_box.insert(END, "No results found.\n")
            tags_label.config(text="")

    search_button = Button(search_bar_frame, text="Search", command=execute_search, bg="#FDF5E6")
    search_button.pack(side="left", padx=10)

    # Left: Search Results
    content_frame = Frame(search_screen, bg="#FDF5E6")
    content_frame.pack(fill="both", expand=True)

    search_frame = Frame(content_frame, bg="#FDF5E6")
    search_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    Label(search_frame, text="Search Results", bg="#FDF5E6", font=("Times New Roman", 14, "bold")).pack()
    results_box = Text(search_frame, height=20, width=60, wrap='word', bg="#FDF5E6", font=("Times New Roman", 12))
    results_box.pack(padx=10, pady=10)

    # Right: Image Display
    image_frame = Frame(content_frame, bg="#FDF5E6")
    image_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    Label(image_frame, text="Image", bg="#FDF5E6", font=("Times New Roman", 14, "bold")).pack()
    image_label = Label(image_frame, bg="#FDF5E6")
    image_label.pack(anchor="center", pady=10)

    # Bottom: Tags Display
    tags_frame = Frame(search_screen, bg="#D2B48C")  # Light brown background
    tags_frame.pack(fill="x", pady=5)

    tags_label = Label(tags_frame, text="Tags: None", bg="#D2B48C", font=("Times New Roman", 12), anchor="w")
    tags_label.pack(padx=10, pady=5, anchor="w")

# Add Article Screen
def open_add_article_screen(parent):
    add_screen = Toplevel(parent)
    add_screen.title("Add Article")
    add_screen.configure(bg="#FDF5E6")
    center_window(add_screen, 600, 400)

    title_var = StringVar()
    content_var = StringVar()
    category_var = StringVar()
    tags_var = StringVar()
    image_path_var = StringVar()

    Label(add_screen, text="Title:", bg="#FDF5E6").pack()
    Entry(add_screen, textvariable=title_var).pack()

    Label(add_screen, text="Content:", bg="#FDF5E6").pack()
    Entry(add_screen, textvariable=content_var).pack()

    Label(add_screen, text="Category:", bg="#FDF5E6").pack()
    Entry(add_screen, textvariable=category_var).pack()

    Label(add_screen, text="Tags:", bg="#FDF5E6").pack()
    Entry(add_screen, textvariable=tags_var).pack()

    def upload_image():
        file_path = filedialog.askopenfilename()
        image_path_var.set(file_path)

    Button(add_screen, text="Upload Image", command=upload_image).pack()

    def save_article():
        add_article(title_var.get(), content_var.get(), category_var.get(), tags_var.get(), image_path_var.get())
        messagebox.showinfo("Success", "Article added successfully!")
        add_screen.destroy()

    Button(add_screen, text="Save Article", command=save_article).pack()

# Run the Program
if __name__ == "__main__":
    setup_database()
    create_gui()
