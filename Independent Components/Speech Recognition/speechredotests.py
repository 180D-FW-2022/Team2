from pocketsphinx import LiveSpeech

speech = LiveSpeech(kws='keyword.list')
for phrase in speech:
    if 'shoot' in str(phrase):
        print('shooting')
    if 'reload' in str(phrase):
        print('reloading')
    if 'right' in str(phrase):
        print('turning right')
    if 'left' in str(phrase):
        print('turning left')
