import pygame
import sys
import carla
import numpy as np

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

# Set up camera sensor
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))  # Camera position relative to vehicle
camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

# Camera image handling
camera_surface = None
def process_image(image):
    global camera_surface
    # Convert CARLA raw image data to Pygame surface
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = array.reshape((image.height, image.width, 4))  # RGBA format
    array = array[:, :, :3]  # Take only RGB (ignore A)
    array = array[:, :, ::-1]  # Convert from BGRA to RGB
    camera_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))  # Transpose for Pygame display

# Attach callback to the camera sensor to receive images
camera.listen(lambda image: process_image(image))

# Vehicle control object


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

# Main loop
try:
    while True:
        control = carla.VehicleControl()
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
        control.brake = 0
        control.hand_brake = False
        vehicle.apply_control(control)


        # Render the camera frame
        if camera_surface is not None:
            screen.blit(camera_surface, (0, 0))

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