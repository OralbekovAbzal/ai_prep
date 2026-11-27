create table camera_moves (
    id bigserial primary key,
    name text not null,
    description text not null,
    embedding vector(768)
);

create index on camera_moves using hnsw (embedding vector_cosine_ops);