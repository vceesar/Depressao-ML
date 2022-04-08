import textblob from TextBlob

def extrair_subjetividade(txt):
    return Textblob(txt).sentiment.subjectivity

def extrair_polaridade(txt):
    return TextBlob(txt).sentiment.polarity