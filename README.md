## Create local db

```sql
CREATE DATABASE rss_local_db;
CREATE USER rss_user WITH ENCRYPTED PASSWORD 'pass';
GRANT ALL PRIVILEGES ON DATABASE rss_local_db TO rss_user;
GRANT ALL ON ALL TABLES IN SCHEMA public to rss_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to rss_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to rss_user;

ALTER USER rss_user CREATEDB; /* команда для возможности создания тестовой базы. */
```