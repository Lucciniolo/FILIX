#!/usr/bin/env python
# -*- coding: utf8 -*- 

import re

def doIt(contents, originalTitle):
# heart of filix module
    if ((contentText(contents) != False) and (forward(originalTitle) == True)):
        content_text = contentText(contents)
        if isThereAnyQuote(content_text):
            #content_text = removeLigneWhitoutQuote(content_text)
            content_text = removeQuote(content_text)
            content_text = removeHeader(content_text)
            content_text = removeTirets(content_text)
            content_text = hideEmails(content_text)
        else:
            content_text = removeHeader(content_text)
            content_text = removeTirets(content_text)
            content_text = hideEmails(content_text)
        return 'text', content_text
    return 'text', hideEmails(contentText(contents))     

def contentText(contents):
# return content in text if contents have a mail in text, else return false
    for i in contents:
        (content_type,content_text) = i
        if content_type == 'text':
            return content_text
    return False

def forward(originalTitle):
# return true if (Fwd:, Re:, RE:, Tr: ...) are founded 
    markers = ('Fwd:', 'Re:', 'RE:', 'TR:', 'Tr:')
    for i in markers:
        if originalTitle.count(i):   
            return True   
    return False
            
def changeTitle(title):
# remove the Forward marker from the title if there is one else do nothing
    markers = ('Fwd:', 'Re:', 'RE:', 'TR:', 'Tr:')
    for i in markers:
        if title.count(i):
            title = title.replace(i, '', 1)    
            return title
    return title

def isThereAnyQuote(content_text):
# return True if there is any '> '
    l_content = content_text.split('\n')
    for index in range(len(l_content)):
            l = re.match('> (.*)$|^>(.*)$', l_content[index])
            if l:
                return True
    return False

def removeQuote(content_text):
# remove all the '> '
    l_content = content_text.split('\n')
    for index in range(len(l_content)):
            l = re.match('> (.*)$|^>(.*)$', l_content[index])
            if l:
                    line = l.group(1)
                    if line:
                        l_content[index] = line
                    else:
                        l_content[index] = ''
    content_text = '\n'.join(l_content)
    return content_text

def hideEmails(content_text):
# hide "monsieur@mail.com" == "monsieur@hidemymail"
    l_content = content_text.split('\n')
    for index in range(len(l_content)):
            l_mail = re.findall('@[a-zA-Z0-9.-]{2,}[.][a-zA-Z]{2,4}', l_content[index])
            for index2 in range(len(l_mail)):
                    m = re.search(l_mail[index2], l_content[index])
                    if m:
                        l_content[index] = l_content[index][:m.start()] + "@hidemymail" + l_content[index][m.end():]
    content_text = '\n'.join(l_content)
    return content_text
    
    
    
def removeLigneWhitoutQuote(content_text):
# remove all the lines whitout '> '
    pass

def removeHeader(content_text):
# remove all the header ('subjet : ....' 'from : ....' ...) et tout ce qu'il y a avant
    l_content = content_text.split('\n')
    longueur = len(l_content)
    index = 0
    fallow = True
    # Un premier parcours pour chercher le premier "De : .....". On s'arrete dès qu'il est trouvé 
    while (index < longueur and fallow == True): 
            l = re.match('^[A-Z]+[a-z]*[ ]:[ ]+.*|^[A-Z]+[a-z]*:[ ]+.*|^[^a-zA-Z]*:[ ]+.*|^.+:[ ]+.*@[a-zA-Z0-9.-]{2,}[.][a-zA-Z]{2,4}', l_content[index])
            if l:
                  fallow = False
                  index2 = index
            else:
                  index = index + 1
    if fallow == False: # On verifie qu'il y a bien un header. Si il y en a un, on continue
        fallow = True  
        # Un second parcours, supprimant tous le header, debutant au premier "De : ........" et s'arretant juste apres le dernier
        while (index2 < longueur and fallow == True):
                l = re.match('^[A-Z]+[a-z]*[ ]:[ ]+.*|^[A-Z]+[a-z]*:[ ]+.*|^[^a-zA-Z]*:[ ]+.*|^.+:[ ]+.*@[a-zA-Z0-9.-]{2,}[.][a-zA-Z]{2,4}', l_content[index2])
                if l:
                       l_content.pop(index2)
                       index2 = index2 - 1
                       longueur = longueur - 1
                else:
                        fallow = False
                index2 = index2 + 1
            # Un dernier parcours, on supprime tout se qui se trouve avant le Header si il y avait bien un header
        index3 = 0
        while (index3 < index):
              l_content.pop(0) # Supprime la premiere ligne
              index3 = index3 + 1
    content_text = '\n'.join(l_content)
    return content_text
          
         
            
def removeTirets(content_text):
# remove the FIRST line like that one ("------------ Forwarded message ------------")
    l_content = content_text.split('\n')
    longueur = len(l_content)
    index = 0
    while index < longueur:
            l = re.match('^[-]+([a-zA-Z].+)+[-]|[-]+[ ]+([a-zA-Z].+)[-]+', l_content[index])
            if l:
                   l_content.pop(index)
                   content_text = '\n'.join(l_content)
              