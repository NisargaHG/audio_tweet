from django import forms
from .models import AudioTweet
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import os
import tempfile

class AudioTweetForm(forms.ModelForm):
    class Meta:
        model = AudioTweet
        fields = ['audio_file']

    def clean_audio_file(self):
        audio = self.cleaned_data.get('audio_file')

        # Check file size
        if audio.size > 100 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 100MB.")

        ext = os.path.splitext(audio.name)[1].lower()
        if ext not in ['.mp3', '.wav']:
            raise forms.ValidationError("Only MP3 and WAV files are supported.")

       
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            for chunk in audio.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            if ext == '.mp3':
                audio_info = MP3(temp_file_path)
                duration = audio_info.info.length
            else:
                audio_info = WAVE(temp_file_path)
                duration = audio_info.info.length
        except Exception as e:
            raise forms.ValidationError("Unable to process audio file for duration check.")

        finally:
            os.remove(temp_file_path)

        if duration > 300:
            raise forms.ValidationError("Audio duration must not exceed 5 minutes.")

        return audio
