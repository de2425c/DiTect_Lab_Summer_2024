import pygame
import numpy as np

class Vehicle:
    def __init__(self, position, speed, waypoints=[], curr=0,width=30, height=30, wheelbase=0.15, dt=0.05, color=(255,0,0)):
        self.position = np.array(position)
        self.speed = speed
        self.width = width
        self.height = height
        self.direction = np.array([1, 0])
        self.wheelbase = wheelbase
        self.dt = dt
        self.x = position[0]
        self.y = position[1]
        self.yaw = -np.pi / 2
        self.velocity = 0.0  
        self.color = color 
        self.waypoints = waypoints
        self.current_waypoint_index = self.find_closest_waypoint()
        
    def find_closest_waypoint(self):
        min_distance = float('inf')
        closest_index = 0
        for i, waypoint in enumerate(self.waypoints):
            distance = np.linalg.norm(np.array(waypoint, dtype=float) - self.position)
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        return closest_index

    def move(self, steering_angle, acceleration):
        self.velocity += acceleration * self.dt
        yaw_rate = self.velocity * np.tan(steering_angle) / self.wheelbase
        self.yaw += yaw_rate * self.dt
        self.x += self.velocity * np.cos(self.yaw) * self.dt
        self.y += self.velocity * np.sin(self.yaw) * self.dt
        self.position = np.array([self.x, self.y])
        self.direction = np.array([np.cos(self.yaw), np.sin(self.yaw)])
        
    def move_to_waypoint(self):
        if self.current_waypoint_index < len(self.waypoints):
            target = np.array(self.waypoints[self.current_waypoint_index])
            direction_to_target = target - self.position
            distance_to_target = np.linalg.norm(direction_to_target)

            if distance_to_target < 10: 
                self.current_waypoint_index += 1
                if self.current_waypoint_index >= len(self.waypoints):
                    self.current_waypoint_index = 0  
            direction_to_target = direction_to_target.astype(float)
            direction_to_target /= distance_to_target  
            self.x += direction_to_target[0] * self.speed * self.dt
            self.y += direction_to_target[1] * self.speed * self.dt
            self.position = np.array([self.x, self.y])
    
    def draw(self, screen):
        rect = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect.fill(self.color)
        rotated_rect = pygame.transform.rotate(rect, -np.degrees(self.yaw))
        rotated_rect_rect = rotated_rect.get_rect(center=(self.x, self.y))
        screen.blit(rotated_rect, rotated_rect_rect.topleft)