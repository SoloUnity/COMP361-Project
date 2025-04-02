CREATE TABLE IF NOT EXISTS Project (
    ProjectID VARCHAR(36) PRIMARY KEY NOT NULL,
    CreatedOn DATETIME NOT NULL,
    LastSavedOn DATETIME NOT NULL,
    TopLeftX FLOAT NOT NULL DEFAULT 0.0,
    TopLeftY FLOAT NOT NULL DEFAULT 0.0,
    BottomRightX FLOAT NOT NULL DEFAULT 100.0,
    BottomRightY FLOAT NOT NULL DEFAULT 100.0
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
    distanceTraveled FLOAT NULL,
    algo VARCHAR(36) NOT NULL,
    heuristics JSON DEFAULT '{}'
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
    spriteFilePath VARCHAR(255),
    totalDistanceTraveled FLOAT NOT NULL,
    powerSource VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    lowSlopeEnergy FLOAT NOT NULL DEFAULT 10.0,
    midSlopeEnergy FLOAT NOT NULL DEFAULT 20.0,
    highSlopeEnergy FLOAT NOT NULL DEFAULT 30.0
);

CREATE TABLE IF NOT EXISTS LicenseKey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(255) NOT NULL,
    verifiedOn DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS HazardArea (
    HazardID VARCHAR(36) PRIMARY KEY NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    x1 FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    x2 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    x3 FLOAT NOT NULL,
    y3 FLOAT NOT NULL,
    x4 FLOAT NOT NULL,
    y4 FLOAT NOT NULL
);