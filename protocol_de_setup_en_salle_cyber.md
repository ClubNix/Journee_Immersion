

# Avant la Journée d'immersion

## 1. S'assurer que le programme `rust` compile sur les distributions actuelles

## 1.1 Cas ou le programme déjà compilé marche :

**Les fichiers nécessaires sont : `boot.sh`, `deploy.sh` et `initscript`**
```bash
# déplacer ces trois fichiers dans un endroit comme /root
# Ou cloner le repos git
git clone https://github.com/ClubNix/Journee_Immersion.git
cd Journee_Immersion/immersion
ls
# boot.sh deploy.sh initscript [Autres fichiers]
chmod +x initscript
# Test du script pour voir s'il fonctionne : 
./initscript
# En cas d'erreurs dans la console, ne pas chercher plus loin et recompilé : notament si l'erreur fait allusion à une libc
sh deploy.sh
```

#### Commandes (dans le cas ou l'on doit tous recompiler si un problème de version parvient): 

```bash
apt install -y cargo

git clone https://github.com/ClubNix/Journee_Immersion.git
cd Journee_Immersion/immersion

cargo build
# ./target/debug/project
cp ./target/debug/project initscript

chmod +x initscript
# Test du script pour voir s'il fonctionne : 
./initscript

sh deploy.sh
```


# Pendant la journée d'immersion

## 1. Démarrer tous les pcs de la salle cyber (au moins **`25`**)

## 2. Après avoir booté sur kali, il faut taper le nom d'utilisateur et le mot de passe : **kali:kali**

## 3. Faire `Ctlr + Alt + T` pour ouvrir un terminal

## 4. Activer **ssh** en faisant `sudo su` puis
```bash
systemctl enable ssh && systemctl start ssh
```

## 5. S'assurer que le script  fonctionne en se connectant internet avec 2 pcs idéalement un à gauche et un à droite.

## 6. Tester le script de déploiement sur le pc de devant en faisant `sh deploy.sh`

## _A faire en parallèle_ Distribuer un sujet par pc

## 7. S'assurer que les stickers en dessous des clavier sont présents
## >> Si ça n'est pas le cas prenez un papier et noté y le résultat de la commande `ip a` **Que vous taperez non pas sur le pc auquel est branché le clavier mais celui à coté**.

