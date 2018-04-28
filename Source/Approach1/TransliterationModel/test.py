
import Transliteration
enNE = 'Stanford university'
vnNE = 'Đại học Stanford'

res = Transliteration.getTransliterationProb(enNE,vnNE)
print(res)