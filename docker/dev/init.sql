CREATE USER yumecloudadmin WITH PASSWORD '@WSX3edc';
CREATE DATABASE yumecloud;
GRANT ALL PRIVILEGES ON DATABASE yumecloud TO yumecloudadmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO yumecloudadmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO yumecloudadmin;
ALTER DATABASE yumecloud OWNER TO yumecloudadmin;