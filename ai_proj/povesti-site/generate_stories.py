import os
import json

def generate():
    stories_dir = '../povesti_cu_talc'
    output_file = 'static/js/stories.js'
    
    all_stories = []
    
    # Verificăm dacă directorul există
    if not os.path.exists(stories_dir):
        print(f"Eroare: Directorul {stories_dir} nu a fost găsit.")
        return

    # Listăm toate fișierele .md
    files = [f for f in os.listdir(stories_dir) if f.endswith('.md') and f != 'README.md']
    
    for filename in files:
        file_path = os.path.join(stories_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Încercăm să extragem titlul din prima linie (dacă e ## Titlu)
            title = filename.replace('.md', '').replace('_', ' ').capitalize()
            lines = content.split('\n')
            for line in lines:
                if line.startswith('## '):
                    title = line.replace('## ', '').strip()
                    break
            
            all_stories.append({
                "title": title,
                "content": content
            })
    
    # Generăm fișierul JS
    js_content = f"const storyData = {json.dumps(all_stories, ensure_ascii=False, indent=4)};"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Succes! Am procesat {len(all_stories)} povești în {output_file}.")

if __name__ == "__main__":
    generate()
