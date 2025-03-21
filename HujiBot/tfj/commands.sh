tfj run "centitanha" --command ~/tfj/jobs/centitanha.sh -e ~/tfj/logs/centitanha.log -o ~/tfj/logs/centitanha.log --image tf-python37 --schedule "@weekly"
tfj run "daily" --command ~/tfj/jobs/daily.sh -e ~/tfj/logs/daily.log -o ~/tfj/logs/daily.log --image tf-python37 --schedule "@daily"
tfj run "findproxy" --command ~/tfj/jobs/findproxy.sh -e ~/tfj/logs/findproxy.log -o ~/tfj/logs/findproxy.log --image tf-python37 --schedule "@daily"
tfj run "hourly" --command ~/tfj/jobs/hourly.sh -e ~/tfj/logs/hourly.log -o ~/tfj/logs/hourly.log --image tf-python37 --schedule "@hourly"
tfj run "image-resizer" --command ~/tfj/jobs/image_resizer.sh -e ~/tfj/logs/image_resizer.log -o ~/tfj/logs/image_resizer.log --image tf-python37 --schedule "@weekly"
tfj run "import-all-blocks" --command ~/tfj/jobs/import-all-blocks.sh -e ~/tfj/logs/import-all-blocks.log -o ~/tfj/logs/import-all-blocks.log --image tf-python37 --schedule "@monthly"
tfj run "import-blocks" --command ~/tfj/jobs/import-blocks.sh -e ~/tfj/logs/import-blocks.log -o ~/tfj/logs/import-blocks.log --image tf-python37 --schedule "@weekly"
tfj run "inactive-users" --command ~/tfj/jobs/inactive-users.sh -e ~/tfj/logs/inactive-users.log -o ~/tfj/logs/inactive-users.log --image tf-python37 --schedule "@weekly"
tfj run "active-users" --command ~/tfj/jobs/active-users.sh -e ~/tfj/logs/active-users.log -o ~/tfj/logs/active-users.log --image tf-python37 --schedule "@weekly"
tfj run "monthly" --command ~/tfj/jobs/monthly.sh -e ~/tfj/logs/monthly.log -o ~/tfj/logs/monthly.log --image tf-python37 --schedule "@monthly"
tfj run "nightly" --command ~/tfj/jobs/nightly.sh -e ~/tfj/logs/nightly.log -o ~/tfj/logs/nightly.log --image tf-python37 --schedule "@daily"
tfj run "weekly" --command ~/tfj/jobs/weekly.sh -e ~/tfj/logs/weekly.log -o ~/tfj/logs/weekly.log --image tf-python37 --schedule "0 11 * * 5"
tfj run "weekly-en" --command ~/tfj/jobs/weekly-en.sh -e ~/tfj/logs/weekly-en.log -o ~/tfj/logs/weekly-en.log --image tf-python37 --schedule "0 11 * * 5"
tfj run "weekly-slow" --command ~/tfj/jobs/weekly-slow.sh -e ~/tfj/logs/weekly-slow.log -o ~/tfj/logs/weekly-slow.log --image tf-python37 --schedule "30 10 * * 5"
