# Librairies
import string

# =============== CLASSE POST ===============
class Post:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", horaire="", url="", texte="", score= "", upvote="", downvote=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.horaire = horaire
        self.url = url
        self.texte = texte
        self.score = score
        self.upvote = upvote
        self.downvote = downvote

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tHoraire : {self.horaire}\tURL : {self.url}\tTexte : {self.texte}\tScore : {self.score}\tUpvote : {self.upvote}\tDownvote : {self.downvote}\n"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    # Fonction qui nettoie un texte pour le rendre exploitable
    def nettoyer_texte(chaineDeCaractere):
        #le texte est mis en minuscule
        chaineDeCaractere = chaineDeCaractere.lower()
        #on récupère la ponctuation
        punct = string.punctuation
        #on récupère les chiffres
        chiffre = '0123456789'
        #on récupère les caractères de types apostrophe
        apostrophe = "’‘"
        #en parcourant l'ensemble de ces caractères
        for p in punct:
            #on les enlève
            chaineDeCaractere = chaineDeCaractere.replace(p, "")
        for c in chiffre:
            #on les enlève
            chaineDeCaractere = chaineDeCaractere.replace(c, "")
        for a in apostrophe:
            #on les remplace par un espace
            chaineDeCaractere = chaineDeCaractere.replace(a, " ")
        #on enlève les sauts de lignes
        chaineDeCaractere = chaineDeCaractere.replace("\n", "")
        return(chaineDeCaractere)


# =============== CLASSE AUTEUR ===============
class Auteur:
    # Initialisation des variables de la classe
    def __init__(self, nom):
        self.nom = nom
        self.nb_doc = 0
        self.production = []

    def add(self, production):
        self.nb_doc += 1
        self.production.append(production)
        
    def __str__(self):
        return f"Auteur : {self.nom}\t# productions : {self.nb_doc}"


# =============== CLASSE POSTBIS ===============    
class PostBis(Post):
    #PostBis héritage de Post
    def __init__(self, titre="", auteur="", date="", horaire="", url="", texte="", score= "", upvote="", downvote="", succes=False):
        super().__init__(titre=titre, auteur=auteur, date=date, horaire=horaire, url=url, texte=texte, score= score, upvote=upvote, downvote=downvote)  # Ou bien super(RedditDocument, self).__init__(paramètres)
        self.succes = succes
    
    #on écrase le str de Post
    def __str__(self):
        return f"Post Bis : {self.titre}, avec {self.succes}"