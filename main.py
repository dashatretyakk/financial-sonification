import mido
from mido import MidiFile, MidiTrack, Message
import pandas as pd

data = pd.read_csv('AAPL Historical Data (2).csv')

def price_to_note(price, min_price, max_price):
    min_midi_note = 21
    max_midi_note = 108

    note = int((price - min_price) / (max_price - min_price) * (max_midi_note - min_midi_note) + min_midi_note)
    return note

def volume_to_duration(volume, min_vol, max_vol):
    min_duration = 240
    max_duration = 960

    duration = int((volume - min_vol) / (max_vol - min_vol) * (max_duration - min_duration) + min_duration)
    return duration


closing_prices = data['Price'].astype(float)
volumes = data['Vol.'].replace({'M': '*1e6', 'B': '*1e9'}, regex=True).map(pd.eval).astype(float)


min_price = closing_prices.min()
max_price = closing_prices.max()
min_vol = volumes.min()
max_vol = volumes.max()


midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)


for price, volume in zip(closing_prices, volumes):
    note = price_to_note(price, min_price, max_price)
    duration = volume_to_duration(volume, min_vol, max_vol)
    track.append(Message('note_on', note=note, velocity=64, time=duration))
    track.append(Message('note_off', note=note, velocity=64, time=duration))


midi_file.save('financial_sonification_variable_duration.mid')
