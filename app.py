# Import Kivy core modules
from kivy.app import App                      # Base class for creating a Kivy app
from kivy.uix.boxlayout import BoxLayout      # Layout widget that arranges children in a vertical or horizontal box
from kivy.uix.label import Label              # Label widget to display text
from kivy.uix.button import Button            # Button widget
from kivy.clock import Clock                  # Clock module for scheduling recurring tasks

# Import the custom audio recorder class
from record_audio import AudioRecorder

class SpellingBeeApp(App):
  def build(self):
    # Initialize audio recorder and recording state
    self.recorder = AudioRecorder()
    self.recording = False             # Boolean to track if we're currently recording
    self.start_time = 0                # Timer for the duration of the recording
    self.MAX_RECORD_TIME = 10          # Maximum duration in seconds for recording

    # Create the main layout
    self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

    # UI Elements
    self.title_label = Label(
      text='Spelling Bee Practice',
      font_size='24sp'
    )

    self.timer_label = Label(
      text='Time: 0.0s',
      font_size='18sp'
    )

    self.button = Button(
      text='Start Recording',
      font_size='20sp',
      size_hint=(1, 0.3)
    )

    # Bind button press to the toggle_recording method
    self.button.bind(on_press=self.toggle_recording)

    # Add widgets to the layout
    self.layout.add_widget(self.title_label)
    self.layout.add_widget(self.timer_label)
    self.layout.add_widget(self.button)

    return self.layout

  def toggle_recording(self, instance):
    # Flip the recording state: start if stopped, stop if started
    self.recording = not self.recording

    if self.recording:
      # Start recording audio to file
      self.recorder.start("spelling_word_audio.wav")

      # Reset timer and update UI
      self.start_time = 0
      self.timer_label.text = 'Time: 0.0s'
      self.button.text = 'Stop Recording'

      # Schedule the timer to update every 0.1 seconds
      Clock.schedule_interval(self.update_timer, 0.1)
    else:
      # Stop the audio recording
      self.recorder.stop_recording()

      # Stop updating the timer
      Clock.unschedule(self.update_timer)

      # Show Submit and redo buttons
      self.show_post_recording_buttons()

  def show_post_recording_buttons(self):
    # Remove the start/stop button
    self.layout.remove_widget(self.button)

    # Create Submit and redo buttons
    self.submit_button = Button(
      text='Submit',
      font_size='20sp',
      size_hint=(1, 0.3)
    )
    self.redo_button = Button(
      text='Redo',
      font_size='20sp',
      size_hint=(1, 0.3)
    )

    self.submit_button.bind(on_press=self.submit)
    self.redo_button.bind(on_press=self.redo)

    self.layout.add_widget(self.submit_button)
    self.layout.add_widget(self.redo_button)
  
  def redo(self, instance):
    # Hide the submit and redo buttons
    self.layout.remove_widget(self.submit_button)
    self.layout.remove_widget(self.redo_button)
    # Show the recording button again
    self.layout.add_widget(self.button)
    # Start recording again
    self.toggle_recording(None)

  def submit(self, instance):
    # Remove Submit and redo buttons, reset timer, and show Start Recording button
    self.layout.remove_widget(self.submit_button)
    self.layout.remove_widget(self.redo_button)
    self.timer_label.text = 'Time: 0.0s'
    self.button.text = 'Start Recording'
    self.layout.add_widget(self.button)
    self.start_time = 0
    self.recording = False

  def update_timer(self, dt):
    # Increment the internal timer
    self.start_time += dt

    # Update the label to show current elapsed time
    self.timer_label.text = f'Time: {self.start_time:.1f}s'

    # Automatically stop recording when time limit is reached
    if self.start_time >= self.MAX_RECORD_TIME:
      self.toggle_recording(None)

# Run the Kivy app
if __name__ == '__main__':
  SpellingBeeApp().run()
