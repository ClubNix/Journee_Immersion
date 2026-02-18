# Avant la Journée d'immersion :

---

### 1. S'assurer que le programme dans `immersion_csharp/immersion` s'execute bien sur un debian, en cas d'erreur voir le protocole de recompilation

---

### Dans le cas ou le binaire `immersion_csharp/immersion` s'execute et renvoie une instruction du style : `Usage: ./immersion <password>` :

# Pendant la Journée d'immersion

## 1. Démarrer tous les pcs de la salle cyber (au moins 25)
## 2. Après avoir booté sur kali, il faut taper le nom d'utilisateur et le mot de passe : kali:kali
## 3. Faire `Ctlr + Alt + T` pour ouvrir un terminal
## 4. Activer ssh en faisant `sudo su` puis
```bash
systemctl enable ssh && systemctl start ssh
```

### Il faut clonner le repos github sur le pc maitre de la salle cyber (celui de devant), il faudra se connecter à internet avant via le portail captif dans un navigateur.

```bash
sudo su
cd /root

git clone https://github.com/ClubNix/Journee_Immersion.git
cd Journee_Immersion/immersion_csharp
ls
# scripts Program.cs deploy.py immersion immersion.csproj

# Installer les composants nécéssaires
apt update
apt install -y sshpass

# Lancer le script de deploiement

python3 ./deploy.py

```

```bash
# Si besoin de recompiler :
# Dans Journee_Immersion/
mkdir -p dotnet && cd dotnet && wget https://builds.dotnet.microsoft.com/dotnet/Sdk/8.0.418/dotnet-sdk-8.0.418-linux-x64.tar.gz && tar -xzf dotnet-sdk-8.0.418-linux-x64.tar.gz && cd ../immersion_csharp && ../dotnet/dotnet publish immersion.csproj && cp ./bin/Release/net8.0/linux-x64/publish/immersion . 
```

## 5. S'assurer que le script fonctionne en se connectant internet avec 2 pcs idéalement un à gauche et un à droite.

## *A faire en parallèle Distribuer un sujet par pc*
## 6. S'assurer que les stickers en dessous des clavier sont présents
## >> Si ça n'est pas le cas prenez un papier et noté y le résultat de la commande ip a Que vous taperez non pas sur le pc auquel est branché le clavier mais celui à coté.
## >> Protocol pour envoyer un fichier quelconque sur tous les pc (comme le fichier Pense-bete-2.pdf)
