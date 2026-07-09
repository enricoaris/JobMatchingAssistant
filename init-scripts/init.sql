-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "Jobs" (
    "Id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "Title" VARCHAR(255),
    "ContextText" TEXT,
    "Status" INTEGER,
    "Embedding" VECTOR(384),  -- Adjust dimension as needed
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- JOB FEATURES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "JobFeatures" (
    "Id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "JobId" UUID NOT NULL,
    "Skills" JSONB,
    "SkillsMeta" JSONB,
    "ExperienceYears" INTEGER NOT NULL DEFAULT 0,
    "Seniority" VARCHAR(50),
    "EmbeddingNorm" REAL,
    "EmbeddingStd" REAL,
    "Requirements" TEXT[],
    "Highlights" TEXT[],
    CONSTRAINT fk_job_features_job FOREIGN KEY ("JobId") 
        REFERENCES "Jobs"("Id") ON DELETE CASCADE
);

-- ============================================
-- RESUMES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "Resumes" (
    "Id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "FilePath" TEXT NOT NULL,
    "Status" INTEGER,
    "ContextText" TEXT,
    "Embedding" VECTOR(384),  -- Adjust dimension as needed
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "Filename" VARCHAR(255)
);

-- ============================================
-- RESUME FEATURES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "ResumeFeatures" (
    "Id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "ResumeId" UUID NOT NULL,
    "Skills" JSONB,
    "SkillsMeta" JSONB,
    "ExperienceYears" INTEGER NOT NULL DEFAULT 0,
    "Seniority" VARCHAR(50),
    "EmbeddingNorm" REAL,
    "EmbeddingStd" REAL,
    "Requirements" TEXT[],
    "Highlights" TEXT[],
    CONSTRAINT fk_resume_features_resume FOREIGN KEY ("ResumeId") 
        REFERENCES "Resumes"("Id") ON DELETE CASCADE
);

-- ============================================
-- MATCHES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS "Matches" (
    "MatchId" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "ResumeId" UUID NOT NULL,
    "JobId" UUID NOT NULL,
    "Score" REAL NOT NULL,
    "Suggestions" TEXT[],
    "MissingSkills" TEXT[],
    "match_level" VARCHAR(50),
    "assessment" TEXT,
    "key_gaps" TEXT[],
    "CreatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_matches_resume FOREIGN KEY ("ResumeId") 
        REFERENCES "Resumes"("Id") ON DELETE CASCADE,
    CONSTRAINT fk_matches_job FOREIGN KEY ("JobId") 
        REFERENCES "Jobs"("Id") ON DELETE CASCADE
);

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE
-- ============================================

-- Vector similarity indexes (using IVF for approximate nearest neighbor)
-- CREATE INDEX IF NOT EXISTS idx_jobs_embedding ON "Jobs" 
--     USING ivfflat ("Embedding" vector_cosine_ops) 
--     WITH (lists = 100);

-- CREATE INDEX IF NOT EXISTS idx_resumes_embedding ON "Resumes" 
--     USING ivfflat ("Embedding" vector_cosine_ops) 
--     WITH (lists = 100);

-- Foreign key indexes
CREATE INDEX IF NOT EXISTS idx_jobfeatures_jobid ON "JobFeatures"("JobId");
CREATE INDEX IF NOT EXISTS idx_resumefeatures_resumeid ON "ResumeFeatures"("ResumeId");
CREATE INDEX IF NOT EXISTS idx_matches_resumeid ON "Matches"("ResumeId");
CREATE INDEX IF NOT EXISTS idx_matches_jobid ON "Matches"("JobId");

-- Other useful indexes
CREATE INDEX IF NOT EXISTS idx_jobs_status ON "Jobs"("Status");
CREATE INDEX IF NOT EXISTS idx_resumes_status ON "Resumes"("Status");
CREATE INDEX IF NOT EXISTS idx_matches_score ON "Matches"("Score");

-- JSONB indexes for better query performance on JSON fields
CREATE INDEX IF NOT EXISTS idx_jobfeatures_skills ON "JobFeatures" 
    USING gin ("Skills" jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_jobfeatures_skillsmeta ON "JobFeatures" 
    USING gin ("SkillsMeta" jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_resumefeatures_skills ON "ResumeFeatures" 
    USING gin ("Skills" jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_resumefeatures_skillsmeta ON "ResumeFeatures" 
    USING gin ("SkillsMeta" jsonb_path_ops);

-- ============================================
-- CREATE HELPER FUNCTIONS
-- ============================================

-- Function to update UpdatedAt timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW."UpdatedAt" = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update UpdatedAt
CREATE TRIGGER update_jobs_updated_at 
    BEFORE UPDATE ON "Jobs" 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resumes_updated_at 
    BEFORE UPDATE ON "Resumes" 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VERIFY SETUP
-- ============================================

DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
    RAISE NOTICE 'Tables created: Jobs, JobFeatures, Resumes, ResumeFeatures, Matches';
    RAISE NOTICE 'Extensions enabled: vector, uuid-ossp';
    RAISE NOTICE 'Indexes and triggers created';
END $$;