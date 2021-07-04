from googletrans import Translator, LANGCODES
## march 21 : install googletrans=3.1.0a0 
## https://github.com/ssut/py-googletrans/issues/280

#print(LANGCODES)
translator = Translator()
print(translator.translate('站點名稱').text  ) ## , src='auto',dest='en')
