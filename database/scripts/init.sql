CREATE EXTENSION IF NOT EXISTS vector;

-- CREATE DATABASE procurement

-- \c procurement;

-- PACKAGES

CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    package_code INTEGER NOT NULL,
    package_description TEXT NOT NULL,
    category VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE packages
ADD CONSTRAINT chk_category
CHECK (category IN ('A','B','C','Std'));



-- MILESTONES

CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    milestone_order INTEGER NOT NULL
);

ALTER TABLE milestones
ADD CONSTRAINT uq_milestone_order UNIQUE (milestone_order);

-- PSR (PLANNED vs ACTUAL TRACKING)

CREATE TABLE psr (
    id SERIAL PRIMARY KEY,

    package_id INTEGER NOT NULL,
    milestone_id INTEGER NOT NULL,

    planned_date DATE,
    actual_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_psr_package
        FOREIGN KEY (package_id)
        REFERENCES packages(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_psr_milestone
        FOREIGN KEY (milestone_id)
        REFERENCES milestones(id)
        ON DELETE CASCADE
);

-- COMMENTS / JUSTIFICATIONS

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,

    psr_id INTEGER NOT NULL,

    comment_text TEXT NOT NULL,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_comment_psr
        FOREIGN KEY (psr_id)
        REFERENCES psr(id)
        ON DELETE CASCADE
);

-- INDEXES

CREATE INDEX idx_psr_package
ON psr(package_id);

CREATE INDEX idx_psr_milestone
ON psr(milestone_id);

CREATE INDEX idx_comments_psr
ON comments(psr_id);

-- INSERTS

INSERT INTO milestones (name, milestone_order) VALUES
('contract_open', 1),
('contract_agreement', 2),
('documentation', 3),
('package_ordering', 4),
('package_received', 5),
('package_accepted', 6),
('package_verified', 7),
('payment_open', 8),
('payment_complete', 9);

INSERT INTO packages (package_code, package_description, category)
VALUES
(1001,'Industrial Pump','A'),
(1002,'Control Valves','A'),
(1003,'Heat Exchanger','B'),
(1004,'Steel Piping','B'),
(1005,'Electrical Panels','A'),
(1006,'Instrumentation Set','B'),
(1007,'Safety Equipment','C'),
(1008,'Cooling Tower Parts','B'),
(1009,'Compressor Spare Kit','A'),
(1010,'Lubrication System','Std');

INSERT INTO psr (package_id, milestone_id, planned_date, actual_date) VALUES

-- PACKAGE 1
(1,1,'2026-01-01','2026-01-01'),
(1,2,'2026-01-05','2026-01-06'),
(1,3,'2026-01-10','2026-01-09'),
(1,4,'2026-01-15','2026-01-18'),
(1,5,'2026-02-01',NULL),
(1,6,'2026-02-05',NULL),
(1,7,'2026-02-10',NULL),
(1,8,NULL,NULL),
(1,9,NULL,NULL),

-- PACKAGE 2
(2,1,'2026-01-03','2026-01-02'),
(2,2,'2026-01-08','2026-01-08'),
(2,3,'2026-01-12','2026-01-15'),
(2,4,'2026-01-18',NULL),
(2,5,'2026-02-02',NULL),
(2,6,NULL,NULL),
(2,7,NULL,NULL),
(2,8,NULL,NULL),
(2,9,NULL,NULL),

-- PACKAGE 3
(3,1,'2026-01-02','2026-01-04'),
(3,2,'2026-01-07','2026-01-07'),
(3,3,'2026-01-14','2026-01-14'),
(3,4,'2026-01-20','2026-01-23'),
(3,5,'2026-02-10','2026-02-12'),
(3,6,'2026-02-15',NULL),
(3,7,'2026-02-18',NULL),
(3,8,NULL,NULL),
(3,9,NULL,NULL),

-- PACKAGE 4
(4,1,'2026-01-01','2026-01-01'),
(4,2,'2026-01-06','2026-01-05'),
(4,3,'2026-01-12','2026-01-12'),
(4,4,'2026-01-17','2026-01-17'),
(4,5,'2026-01-30','2026-02-02'),
(4,6,'2026-02-04','2026-02-04'),
(4,7,'2026-02-08',NULL),
(4,8,'2026-02-12',NULL),
(4,9,'2026-02-15',NULL),

-- PACKAGE 5
(5,1,'2026-01-04','2026-01-04'),
(5,2,'2026-01-09','2026-01-11'),
(5,3,'2026-01-15',NULL),
(5,4,'2026-01-21',NULL),
(5,5,NULL,NULL),
(5,6,NULL,NULL),
(5,7,NULL,NULL),
(5,8,NULL,NULL),
(5,9,NULL,NULL),

-- PACKAGE 6
(6,1,'2026-01-02','2026-01-02'),
(6,2,'2026-01-06','2026-01-07'),
(6,3,'2026-01-11','2026-01-10'),
(6,4,'2026-01-18','2026-01-19'),
(6,5,'2026-02-05',NULL),
(6,6,'2026-02-10',NULL),
(6,7,NULL,NULL),
(6,8,NULL,NULL),
(6,9,NULL,NULL),

-- PACKAGE 7
(7,1,'2026-01-03','2026-01-03'),
(7,2,'2026-01-07','2026-01-08'),
(7,3,'2026-01-12','2026-01-12'),
(7,4,'2026-01-18','2026-01-20'),
(7,5,'2026-02-01','2026-02-03'),
(7,6,'2026-02-06',NULL),
(7,7,'2026-02-10',NULL),
(7,8,NULL,NULL),
(7,9,NULL,NULL),

-- PACKAGE 8
(8,1,'2026-01-02','2026-01-01'),
(8,2,'2026-01-07','2026-01-07'),
(8,3,'2026-01-13','2026-01-14'),
(8,4,'2026-01-19',NULL),
(8,5,'2026-02-04',NULL),
(8,6,NULL,NULL),
(8,7,NULL,NULL),
(8,8,NULL,NULL),
(8,9,NULL,NULL),

-- PACKAGE 9
(9,1,'2026-01-01','2026-01-02'),
(9,2,'2026-01-05','2026-01-06'),
(9,3,'2026-01-10','2026-01-12'),
(9,4,'2026-01-15','2026-01-15'),
(9,5,'2026-01-28','2026-01-30'),
(9,6,'2026-02-02',NULL),
(9,7,'2026-02-06',NULL),
(9,8,NULL,NULL),
(9,9,NULL,NULL),

-- PACKAGE 10
(10,1,'2026-01-03','2026-01-03'),
(10,2,'2026-01-08','2026-01-09'),
(10,3,'2026-01-14','2026-01-13'),
(10,4,'2026-01-20','2026-01-22'),
(10,5,'2026-02-05','2026-02-06'),
(10,6,'2026-02-10','2026-02-10'),
(10,7,'2026-02-15',NULL),
(10,8,'2026-02-18',NULL),
(10,9,'2026-02-25',NULL);