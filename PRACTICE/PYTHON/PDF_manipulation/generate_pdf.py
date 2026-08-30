from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

doc = SimpleDocTemplate("Program_Chair_Tai_Chi_30_Zile.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Heading1'],
    fontSize=18,
    alignment=1,
    spaceAfter=12
)

story.append(Paragraph("<b>Program Zilnic Chair Tai Chi - 30 De Zile</b>", title_style))
story.append(Spacer(1, 12))

data = [["Ziua", "Exercitiu Recomandat", "Descriere Miscare"]]

# Generare program 30 zile
exercitii = [
    ("Respiratia Marii", "Ridicarea si coborarea bratelor in ritm cu respiratia."),
    ("Deschiderea Pieptului", "Ridicarea bratelor si deschiderea lor in lateral."),
    ("Rotirea Norilor", "Rotirea usoara a trunchiului cu impingerea palmei."),
    ("Mangaierea Coamei Calului", "Miscare diagonala a bratelor din pozitia de minge."),
    ("Culegerea Stelelor", "intinderea alternativa a bratelor vertical."),
    ("Mangaierea Cozii Pasarii", "Miscare circulara de imbratisare si retragere."),
    ("impingerea Valului", "Tragerea palmelor spre piept si impingerea in fata.")
]

for i in range(1, 31):
    ex = exercitii[(i - 1) % len(exercitii)]
    data.append([f"Ziua {i}", ex[0], ex[1]])

table = Table(data, colWidths=[60, 150, 280])
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C3E50')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 8),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8F9FA')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
]))

story.append(table)
doc.build(story)