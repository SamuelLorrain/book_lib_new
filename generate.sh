#!/bin/sh

###
#
# To generate DB
# uncomment lasts lines
# and launch the file.
#
# ! Don't save
# ! If you want to keep older data,
# ! Dont forget to change the name
# ! of the old DB to keep it.
#
###
DATABASE_NAME="data.db"
SQL_FILE="schema.sql"

if [ -f "$DATABASE_NAME" ] ;then
    echo -e "\nThe database already exists with the same name. To generate a new database
You must change the name of the existant database first\n"
    exit 1
fi
#rm $DATABASE_NAME
#sqlite3 $DATABASE_NAME < $SQL_FILE
