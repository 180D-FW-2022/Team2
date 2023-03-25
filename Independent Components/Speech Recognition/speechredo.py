from pocketsphinx import LiveSpeech

speech = LiveSpeech(kws='keyword.list', kws_threshold=1e-10)
for phrase in speech:
    print(phrase.segments(detailed=True))

