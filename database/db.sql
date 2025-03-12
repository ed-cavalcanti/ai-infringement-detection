CREATE TABLE IF NOT EXISTS
  public.image_analysis (
    id serial NOT NULL,
    image_id text NULL,
    prompt_strategy text NULL,
    prompt text NULL,
    model text NULL,
    expected_response text NULL,
    ai_response text NULL,
    database text NULL
  );
