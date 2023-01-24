"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
StudentId: 151237366
Name:      Oskari Kuisma
Email:     oskari.kuisma@tuni.fi

PROJECT 5: Click speed test - CPS test

This is a simple program that tells the user how fast they can click in 5 seconds. (Clicks Per Second)
The user can challenge themselves to beat their previous highscore.
The program also tells the what kind of animal they are based on their clicking speed.
"""

from tkinter import *
import time


class CPS:

    def __init__(self):
        self.__mainwindow = Tk()

        self.__welcome_text_1 = Label(self.__mainwindow, text=f"Hello!", font=('Arial',17,'bold'))
        self.__welcome_text_1.grid(row=1, column=2)

        self.__welcome_text_2 = Label(self.__mainwindow, text="Welcome to the Click Speed test.", font=('Arial',17,'bold'))
        self.__welcome_text_2.grid(row=2, column=2)

        self.__start_button = Button(self.__mainwindow, text="START", bg='green',\
                                     font=('Arial',17,'bold'), command=self.start)
        self.__start_button.grid(row=3, column=2, sticky=W)

        self.__quit_button = Button(self.__mainwindow, text="QUIT",bg='red',\
                                    font=('Arial', 17, 'bold'), command=self.quit)
        self.__quit_button.grid(row=3, column=2, sticky=E)

        self.__mainwindow.mainloop()


    def quit(self):
        """
        This method stops the whole program.
        """

        self.__mainwindow.destroy()


    def start(self):
        """
        This method is implemented when the user presses the start button. It tells the
        user some information. When the user clicks the "Click"-button, it calls the increase and
        start timer methods. The click value increases on the screen as the user presses the button.
        """

        # Destroy everything on the start screen
        self.__start_button.destroy()
        self.__quit_button.destroy()
        self.__welcome_text_1.destroy()
        self.__welcome_text_2.destroy()

        self.__game_info_1 = Label(self.__mainwindow, text=f"Let's see how many times", font=('Arial',17,'bold'))
        self.__game_info_1.grid(row=1, column=2)

        self.__game_info_2 = Label(self.__mainwindow, text="you can click in 5 seconds.", font=('Arial',17,'bold'))
        self.__game_info_2.grid(row=2, column=2)

        self.__timer = Label(self.__mainwindow, text="5.00", font=('Arial',22,'bold'))
        self.__timer.grid(row=3, column=2)

        # Set the bool value to false for the timer method (explained later why)
        self.__flag = False

        self.__click_value = 0
        # When the user clicks the "Click"-button, the click value increases and the timer starts.
        self.__click_button = Button(self.__mainwindow, text=f"Clicks: {self.__click_value}",\
                                     font=('Arial',23,'bold'), bg='yellow', \
                                     command=lambda: [self.increase(),self.start_timer()], padx=100, pady = 50)
        self.__click_button.grid(row=4, column=2)

        # Current hichcore is 0, because the user has yet to test their skills
        self.__high_score = 0
        self.__highscore_label = Label(self.__mainwindow, text=f"Current highscore: {self.__high_score:.2f} CPS", font=('Arial',19,'bold'))
        self.__highscore_label.grid(row=5, column=2)


    def increase(self):
        """
        This function increases the click-value everytime the
        "Click"-button is pressed
        """

        self.__click_value += 1
        self.__click_button.config(text=f"Clicks: {self.__click_value}")


    def start_timer(self):
        """
        This funktion starts the timer and cleverly uses a bool value
        to determine if the "Click"-button has been pressed once. This way
        The countdown doesnt start again everytime the "Click"-button is pressed.
        After the countdown has finished, it calls the show results method.
        """

        if not self.__flag:
            # get the current time
            current_time = time.time()
            # calculate the end time (5 seconds from now)
            end_time = current_time + 5

            # update the label with the remaining time until the end
            while time.time() < end_time:
                self.__flag = True
                # calculate the remaining time
                remaining = end_time - time.time()
                # format the remaining time as a string
                remaining_str = "{:.3f}".format(remaining)
                # update the label with the remaining time
                self.__timer.config(text=remaining_str)
                # refresh the label
                self.__timer.update()

            self.show_results()


    def show_results(self):
        """
        This method displays the results of the test. If the user beats their
        highscore, the program will print the new score. Else it will just print
        countdown finished. It will also tell the user what kind of animal they
        are based on their clicking speed. After the results the user can decide to
        play again or quit. Try again button calls the restart method.
        """

        #  Destroy things on the screen
        self.__click_button.destroy()
        self.__highscore_label.destroy()
        self.__game_info_1.destroy()
        self.__game_info_2.destroy()

        # update the timer label with the final message
        if self.__click_value / 5 > self.__high_score:
            self.__timer.config(text=f"New highscore of {self.__click_value / 5:.2f} CPS!")
            # Set the new hich
            self.__high_score = self.__click_value / 5
        else:
            self.__timer.config(text="Countdown finished!")

        # Determine the type of animal
        if 0 < self.__click_value <= 10:
            self.__animal_type = Label(self.__mainwindow, text=f"You are a Snail!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif 10 < self.__click_value <= 20:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Turtle!", font=('Arial', 20, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif 20 < self.__click_value <= 30:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Mouse!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif 30 < self.__click_value <= 45:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Fox!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif 45 < self.__click_value <= 55:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Cheetah!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif 55 < self.__click_value <= 65:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Sailfish!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        elif self.__click_value > 65:

            self.__animal_type = Label(self.__mainwindow, text=f"You are a Peregrine Falcon!", font=('Arial', 22, 'bold'))
            self.__animal_type.grid(row=4, column=2)

        self.__result_label_1 = Label(self.__mainwindow,
                                      text=f"You clicked {self.__click_value} times in 5 seconds,", \
                                      font=('Arial', 19, 'bold'))
        self.__result_label_1.grid(row=5, column=2)

        self.__result_label_2 = Label(self.__mainwindow,
                                      text=f"resulting in a score of {self.__click_value / 5:.2f} CPS", \
                                      font=('Arial', 19, 'bold'))
        self.__result_label_2.grid(row=6, column=2)

        self.__quit_button = self.__quit_button = Button(self.__mainwindow, text="QUIT",bg='red',\
                                    font=('Arial', 19, 'bold'), command=self.quit)

        self.__quit_button.grid(row=7, column=2, sticky=E)

        self.__restart_button = Button(self.__mainwindow, text="Try again?", bg='green',\
                                       font=('Arial', 19, 'bold'), command=self.restart)
        self.__restart_button.grid(row=7, column=2, sticky=W)


    def restart(self):
        """
        This method is similar to the start method. When the user
        clicks the "Click"-button, it calls the increase and
        start timer methods. The click value increases on
        the screen as the user presses the button. Then the start timer
        calls method the show results method, which then calls this method, creating
        a sort of a loop.
        """

        # Destroy things on the screen
        self.__animal_type.destroy()
        self.__result_label_1.destroy()
        self.__result_label_2.destroy()
        self.__quit_button.destroy()
        self.__restart_button.destroy()
        self.__timer.destroy()

        # Reset the bool value
        self.__flag = False

        self.__game_info_1 = Label(self.__mainwindow, text=f"Let's see how many times", font=('Arial', 17, 'bold'))
        self.__game_info_1.grid(row=1, column=2)

        self.__game_info_2 = Label(self.__mainwindow, text="you can click in 5 seconds.", font=('Arial', 17, 'bold'))
        self.__game_info_2.grid(row=2, column=2)

        self.__timer = Label(self.__mainwindow, text="5.00", font=('Arial', 22, 'bold'))
        self.__timer.grid(row=3, column=2)

        # Reset the click value
        self.__click_value = 0
        self.__click_button = Button(self.__mainwindow, text=f"Clicks: {self.__click_value}", \
                                     font=('Arial', 23, 'bold'), bg='yellow', \
                                     command=lambda: [self.increase(), self.start_timer()], padx=100, pady=50)
        self.__click_button.grid(row=4, column=2)

        # Current highscore is displayed
        self.__highscore_label = Label(self.__mainwindow, text=f"Current highscore: {self.__high_score:.2f} CPS",
                                       font=('Arial', 19, 'bold'))
        self.__highscore_label.grid(row=5, column=2)


def main():

  CPS()

if __name__ == "__main__":
  main()