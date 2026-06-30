-- Migration Script: Phase 7.6 Hotfix - Add parsed_data to current_resume

ALTER TABLE public.current_resume ADD COLUMN IF NOT EXISTS parsed_data JSONB;
