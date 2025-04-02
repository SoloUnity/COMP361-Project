_HazardArea_

# Attributes:

- hazard_id: str
- name: str
- description: str
- x1, y1, x2, y2, x3, y3, x4, y4: float (Coordinates of the hazard area)

# Functions:

- create_hazard_area(name, description, x1, y1, x2, y2, x3, y3, x4, y4) -> HazardArea
- delete_hazard_area(hazard_id: str) -> bool
- get_all_hazard_areas() -> List[HazardArea]

---

_Rover_

# Attributes:

- rover_id: str
- name: str
- weight: float
- yearLaunched: int
- status: str
- manufacturer: str
- top_speed: float
- wheel_count: int
- max_incline: float
- last_trajectory: str | None
- sprite_file_path: str
- total_distance_traveled: float
- power_source: str
- description: str
- lowSlopeEnergy: float
- midSlopeEnergy: float
- highSlopeEnergy: float

# Functions:

- get_rover_by_id(rover_id: str) -> Rover | None
- create_rover(rover_type: str) -> Rover
- delete_rover(rover_id: str) -> bool
- Preset creators:
  - create_curiosity() -> Rover
  - create_perseverance() -> Rover
  - create_lunokhod1() -> Rover
  - create_lunokhod2() -> Rover

---

_Project_

# Attributes:

- project_id: str
- created_on: datetime
- last_saved_on: datetime
- top_left_x, top_left_y: float
- bottom_right_x, bottom_right_y: float

# Functions:

- create_project() -> Project
- delete_project(project_id: str) -> bool
- get_project_by_id(project_id: str) -> Project | None
- get_bounding_box() -> Tuple[Tuple[float, float], Tuple[float, float]]
- set_bounding_box(box: Tuple[Tuple[float, float], Tuple[float, float]]) -> None

---

_Trajectory_

# Attributes:

- trajectory_id: str
- rover_id: str
- project_id: str
- current_coord: str
- target_coord: str
- start_time: datetime
- end_time: datetime | None
- coordinate_list: list
- total_distance: float
- distance_traveled: float

# Functions:

- get_trajectory_by_id(trajectory_id: str) -> Trajectory | None
- create_trajectory(rover_id, project_id, current_coord, target_coord, coordinate_list=None, total_distance=0.0) -> Trajectory
- delete_trajectory(trajectory_id: str) -> bool
