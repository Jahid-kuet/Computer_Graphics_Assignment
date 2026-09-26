import docx

doc = docx.Document(r'c:\Users\HP\OneDrive\Desktop\Graphics Nihal\Assignment\trial-02.docx')
for i, p in enumerate(doc.paragraphs):
    for j, r in enumerate(p.runs):
        if 'graphic' in r._element.xml:
            print(f"P{i} run{j}: text='{r.text}'")
