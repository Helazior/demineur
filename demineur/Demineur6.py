
#faire annimation quand gagne Annimation quand record faire annimation
#quand perdu... reduire le nombre de boucle/sec mettre un mode pause
#optimiser l'IA ne plus perdre quand utilisation de "aide"
#enregistrer la partie en cours pour pouvoir la continuer plus tard

from numpy import *
import pygame
from pygame.locals import *
import matplotlib.pyplot as pl
pygame.init()

import random as rd
from copy import deepcopy
from time import *
from decimal import *
from math import *


import sys, os

pathname = os.path.dirname(sys.argv[0])

os.chdir (os.path.abspath(pathname))
os.chdir ("Images demineur")

getcontext().prec = 4
TInter = int(time())


with open("../fichier texte/niveau.txt","r") as fichier:
    texte = fichier.read()   
    niveau = texte[9]


if texte[24] == '0':
    finissable = 0
    print("Avec hasard")
else:
    finissable = 1
    print("Sans hasard")
    
if niveau == '1':
    XlongGrille = 9
    YlongGrille = 9    
    nbBombes = 10
    print("Niveau facile")
    
elif niveau == '2':
    XlongGrille = 16
    YlongGrille = 16
    nbBombes = 40
    print("Niveau moyen")


else:
    XlongGrille = 40
    YlongGrille = 16
    nbBombes = 99
    print("Niveau difficile")

    
"""--------------------------Constantes------------------------"""


tailleBord = 12
tailleHaut = 74

tailleFenetre = 550

continuer = 1

utilisationIA = 0

print("Bon jeu !")

"""-------------------------CreerGrille----------------------------"""
def CreerGrille(XlongGrille, YlongGrille, nbBombes, Xclique, Yclique):
    A=YlongGrille*[0]
    for i in range(len(A)):
        A[i]=XlongGrille*[0]

    B = deepcopy(A)
    if IA:
        for i in range(-1,2):
            for j in range (-1,2):
                if Xclique+i<XlongGrille and Xclique+i>=0 and Yclique+j<YlongGrille and Yclique+j>=0:
                    B[Yclique+j][Xclique+i] = "C"
    else:
        B[Yclique][Xclique] = "C"

    #placer la bombe au hasard + num cases

    for k in range (nbBombes):
        x = rd.randint(0,XlongGrille-1)
        y = rd.randint(0,YlongGrille-1)
        b = 0
        while B[y][x] != 0:
            x = rd.randint(0,XlongGrille-1)
            y = rd.randint(0,YlongGrille-1)
            b+=1
            if b > 10000:
                print("Trop de bombes")
                sys.exit(0)

        B[y][x] = "B"
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0:
                    A[y+j][x+i] += 1

    return array(A),array(B)



"""---------------------clique---------------------------"""
def clique(A,B,C,x,y,nbCases, perdu,IA):

    if C[y][x] != "D" and C[y][x] != "1":

        if B[y][x] == "B":
            if IA != 3:
                fenetre.blit(perduSmiley, posSmiley)
                fenetre.blit(bombeDeclanche, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))

            B[y][x] = "1"
            for x in range(XlongGrille):
                for y in range(YlongGrille):
                    if B[y][x] == "B" and C[y][x] !="D":
                        fenetre.blit(bombe, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))
                    elif B[y][x] != "B" and C[y][x] =="D":
                        fenetre.blit(drapeaubarre, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))
            if IA != 3:
                fenetre.blit(defaite, (XmilieuEcran-170,0.5*(YlongGrille*tailleImage+tailleHaut)))
            pygame.display.flip()
            perdu = 1
            print("perdu")


        else:
            if IA != 2:
                C[y][x] = "1"
                nbCases-=1  
                    
                if IA != 3:
                    print("nbCases=",nbCases)
                    devoileChiffre(A,B,C,x,y)
    
                if A[y][x] == 0:
                    nbZero = 1
                    l=0
    
                    while nbZero > 0 and l<max(XlongGrille,YlongGrille):
                        nbZero = 0
                        A[y][x] == 0
                        for i in range(-l,l+1):
                            for j in range(-l,l+1):
                                if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0:
                                    if A[y+j][x+i] == 0:
                                        for m in range(-1,2):
                                            for n in range(-1,2):
                                                caseDevoile = 0
                                                if x+i+m<XlongGrille and x+i+m>=0 and y+j+n<YlongGrille and y+j+n>=0 and (C[y+j+n][x+i+m] == "0" or C[y+j+n][x+i+m] == "I"):
                                                    for v in range (-1,2):
                                                        for w in range (-1,2):
                                                            if x+i+m+v<XlongGrille and x+i+m+v>=0 and y+j+n+w<YlongGrille and y+j+n+w>=0:
                                                                if C[y+j+n+w][x+i+m+v] == "1" and A[y+j+n+w][x+i+m+v]==0:
                                                                    caseDevoile+=1
    
                                                    if caseDevoile > 0:
                                                        C[y+j+n][x+i+m] = "1"
                                                        nbZero += 1
                                                        nbCases-=1
                                                        if IA != 3:
                                                            devoileChiffre(A,B,C,x+i+m,y+j+n)

                        l+=1
                    
                    
                    
            else:
                C[y][x] = "I"
                fenetre.blit(PointInterrogation, (x*tailleImage+tailleBord, y*tailleImage+tailleHaut))
                
                                                        
                    


    elif C[y][x] == "1":     #On clique sur une case dejà‚ devoile
        nbCases,perdu = DevoileCases(A,B,C,x,y,nbCases, perdu,IA)


    return C,nbCases, perdu

"""---------------On clique sur une case deja devoile-----------"""
def DevoileCases(A,B,C,x,y,nbCases, perdu,IA):
    drapeau = 0
    caseclique = 0

    for i in range(-1,2):
        for j in range(-1,2):
            if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0 and (i!=0 or j!=0):
                if C[y+j][x+i] == "D":
                    drapeau += 1
                elif C[y+j][x+i] == "0" or C[y+j][x+i] == "I":
                    caseclique = 1

    if drapeau == A[y][x] and caseclique == 1:
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0 and C[y+j][x+i] != "1" and C[y+j][x+i] != "D":
                    C,nbCases, perdu = clique(A,B,C,x+i,y+j,nbCases, perdu,IA)

    return nbCases,perdu


"""---------------------clique droit---------------------------"""

def clique_droit(C,x,y,nbBombesRestantes,IA):  #I = point d'interrogation, D = Drapeau, B = bombe, 0 = case non devoile, 1 = Case devoile, dans matrice C
    if C[y][x] != "D" and C[y][x] != "1":
        if C[y][x] == "I" and IA == 0:
            C[y][x] = "0"
            if IA != 3:
                fenetre.blit(case, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))
        elif C[y][x] == "0" or C[y][x] == "I" and IA != 0:
            nbBombesRestantes -=1
            C[y][x] = "D"
            if IA != 3:
                fenetre.blit(drapeau, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))

    elif C[y][x] == "D":
        nbBombesRestantes +=1
        C[y][x] = "I"
        fenetre.blit(PointInterrogation, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))

        if IA != 3:
            print("nbBombesRestantes=",nbBombesRestantes)
    pygame.display.flip()

    return C,nbBombesRestantes


"""-------------------------IA resout demineur----------------------"""
def solveDemineur(A,B,C,nbBombesRestantes,nbBombes,nbCases,XlongGrille,YlongGrille,perdu,IA):
    action = 0
    
    if IA != 3:
        x = rd.randint(0,XlongGrille-1)
        y = rd.randint(0,YlongGrille-1)
    if nbCases == XlongGrille*YlongGrille - nbBombes:
        x = rd.randint(0,XlongGrille-1)
        y = rd.randint(0,YlongGrille-1)
        action = 1
    else:
        
        #COUP CLASSIQUE

        for x in range(XlongGrille):
            for y in range(YlongGrille):
                if C[y][x] == "1" and A[y,x] !=0:
                    drapeau = 0
                    caseclique = 0

                    for i in range(-1,2):
                        for j in range(-1,2):
                            if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0 and (i!=0 or j!=0):
                                if C[y+j][x+i] == "D":
                                    drapeau += 1
                                elif C[y+j][x+i] == "0" or C[y+j][x+i] == "I":
                                    caseclique += 1

                    if drapeau == A[y][x] and caseclique >= 1:

                        nbCases,perdu = DevoileCases(A,B,C,x,y,nbCases, perdu,IA)

                        action = 1
                        if IA == 1:
                            return C,x,y,nbBombesRestantes,nbCases,perdu

                    if drapeau + caseclique == A[y][x]:
                        for i in range(-1,2):
                            for j in range(-1,2):
                                if x+i<XlongGrille and x+i>=0 and y+j<YlongGrille and y+j>=0 and (i!=0 or j!=0):
                                    if C[y+j][x+i] == "0" or C[y+j][x+i] == "I":
                                        if IA != 2:

                                            C,nbBombesRestantes = clique_droit(C,x+i,y+j,nbBombesRestantes,IA)
                                            if IA == 1:
                                                return C,x,y,nbBombesRestantes,nbCases,perdu
                                        
                                        elif IA == 2:
                                            C[y+j][x+i] = "I"
                                            fenetre.blit(PointInterrogation, ((x+i)*tailleImage+tailleBord,(y+j)*tailleImage+tailleHaut))
                                        action = 1

    if action == 0:

        """-----------------Cas complique: arbre de recherche-----------------"""
        ### I. Modelisation:

        place = 0
        D = [[None]*9]      #tableau de l'arbre

        LcasesDevoilesAdj = []

        for i in range (XlongGrille):
            for j in range(YlongGrille):
                caseCache = 0
                nbDrapeauAdj = 0

                if C[j][i] == "1" and A[j][i] > 0:

                    for k in range (-1,2):
                        for l in range (-1,2):
                            if i+k < XlongGrille and i+k>=0 and j+l < YlongGrille and j+l >= 0:
                                if C[j+l][i+k] == "D":
                                    nbDrapeauAdj +=1
                                if C[j+l][i+k] == "0" or C[j+l][i+k] == "I":
                                    caseCache += 1
                                    if caseCache == 1:
                                        place +=1
                                        if place > 1:
                                            D.append(9*[None])

                                    D[place-1][caseCache-1] = i+k+XlongGrille*(j+l)

                    if caseCache > 0:
                        LcasesDevoilesAdj.append(A[j][i]-nbDrapeauAdj)

        #print("LcasesDevoilesAdj=",LcasesDevoilesAdj)
        #print("D = ",D)

        if LcasesDevoilesAdj != []:


            ### II. Arbre de recherche:
            #tenir compte des bombes restantes et optimiser



            long = len(LcasesDevoilesAdj)

            Lnum = []
            for i in range(8):
                for j in range (long):
                    if not(D[j][i] in Lnum) and D[j][i] != None:
                        Lnum.append(D[j][i])

            LColonne = [[0]]
            for h in range(1,long+1):
                LColonne.append(deepcopy([]))

            #print(LColonne)


            Lzeros = [0]*long


            LcasesBombes = [None]

            ligne = 0
            positionBombePlace = []
            monte = 0



            E = []

            while 1:



                ## Pose une bombe


                if LcasesDevoilesAdj[ligne] > 0:
                    case = D[ligne][LColonne[ligne][-1]]
                    #print("D[ligne][LColonne[ligne]] = ",ligne,LColonne[ligne],case)
                    existe = 0
                    for k in range (ligne):
                        if case in D[k]:
                            existe = 1



                    if case in LcasesBombes or existe:#si pas valide
                        if case != None:
                            LColonne[ligne][-1] += 1#on passe au suivant

                    else:#si bonne case
                        for k in range (ligne,long):#On  verifie qu'on peut poser les bombes
                            if case in D[k]:
                                if LcasesDevoilesAdj[k] == 0:
                                    LColonne[ligne][-1]+=1
                                    existe = 2




                        if existe != 2: #Si oui on pose les bombes
                            for k in range (ligne,long):
                                if case in D[k]:
                                    LcasesDevoilesAdj[k] -= 1


                            #print("LcasesBombes=",LcasesBombes)
                            LcasesBombes.append(case)
                            positionBombePlace.append(ligne)
                            if LcasesDevoilesAdj [ligne]==0 and ligne < long-1:
                                ligne += 1
                                LColonne[ligne] = [0]
                            else:

                                LColonne[ligne].append(LColonne[ligne][-1]+1)

                            monte = 1


                    #print("LcasesDevoilesAdj",LcasesDevoilesAdj)

                    if LcasesDevoilesAdj == Lzeros:
                        if len(LcasesBombes)-1<=nbBombesRestantes:
                            E.append(deepcopy(LcasesBombes[1:len(LcasesBombes)]))
                            #print("E=",E)






                    ##Revenir en arriere RETOUR
                conditionRetour = 0

                if positionBombePlace != []:
                    if LcasesDevoilesAdj[ligne]==0 and ligne != positionBombePlace[-1] and monte == 0:
                        conditionRetour = 1

                if LColonne[ligne] != []:
                    if LColonne[ligne][-1] > 8:
                        LColonne[ligne][-1]-=1

                    if D[ligne][LColonne[ligne][-1]] == None:
                        conditionRetour = 1

                if ligne >= long or LcasesDevoilesAdj == Lzeros or conditionRetour:


                    #print("RETOUR")

                    #print("ligne",ligne)


                    if D[0][LColonne[0][0]]== None:
                        break
                    else:


                        del LColonne[ligne][-1]

                        if LColonne[ligne] == []:
                            ligne -= 1

                        monte = 0

                        #print(ligne)
                        #print("positionBombePlace",positionBombePlace)

                        if positionBombePlace != []:
                            while ligne > positionBombePlace[-1]:
                                ligne -= 1
                                if ligne-1 > positionBombePlace[-1]:
                                    del LColonne[ligne][-1]


                        if LColonne[ligne] != []:
                            LColonne[ligne][-1] +=1


                        #print("ligne",ligne)





                        if positionBombePlace != []:

                            if ligne == positionBombePlace[-1]:
                                #print("dans la boucle pour remettre LcasesAdj")
                                case = LcasesBombes[-1]
                                for k in range (ligne,long):
                                    if case in D[k]:
                                        LcasesDevoilesAdj[k] += 1
                                del positionBombePlace[-1]
                                del LcasesBombes[-1]





                ##Avance
                elif LcasesDevoilesAdj[ligne]==0 and (ligne == positionBombePlace[-1] or (ligne != positionBombePlace[-1] and monte == 1)):#revoir cette condition
                    #print("\nAVANCE","ligne=",ligne,"LcasesDevoilesAdj=",LcasesDevoilesAdj)
                    ligne += 1
                    LColonne[ligne].append(0)


                if ligne >= long:
                    print("BUG: derniere ligne depassee")
                    break


            ##Fin boucle principale






            ### III. Interpretation:
            if E != []:
                Lbombes = []
                LsansBombes = []
                univers = len (Lnum)
                Lstats = [0]*univers
                pos = 0
                for case in Lnum:
                    for L in E:
                        if case in L:
                            Lstats[pos] += 1
                    Lstats[pos]=Lstats[pos]/len(E)
                    if Lstats[pos] == 1:
                        Lbombes.append(case)
                    elif Lstats[pos] == 0:
                        LsansBombes.append(case)
                    pos += 1
                action = 2
                if LsansBombes == [] and Lbombes == []:
                    s = max(Lstats)

                    if s > .5 and IA == 1:  #partie a ameliorer avec les maths
                        Lbombes = [Lnum[Lstats.index(max(Lstats))]]
                    else:
                        action = 0
                        
                if action == 2 and IA == 1:
                    if LsansBombes != []:
                        case = LsansBombes[0]
                        x = case%XlongGrille
                        y = int(case/XlongGrille)
                        if C[y][x] != "1":
                            C,nbCases, perdu = clique(A,B,C,x,y,nbCases, perdu,IA)
                    elif Lbombes != []:
                        case = Lbombes[0]
                        q = case%XlongGrille
                        r = int(case/XlongGrille)
                        C,nbBombesRestantes = clique_droit(C,q,r,nbBombesRestantes, IA)


                ### IV. devoiler:

                if action == 2 and IA == 3:
                    for case in Lbombes:
                        q = case%XlongGrille
                        r = int(case/XlongGrille)
                        C,nbBombesRestantes = clique_droit(C,q,r,nbBombesRestantes, IA)

                    for case in LsansBombes:
                        x = case%XlongGrille
                        y = int(case/XlongGrille)
                        if C[y][x] != "1":
                            C,nbCases, perdu = clique(A,B,C,x,y,nbCases, perdu,IA)

                elif action == 2 and IA == 2:
                    print(Lstats,Lbombes,LsansBombes)
                    for case in Lbombes:
                        x = case%XlongGrille
                        y = int(case/XlongGrille)
                        C[y][x] = "I"
                        fenetre.blit(PointInterrogation, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))

                    for case in LsansBombes:
                        x = case%XlongGrille
                        y = int(case/XlongGrille)
                        C[y][x] = "I"
                        fenetre.blit(PointInterrogation, (x*tailleImage+tailleBord,y*tailleImage+tailleHaut))

    if IA != 3:
        x = rd.randint(0,XlongGrille-1)
        y = rd.randint(0,YlongGrille-1) 

    if action == 0 and IA == 3:
        print("recommencer")
        passer = 1
        continuer = 2
        perdu = 2
    
    if action == 0 and IA == 1:
        while C[y][x] != "0" and C[y][x] != "I":
            x = rd.randint(0,XlongGrille-1)
            y = rd.randint(0,YlongGrille-1)
        C,nbCases, perdu = clique(A,B,C,x,y,nbCases, perdu,IA)
        


    return C,x,y,nbBombesRestantes,nbCases,perdu







"""-------------------------devoileChiffre-------------------------"""

def devoileChiffre(A,B,C,x,y):
    chiffre = A[y][x]
    pygame.event.pump()
    p=(x*tailleImage+tailleBord,y*tailleImage+tailleHaut)

    if chiffre == 0:
        fenetre.blit(i0, p)
    if chiffre == 1:
        fenetre.blit(i1, p)
    if chiffre == 2:
        fenetre.blit(i2, p)
    if chiffre == 3:
        fenetre.blit(i3, p)
    if chiffre == 4:
        fenetre.blit(i4, p)
    if chiffre == 5:
        fenetre.blit(i5, p)
    if chiffre == 6:
        fenetre.blit(i6, p)
    if chiffre == 7:
        fenetre.blit(i7, p)
    if chiffre == 8:
        fenetre.blit(i8, p)
    pygame.display.flip()

    return


"""----------------------Ecrit chiffre---------------------"""
def ecritChiffre(nombre,Xposition,Yposition):
    nombreDepart = -nombre
    if nombre < 0:
        nombre *=-1
        
    while nombre > 0:  #On decompose le nombre en chiffres
        i = 0
        c = nombre
        while c >= 10:
            c//=10
            i+=1

        p = (Xposition+28-i*13,Yposition+2)

        if c == 1:
            fenetre.blit(compteur1, p)
        if c == 2:
            fenetre.blit(compteur2, p)
        if c == 3:
            fenetre.blit(compteur3, p)
        if c == 4:
            fenetre.blit(compteur4, p)
        if c == 5:
            fenetre.blit(compteur5, p)
        if c == 6:
            fenetre.blit(compteur6, p)
        if c == 7:
            fenetre.blit(compteur7, p)
        if c == 8:
            fenetre.blit(compteur8, p)
        if c == 9:
            fenetre.blit(compteur9, p)
        if nombre == nombreDepart:
            fenetre.blit(moins, (Xposition+28-(2)*13,Yposition+2))

        nombre -= c*10**i
    
    pygame.display.flip()

    return


"""-----------------------------------------------------------------------------------------"""




def menu(passer, continuer, perdu, XlongGrille,YlongGrille,nbBombes, finissable, texte, niveau, utilisationIA, nbCases):
    fenetre_avant_menu = pygame.display.get_surface().copy()
    fenetre.blit(Menu,(0,tailleHaut-55))
    passerMenu = 0
    
    caracteres = list(texte)
    
    #Boucle infinie pour attendre le clique
    while passerMenu==0:
        if finissable:
            fenetre.blit(oui,(60,tailleHaut+90))
        else:
            fenetre.blit(non,(60,tailleHaut+90))
            
        pygame.display.flip()
        for event in pygame.event.get():
            
            if event.type == MOUSEBUTTONDOWN:
                passerMenu = 1
                    
                if event.pos[1] >= 20 and event.pos[1] < 190 and event.pos[0] < 156:
                    
                    if event.pos[1] >= 20 and event.pos[1] < 140:
                        if event.pos[1] >= 20 and event.pos[1] < 55: #Niv Facile
                        
                            XlongGrille = 9
                            YlongGrille = 9
                            
                            nbBombes = 10
                            caracteres[9] = "1"
                            niveau = '1'
                            
                            
                        if event.pos[1] >= 55 and event.pos[1] < 96: #Niv Moyen
                            XlongGrille = 16
                            YlongGrille = 16
                            
                            nbBombes = 40
                            caracteres[9] = "2"
                            niveau = '2'

        
                        if event.pos[1] >= 96 and event.pos[1] < 140: #Niv Difficile
                            XlongGrille = 40
                            YlongGrille = 16
                            
                            nbBombes = 99
                            caracteres[9] = "3"
                            niveau = '3'
                        
                        nbCases = XlongGrille*YlongGrille - nbBombes

                        passer = 1
                        continuer = 2
                        perdu = 1
                        utilisationIA = 0

                        print("Recommencer")
                
                    #Recommencer
                    
                    if event.pos[1] >= 140:
                        passerMenu = 0
                        finissable = -finissable + 1
                        
                        if finissable:
                            caracteres[24] = '1'
                        else:
                            caracteres[24] = '0'
                            
                    
            
            if event.type == KEYDOWN:
                if event.key == K_CLEAR or event.key == K_BREAK or event.key == K_ESCAPE:
                    passerMenu = 2
    
                if event.key == K_DELETE:
                    passerMenu = 2
                    passer = 2
                    perdu = 1
                    continuer = 0
            if event.type == pygame.QUIT:
                passerMenu = 2
                passer = 2
                perdu = 1
                continuer = 0
            
    texte = "".join(caracteres)
    fichier = open("../fichier texte/niveau.txt", "w")
    fichier.write(texte)
    fichier.close()
    fenetre.blit(fenetre_avant_menu,(0,0))
    
    return passer, continuer, perdu, XlongGrille, YlongGrille, nbBombes, niveau, finissable, utilisationIA, nbCases

    
    
"""-----------------------------stats----------------------"""
def stats(niveau, finissable):
    if finissable == 0:
        if niveau == '1':
            cheminFichier_temps = '../fichier texte/facile.txt'
            fichier_dates = open('../fichier texte/facile_date.txt', 'r')            
        elif niveau == '2':
            cheminFichier_temps = '../fichier texte/moyen.txt'
            fichier_dates = open('../fichier texte/moyen_date.txt', 'r')
            print("moyen")
        else:
            cheminFichier_temps = '../fichier texte/difficile.txt'
            fichier_dates = open('../fichier texte/difficile_date.txt', 'r')
    
    else:
        if niveau == '1':
            cheminFichier_temps = '../fichier texte/facileFinissable.txt'
            fichier_dates = open('../fichier texte/facileFinissable_date.txt', 'r')
        elif niveau == '2':
            cheminFichier_temps = '../fichier texte/moyenFinissable.txt'
            fichier_dates = open('../fichier texte/moyenFinissable_date.txt', 'r')                    
        else:
            cheminFichier_temps = '../fichier texte/difficileFinissable.txt'
            fichier_dates = open('../fichier texte/difficileFinissable_date.txt', 'r')
    
    fichier_temps = open(cheminFichier_temps, 'r')
    
    scores = fichier_temps.read()
    Liste_scores = scores.split("\n")
    
    dates = fichier_dates.read()
    Liste_dates = dates.split("\n")
    
    nbVictoires = int(Liste_scores[0][8:len(Liste_scores[0])]) #nb de victoire
    record = float(Liste_scores[2][9:len(Liste_scores[2])]) #record
    nbParties = int(Liste_scores[1][20:len(Liste_scores[1])]) #nb de victoire



    Xdates = []
    for i in range(1,len(Liste_dates)):
        Xdates.append((float(Liste_dates[i])-float(Liste_dates[1]))/86400)
    
    Yscores = []
    for i in range(3,len(Liste_scores)):
        Yscores.append(float(Liste_scores[i]))

    if Xdates != []:   
        YscoresMoy = []
        XdatesMoy = []
        nombreDePoints = 4
        
        epsilon = Xdates[-1]*86400/nombreDePoints
        """print("intervalle =",epsilon)"""
        
        i = 0
        for a in range(nombreDePoints):
            Yscoreepsilon = []
            while i < len(Xdates) and Xdates[i]*86400 <= (a+1)*epsilon:
                Yscoreepsilon.append(Yscores[i])
                i+=1
            i -= 1
            """print(Xdates[i],(a+1)*epsilon)
            print("i=",i)
            print(YscoresMoy,Yscoreepsilon)"""
            YscoresMoy.append(average(Yscoreepsilon))
            XdatesMoy.append((a+.5)*epsilon/86400)




        """print(Xdates,Yscores,YscoresMoy)"""
        
        scoreMoy = float(average(Yscores))
        if record >= 100:
            record = int(record)
        else:
            record = int(10*record)/10

        if scoreMoy >= 100:
            scoreMoy = int(scoreMoy)
        else:
            scoreMoy = int(10*scoreMoy)/10

        pl.title("Evolution de vos temps:")
        pl.plot(Xdates,Yscores,label="Temps par rapport à la date")
        pl.plot(XdatesMoy,YscoresMoy,label="Courbe moyenne")
        pl.xlabel('Date(j)')
        pl.ylabel('Temps(s)')          
        pl.text(Xdates[-1]/1.33,max(Yscores)*8.9/10,"Record    :        s")
        pl.text(Xdates[-1]/1.09,max(Yscores)*8.9/10,record)
        pl.text(Xdates[-1]/1.33,max(Yscores)*8.55/10,"Moyenne :        s")
        pl.text(Xdates[-1]/1.09,max(Yscores)*8.55/10,scoreMoy)
        pl.text(Xdates[-1]/1.33,max(Yscores)*7.85/10,int(100*nbVictoires/nbParties))
        pl.text(Xdates[-1]/1.25,max(Yscores)*7.85/10,"% victoire")
        pl.text(Xdates[-1]/1.33,max(Yscores)*8.2/10,nbVictoires)
        pl.text(Xdates[-1]/1.23,max(Yscores)*8.2/10,"/        victoires")
        pl.text(Xdates[-1]/1.2,max(Yscores)*8.2/10,nbParties)
        
        pl.legend() 
    
    
        pl.show()
    else:
        print("Pas encore de temps")
    
    return





"""------------------------------Boucle principale---------------------------"""


"""largFenetre=fenetre.get_width()
hautFenetre=fenetre.get_height()"""











while continuer!=0:
    #Ouverture de la fenetre Pygame
    
    tailleImage = min(int(tailleFenetre/max((XlongGrille/2.1),YlongGrille)),int(tailleFenetre/12))
    XmilieuEcran = int(XlongGrille*tailleImage/2)+tailleBord
    tupleTailleImage = (tailleImage,tailleImage)
    
    fenetre = pygame.display.set_mode((tailleImage*XlongGrille+2*tailleBord-4, tailleImage*YlongGrille+tailleHaut+tailleBord-4))
    
    posSmiley = (XmilieuEcran-9,tailleHaut-36)
    

    pygame.display.set_caption("Demineur")
    
    
    ##Chargement Images
    
    
    case = pygame.image.load("case.png").convert()
    caseclique = pygame.image.load("caseclique.png").convert()
    drapeauclique = pygame.image.load("drapeauclique.png").convert()
    PointInterrogationclique = pygame.image.load("PointInterrogationclique.png").convert()
    
    i0 = pygame.image.load("0.png").convert()
    i1 = pygame.image.load("1.png").convert()
    i2 = pygame.image.load("2.png").convert()
    i3 = pygame.image.load("3.png").convert()
    i4 = pygame.image.load("4.png").convert()
    i5 = pygame.image.load("5.png").convert()
    i6 = pygame.image.load("6.png").convert()
    i7 = pygame.image.load("7.png").convert()
    i8 = pygame.image.load("8.png").convert()
    drapeau = pygame.image.load("drapeau.png").convert()
    bombe = pygame.image.load("bombe.png").convert()
    bombeDeclanche = pygame.image.load("bombeclique.png").convert()
    PointInterrogation = pygame.image.load("PointInterrogation.png").convert()
    drapeaubarre = pygame.image.load("drapeaubarre.png").convert()
    
    cool = pygame.image.load("cool.png").convert()
    peur = pygame.image.load("peur.png").convert()
    perduSmiley = pygame.image.load("perdu.png").convert()
    gagne = pygame.image.load("gagne.png").convert()
    smileyDebut = pygame.image.load("smileyDebut.png").convert()
    
    
    coinbasdroit = pygame.image.load("coinbasdroit.png").convert()
    coinbasgauche = pygame.image.load("coinbasgauche.png").convert()
    coinhautdroit = pygame.image.load("coinhautdroit.png").convert()
    coinhautgauche = pygame.image.load("coinhautgauche.png").convert()
    hautgauche = pygame.image.load("hautgauche.png").convert()
    hautdroit = pygame.image.load("hautdroit.png").convert()
    
    
    borddroit = pygame.image.load("bord droit.png").convert()
    bordgauche = pygame.image.load("bord gauche.png").convert()
    bas = pygame.image.load("bas.png").convert()
    haut = pygame.image.load("haut.png").convert()
    bandeau = pygame.image.load("bandeau.png").convert()
    bandeauUni = pygame.image.load("bandeauUni.png").convert()
    
    compteur = pygame.image.load("compteur.png").convert()
    
    compteur1 = pygame.image.load("compteur1.png").convert()
    compteur2 = pygame.image.load("compteur2.png").convert()
    compteur3 = pygame.image.load("compteur3.png").convert()
    compteur4 = pygame.image.load("compteur4.png").convert()
    compteur5 = pygame.image.load("compteur5.png").convert()
    compteur6 = pygame.image.load("compteur6.png").convert()
    compteur7 = pygame.image.load("compteur7.png").convert()
    compteur8 = pygame.image.load("compteur8.png").convert()
    compteur9 = pygame.image.load("compteur9.png").convert()
    moins = pygame.image.load("moins.png").convert()
    
    
    Menu = pygame.image.load("Menu.png").convert()
    oui = pygame.image.load("oui.png").convert_alpha()
    
    non = pygame.image.load("non.png").convert_alpha()
    
        
    victoire = pygame.image.load("victoire.png").convert_alpha()
    defaite = pygame.image.load("defaite.png").convert_alpha()
    nouvRecord = pygame.image.load("record.png").convert_alpha()
    

    
    """ ------------On redimensionne ----------"""
    
    case = pygame.transform.scale(case, tupleTailleImage)
    caseclique = pygame.transform.scale(caseclique, tupleTailleImage)
    drapeauclique = pygame.transform.scale(drapeauclique, tupleTailleImage)
    PointInterrogationclique = pygame.transform.scale(PointInterrogationclique, tupleTailleImage)
    
    i0 = pygame.transform.scale(i0, tupleTailleImage)
    i1 = pygame.transform.scale(i1, tupleTailleImage)
    i2 = pygame.transform.scale(i2, tupleTailleImage)
    i3 = pygame.transform.scale(i3, tupleTailleImage)
    i4 = pygame.transform.scale(i4, tupleTailleImage)
    i5 = pygame.transform.scale(i5, tupleTailleImage)
    i6 = pygame.transform.scale(i6, tupleTailleImage)
    i7 = pygame.transform.scale(i7, tupleTailleImage)
    i8 = pygame.transform.scale(i8, tupleTailleImage)
    drapeau = pygame.transform.scale(drapeau, tupleTailleImage)
    bombe = pygame.transform.scale(bombe, tupleTailleImage)
    bombeDeclanche = pygame.transform.scale(bombeDeclanche, tupleTailleImage)
    PointInterrogation = pygame.transform.scale(PointInterrogation, tupleTailleImage)
    drapeaubarre = pygame.transform.scale(drapeaubarre, tupleTailleImage)
    
    borddroit = pygame.transform.scale(borddroit, (8,YlongGrille*tailleImage+50))
    bordgauche = pygame.transform.scale(bordgauche, (12,YlongGrille*tailleImage+50))
    bas = pygame.transform.scale(bas, (XlongGrille*tailleImage,8))
    haut = pygame.transform.scale(haut, (XlongGrille*tailleImage,55))
    bandeauUni = pygame.transform.scale(bandeauUni, (XlongGrille*tailleImage+2*tailleBord-168,19))
    
    
    
    
    
    ### creation du fond d ecran adapte la taille de la fenetre
    

    
    fenetre.blit(haut,(tailleBord,tailleHaut-55))
    fenetre.blit(bordgauche,(0,tailleHaut-50))
    fenetre.blit(borddroit,(XlongGrille*tailleImage+tailleBord,tailleHaut-50))
    fenetre.blit(bas,(tailleBord,tailleHaut+YlongGrille*tailleImage))
    
    fenetre.blit(hautgauche,(0,tailleHaut-55))
    fenetre.blit(hautdroit,(XlongGrille*tailleImage+tailleBord-1,tailleHaut-55))
    fenetre.blit(coinhautgauche,(0,tailleHaut-10))
    fenetre.blit(coinhautdroit,(XlongGrille*tailleImage+tailleBord-1,tailleHaut-11))
    fenetre.blit(coinbasdroit,(XlongGrille*tailleImage+tailleBord,tailleHaut+YlongGrille*tailleImage-1))
    fenetre.blit(coinbasgauche,(0,tailleHaut+YlongGrille*tailleImage-1))
    
    fenetre.blit(bandeauUni, (164,0))
    fenetre.blit(bandeau, (0,0))

    
    fenetre.blit(smileyDebut, (XmilieuEcran-12,tailleHaut-39))

    fenetre.blit(compteur, (XlongGrille*tailleImage+tailleBord-48,tailleHaut-39))
    
    
    
    """_____________________________________________"""

    nbBombesRestantes = nbBombes

    nbCases = XlongGrille*YlongGrille - nbBombes

    C=YlongGrille*["0"]
    for i in range(len(C)):
        C[i]=XlongGrille*["0"]
    C = array(C)
    if utilisationIA != 3:
        B = deepcopy(C)
        A = deepcopy(C)

    aideUtilise = 0
    continuer = 1
    perdu = 0

    for i in range(XlongGrille):
        for j in range(YlongGrille):
            fenetre.blit(case, (i*tailleImage+tailleBord,j*tailleImage+tailleHaut))

    pygame.event.pump()


    #Rafraichissement de l'ecran
    pygame.display.flip()
    
    if utilisationIA == 0 or IA != 3:
        IA = 0
        
    if utilisationIA == 3:
        IA = 0
    else:
        utilisationIA = 0
        if IA == 3:
            x = xDepart
            y = yDepart
        else:
            x = 5
            y = 5
        




    while nbCases>0 and perdu == 0:
        if nbBombesRestantes >-100:
            fenetre.blit(compteur, (15,tailleHaut-39))
            ecritChiffre(nbBombesRestantes,15,tailleHaut-39)

        if IA != 3:
            IA = 0

        continuer = 1
        passer = 0
        ##Boucle infinie pour attendre le clique
        while passer == 0:
            if IA == 0 and utilisationIA == 3 and nbCases == XlongGrille*YlongGrille - nbBombes:
                
                C,nbCases,perdu = clique(A,B,C,xDepart,yDepart,nbCases,perdu,IA)
            if IA == 3:
                passer = 1
                continuer = 2
            else:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if event.pos[0]-tailleBord > 0 and event.pos[0]-tailleBord < XlongGrille*tailleImage and event.pos[1]-tailleHaut > 0 and event.pos[1]-tailleHaut < YlongGrille*tailleImage:
    
                            x = floor ((event.pos[0]-tailleBord)/tailleImage)
                            y = floor (Decimal(event.pos[1]-tailleHaut)/Decimal(tailleImage))
                            p = (x*tailleImage+tailleBord,y*tailleImage+tailleHaut)
                            
                            if C[y][x] == '0':
                                fenetre.blit(caseclique, p)
                                if event.button == 1:
                                    fenetre.blit(peur, posSmiley)
                                pygame.display.flip()
                                fenetre.blit(case,p)
        
                            if C[y][x] == 'D':
                                fenetre.blit(drapeauclique, p)
                                pygame.display.flip()
                                fenetre.blit(drapeau, p)
                                
                            if C[y][x] == 'I':
                                fenetre.blit(PointInterrogationclique, p)
                                if event.button == 1:
                                    fenetre.blit(peur, posSmiley)
                                pygame.display.flip()
                                fenetre.blit(PointInterrogation, p)
        
                            fenetre.blit(cool, posSmiley)
        
                        elif event.pos[0] > 0 and event.pos[0] < XlongGrille*tailleImage and event.pos[1] > 0 and event.pos[1] < tailleHaut:
                            
                            if event.pos[1] > 0 and event.pos[1] < 19 and event.pos[0] >= 135 and event.pos[0] < 170:                                                 #Aide
                                IA = 1
                                passer = 1
                                utilisationIA = 1
                                aideUtilise = 1
            
                            elif nbCases != XlongGrille*YlongGrille - nbBombes and event.pos[1] > 0 and event.pos[1] < 19 and event.pos[0] >= 90 and event.pos[0] < 135:#Indice
                                IA = 2
                                passer = 1
                                
                            elif event.pos[1] >= 0 and event.pos[1] < 19 and event.pos[0] > 0 and event.pos[0] < 46:                                                  #Menu
                                passer, continuer, perdu, XlongGrille,YlongGrille,nbBombes, niveau, finissable, utilisationIA, nbCases = menu(passer, continuer, perdu, XlongGrille,YlongGrille,nbBombes, finissable, texte, niveau, utilisationIA, nbCases)
                                
                            elif event.pos[1] >= 0 and event.pos[1] < 19 and event.pos[0] >= 46 and event.pos[0] < 90:                                                  #Stats
                                print("stats")
                                stats(niveau,finissable)
                                
                            elif event.pos[1] > tailleHaut-39 and event.pos[1] < tailleHaut+39 and event.pos[0]> XmilieuEcran-12 and event.pos[0] < XmilieuEcran+12: #Recommenecer
                                passer = 1
                                continuer = 2
                                perdu = 1
                                utilisationIA = 0
                                aideUtilise = 1
                                print("Recommencer")
                        
    
                    if event.type == KEYDOWN:
                        if event.key == K_CLEAR or event.key == K_DELETE or event.key == K_BREAK or event.key == K_ESCAPE:
                            passer = 2
                            perdu = 1
                            continuer = 0
                    if event.type == pygame.QUIT:
                            passer = 2
                            perdu = 1
                            continuer = 0
                        
    
                    if event.type == MOUSEBUTTONUP or IA == 3:
                        passer = 1      #On arrete la boucle




            """---------------------En partie, gestion des secondes:--------------"""
            if nbCases != XlongGrille*YlongGrille - nbBombes and int(time())>TInter and event.type != MOUSEBUTTONDOWN:
                TInter = int(time())
                if time()-Tini < 999:
                    fenetre.blit(compteur, (XlongGrille*tailleImage+tailleBord-48,tailleHaut-39))
                    ecritChiffre(int(time()-Tini),XlongGrille*tailleImage+tailleBord-48,tailleHaut-39)


        pygame.display.flip()
        

        if  (event.type == 6 or event.type == 5) and passer == 1 and (x == floor ((event.pos[0]-tailleBord)/tailleImage) and y == floor ((event.pos[1]-tailleHaut)/tailleImage) or IA):

            
            ##AIDE OU INDICE:

            if IA or finissable and utilisationIA == 0:
                if nbCases == XlongGrille*YlongGrille - nbBombes:
                    xDepart = x
                    yDepart = y
                C,x,y, nbBombesRestantes,nbCases,perdu = solveDemineur(A,B,C,nbBombesRestantes,nbBombes,nbCases,XlongGrille,YlongGrille,perdu,IA)
                if IA and utilisationIA == 3 and IA != 2:
                    IA = 0
                if IA == 1:
                    IA = 0
                
                
            if not(IA) or nbCases == XlongGrille*YlongGrille - nbBombes:

                """----------Si premier coup on creer la grille---------"""
                if finissable and utilisationIA != 3 and utilisationIA != 1:
                    IA = 3
                    utilisationIA = 2
                    x = xDepart
                    y = yDepart
                
                if (nbCases == XlongGrille*YlongGrille - nbBombes and (event.button == 1 or IA == 3)) and utilisationIA != 3:
                    A,B = CreerGrille(XlongGrille, YlongGrille, nbBombes, x,y)
                    
                    C=YlongGrille*["0"]
                    for i in range(len(C)):
                        C[i]=XlongGrille*["0"]
                        
                    nbBombesRestantes = nbBombes
                
                    for i in range(XlongGrille):
                        for j in range(YlongGrille):
                            fenetre.blit(case, (i*tailleImage+tailleBord,j*tailleImage+tailleHaut))
                

                if (nbCases == XlongGrille*YlongGrille - nbBombes and (event.button == 1 or IA == 3)):  
                    Tini = time()
                """---------------------------------------------------------"""

                if event.button == 1 and IA != 2 or IA == 3:
                    C,nbCases,perdu = clique(A,B,C,x,y,nbCases,perdu,IA)
                if event.button == 3:
                    C,nbBombesRestantes = clique_droit(C,x,y,nbBombesRestantes, 0)



    """----------------sortie boucle principale---------------------"""


    if nbCases == 0 and IA != 3:
        fenetre.blit(gagne, posSmiley)
        pygame.display.flip()
        Tfin= time()
        temps = int(100*(Tfin - Tini))/100
        print("gagne en ",temps,"s !!!")
        fenetre.blit(victoire, (XmilieuEcran-200,0.5*(YlongGrille*tailleImage+tailleHaut)))
        pygame.display.flip()
        


    ##Enregistrer les scores
    if nbCases != XlongGrille*YlongGrille - nbBombes and utilisationIA != 2 and aideUtilise == 0:
        if utilisationIA != 3:
            print(nbCases,XlongGrille*YlongGrille - nbBombes)
        utilisationIA = 0
        if finissable == 0:
            if niveau == '1':
                cheminFichier_temps = '../fichier texte/facile.txt'
                fichier_dates = open('../fichier texte/facile_date.txt', 'a')            
            elif niveau == '2':
                cheminFichier_temps = '../fichier texte/moyen.txt'
                fichier_dates = open('../fichier texte/moyen_date.txt', 'a')
                print("moyen")
            else:
                cheminFichier_temps = '../fichier texte/difficile.txt'
                fichier_dates = open('../fichier texte/difficile_date.txt', 'a')
        
        else:
            if niveau == '1':
                cheminFichier_temps = '../fichier texte/facileFinissable.txt'
                fichier_dates = open('../fichier texte/facileFinissable_date.txt', 'a')
            elif niveau == '2':
                cheminFichier_temps = '../fichier texte/moyenFinissable.txt'
                fichier_dates = open('../fichier texte/moyenFinissable_date.txt', 'a')                    
            else:
                cheminFichier_temps = '../fichier texte/difficileFinissable.txt'
                fichier_dates = open('../fichier texte/difficileFinissable_date.txt', 'a')
        
        fichier_temps = open(cheminFichier_temps, 'a')
    
                
        if perdu == 0 and (utilisationIA == 0 or utilisationIA == 3):
            print("Enregistrement des scores")
            
            fichier_temps.write("\n")
            fichier_temps.write(str(temps))
            fichier_dates.write("\n")
            fichier_dates.write(str(int(time()-1533934900)))
            
            fichier_temps.close()
            
            
        fichier_temps = open(cheminFichier_temps, 'r')
        
        scores = fichier_temps.read()
        Liste_scores = scores.split("\n")
        """print(Liste_scores)"""
        
        if perdu == 0 and (utilisationIA == 0 or utilisationIA == 3):
            nbVictoires = int(Liste_scores[0][8:]) #nb de victoire +1
            nbVictoires += 1
            Liste_scores[0] = Liste_scores[0][0:8] + str(nbVictoires)
            
            print("nb de nbVictoires =",nbVictoires)
            
            record = float(Liste_scores[2][9:]) #record
            if temps < record:
                record = temps
                Liste_scores[2] = Liste_scores[2][0:9] + str(record)
                print("Nouveau record !")
                fenetre.blit(nouvRecord, (XmilieuEcran-190,0.3*(YlongGrille*tailleImage+tailleHaut)))
                pygame.display.flip()
                
    
        nbParties = int(Liste_scores[1][20:]) #nb de victoire + 1
        nbParties += 1
        Liste_scores[1] = Liste_scores[1][0:20] + str(nbParties)
        
        print("nb de parties =",nbParties)
        
        
        scores = ""
        
        for i in range(len(Liste_scores)-1):
            scores += Liste_scores[i] + "\n"
        scores += Liste_scores[len(Liste_scores)-1]
        
            
        fichier_temps.close()
        
        with open(cheminFichier_temps, "w") as fichier_temps:
            fichier_temps.write(scores)
        
        fichier_temps.close()
        fichier_dates.close()
        
    if IA == 3 and nbCases == 0:
        utilisationIA = 3
        IA = 0


    """----------------------recommencer ?--------------------------"""
    while continuer == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_CLEAR or event.key == K_DELETE or event.key == K_BREAK or event.key == K_ESCAPE:
                    continuer = 0
                else:
                    continuer = 2
            
            if event.type == pygame.QUIT:
                continuer = 0


            if event.type == MOUSEBUTTONUP or perdu == 2:
                continuer = 2
        
                

pygame.quit()
