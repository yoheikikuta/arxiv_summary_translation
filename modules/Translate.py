#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from google.cloud import translate
from IPython.display import clear_output

SOURCE_LANG = 'en'


class Translate:
    def __init__(self,target_lang):
        self.translate_client = translate.Client()
        self.target_lang = target_lang
    
    def get_translation(self, text, nmt=True):
        text = text.replace("\n", " ")
        text = text.replace("\\", "")
        #Call translation api with NMT
        model = translate.NMT if nmt else translate.BASE
        result = self.translate_client.translate(
            text
            , source_language=SOURCE_LANG
            , target_language=self.target_lang
            , model=model
        )
        #Return the translated result
        return result['translatedText']
    
    def check_arxiv(self, bulk, nmt=True):
        N = len(bulk)
        lc = 0
        breaker = None
        
        while not breaker:
            title = bulk[lc]['title']
            pdf_url = bulk[lc]['pdf_url']
            abst = bulk[lc]['summary']
            
            translation = self.get_translation(abst, nmt)
            
            print()
            print("{} / {}(Total number)".format(lc+1,N))
            print()
            print(title)
            print()
            print(pdf_url)
            print()
            print(translation)
            
            sleep(0.3)
            breaker = input(
                    "Just enter to proceed or enter any key to quit:"
            )
            clear_output()
            lc +=1
            if lc == N:
                print("All papers were translated.")
                break
