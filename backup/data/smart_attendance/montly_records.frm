TYPE=VIEW
query=select `smart_attendance`.`attendance`.`id` AS `id`,`smart_attendance`.`attendance`.`username` AS `username`,`smart_attendance`.`attendance`.`name` AS `name`,`smart_attendance`.`attendance`.`email` AS `email`,`smart_attendance`.`attendance`.`contact` AS `contact`,`smart_attendance`.`attendance`.`course` AS `course`,`smart_attendance`.`attendance`.`divison` AS `divison`,`smart_attendance`.`attendance`.`class_code` AS `class_code`,`smart_attendance`.`attendance`.`subject` AS `subject`,`smart_attendance`.`attendance`.`status` AS `status`,`smart_attendance`.`attendance`.`date` AS `date`,count(`smart_attendance`.`attendance`.`status`) * 100 / 28 AS `perc` from `smart_attendance`.`attendance` where `smart_attendance`.`attendance`.`status` = \'present\' group by `smart_attendance`.`attendance`.`id`
md5=fca01e92447845a5371a219138831089
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=1
with_check_option=0
timestamp=0001675087943709539
create-version=2
source=select `attendance`.`id` AS `id`,`attendance`.`username` AS `username`,`attendance`.`name` AS `name`,`attendance`.`email` AS `email`,`attendance`.`contact` AS `contact`,`attendance`.`course` AS `course`,`attendance`.`divison` AS `divison`,`attendance`.`class_code` AS `class_code`,`attendance`.`subject` AS `subject`,`attendance`.`status` AS `status`,`attendance`.`date` AS `date`,((count(`attendance`.`status`) * 100) / 28) AS `perc` from `attendance` where (`attendance`.`status` = \'present\') group by `attendance`.`id`
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `smart_attendance`.`attendance`.`id` AS `id`,`smart_attendance`.`attendance`.`username` AS `username`,`smart_attendance`.`attendance`.`name` AS `name`,`smart_attendance`.`attendance`.`email` AS `email`,`smart_attendance`.`attendance`.`contact` AS `contact`,`smart_attendance`.`attendance`.`course` AS `course`,`smart_attendance`.`attendance`.`divison` AS `divison`,`smart_attendance`.`attendance`.`class_code` AS `class_code`,`smart_attendance`.`attendance`.`subject` AS `subject`,`smart_attendance`.`attendance`.`status` AS `status`,`smart_attendance`.`attendance`.`date` AS `date`,count(`smart_attendance`.`attendance`.`status`) * 100 / 28 AS `perc` from `smart_attendance`.`attendance` where `smart_attendance`.`attendance`.`status` = \'present\' group by `smart_attendance`.`attendance`.`id`
mariadb-version=100427
