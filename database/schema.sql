-- SQLite schema for mars_rover_sim

-- Project table
CREATE TABLE IF NOT EXISTS Project (
    ProjectID VARCHAR(36) PRIMARY KEY NOT NULL,
    CreatedOn DATETIME NOT NULL,
    LastSavedOn DATETIME NOT NULL
);

-- Trajectory table (create first since Rover references it)
CREATE TABLE IF NOT EXISTS Trajectory (
    TrajectoryID VARCHAR(36) PRIMARY KEY NOT NULL,
    RoverID VARCHAR(36) NOT NULL,
    ProjectID VARCHAR(36) NOT NULL,
    currentCoord VARCHAR(100) NOT NULL,
    targetCoord VARCHAR(100) NOT NULL,
    startTime DATETIME NOT NULL,
    endTime DATETIME,
    totalDistance FLOAT NOT NULL
);

-- Rover table
CREATE TABLE IF NOT EXISTS Rover (
    RoverID VARCHAR(36) PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Dimensions VARCHAR(50) NOT NULL,
    Weight FLOAT NOT NULL,
    dateCreated DATETIME NOT NULL,
    Status TEXT CHECK(Status IN ('Healthy', 'Damaged', 'Lost')) NOT NULL,
    Manufacturer VARCHAR(255) NOT NULL,
    totalRange FLOAT NOT NULL,
    rangeLeft FLOAT NOT NULL,
    topSpeed FLOAT NOT NULL,
    wheelCount INT NOT NULL,
    wheelDiameter FLOAT NOT NULL,
    lastTrajectory VARCHAR(36),
    spriteFilePath VARCHAR(500),
    totalDistanceTraveled FLOAT NOT NULL,
    totalCapacity FLOAT NOT NULL,
    powerSource TEXT CHECK(powerSource IN ('Nuclear', 'Solar', 'Battery')) NOT NULL,
    FOREIGN KEY (lastTrajectory) REFERENCES Trajectory(TrajectoryID)
);

-- Add foreign keys to Trajectory after both tables exist
CREATE TABLE IF NOT EXISTS Direction (
    DirectionID VARCHAR(36) PRIMARY KEY NOT NULL,
    TrajectoryID VARCHAR(36) NOT NULL,
    Angle FLOAT NOT NULL,
    distanceTraveled FLOAT NOT NULL,
    FOREIGN KEY (TrajectoryID) REFERENCES Trajectory(TrajectoryID)
);