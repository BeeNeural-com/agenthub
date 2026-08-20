---
name: web-database-integration
description: >-
  PostgreSQL, MySQL, MongoDB, Prisma, Drizzle, connection pooling, and migrations
  for web/backend applications.
tags: [web-development, database, backend]
---

# Web Database Integration

## When to Use

- Connecting a web app or API to PostgreSQL, MySQL, or MongoDB
- Choosing between Prisma, Drizzle, or native drivers
- Designing schemas, migrations, and connection pooling for production
- Debugging query performance or N+1 issues in ORM-backed apps

## Procedure

### Step 1: Select database and ORM

- PostgreSQL: default for relational data with strong constraints (recommended)
- MySQL/MariaDB: legacy or hosting constraints
- MongoDB: flexible document models; use when schema varies heavily
- Consult **web-ecosystem-catalog** ORM section; verify package versions via **npm-package-research**

### Step 2: Schema and migrations

- Define schema in ORM DSL (Prisma `schema.prisma`, Drizzle `schema.ts`) or SQL migrations
- Include `createdAt`, `updatedAt`, indexes on foreign keys and query filters
- Both sides of relations defined (Prisma `@relation` on both models)
- Run migrations in CI; never edit applied migration files

### Step 3: Connection management

- Use connection pooling (PgBouncer, Prisma Accelerate, `@vercel/postgres` pool)
- Set pool size based on serverless vs long-running process constraints
- Store `DATABASE_URL` in env; never commit credentials
- Graceful shutdown: close pools on process exit

### Step 4: Query patterns

- Parameterized queries only; never string-concatenate user input
- Use transactions for multi-step writes (`prisma.$transaction`, Drizzle `db.transaction`)
- Select only needed columns; paginate list endpoints
- Add indexes after profiling slow queries (EXPLAIN ANALYZE)

### Step 5: Environment-specific setup

- Local: Docker Compose or managed dev instance
- Production: managed service (RDS, Neon, PlanetScale, Atlas) with TLS
- Seed scripts for dev/staging; separate migration deploy step

## Output

- Schema definition, migration files, and connection configuration
- Query examples with pooling notes for deployment target

## References

- Prisma docs: https://www.prisma.io/docs
- Drizzle ORM: https://orm.drizzle.team/docs/overview
- PostgreSQL docs: https://www.postgresql.org/docs/current/
- MongoDB Node driver: https://www.mongodb.com/docs/drivers/node/current/
- node-postgres (pg): https://node-postgres.com/
