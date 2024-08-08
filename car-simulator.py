import pygame
import numpy as np
from Vehicle import Vehicle
    
def distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))
        
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    track_image = pygame.image.load('track.png')
    track_image = pygame.transform.scale(track_image, (800, 800))
    running = True
    steering = 0
    acceleration = 0.5
    
    auton_vehicle = Vehicle(position=[40,300], speed = 2)
    
    surrounding_vehicles_positions = [[60,61], [739,60], [739,739]] #Instantiate surrounding vehicles at predetermined points (as many as you like)
    surrounding_vehicles =[]
    for pos in surrounding_vehicles_positions:
        surrounding_vehicles.append(Vehicle(position=pos,speed=10, waypoints=[[60, 60],[740, 60],[740, 740],[60, 740]], color=(0,0,255)))
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        auton_vehicle.move(steering, acceleration)
        #auton vehicle needs its own logic for
        for sur in surrounding_vehicles:
            #here surrounding vehicle can receive instructions to follow predetermined path, or take deviations
            sur.move_to_waypoint()
        
        screen.fill((255, 255, 255))
        screen.blit(track_image, (0, 0))
        
        auton_vehicle.draw(screen)
        for sur in surrounding_vehicles:
            sur.draw(screen)
            
    
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
