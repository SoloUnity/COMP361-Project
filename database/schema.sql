CREATE TABLE IF NOT EXISTS Project (
    ProjectID VARCHAR(36) PRIMARY KEY NOT NULL,
    CreatedOn DATETIME NOT NULL,
    LastSavedOn DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Trajectory (
    TrajectoryID VARCHAR(36) PRIMARY KEY NOT NULL,
    RoverID VARCHAR(36) NOT NULL,
    ProjectID VARCHAR(36) NOT NULL,
    currentCoord VARCHAR(100) NOT NULL,
    targetCoord VARCHAR(100) NOT NULL,
    startTime DATETIME NOT NULL,
    endTime DATETIME,
    coordinateList TEXT NOT NULL,
    totalDistance FLOAT NOT NULL,
    distanceTraveled FLOAT NULL
);

CREATE TABLE IF NOT EXISTS Rover (
    RoverID VARCHAR(36) PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Weight FLOAT NOT NULL,
    yearLaunched INT NOT NULL,
    Status TEXT CHECK(Status IN ('Healthy', 'Damaged', 'Lost')) NOT NULL,
    Manufacturer VARCHAR(255) NOT NULL,
    topSpeed FLOAT NOT NULL,
    wheelCount INT NOT NULL,
    maxIncline FLOAT NOT NULL,
    lastTrajectory VARCHAR(36),
    spriteFilePath VARCHAR(500),
    totalDistanceTraveled FLOAT NOT NULL,
    powerSource TEXT CHECK(powerSource IN ('Nuclear', 'Solar', 'Battery')) NOT NULL,
    description TEXT,
    FOREIGN KEY (lastTrajectory) REFERENCES Trajectory(TrajectoryID)
);

CREATE TABLE IF NOT EXISTS LicenseKey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(255) NOT NULL,
    verifiedOn DATETIME NOT NULL
);