create table llm_calls (
    id bigserial primary key,
    model text not null,
    input_text text not null,
    input_tokens int not null,
    output_tokens int,
    response_time_ms int not null,
    response_text text,
    error_text text,
    created_at timestamptz default now()
)