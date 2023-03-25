# import kivy
from kivy.app import App
# from kivy.uix.label import Label
from kivy.uix.button import Button
import pyttsx3


class MyApp(App):
    def build(self):
        btn = Button(text="Activate", size_hint=(.10, .20))
        btn.bind(on_press=self.callback)
        return btn

    @staticmethod
    def callback(event):
        engine = pyttsx3.init()
        engine.setProperty("rate", 130)
        engine.say("Now! let's pronounce some words: book, bird, cookies, city, Afghanistan.")
        engine.runAndWait()


if __name__ == "__main__":
    MyApp().run()
