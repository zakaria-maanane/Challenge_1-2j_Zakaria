'''Challenge 4: Recherche d'images avec Pygame et API Pixabay  Par Zakaria Maanane , 21/04/2025'''


import pygame
import sys
import requests
import io
from urllib.parse import quote
import threading
import json

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recherche d'images")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_BLUE = (173, 216, 230)

# Police d'écriture
font = pygame.font.SysFont('Arial', 32)
prompt_font = pygame.font.SysFont('Arial', 24)
status_font = pygame.font.SysFont('Arial', 18)


PIXABAY_API_KEY = "49857019-423e42c2c3ca6c6b6f6b5ed8b"  # Inscrivez-vous sur pixabay.com pour obtenir une clé gratuite

class TextPrompt:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False
        self.color = GRAY
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activer/désactiver le prompt en cliquant dessus
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = WHITE
            else:
                self.active = False
                self.color = GRAY
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                # Effacer le dernier caractère
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Géré dans la boucle principale
                pass
            else:
                # Ajouter le caractère tapé au texte
                self.text += event.unicode
    
    def update(self):
        # Faire clignoter le curseur
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, surface):
        # Dessiner le rectangle du prompt
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        # Afficher le texte dans le prompt
        text_surface = font.render(self.text, True, BLACK)
        # Limiter l'affichage au rectangle
        text_rect = text_surface.get_rect(x=self.rect.x + 5, y=self.rect.y + 5)
        surface.blit(text_surface, text_rect)
        
        # Afficher le curseur si actif
        if self.active and self.cursor_visible:
            cursor_pos = font.size(self.text)[0] + self.rect.x + 5
            pygame.draw.line(surface, BLACK, (cursor_pos, self.rect.y + 5), 
                            (cursor_pos, self.rect.y + self.rect.height - 10), 2)

class ImageLoader:
    def __init__(self):
        self.image = None
        self.loading = False
        self.error = None
        self.current_search = ""
    
    def search_image(self, query):
        if not query or self.loading:
            return
            
        self.loading = True
        self.current_search = query
        self.error = None
        
        # Lancer la recherche d'image dans un thread séparé
        thread = threading.Thread(target=self._fetch_image, args=(query,))
        thread.daemon = True
        thread.start()
    
    def _fetch_image(self, query):
        try:
            # Utiliser l'API Pixabay pour obtenir une image
            # Pour plus d'informations: https://pixabay.com/api/docs/
            url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={quote(query)}&image_type=photo&per_page=3"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = json.loads(response.content)
                
                if data["totalHits"] > 0:
                    # Obtenir l'URL de la première image
                    image_url = data["hits"][0]["webformatURL"]
                    
                    # Télécharger l'image
                    img_response = requests.get(image_url, timeout=10)
                    if img_response.status_code == 200:
                        # Convertir l'image en surface Pygame
                        image_data = io.BytesIO(img_response.content)
                        image = pygame.image.load(image_data)
                        
                        # Redimensionner l'image si nécessaire
                        max_width = WIDTH - 100
                        max_height = HEIGHT - 200
                        img_width, img_height = image.get_size()
                        
                        if img_width > max_width or img_height > max_height:
                            # Garder le ratio
                            ratio = min(max_width / img_width, max_height / img_height)
                            new_size = (int(img_width * ratio), int(img_height * ratio))
                            self.image = pygame.transform.smoothscale(image, new_size)
                        else:
                            self.image = image
                    else:
                        self.error = f"Erreur lors du téléchargement de l'image: {img_response.status_code}"
                else:
                    self.error = "Aucune image trouvée pour cette recherche"
            else:
                self.error = f"Erreur API: {response.status_code}"
        except Exception as e:
            self.error = f"Erreur: {str(e)}"
        
        self.loading = False

def main():
    clock = pygame.time.Clock()
    prompt = TextPrompt(50, 50, 700, 50)
    image_loader = ImageLoader()
    
    # Texte d'instruction
    instruction_text = prompt_font.render("Écrivez ce que vous voulez voir et appuyez sur Entrée", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(WIDTH//2, 130))
    
    # Message d'alerte pour la clé API
    api_key_alert = None
    if PIXABAY_API_KEY == "VOTRE_CLE_API_PIXABAY":
        api_key_alert = status_font.render("Veuillez remplacer 'VOTRE_CLE_API_PIXABAY' par votre clé API", True, (255, 0, 0))
    
    running = True
    while running:
        win.fill(LIGHT_BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            prompt.handle_event(event)
            
            # Rechercher une image quand l'utilisateur appuie sur Entrée
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and prompt.active:
                if api_key_alert is None:  # Ne rechercher que si la clé API est configurée
                    image_loader.search_image(prompt.text)
        
        prompt.update()
        prompt.draw(win)
        
        # Afficher l'instruction
        win.blit(instruction_text, instruction_rect)
        
        # Afficher l'alerte de clé API si nécessaire
        if api_key_alert:
            win.blit(api_key_alert, (WIDTH//2 - api_key_alert.get_width()//2, HEIGHT//2))
        
        # Afficher l'image ou le statut
        elif image_loader.loading:
            status_text = status_font.render(f"Chargement d'une image pour: {image_loader.current_search}...", True, BLACK)
            win.blit(status_text, (WIDTH//2 - status_text.get_width()//2, 180))
        elif image_loader.error:
            status_text = status_font.render(image_loader.error, True, (255, 0, 0))
            win.blit(status_text, (WIDTH//2 - status_text.get_width()//2, 180))
        elif image_loader.image:
            img_rect = image_loader.image.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            win.blit(image_loader.image, img_rect)
            
            # Afficher le terme de recherche au-dessus de l'image
            search_text = prompt_font.render(f"Image pour: {image_loader.current_search}", True, BLACK)
            win.blit(search_text, (WIDTH//2 - search_text.get_width()//2, 180))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()