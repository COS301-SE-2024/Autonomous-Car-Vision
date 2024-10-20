import pygame
import sys
import carla
import time

# Initialize Pygame
pygame.init()

# Window settings
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Logitech G920 + CARLA Integration")

# Set up font for displaying values on screen
font = pygame.font.SysFont(None, 48)

# Connect to CARLA Simulator
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# Spawn a vehicle in CARLA
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.filter('vehicle.*')[0]  # Grab the first available vehicle
spawn_point = world.get_map().get_spawn_points()[0]
vehicle = world.spawn_actor(vehicle_bp, spawn_point)

# Vehicle control object
control = carla.VehicleControl()

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
    vehicle.destroy()
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
    throttle = 1 - throttle  # Flip throttle value (0 is at the bottom, 1 is at the top)
    
    brake = (joystick.get_axis(2) + 1) / 2.0  # Normalize to 0 to 1
    brake = 1 - brake  # Flip brake value (0 is at the bottom, 1 is at the top)
    
    # Buttons
    buttons = []
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            buttons.append(i)
    
    return steering, throttle, brake, buttons

def render_carla_frame():
    """
    Grab the current frame from the CARLA simulator and display it.
    """
    camera_image = None
    for actor in world.get_actors():
        if actor.type_id.startswith('sensor.camera'):
            camera_image = actor.listen(lambda image: image)
            break
    if camera_image:
        array = pygame.surfarray.make_surface(camera_image.raw_data)
        screen.blit(array, (0, 0))

# Main loop
try:
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vehicle.destroy()
                pygame.quit()
                sys.exit()

        pygame.event.pump()  # Process event queue
        
        # Get steering wheel inputs
        steering, throttle, brake, buttons = get_wheel_input()

        # Apply the inputs to the vehicle control
        control.steer = steering
        control.throttle = throttle
        control.brake = brake
        vehicle.apply_control(control)
        
        # Clear the screen (for overlay)
        screen.fill((0, 0, 0))

        # Render CARLA frame
        render_carla_frame()

        # Overlay the steering, throttle, brake values, and buttons on the screen
        draw_text(f"Steering: {steering:.2f}", 50, 50)
        draw_text(f"Throttle: {throttle:.2f}", 50, 150)
        draw_text(f"Brake: {brake:.2f}", 50, 250)
        draw_text(f"Buttons Pressed: {buttons}", 50, 350)

        # Update the display
        pygame.display.flip()

        pygame.time.wait(50)  # Simulate at around 20 FPS

finally:
    # Clean up CARLA and Pygame resources
    vehicle.destroy()
    pygame.quit()
