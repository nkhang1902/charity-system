-- =====================
-- USERS TABLE
-- =====================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- =====================
-- ORGANIZATIONS TABLE
-- =====================
CREATE TABLE organizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    logo_url VARCHAR(255),
    contact_email VARCHAR(150),
    website_url VARCHAR(255),
    category VARCHAR(100),
    rating FLOAT DEFAULT 0,
    vote_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- =====================
-- CAMPAIGNS TABLE
-- =====================
CREATE TABLE campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    org_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    goal_amount DECIMAL(12,2),
    current_amount DECIMAL(12,2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'draft',
    media_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE
);

-- =====================
-- TRANSACTIONS TABLE
-- =====================
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    campaign_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    blockchain_hash VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message VARCHAR(255),
    receipt_url VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
);

-- =====================
-- USER INTERACTIONS TABLE
-- =====================
CREATE TABLE user_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id INT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    weight INT DEFAULT 1,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =====================
-- REGISTRATIONS TABLE
-- =====================
CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    org_id INT NULL,
    type VARCHAR(50) DEFAULT 'organization',
    payload JSON,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE
);

-- USERS
INSERT INTO users (name, avatar_url) VALUES
('Alice Nguyen', 'https://example.com/avatar/alice.png'),
('Alice Nguyen', 'https://example.com/avatar/alice.png'),
('Bao Tran', 'https://example.com/avatar/bao.png'),
('Minh Le', 'https://example.com/avatar/minh.png');

DELETE FROM organizations;
INSERT INTO organizations (name, description, logo_url, contact_email, website_url, category, rating, vote_count) VALUES
('EduFuture Foundation', 'Non-profit focused on improving education access in rural areas.', 'https://example.com/logo1.png', 'contact@edufuture.org', 'https://edufuture.org', 'Education', 4.7, 120),

('GreenEarth Initiative', 'Environmental organization dedicated to reforestation and climate action.', 'https://example.com/logo2.png', 'hello@greenearth.org', 'https://greenearth.org', 'Environment', 4.9, 300),

('Health4All', 'Provides healthcare access for underprivileged communities.', 'https://example.com/logo3.png', 'support@health4all.org', 'https://health4all.org', 'Health', 4.5, 90),

('Tech4Kids', 'Organization promoting digital literacy and STEM education for kids.', 'https://example.com/logo4.png', 'info@tech4kids.org', 'https://tech4kids.org', 'Education', 4.8, 150),

('CleanWater Project', 'Non-profit bringing clean drinking water to remote communities.', 'https://example.com/logo5.png', 'team@cleanwater.org', 'https://cleanwater.org', 'Environment', 4.6, 100),

('AnimalRescue Asia', 'Rescue and rehabilitation for injured and abandoned animals.', 'https://example.com/logo6.png', 'care@animalrescueasia.org', 'https://animalrescueasia.org', 'Animals', 4.7, 200),

('HopeForWomen', 'Empowerment programs and shelters for women in crisis.', 'https://example.com/logo7.png', 'help@hopeforwomen.org', 'https://hopeforwomen.org', 'Social', 4.8, 180),

('YouthSports United', 'Sports development programs for low-income youth.', 'https://example.com/logo8.png', 'contact@youthsports.org', 'https://youthsports.org', 'Sports', 4.4, 70),

('SeniorCare Connect', 'Improving lives of the elderly with social and medical support.', 'https://example.com/logo9.png', 'hello@seniorcare.org', 'https://seniorcare.org', 'Health', 4.6, 140),

('CommunityBuilders', 'Supports community development, housing, and food programs.', 'https://example.com/logo10.png', 'team@communitybuilders.org', 'https://communitybuilders.org', 'Social', 4.5, 110);

-- CAMPAIGNS
DELETE FROM campaigns;
INSERT INTO campaigns (org_id, title, description, goal_amount, current_amount, start_date, end_date, status, media_url) VALUES
(1, 'Rural School Libraries', 'Building libraries for rural primary schools.', 20000, 4500, '2025-01-01', '2025-06-01', 'active', 'https://example.com/c1.jpg'),
(1, 'Scholarships for Girls', 'Funding 50 scholarships for girls in underserved areas.', 15000, 8000, '2025-02-01', '2025-07-01', 'active', 'https://example.com/c2.jpg'),

(2, 'Reforest 10,000 Trees', 'Planting trees to restore degraded land.', 30000, 12000, '2025-01-15', '2025-05-30', 'active', 'https://example.com/c3.jpg'),
(2, 'Clean Air Awareness', 'Educational program on reducing air pollution.', 10000, 5000, '2025-03-01', '2025-08-01', 'active', 'https://example.com/c4.jpg'),

(3, 'Mobile Health Clinics', 'Running mobile clinics for remote villages.', 25000, 9000, '2025-01-10', '2025-06-15', 'active', 'https://example.com/c5.jpg'),
(3, 'Vaccination Drive', 'Supporting vaccinations for 2,000 children.', 18000, 6000, '2025-02-10', '2025-07-10', 'active', 'https://example.com/c6.jpg'),

(4, 'STEM Bootcamps', 'Free STEM bootcamps for low-income students.', 22000, 7000, '2025-01-20', '2025-05-20', 'active', 'https://example.com/c7.jpg'),
(4, 'Tech Kits for Kids', 'Providing laptops and coding kits to students.', 17000, 6500, '2025-03-05', '2025-08-05', 'active', 'https://example.com/c8.jpg'),

(5, 'Village Water Wells', 'Build sustainable water wells in 4 villages.', 28000, 11000, '2025-01-12', '2025-06-12', 'active', 'https://example.com/c9.jpg'),
(5, 'Sanitation Education', 'Programs teaching sanitation and hygiene.', 9000, 3500, '2025-03-10', '2025-09-10', 'active', 'https://example.com/c10.jpg'),

(6, 'Animal Rescue Vans', 'Buying rescue vans for emergency response.', 20000, 7500, '2025-01-15', '2025-05-15', 'active', 'https://example.com/c11.jpg'),
(6, 'Stray Dog Medical Fund', 'Medical care for 300 stray dogs.', 12000, 4000, '2025-02-20', '2025-08-20', 'active', 'https://example.com/c12.jpg'),

(7, 'Women Shelter Renovation', 'Renovating two crisis shelters.', 26000, 15000, '2025-01-08', '2025-06-08', 'active', 'https://example.com/c13.jpg'),
(7, 'Job Training for Women', 'Vocational training for 100 women.', 14000, 6000, '2025-03-12', '2025-08-12', 'active', 'https://example.com/c14.jpg'),

(8, 'Youth Football Kits', 'Providing equipment to youth football teams.', 8000, 2500, '2025-01-25', '2025-06-25', 'active', 'https://example.com/c15.jpg'),
(8, 'Sports Coaching Program', 'Hiring coaches for long-term youth sports programs.', 15000, 5000, '2025-03-18', '2025-08-18', 'active', 'https://example.com/c16.jpg'),

(9, 'Elderly Care Packages', 'Monthly care packages for 300 seniors.', 13000, 4500, '2025-02-01', '2025-07-01', 'active', 'https://example.com/c17.jpg'),
(9, 'Home Visits for Seniors', 'Medical home visits to the elderly.', 20000, 9000, '2025-01-20', '2025-06-20', 'active', 'https://example.com/c18.jpg'),

(10, 'Community Food Drive', 'Feeding 1,000 families in need.', 16000, 6000, '2025-02-15', '2025-07-15', 'active', 'https://example.com/c19.jpg'),
(10, 'Affordable Housing Fund', 'Supporting housing repairs for low-income families.', 30000, 15000, '2025-03-10', '2025-09-10', 'active', 'https://example.com/c20.jpg');

-- CAMPAIGNS (50 sample rows)
INSERT INTO campaigns (org_id, title, description, goal_amount, current_amount, start_date, end_date, status, media_url) VALUES
(1, 'STEM Scholarships for Underprivileged Youth', 'Support talented students from low-income families to attend STEM programs.', 50000, 12000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/stem_scholarship.jpg'),
(1, 'After-school Tutoring Program', 'Provide tutoring and mentorship for high school students struggling with math and science.', 30000, 8000, '2025-11-15', '2026-05-15', 'active', 'https://example.com/images/tutoring.jpg'),
(1, 'EduFuture Digital Library', 'Create an online library of educational resources accessible to all students.', 20000, 5000, '2025-12-10', '2026-06-30', 'active', 'https://example.com/images/digital_library.jpg'),
(2, 'Tree Planting Campaign', 'Plant 10,000 trees in urban areas to improve air quality.', 40000, 15000, '2025-11-01', '2026-04-30', 'active', 'https://example.com/images/tree_planting.jpg'),
(2, 'Plastic-Free Cities', 'Promote and support community initiatives to reduce single-use plastics.', 25000, 7000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/plastic_free.jpg'),
(2, 'Community Garden Program', 'Build community gardens in neighborhoods to increase green spaces.', 30000, 10000, '2025-12-15', '2026-07-31', 'active', 'https://example.com/images/community_garden.jpg'),
(3, 'Mobile Health Clinics', 'Deploy mobile clinics to underserved rural areas for basic health services.', 60000, 20000, '2025-11-05', '2026-06-30', 'active', 'https://example.com/images/mobile_clinic.jpg'),
(3, 'Vaccination Drive', 'Organize community vaccination campaigns for children and elderly.', 40000, 15000, '2025-11-10', '2026-05-31', 'active', 'https://example.com/images/vaccine_drive.jpg'),
(3, 'Health Awareness Workshops', 'Educate communities on nutrition, hygiene, and preventive healthcare.', 20000, 8000, '2025-12-01', '2026-04-30', 'active', 'https://example.com/images/health_workshops.jpg'),
(4, 'Coding Bootcamp for Kids', 'Teach programming and robotics to children aged 8-15.', 35000, 12000, '2025-11-20', '2026-05-31', 'active', 'https://example.com/images/coding_bootcamp.jpg'),
(4, 'Tech for Girls', 'Encourage girls to participate in technology workshops and competitions.', 30000, 10000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/tech_for_girls.jpg'),
(4, 'Robotics Club Expansion', 'Provide resources and kits to expand school robotics clubs.', 25000, 8000, '2025-11-25', '2026-05-15', 'active', 'https://example.com/images/robotics_club.jpg'),
(5, 'Clean Water Wells', 'Build and maintain clean water wells in villages.', 50000, 18000, '2025-11-01', '2026-07-31', 'active', 'https://example.com/images/wells.jpg'),
(5, 'Water Filtration Kits', 'Distribute household water filtration kits to prevent waterborne diseases.', 20000, 7000, '2025-11-15', '2026-06-30', 'active', 'https://example.com/images/filters.jpg'),
(5, 'Hygiene Education Program', 'Educate communities on proper hygiene and sanitation practices.', 15000, 5000, '2025-12-01', '2026-04-30', 'active', 'https://example.com/images/hygiene.jpg'),
(6, 'Animal Shelter Renovation', 'Upgrade facilities to provide better care for rescued animals.', 40000, 12000, '2025-11-05', '2026-06-30', 'active', 'https://example.com/images/shelter.jpg'),
(6, 'Pet Adoption Campaign', 'Promote adoption of abandoned pets through community events.', 15000, 5000, '2025-12-01', '2026-05-31', 'active', 'https://example.com/images/adoption.jpg'),
(6, 'Wildlife Rescue Training', 'Train volunteers in animal rescue and rehabilitation techniques.', 20000, 7000, '2025-11-20', '2026-06-30', 'active', 'https://example.com/images/wildlife_training.jpg'),
(7, 'Women Empowerment Workshops', 'Organize workshops on skill development and entrepreneurship for women.', 30000, 10000, '2025-11-15', '2026-05-15', 'active', 'https://example.com/images/women_workshops.jpg'),
(7, 'Microfinance Program', 'Provide small loans to women to start businesses.', 50000, 20000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/microfinance.jpg'),
(7, 'Career Mentorship', 'Pair professional women mentors with young women seeking career guidance.', 25000, 8000, '2025-12-10', '2026-06-30', 'active', 'https://example.com/images/mentorship.jpg'),
(8, 'Youth Soccer League', 'Organize community soccer tournaments for youth engagement.', 20000, 7000, '2025-11-01', '2026-05-31', 'active', 'https://example.com/images/soccer.jpg'),
(8, 'Basketball Skills Camp', 'Provide training and development camps for young athletes.', 15000, 5000, '2025-11-20', '2026-04-30', 'active', 'https://example.com/images/basketball.jpg'),
(8, 'Mentorship for Young Athletes', 'Connect youth with experienced sports mentors.', 10000, 3000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/mentorship_sports.jpg'),
(9, 'Senior Care Home Upgrade', 'Improve facilities and services for elderly residents.', 40000, 15000, '2025-11-01', '2026-06-30', 'active', 'https://example.com/images/senior_home.jpg'),
(9, 'Home Care Assistance', 'Provide home care support and regular checkups for seniors.', 25000, 8000, '2025-11-15', '2026-05-15', 'active', 'https://example.com/images/home_care.jpg'),
(9, 'Senior Nutrition Program', 'Deliver meals and nutrition guidance for elderly residents.', 15000, 5000, '2025-12-01', '2026-04-30', 'active', 'https://example.com/images/nutrition.jpg'),
(10, 'Community Builders Fund', 'Support local initiatives to improve neighborhood infrastructure.', 50000, 20000, '2025-11-01', '2026-07-31', 'active', 'https://example.com/images/community_fund.jpg'),
(10, 'Local Arts Festival', 'Fund a community arts festival to promote cultural engagement.', 30000, 10000, '2025-11-15', '2026-05-15', 'active', 'https://example.com/images/arts_festival.jpg'),
(10, 'Neighborhood Cleanup Drive', 'Organize cleanups and environmental awareness events.', 20000, 7000, '2025-12-01', '2026-06-30', 'active', 'https://example.com/images/cleanup.jpg');

-- USER INTERACTIONS
DELETE FROM user_interactions;
INSERT INTO user_interactions (user_id, target_type, target_id, action_type, weight) VALUES

-- User 4: Mixed random
(4, 'campaign', 4, 'view', 1),
(4, 'campaign', 10, 'click', 2),
(4, 'campaign', 15, 'view', 1),
(4, 'campaign', 19, 'donate', 4);

-- TRANSACTIONS
INSERT INTO transactions (user_id, campaign_id, amount, status, blockchain_hash, message, receipt_url) VALUES
(1, 1, 100.00, 'confirmed', '0xabc123', 'Keep up the great work!', 'https://example.com/receipts/tx1.pdf'),
(2, 1, 250.00, 'confirmed', '0xdef456', 'For the kids!', 'https://example.com/receipts/tx2.pdf'),
(3, 2, 300.00, 'pending', '0xghi789', 'Let’s make it green.', 'https://example.com/receipts/tx3.pdf');

-- REGISTRATIONS
INSERT INTO registrations (org_id, type, payload, status) VALUES
(1, 'organization', JSON_OBJECT('documents', 'submitted', 'reviewer', 'admin1'), 'approved'),
(2, 'campaign', JSON_OBJECT('draft_id', 3, 'submitted_by', 'Green Earth'), 'pending');
