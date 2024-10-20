import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Logitech G920 Input Test")

# Set up font for displaying values on screen
font = pygame.font.SysFont(None, 48)

# Find the connected joystick (Logitech G920)
joystick = None
for i in range(pygame.joystick.get_count()):
    j = pygame.joystick.Joystick(i)
    j.init()
    print(f"Joystick {i}: {j.get_name()}")
    if "Logitech G HUB G920 Driving Force Racing Wheel USB" in j.get_name():
        joystick = j
        print(f"Found {joystick.get_name()}!")
        break

if not joystick:
    print("No Logitech G920 found. Exiting...")
    sys.exit()

def draw_text(text, x, y, color=(255, 255, 255)):
    """Helper function to draw text on the Pygame window."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def get_wheel_input():
    """
    Get steering wheel, pedals, and buttons input from the Logitech G920.
    """
    # Axis 0: Steering wheel (-1 to 1)
    steering = joystick.get_axis(0)
    
    throttle = (joystick.get_axis(1) + 1) / 2.0  # Normalize to 0 to 1
    
    # Flip throttle value (0 is at the bottom, 1 is at the top)
    throttle = 1 - throttle
    
    brake = (joystick.get_axis(2) + 1) / 2.0  # Normalize to 0 to 1
    
    brake = 1 - brake  # Flip brake value (0 is at the bottom, 1 is at the top)
    
    clutch = (joystick.get_axis(3) + 1) / 2.0  # Normalize to 0 to 1
    
    clutch = 1 - clutch  # Flip clutch value (0 is at the bottom, 1 is at the top)
    
    # Buttons
    buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            buttons.append(i)
    
    return steering, throttle, brake, clutch, buttons

# Main loop
try:
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.event.pump()  # Process event queue
        
        # Get steering wheel inputs
        steering, throttle, brake, clutch, buttons = get_wheel_input()
        
        # Print the values to the console
        print(f"Steering: {steering:.2f}, Throttle: {throttle:.2f}, Brake: {brake:.2f}, Clutch: {clutch:.2f}, Buttons Pressed: {buttons}")

        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw steering, throttle, brake values and buttons on the screen
        draw_text(f"Steering: {steering:.2f}", 50, 50)
        draw_text(f"Throttle: {throttle:.2f}", 50, 150)
        draw_text(f"Brake: {brake:.2f}", 50, 250)
        draw_text(f"Clutch: {clutch:.2f}", 50, 350)
        draw_text(f"Buttons Pressed: {buttons}", 50, 450)

        # Update the display
        pygame.display.flip()

        pygame.time.wait(50)  # Simulate at around 20 FPS

finally:
    # Quit Pygame
    pygame.quit()
