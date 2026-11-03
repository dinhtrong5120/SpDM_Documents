# Kéo db về local
## demo
```
mysqldump --default-character-set=utf8mb4 \
-h uu3-spdm-database.cizy4ci6ujh1.us-east-1.rds.amazonaws.com \
-u admin -p'MasterDB$sqZ**' demo_spdm > db_demo.sql && \
aws s3 cp db_demo.sql \
"s3://spdm-artifacts-bucket/db_demo_$(TZ=Asia/Ho_Chi_Minh date +%Y%m%d_%H%M%S).sql" && \
rm db_demo.sql
```

## stg
```
mysqldump --default-character-set=utf8mb4 \
  --single-transaction \
  --quick \
  --no-tablespaces \
  --set-gtid-purged=OFF \
  -h spdmtokyo-datastoredatabased48102a6-nxu8ri899nro.c7ksccaeghql.ap-northeast-1.rds.amazonaws.com \
  -u spdm_stg_user \
  -p'u1iCsadp1YW5X5CtjvVe37FLS0N2jCMV' \
  stg_spdm > /tmp/db_stg.sql && \
  aws s3 cp /tmp/db_stg.sql \
"s3://spdmtokyo-datastorebucketsappdata7fd474b4-luulslqhdvcw/db_stg_$(TZ=Asia/Ho_Chi_Minh date +%Y%m%d_%H%M%S).sql" && \
rm /tmp/db_stg.sql
```

# Xuất file dump sql
```
mysqldump --default-character-set=utf8mb4 -u root -p'Sql123456' spdm > "/Users/TrongKieu/Downloads/database/db_local/db_local_$(TZ=Asia/Ho_Chi_Minh date +%Y%m%d_%H%M%S).sql"
```
# Kết nối db rds
```angular2html
mysql -h uu3-spdm-database.cizy4ci6ujh1.us-east-1.rds.amazonaws.com -u admin -p'MasterDB$sqZ**';
USE demo_spdm;
```

# Import db vào local
```angular2html
mysql -u root -p'Sql123456' \
  -e "DROP DATABASE IF EXISTS spdm; CREATE DATABASE spdm;" \
&& \
mysql --default-character-set=utf8mb4 \
  -h localhost \
  -u root \
  -p'Sql123456' \
  spdm < /Users/TrongKieu/Downloads/database/db_demo/db_local_20261031_102336.sql
```