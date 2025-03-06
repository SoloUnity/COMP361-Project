import uuid
from datetime import datetime
from models.rover import Rover

def create_curiosity():
    return Rover(
            rover_id=str(uuid.uuid4()),
            name="Curiosity",
            dimensions="2.9 x 2.7 x 2.2",
            weight=900.0,
            date_created=datetime.now(),
            status="Healthy",
            manufacturer="NASA",
            total_range=18000.0,
            range_left=18000.0,
            top_speed=0.14,
            wheel_count=6,
            wheel_diameter=0.5,
            max_incline=30.0,
            last_trajectory=None,
            sprite_file_path="sprites/curiosity.png", # UPDATE
            total_distance_traveled=0.0,
            total_capacity=500.0,
            power_source="Nuclear"
        )

def create_perseverance():
    return Rover(
            rover_id=str(uuid.uuid4()),
            name="Perseverance",
            dimensions="3.0 x 2.7 x 2.2",
            weight=1025.0,
            date_created=datetime.now(),
            status="Healthy",
            manufacturer="NASA",
            total_range=20000.0,
            range_left=20000.0,
            top_speed=0.36,
            wheel_count=6,
            wheel_diameter=0.5,
            max_incline=30.0,
            last_trajectory=None,
            sprite_file_path="sprites/perseverance.png", # UPDATE
            total_distance_traveled=0.0,
            total_capacity=500.0,
            power_source="Nuclear"
        )

def create_lunokhod1():
    return Rover(
            rover_id=str(uuid.uuid4()),
            name="Lunokhod 1",
            dimensions="2.3 x 1.8 x 1.5",
            weight=560.0,
            date_created=datetime.now(),
            status="Healthy",
            manufacturer="Soviet Union",
            total_range=10500.0,
            range_left=10500.0,
            top_speed=0.42,
            wheel_count=8,
            wheel_diameter=0.45,
            max_incline=25.0,
            last_trajectory=None,
            sprite_file_path="sprites/lunokhod1.png", # UPDATE
            total_distance_traveled=0.0,
            total_capacity=300.0,
            power_source="Nuclear"
        )

def create_lunokhod2():
    return Rover(
            rover_id=str(uuid.uuid4()),
            name="Lunokhod 2",
            dimensions="2.3 x 1.8 x 1.5",
            weight=600.0,
            date_created=datetime.now(),
            status="Healthy",
            manufacturer="Soviet Union",
            total_range=37000.0,
            range_left=37000.0,
            top_speed=0.42,
            wheel_count=8,
            wheel_diameter=0.45,
            max_incline=25.0,
            last_trajectory=None,
            sprite_file_path="sprites/lunokhod2.png", # UPDATE
            total_distance_traveled=0.0,
            total_capacity=300.0,
            power_source="Nuclear"
        )