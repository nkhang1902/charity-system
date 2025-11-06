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
('Bao Tran', 'https://example.com/avatar/bao.png'),
('Minh Le', 'https://example.com/avatar/minh.png');

-- ORGANIZATIONS
INSERT INTO organizations (name, description, logo_url, contact_email, website_url, category, rating, vote_count) VALUES
('Hope Foundation', 'Supporting children education in rural areas.', 'https://example.com/logo/hope.png', 'contact@hope.org', 'https://hope.org', 'Education', 4.5, 20),
('Green Earth', 'Environmental protection and reforestation projects.', 'https://example.com/logo/green.png', 'info@greenearth.org', 'https://greenearth.org', 'Environment', 4.8, 35);

-- CAMPAIGNS
INSERT INTO campaigns (org_id, title, description, goal_amount, current_amount, start_date, end_date, status, media_url) VALUES
(1, 'Books for Kids', 'Provide 1000 books to rural schools.', 5000.00, 1500.00, '2025-10-01', '2025-12-31', 'active', 'https://example.com/media/books.jpg'),
(2, 'Plant 10,000 Trees', 'Reforest 50 hectares in the Mekong region.', 10000.00, 4200.00, '2025-09-15', '2025-12-15', 'active', 'https://example.com/media/trees.jpg'),
(2, 'Clean Rivers Initiative', 'Reduce river pollution through community efforts.', 8000.00, 500.00, '2025-11-01', '2026-01-31', 'draft', 'https://example.com/media/river.jpg');

-- TRANSACTIONS
INSERT INTO transactions (user_id, campaign_id, amount, status, blockchain_hash, message, receipt_url) VALUES
(1, 1, 100.00, 'confirmed', '0xabc123', 'Keep up the great work!', 'https://example.com/receipts/tx1.pdf'),
(2, 1, 250.00, 'confirmed', '0xdef456', 'For the kids!', 'https://example.com/receipts/tx2.pdf'),
(3, 2, 300.00, 'pending', '0xghi789', 'Let’s make it green.', 'https://example.com/receipts/tx3.pdf');

-- USER INTERACTIONS
INSERT INTO user_interactions (user_id, target_type, target_id, action_type, weight) VALUES
(1, 'organization', 1, 'view', 1),
(1, 'campaign', 1, 'donate', 5),
(2, 'campaign', 2, 'share', 2),
(3, 'organization', 2, 'click', 1);

-- REGISTRATIONS
INSERT INTO registrations (org_id, type, payload, status) VALUES
(1, 'organization', JSON_OBJECT('documents', 'submitted', 'reviewer', 'admin1'), 'approved'),
(2, 'campaign', JSON_OBJECT('draft_id', 3, 'submitted_by', 'Green Earth'), 'pending');
