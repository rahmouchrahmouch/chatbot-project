from fpdf import FPDF

texte = """Voici un exemple de plan d'entraînement pour vous :

Lundi (Entraînement)

Échauffement : 10 minutes de cardio (tapis roulant, vélo, etc.)
Entraînement de la poitrine et des triceps :
Développé couché : 3 séries de 12 répétitions
Développé incliné : 3 séries de 12 répétitions
Triceps : 3 séries de 12 répétitions
Étirement : 10 minutes
Mardi (Repos)

Pas d'entraînement aujourd'hui, reposez-vous et récupérez !
Mercredi (Entraînement)

Échauffement : 10 minutes de cardio (tapis roulant, vélo, etc.)
Entraînement des jambes et des épaules :
Squat : 3 séries de 12 répétitions
Leg Press : 3 séries de 12 répétitions
Épaules : 3 séries de 12 répétitions
Étirement : 10 minutes
Jeudi (Repos)

Pas d'entraînement aujourd'hui, reposez-vous et récupérez !
Vendredi (Entraînement)

Échauffement : 10 minutes de cardio (tapis roulant, vélo, etc.)
Entraînement du dos et des biceps :
Tractions : 3 séries de 12 répétitions
Rowing : 3 séries de 12 répétitions
Biceps : 3 séries de 12 répétitions
Étirement : 10 minutes
Samedi et Dimanche (Repos)

Pas d'entraînement ces jours-là, reposez-vous et récupérez !
C'est juste un exemple de plan d'entraînement, et vous pouvez l'adapter à vos besoins et à vos préférences. Il est important de ne pas oublier de vous échauffer avant chaque entraînement et de vous étirer après chaque entraînement. Il est également important de boire suffisamment d'eau et de manger une alimentation équilibrée pour soutenir votre entraînement.
Machines :

Développé couché : c'est une machine qui vous permet de développer votre poitrine. Vous vous allongez sur un banc et vous poussez une barre avec vos mains.
Développé incliné : c'est une machine qui vous permet de développer votre poitrine, mais avec un angle incliné. Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Triceps : c'est une machine qui vous permet de développer vos triceps. Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Squat : c'est une machine qui vous permet de développer vos jambes. Vous vous tenez debout et vous poussez une barre avec vos jambes.
Leg Press : c'est une machine qui vous permet de développer vos jambes. Vous vous asseyez sur un banc et vous poussez une barre avec vos jambes.
Épaules : c'est une machine qui vous permet de développer vos épaules. Vous vous tenez debout et vous poussez une barre avec vos épaules.
Tractions : c'est une machine qui vous permet de développer votre dos. Vous vous tenez debout et vous poussez une barre avec vos mains.
Rowing : c'est une machine qui vous permet de développer votre dos. Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Biceps : c'est une machine qui vous permet de développer vos biceps. Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Exercices :

Développé couché : 3 séries de 12 répétitions
Vous vous allongez sur un banc et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
Développé incliné : 3 séries de 12 répétitions
Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
Triceps : 3 séries de 12 répétitions
Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
Squat : 3 séries de 12 répétitions
Vous vous tenez debout et vous poussez une barre avec vos jambes.
Vous inspirez et vous poussez la barre vers le bas.
Vous expirez et vous ramenez la barre vers le haut.
Leg Press : 3 séries de 12 répétitions
Vous vous asseyez sur un banc et vous poussez une barre avec vos jambes.
Vous inspirez et vous poussez la barre vers le bas.
Vous expirez et vous ramenez la barre vers le haut.
Épaules : 3 séries de 12 répétitions
Vous vous tenez debout et vous poussez une barre avec vos épaules.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
Tractions : 3 séries de 12 répétitions
Vous vous tenez debout et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
Rowing : 3 séries de 12 répétitions
Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le bas.
Vous expirez et vous ramenez la barre vers le haut.
Biceps : 3 séries de 12 répétitions
Vous vous asseyez sur un banc et vous poussez une barre avec vos mains.
Vous inspirez et vous poussez la barre vers le haut.
Vous expirez et vous ramenez la barre vers le bas.
"""

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

for ligne in texte.split('\n'):
    pdf.cell(0, 10, ligne, ln=True)

pdf.output("exemple.pdf")
