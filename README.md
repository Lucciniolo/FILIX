Le package Python Atomail (http://el-tramo.be/software/atomail) permet de convertir des mails en flux RSS. FILIX y ajoute plusieurs
fonctionnalités :


- cache les mails sous la forme : nom.prenom@hidemymail afin de se
protéger des robots de spam
- supprime tous ce qu'il y a avant le header
- supprime le header
- Retire les > disgracieux
- Retire les 'Re:', 'RE:', 'TR:', 'Tr:' Fwd: du titre
- Retire les ---------- Forwarded message ---------- Que certains
mailers mettent (Gmail, SOGo ...)

Comment le tester ?

Il faut envoyer le mail à filtrer à axiome.henry@gmail.com

Ensuite lancer la commande suivante :

python atomail.py --title 'Some Mailbox'
--uri='http://mysite.com/somemailbox.xml'
$HOME/Developpement/python/anti-spam/somemailbox.xml --mode=imap-ssl
--host imap.gmail.com --user=axiome.henry@gmail.com --password=tototiti

Grâce au 3 lignes, le contenu du mail modifié et son titre sont
affichés dans la console.