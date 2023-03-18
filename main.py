import threading

import pyttsx3
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

Window.clearcolor = (1, 1, 1, 1)  # set background color to white

class TextToSpeechApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the orientation of the layout
        self.orientation = "vertical"
        self.padding = (20, 10)

        # Create the text input for entering the text to speak
        self.text_input = TextInput(
            multiline=True,
            size_hint=(1, 0.8),
            hint_text="Enter the text to speak...",
            font_size=24,
            padding=(20, 10),
        )

        # Create the speak button
        self.button = Button(
            text="Speak",
            size_hint=(1, 0.2),
            font_size=24,
            background_color=(0, 0.7, 0.7, 1),
            color=(1, 1, 1, 1),
            disabled=False,
        )

        # Bind the speak button to the speak_text method
        self.button.bind(on_release=self.speak_text)

        # Create the voice dropdown button
        self.voice_dropdown = DropDown()

        # Get the list of available voices
        voices = self.get_voices

        # Create the voice button for selecting the voice
        self.voice_button = Button(
            text="Select Voice",
            size_hint=(0.5, 0.1),
            font_size=18,
            background_color=(0.7, 0.7, 0, 1),
            color=(1, 1, 1, 1),
        )
        self.voice_button.bind(on_release=self.voice)

        # Add the available voices to the voice dropdown
        for voice in voices:
            btn = Button(text=voice, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.voice_dropdown.select(btn.text))
            self.voice_dropdown.add_widget(btn)

        # Set the default voice
        self.voice_label = Label(text="Voice: Default", font_size=18, size_hint=(0.5, 0.1))
        self.selected_voice = None

        # Create the speech rate slider
        self.rate_slider = Slider(
            orientation="horizontal",
            min=50,
            max=200,
            value=100,
            size_hint=(1, 0.1),
        )

        # Bind the speech rate slider to the update_rate_label method
        self.rate_slider.bind(value=self.update_rate_label)

        # Create the speech rate label
        self.rate_label = Label(text="Speech rate: 1.0x", font_size=18, size_hint=(1, 0.1))

        # Add the widgets to the layout
        self.add_widget(self.text_input)
        self.add_widget(self.button)

        self.add_widget(self.voice_button)
        self.voice_dropdown.bind(on_select=self.update_voice_label)

        self.add_widget(self.voice_label)

        self.add_widget(self.rate_slider)
        self.add_widget(self.rate_label)

    def voice(self, instance):
        """Function to show the voice dropdown."""
        self.voice_dropdown.open(instance)

    def speak_text(self, instance):
        """Function to speak the text entered in the text input."""

        # Get the text entered in the text input
        text = self.text_input.text.strip()

        if text:
            # Disable the speak button while speaking
            self.button.disabled = True

            # Get the selected voice and speech rate
            voice = self.selected_voice
            rate = self.rate_slider.value / 100.0

            # Create a new thread
            speak_thread = threading.Thread(target=self.speak, args=(text, voice, rate))

            # Start the thread to speak the text
            speak_thread.start()

    def speak(self, text, voice, rate):
        """Function to speak the text with the selected voice and speech rate."""

        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set the voice and speech rate
        if voice:
            engine.setProperty("voice", voice)
        engine.setProperty("rate", int(200 * rate))

        # Speak the text
        engine.say(text)
        engine.runAndWait()

        # Enable the speak button after speaking
        self.button.disabled = False

    @property
    def get_voices(self):
        """Function to get the list of available voices."""

        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Get the list of available voices
        voices = engine.getProperty("voices")
        voice_list = []
        for voice in voices:
            voice_list.append(voice.name)

        # Return the list of available voices
        return voice_list

    def update_voice_label(self, instance, voice):
        """Function to update the selected voice label."""

        self.selected_voice = voice
        self.voice_label.text = f"Voice: {voice}"

    def update_rate_label(self, instance, value):
        """Function to update the speech rate label."""

        self.rate_label.text = f"Speech rate: {value / 100.0:.1f}x"

        self.voice_label.text = f"Voice: {value}"
        self.selected_voice = value

class TextToSpeechMain(App):
    def build(self):
        return TextToSpeechApp()

if __name__ == "__main__":
    TextToSpeechMain().run()

