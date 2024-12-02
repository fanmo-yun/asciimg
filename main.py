from interface import interface

app = interface()
app.layout()
app.layup()

if __name__ == "__main__":
    app.protocol("WM_DELETE_WINDOW", app.delete_temp_files)
    app.mainloop()
