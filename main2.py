from tkinter import Tk,Label,Button,END,messagebox,ttk
import sqlite3

def init_db():
    try:
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            author TEXT,
                            year INTEGER,
                            quantity INTEGER,
                            price REAL)''')
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Datubazes kluda", f"Neizdevas inicializet datubazi:{e}")

def load_book_titles():
    try:
        book_combobox['values']=()
        conn=sqlite3.connect('library.db')
        cursor=conn.cursor()
        cursor.execute("SELECT title FROM books")
        titles=[]
        title_all=cursor.fetchall()
        for title in title_all:
            titles.append(title[0])
        conn.close

        book_combobox['values']=titles
    except Exception as e:
        messagebox.showerror("Kluda", f"Neizdevas nolasit gramatu nosaukumu: {e}")

def show_book_details():
    try:
        selected_title=book_combobox.get()
        if not selected_title:
            messagebox.showwarning('Bridinajums', "Ludzu izveleties grāmatu no saraksta.")
            return
        
        conn=sqlite3.connect('library.db')
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM books WHERE title=?', (selected_title,))
        book=cursor.fetchone()
        conn.close()

        if book:
            price=f'{float(book[5]):.2f}'
            messagebox.showinfo('Gramatas informacija', f'Nosaukums:{book[1]}\nAutors: {book[2]}\nSkaits: {book[4]}\nCena: {price}')
        else:
            messagebox.showwarning('Kluda', 'Neizdevas atrast informaciju par gramatu.')
    except Exception as e:
        messagebox.showerror('Kluda', f'Neizdevas paradit gramatas informaciju: {e}')

root=Tk()
root.title('Biblioteka gramatu sistema')

Label(root,text='Izveleties gramatu:').grid(row=0,column=0,padx=10,pady=10)
book_combobox=ttk.Combobox(root,width=47,state='readonly')
book_combobox.grid(row=1,column=0,padx=10,pady=10)

Button(root, text='radit informaciju', command=show_book_details).grid(row=2, column=0,padx=10,pady=10)
init_db()
load_book_titles()
root.mainloop()



   