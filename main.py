from tkinter import *
import os
import csv
import random


class EndMenu:
    def restart(self):
        self.root.destroy()
        Game(self.csvset)

    def go_to_menu(self):
        self.root.destroy()
        Menu()

    def __init__(self, score, accuracy, csvset):
        self.csvset = csvset
        self.root = Tk()
        self.root.title("Good Game")
        self.root.geometry("500x300")

        self.title = Label(text="You win", font=("Segoe UI Black", 38))
        self.title.pack()

        self.scoretitle = Label(text="Score", font=("Arial Black", 24))
        self.scoretitle.place(relx=0.1, rely=0.3, anchor=W)
        self.score = Label(text=score, font=("Arial", 24))
        self.score.place(relx=0.1, rely=0.5, anchor=W)

        self.accuracytitle = Label(text="Accuracy", font=("Arial Black", 24))
        self.accuracytitle.place(relx=0.9, rely=0.3, anchor=E)
        self.accuracy = Label(text=accuracy, font=("Arial", 24))
        self.accuracy.place(relx=0.9, rely=0.5, anchor=E)

        self.restartbutton = Button(text="Restart", font=("Liberation Mono", 24), command=self.restart)
        self.restartbutton.place(relx=0.1, rely=0.8, relheight=0.3, relwidth=0.3, anchor=W)

        self.menubutton = Button(text="Menu", font=("Liberation Mono", 24), command=self.go_to_menu)
        self.menubutton.place(relx=0.9, rely=0.8, relheight=0.3, relwidth=0.3, anchor=E)

        self.root.mainloop()


class Game:
    def endGame(self):
        total = self.correctGuesses + self.wrongGuesses
        accuracy = str(round(self.correctGuesses / total * 100, 2)) + "%"
        self.root.destroy()
        EndMenu(f"{self.correctGuesses}/{total}", accuracy, self.csvset)

    def getRandom(self):  # random question
        key, value = random.choice(list(self.set.items()))
        if random.randint(1, 2) == 1:
            self.question = key
            self.answer = value
        else:
            self.question = value
            self.answer = key
        self.question_label['text'] = self.question

    def check(self, text):
        self.entry.delete(0, 'end')
        if text == self.answer:
            self.set = {key: val for key, val in self.set.items() if not (val == self.answer or key == self.answer)}
            self.correctGuesses += 1
            if len(self.set) > 0:
                self.getRandom()
            else:
                self.endGame()
        else:
            self.wrongGuesses += 1
            self.getRandom()
        total = self.correctGuesses + self.wrongGuesses
        self.progress['text'] = f"{self.correctGuesses}/{self.total}"

    def __init__(self, csvset):
        self.csvset = csvset
        self.root = Tk()
        self.root.title("Word Learner")
        self.root.geometry("500x300")

        self.question = None
        self.answer = None

        self.correctGuesses = 0
        self.wrongGuesses = 0

        self.question_label = Label(self.root, text="Question", font=("Consolas Bold", 48))
        self.question_label.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.entry = Entry(self.root, font=("Fixedsys", 60))
        self.entry.place(anchor=N, rely=0.3, relx=0.5, relheight=0.5, relwidth=0.95)
        self.entry.bind("<Return>", (lambda event: self.check(self.entry.get())))

        self.progress = Label(self.root, text="0/10", font=("Consolas", 24))
        self.progress.place(relx=0.5, rely=0.95, anchor="s")

        try:
            with open(f"sets/{csvset}", 'r') as file:
                reader = csv.reader(file, delimiter=":")
                self.set = {rows[0]: rows[1] for rows in reader}
                self.total = len(self.set)
        except IndexError:
            self.question_label['text'] = "CSV ERROR"

        self.progress['text'] = f"0/{self.total}"

        self.getRandom()
        self.root.mainloop()


class Menu():
    def __init__(self):
        sets = os.listdir("sets")
        print(f"Loaded sets: {sets}")

        self.root = Tk()
        self.root.title("Word Learner")
        self.root.geometry("500x300")

        self.title = Label(self.root, text="Welcome", font=("Source Sans Pro Light", 36))
        self.title.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.listbox = Listbox(self.root, selectmode=SINGLE)
        self.listbox.place(anchor=N, rely=0.2, relx=0.5, relheight=0.3, relwidth=0.95)
        for i, v in enumerate(sets):
            self.listbox.insert(i, v)

        self.button = Button(self.root, text="Begin", font=("Source Sans Pro", 26), command=self.start_game)
        self.button.place(anchor=N, rely=0.6, relx=0.5, relheight=0.3, relwidth=0.5)
        self.root.mainloop()

    def start_game(self):
        selection = self.listbox.get(ANCHOR)
        if selection:
            self.root.destroy()
            Game(selection)


menu = Menu()
