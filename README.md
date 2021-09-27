## Create local db

```sql
CREATE USER rss_user WITH ENCRYPTED PASSWORD 'pass';
CREATE DATABASE rss_local_db OWNER rss_user;
CREATE DATABASE test_rss_local_db OWNER rss_user;
```