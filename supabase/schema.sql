-- CrowdLuma — Supabase schema
-- À exécuter dans : Supabase Dashboard › SQL Editor › New query

-- ── Commandes shop ────────────────────────────────────────────────────────────
create table if not exists orders (
  id           uuid primary key default gen_random_uuid(),
  stadium_id   text not null default 'default',
  seat_id      text not null,
  row          int  not null,
  col          int  not null,
  item_id      text not null,
  item_label   text,
  price        decimal(6,2),
  status         text not null default 'pending',  -- pending | preparing | delivering | paid | cancelled
  participant_id text,                              -- UUID localStorage du supporter (MVP2)
  stand          text,                              -- Nom de la tribune (ex: "Tribune Nord")
  zone_id        text,                              -- Zone optionnelle
  block_id       text,                              -- Bloc (ex: "A")
  created_at     timestamptz not null default now()
);

-- ── Votes ─────────────────────────────────────────────────────────────────────
create table if not exists votes (
  id           uuid primary key default gen_random_uuid(),
  stadium_id   text not null default 'default',
  question     text not null,
  options      jsonb not null,   -- ["Option A", "Option B", ...]
  active       boolean not null default true,
  created_at   timestamptz not null default now()
);

-- ── Réponses aux votes ────────────────────────────────────────────────────────
create table if not exists vote_responses (
  id           uuid primary key default gen_random_uuid(),
  vote_id      uuid not null references votes(id) on delete cascade,
  seat_id      text not null,
  option_idx   int  not null,
  created_at   timestamptz not null default now(),
  unique (vote_id, seat_id)   -- un vote par siège
);

-- ── Row Level Security ────────────────────────────────────────────────────────
alter table orders         enable row level security;
alter table votes          enable row level security;
alter table vote_responses enable row level security;

-- Participants (anon) : insérer des commandes et des réponses, lire les votes
create policy "anon_insert_orders"    on orders         for insert to anon with check (true);
create policy "anon_read_orders"      on orders         for select to anon using (true);
create policy "anon_read_votes"       on votes          for select to anon using (true);
create policy "anon_insert_vote_resp" on vote_responses for insert to anon with check (true);
create policy "anon_read_vote_resp"   on vote_responses for select to anon using (true);

-- Admin (authenticated) : tout
create policy "auth_all_orders"    on orders         for all to authenticated using (true) with check (true);
create policy "auth_all_votes"     on votes          for all to authenticated using (true) with check (true);
create policy "auth_all_vote_resp" on vote_responses for all to authenticated using (true) with check (true);

-- ── Realtime ──────────────────────────────────────────────────────────────────
-- Activer la réplication pour les résultats de votes en temps réel :
-- Supabase Dashboard › Database › Replication › Tables → cocher vote_responses

-- ── Index ─────────────────────────────────────────────────────────────────────
create index if not exists orders_stadium_idx       on orders(stadium_id, created_at desc);
create index if not exists vote_responses_vote_idx  on vote_responses(vote_id);
create index if not exists orders_participant_idx on orders(participant_id);

-- ── Migration MVP2 (si la table orders existe déjà) ───────────────────────────
-- Ajouter les nouvelles colonnes à une installation existante :
-- alter table orders add column if not exists stand     text;
-- alter table orders add column if not exists zone_id   text;
-- alter table orders add column if not exists block_id  text;
-- alter table orders add column if not exists status    text not null default 'pending'; -- déjà existant
-- Modifier le statut si nécessaire : pending | preparing | delivering | paid | cancelled

-- ── Index supplémentaire ──────────────────────────────────────────────────────
create index if not exists orders_stand_idx on orders(stadium_id, stand, block_id);
