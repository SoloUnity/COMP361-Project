from models.rover import Rover

def create_curiosity():
    return Rover(
        name="Curiosity",
        weight=900,
        yearLaunched=2011,
        status="Healthy",
        manufacturer="NASA",
        top_speed=0.14,
        wheel_count=6,
        max_incline=45.0,
        sprite_file_path="gui/images/rovers/curiosity.png",
        total_distance_traveled=28.06,
        power_source="Nuclear",
        description="Add description to presets.py"
    )

def create_perseverance():
    return Rover(
        name="Perseverance",
        weight=1025,
        yearLaunched=2020,
        status="Healthy",
        manufacturer="NASA",
        top_speed=0.14,
        wheel_count=6,
        max_incline=30.0,
        sprite_file_path="gui/images/rovers/perseverance.png",
        total_distance_traveled=33.01,
        power_source="Nuclear",
        description="NASA's Mars Perseverance rover seeks signs of ancient life and collects samples of rock and regolith for possible Earth return."
    )

def create_lunokhod1():
    return Rover(
        name="Lunokhod 1",
        weight=756,
        yearLaunched=1970,
        status="Healthy",
        manufacturer="Lavochkin",
        top_speed=2.0,
        wheel_count=8,
        max_incline=20.0,
        sprite_file_path="gui/images/rovers/lunokhod.png",
        total_distance_traveled=10.54,
        power_source="Solar",
        description="Lunokhod 1 was the first lunar rover to land on the Moon by the Soviet Union as part of its Lunokhod program."
    )

def create_lunokhod2():
    return Rover(
        name="Lunokhod 2",
        weight=840,
        yearLaunched=1973,
        status="Healthy",
        manufacturer="Lavochkin",
        top_speed=2.0,
        wheel_count=8,
        max_incline=30.0,
        sprite_file_path="gui/images/rovers/lunokhod.png", 
        total_distance_traveled=39.0,
        power_source="Solar",
        description="Lunokhod 2 was the second lunar rover to land on the Moon by the Soviet Union as part of its Lunokhod program."
    )