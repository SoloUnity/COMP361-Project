CREATE DATABASE mars_rover_sim;

USE mars_rover_sim;

CREATE TABLE Project (
    ProjectID VARCHAR(36) PRIMARY KEY NOT NULL,
    CreatedOn DATETIME NOT NULL,
    LastSavedOn DATETIME NOT NULL
);

CREATE TABLE Rover (
    RoverID VARCHAR(36) PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Dimensions VARCHAR(50) NOT NULL,
    Weight FLOAT NOT NULL,
    dateCreated DATETIME NOT NULL,
    Status ENUM('Healthy', 'Damaged', 'Lost') NOT NULL,
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
    powerSource ENUM('Nuclear', 'Solar', 'Battery') NOT NULL,
    FOREIGN KEY (lastTrajectory) REFERENCES Trajectory(TrajectoryID) ON DELETE SET NULL
);

CREATE TABLE Trajectory (
    TrajectoryID VARCHAR(36) PRIMARY KEY NOT NULL,
    RoverID VARCHAR(36) NOT NULL,
    ProjectID VARCHAR(36) NOT NULL,
    currentCoord VARCHAR(100) NOT NULL,
    targetCoord VARCHAR(100) NOT NULL,
    startTime DATETIME NOT NULL,
    endTime DATETIME NULL,
    totalDistance FLOAT NOT NULL,
    FOREIGN KEY (RoverID) REFERENCES Rover(RoverID) ON DELETE CASCADE,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID) ON DELETE CASCADE
);

CREATE TABLE Direction (
    DirectionID VARCHAR(36) PRIMARY KEY NOT NULL,
    TrajectoryID VARCHAR(36) NOT NULL,
    Angle FLOAT NOT NULL,
    distanceTraveled FLOAT NOT NULL,
    FOREIGN KEY (TrajectoryID) REFERENCES Trajectory(TrajectoryID) ON DELETE CASCADE
);