# =============== FONCTION UTILISATEUR SUSPENDU ===============
def suspendu(username: str, reddit):
    #si le compte de l'utilisateur est suspendu, on renvoie True
    if hasattr(reddit.redditor(username), 'is_suspended'):
        return True
    #sinon False
    else:
        return False
    
# =============== FONCTION POST PLAGEHORAIRE ===============
def plageHoraire(collection: list, heure):   
    plageHoraire = [['08:00:00','14:00:00',0, 'le matin'], ['14:00:00','19:00:00',0,'l après midi'] , ['19:00:00','23:59:59',0, 'le soir'] , ['00:00:00','08:00:00',0, 'la nuit']]
    for h in collection:    
        for i in range(0, len(plageHoraire)):
            if plageHoraire[i][0]<= h.horaire <plageHoraire[i][1]:
                plageHoraire[i][2]+=1

    plageHoraire = sorted(plageHoraire,key=lambda x: x[2], reverse=True)
    
    heure.setText("Le moment de la journée où les gens postent le plus est " + str(plageHoraire[0][3]))
    return "Le moment de la journée où les gens postent le plus est: " + str(plageHoraire[0][3])

# =============== FONCTION POSTASUCCES ===============
def postASucces(collectionbis, postasucces):
        postsucces = 0
        for i in collectionbis:
            if(i.succes == True):
                postsucces += 1
        
        # On cherche donc à savoir si, parmis les autres post (postbis) de l'auteur, s'il y a plus de post a succes que de post peu connu
        ratio = postsucces/len(collectionbis)
        if ratio >0.5:
            # Insertion du texte dans l'interface
            postasucces.setText("En moyenne, les auteurs des posts à succès produisent des posts du même type")
            return "En moyenne, les auteurs des posts à succès produisent des posts du même type"
        else:
            # Insertion du texte dans l'interface
            postasucces.setText("En moyenne, les auteurs des posts à succès ne produisent pas forcément des posts du même type ")
            return "En moyenne, les auteurs des posts à succès ne produisent pas forcément des posts du même type "
        
# =============== FONCTION POURCENTAGE ===============
def pourcentage(collection,pourcentageup , pourcentagedown ):
    # Mise en place d'un tableau
    tableau = []
    # Création des variables contenant le pourcentage d'Upvote et Downvote
    subredditPourcentUpvote=0
    subredditPourcentDownvote=0
    k=0
    # Parcours de collection
    for i in collection:
        # Si le score n'est pas nul
        if(i.score > 0):
            # On calcule le pourcentage
            pourcentUpvote = (i.upvote / i.score) * 100
            pourcentDownvote = (i.downvote / i.score) * 100
            # On rempli le tableau 
            tableau.append({
                'nbUpvote': i.upvote,
                'nbDownvote': i.downvote,
                'nbScore': i.score,
                'pourcentUpvote': pourcentUpvote,
                'pourcentDownvote': pourcentDownvote
                })
            # On ajoute le pourcentage pour ensuite faire la moyenne
            subredditPourcentUpvote += pourcentUpvote
            subredditPourcentDownvote += pourcentDownvote
        k=k+1
    # On fait la moyenne, avec arrondi de 2 après la virgule
    subredditPourcentUpvote = round(subredditPourcentUpvote/ len(tableau), 2)
    subredditPourcentDownvote = round(subredditPourcentDownvote/ len(tableau), 2)

    pourcentageup.setText("Le pourcentage moyen d'upvote des posts de ce subreddit est de: " + str(subredditPourcentUpvote) + "%.") 
    pourcentagedown.setText("Le pourcentage moyen de downvote des posts de ce subreddit est de: " + str(subredditPourcentDownvote) + " %.")
    return "Le pourcentage moyen d'upvote et downvote est " + str(subredditPourcentUpvote) + " et " + str(subredditPourcentDownvote)

            
# =============== MAIN : PROGRAMME PRINCIPAL ===============
#Prend en paramètre les variables définies dans le fichier interface
def main(subreddit, reddit, nbsubs, heure, frequence, graphique, postasucces, pourcentageup, pourcentagedown):

    # Requête pour sélectionner les posts de la catégorie choisie
    # Ici, on limite à 3 le nombre de posts retournés
    # Ce chiffre peut, bien entendu, être augmenté pour plus de précisions, mais cela risque de ralentir l'exécution du code
    limite = 3
    top_posts = reddit.subreddit(subreddit).top("all", limit = limite)
    
    # Récupération du nombre de personnes qui ont souscrit à ce subreddit
    subs = reddit.subreddit(subreddit).subscribers
    
    # Insertion du texte dans l'interface
    nbsubs.setText("Le nombre d'abonnés de ce subreddit est de " + str(subs))
    
    # Récupération du texte
    docs = []
    docs_bruts = []
    afficher_cles = False
    for i, post in enumerate(top_posts):
        if afficher_cles:  # Pour connaître les différentes variables et leur contenu
            for k, v in post.__dict__.items():
                pass
        docs.append(post.title.replace("\n", " "))
        docs_bruts.append(post)
    
    # =============== CLASSE POST ===============
    # Importation de la classe Post
    from Classes import Post
    
    # Manipulation des posts
    import datetime
    collection = []
    for doc in docs_bruts:
        titre = doc.title.replace("\n", "")
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        horaire = datetime.datetime.fromtimestamp(doc.created).strftime("%H:%M:%S")
        url = "https://www.reddit.com/" + doc.permalink
        texte = doc.selftext.replace("\n", "")
        score = doc.score
        upvote = doc.upvote_ratio
        upvote = round(score*upvote)
        downvote = score - upvote
    
        doc_classe = Post(titre, auteur, date, horaire, url, texte, score, upvote, downvote)
        
        collection.append(doc_classe)    
    
    # Création de l'index de documents
    id_doc = {}
    for i, doc in enumerate(collection):
        id_doc[i] = doc.titre
    
    # =============== CLASSE AUTEUR ===============
    # Importation de la classe Auteur
    from Classes import Auteur
    
    # =============== DICT AUTEURS ===============
    # Dictionnaire des auteurs
    auteurs = {}
    aut_id = {}
    num_auteurs_vus = 0
    
    # Création de la liste et de l'index des auteurs
    for doc in collection:
        if doc.auteur not in aut_id:
            num_auteurs_vus += 1
            auteurs[num_auteurs_vus] = Auteur(doc.auteur)
            aut_id[doc.auteur] = num_auteurs_vus
    
        auteurs[aut_id[doc.auteur]].add(doc.texte)
    
    # =============== CLASSE POSTBIS ===============
    from Classes import PostBis
    
    # Manipulation des postsBis 
    docBis = []
    collectionbis = []
    
    # Pour l'ensemble des auteurs des posts récupérés précédemment
    for auteur in aut_id:
        # Si l'auteur n'est pas suspendu
        if suspendu(auteur, reddit)==False:
            
            # On récupère 2 de ses top posts 
            # Ce chiffre peut, bien entendu, être augmenté pour plus de précisions, mais cela risque de ralentir l'exécution du code
            # On pourrait par exemple définir à None ce nombre, pour obtenir l'ensemble des posts de l'auteur 
            postBis = reddit.redditor(auteur).top("all", limit = 2)
            
            # Récupération du texte
            afficher_cles = False
            for i, post in enumerate(postBis):
                if afficher_cles:  # Pour connaître les différentes variables et leur contenu
                    for k, v in post.__dict__.items():
                        pass
                docBis.append(post)
     
    for element in docBis:
        #utilisation d'un try pour ne prendre que les posts et non les commentaires
        try:
            titre = (reddit.submission(element)).title
            auteur = (reddit.submission(element)).author
            date = datetime.datetime.fromtimestamp((reddit.submission(element)).created).strftime("%Y/%m/%d")
            horaire = datetime.datetime.fromtimestamp((reddit.submission(element)).created).strftime("%H:%M:%S")
            url = "https://www.reddit.com/" + (reddit.submission(element)).permalink
            texte = (reddit.submission(element)).selftext.replace("\n", "")
            score = (reddit.submission(element)).score
            upvote = (reddit.submission(element)).upvote_ratio
            upvote = round(score*upvote)
            downvote = score - upvote
            
            # On a défini à 100 000 la limite qui permet de définir si un post est ou non un post à succès
            # Cette limite peut bien évidemment changer
            if score < 100000:
                succes = False
            else:
                succes = True
        
            doc_classe_bis = PostBis(titre, auteur, date, horaire, url, texte, score, upvote, downvote, succes)
            
            collectionbis.append(doc_classe_bis)
        except:
            pass
    
    # =============== FREQUENCE DES MOTS  =============
    from collections import Counter 
    
    # On récupère l'ensemble des titres et on les ajoute dans une même chaîne de caractères
    longueChaineDeCaracteres = " ".join(docs)
    # On nettoie cette chaîne de caractères à l'aide la fonction nettoyer_texte
    Post.nettoyer_texte(longueChaineDeCaracteres)
    
    # On récupère les 10 premiers mots les plus utilisés ainsi que leur fréquence d'utilisation
    res = Counter(longueChaineDeCaracteres.split()).most_common(10)
    #print("Les mots les plus utilisés sont : " + str(dict(res))) 
    
    # =============== FREQUENCE DES MOTS : BIS  =============
    from wordcloud import WordCloud
    
    # Insertion du texte dans l'interface
    frequence.setText("Les mots les plus utilisés sont : ")
    
    # Ici, on se permet d'exclure un certain nombre de mots qui n'auraient pas d'importance pour nos analyses
    # Il s'agit ici d'une liste non exhaustive 
    exclure_mots = ['i','me','my','mine','myself','you','your','yours','yourself','he','him','his','himself','she','her','hers','herself','it','its','itself','we','us','our','ours','ourselves','you','your','yours','yourselves','they','them','their','theirs','themselve','did','d','was','were','s','do','have','had','will','what','where','when','who','how','why','which','whose','a','an','the','of','and','in','on','at','to','so','with','this','from','that','for','as','at','by','if','of','is','would','should','ve','off','all','wasn','t', 'not']
    wordcloud = WordCloud(background_color = 'white', stopwords = exclure_mots, max_words = 50).generate(longueChaineDeCaracteres)
    # Affichage dans l'interface
    graphique.axes.imshow(wordcloud)
    graphique.draw()
    
    # =============== HEURE DE PUBLICATION  =============
    # On défini la plage horaire ou il y a le plus de post publié
    plageHoraire(collection, heure)
    
    # =============== POST A SUCCES  =============
    # On verifie si les postbis sont des posts à succés ou non
    postASucces(collectionbis, postasucces)
    
    # =============== POST A SUCCES  =============
    # On verifie si les postbis sont des posts à succés ou non
    
    pourcentage(collection, pourcentageup , pourcentagedown)