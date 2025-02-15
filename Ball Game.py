import pygame
import random

pygame.init()

# Display Resolution
display = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Ball Game")

# Real-time clock / fps
clock = pygame.time.Clock()
FPS = 50

# Set ng Acceleration para sa bounce ng ball
ACCELERATION = 0.5

# Font for displaying points and menu
title_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 36)

def get_random_color():
    """Generate a random color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Ball():
    # initialize yung ball
    def __init__(self):
        self.x = 500
        self.y = 200
        self.velocity = 10
    
    # define mo yung circle (ball) with border
    def draw(self):
        # Draw the border
        pygame.draw.circle(display, (0, 0, 0), (self.x, int(self.y)), 17)  # Border color and radius
        # Draw the ball
        pygame.draw.circle(display, (255, 215, 0), (self.x, int(self.y)), 15)  # Ball color and radius

    # define mo yung movement ng ball
    def move(self):
        self.velocity += ACCELERATION
        self.y += self.velocity
        if self.y >= 600 - 15:  # Check if the ball hits the bottom boundary
            self.y = 600 - 15  # Reset the ball's position to the bottom boundary
            self.velocity = -self.velocity  # Reverse the velocity to make the ball bounce
        elif self.y <= 15:  # Check if the ball hits the top boundary
            self.y = 15  # Reset the ball's position to the top boundary
            self.velocity = -self.velocity  # Reverse the velocity to make the ball bounce

    # define mo yung control ng ball
    def control(self, keys):
        if keys[pygame.K_LEFT] and self.x > 15:  # Restrict movement within the left border
            self.x -= 5
        if keys[pygame.K_RIGHT] and self.x < 1000 - 15:  # Restrict movement within the right border
            self.x += 5
        if keys[pygame.K_UP] and self.y > 15:  # Restrict movement within the top border
            self.y -= 5
        if keys[pygame.K_DOWN] and self.y < 600 - 15:  # Restrict movement within the bottom border
            self.y += 5

    # check for collision with obstacle
    def check_collision(self, obstacle):
        ball_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)  # Ball's bounding box
        obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        return ball_rect.colliderect(obstacle_rect)

class Obstacle():
    # initialize yung obstacle
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    # draw the obstacle
    def draw(self):
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))  # Obstacle color and dimensions

    # set a random position for the obstacle
    def set_random_position(self):
        self.x = random.randint(0, 1000 - self.width)
        self.y = random.randint(0, 600 - self.height)

def draw_button(text, rect, color, border_color):
    pygame.draw.rect(display, border_color, rect, 2)  # Draw border
    display.blit(text, text.get_rect(center=rect.center))

def menu():
    while True:
        display.fill((0, 0, 0))
        title_text = title_font.render("Ball Game", True, (255, 255, 255))
        start_text = button_font.render("Start", True, (255, 255, 255))
        quit_text = button_font.render("Quit", True, (255, 255, 255))

        title_rect = title_text.get_rect(center=(500, 200))
        start_rect = pygame.Rect(450, 280, 100, 50)
        quit_rect = pygame.Rect(450, 380, 100, 50)

        display.blit(title_text, title_rect)
        draw_button(start_text, start_rect, (255, 255, 255), (255, 255, 255))
        draw_button(quit_text, quit_rect, (255, 255, 255), (255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return  # Start the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def pause_menu():
    while True:
        display.fill((0, 0, 0))
        resume_text = button_font.render("Resume", True, (255, 255, 255))
        quit_text = button_font.render("Quit", True, (255, 255, 255))

        resume_rect = pygame.Rect(450, 280, 100, 50)
        quit_rect = pygame.Rect(450, 380, 100, 50)

        draw_button(resume_text, resume_rect, (255, 255, 255), (255, 255, 255))
        draw_button(quit_text, quit_rect, (255, 255, 255), (255, 255, 255))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    return  # Resume the game
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Game loop
def game():
    ball = Ball()
    obstacle = Obstacle(400, 300, 50, 50)  # Create an obstacle at position (400, 300) with width and height of 50
    points = 0  # Initialize points
    background_color = (255, 255, 255)  # Initial background color

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        # Move the ball
        ball.move()

        # Get the pressed keys
        keys = pygame.key.get_pressed()
        ball.control(keys)

        # Check for collision
        if ball.check_collision(obstacle):
            ball = Ball()  # Reset the ball
            obstacle.set_random_position()  # Move the obstacle to a random position
            points += 1  # Increment points
            background_color = get_random_color()  # Change the background color

        # Set the background color
        display.fill(background_color)

        # Draw the ball
        ball.draw()

        # Draw the obstacle
        obstacle.draw()

        # Display points
        points_text = button_font.render(f"Points: {points}", True, (0, 0, 0))
        display.blit(points_text, (10, 10))

        # Show pause button if points >= 10
        if points >= 10:
            pause_text = button_font.render("Pause", True, (255, 255, 255))
            pause_rect = pygame.Rect(890, 10, 100, 50)
            draw_button(pause_text, pause_rect, (255, 255, 255), (255, 255, 255))

            if pygame.mouse.get_pressed()[0] and pause_rect.collidepoint(pygame.mouse.get_pos()):
                pause_menu()

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

menu()
game()
pygame.quit()