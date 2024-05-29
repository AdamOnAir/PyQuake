import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PyQuake")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (153, 76, 0)
GRAY = (128, 128, 128)
GRASS_GREEN = (100, 200, 100)
SKY_BLUE = (135, 206, 250)
BUILDING_COLORS = [(255, 215, 0), (255, 140, 0), (255, 99, 71), (139, 69, 19)]

# Define object classes
class Person(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alive = True

    def die(self):
        self.image.fill(GRAY)
        self.alive = False

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface((30, height))
        self.image.fill(random.choice(BUILDING_COLORS))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = WINDOW_HEIGHT - height
        self.destroyed = False

    def destroy(self):
        self.image.fill(GRAY)
        self.destroyed = True

# Create sprite groups
people = pygame.sprite.Group()
buildings = pygame.sprite.Group()

# Add some initial objects
for _ in range(10):
    x = random.randint(50, WINDOW_WIDTH - 80)
    y = random.randint(WINDOW_HEIGHT - 100, WINDOW_HEIGHT - 70)
    person = Person(x, y)
    people.add(person)

for _ in range(5):
    x = random.randint(50, WINDOW_WIDTH - 80)
    height = random.randint(50, 300)
    building = Building(x, height, height)
    buildings.add(building)

# Set up button
button_rect = pygame.Rect(WINDOW_WIDTH - 150, 10, 140, 40)
button_color = (128, 128, 128)

# Set up Richter scale selector
richter_scale = 1
richter_scale_rect = pygame.Rect(10, 10, 200, 40)
richter_scale_color = (128, 128, 128)

# Set up object chooser
chooser_rect = pygame.Rect(10, 60, 200, 40)
chooser_color = (128, 128, 128)
chooser_text = "Place People"
chooser_mode = "people"

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Left mouse button
                if chooser_mode == "people" and mouse_y >= WINDOW_HEIGHT - 100:
                    person = Person(mouse_x, mouse_y)
                    people.add(person)
                elif chooser_mode == "buildings" and mouse_y >= WINDOW_HEIGHT - 100:
                    height = random.randint(50, 300)
                    building = Building(mouse_x, mouse_y, height)
                    buildings.add(building)
            # Check if the button was clicked
            if button_rect.collidepoint(event.pos):
                richter_scale = random.randint(1, 9)
            # Check if the Richter scale selector was clicked
            if richter_scale_rect.collidepoint(event.pos):
                if event.button == 3:  # Right mouse button
                    richter_scale += 0.5
                    if richter_scale > 9.5:
                        richter_scale = 1
            # Check if the chooser was clicked
            if chooser_rect.collidepoint(event.pos):
                if chooser_mode == "people":
                    chooser_mode = "buildings"
                    chooser_text = "Place Buildings"
                else:
                    chooser_mode = "people"
                    chooser_text = "Place People"

    # Clear the screen
    screen.fill(SKY_BLUE)

    # Draw ground
    ground_rect = pygame.Rect(0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100)
    pygame.draw.rect(screen, GRASS_GREEN, ground_rect)

    # Draw objects
    people.draw(screen)
    buildings.draw(screen)

    # Simulate earthquake
    if richter_scale > 0:
        for person in people:
            if person.alive:
                person.rect.x += random.randint(-int(richter_scale) * 10, int(richter_scale) * 10)
                person.rect.y += random.randint(-int(richter_scale) * 10, int(richter_scale) * 10)
                if richter_scale >= 7:
                    person.die()
        for building in buildings:
            if not building.destroyed:
                building.rect.x += random.randint(-int(richter_scale) * 5, int(richter_scale) * 5)
                building.rect.y += random.randint(-int(richter_scale) * 5, int(richter_scale) * 5)
                if richter_scale >= 7:
                    building.destroy()

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect)
    font = pygame.font.Font(None, 24)
    text = font.render("Provoke Earthquake", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    # Draw Richter scale selector
    pygame.draw.rect(screen, richter_scale_color, richter_scale_rect)
    text = font.render(f"Richter Scale: {richter_scale:.1f}", True, WHITE)
    text_rect = text.get_rect(center=richter_scale_rect.center)
    screen.blit(text, text_rect)

    # Draw chooser
    pygame.draw.rect(screen, chooser_color, chooser_rect)
    text = font.render(chooser_text, True, WHITE)
    text_rect = text.get_rect(center=chooser_rect.center)
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
