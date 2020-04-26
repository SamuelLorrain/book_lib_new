import acces_files
import query
import tools
from database import select_items
from database import bdd_misc_queries
from database import sqliteConnect
from tables import simple_table
from tables import factory_table
from tables import bind_table
from tables import complex_table
from pathlib import Path
import config
import shutil
import sys


# Initialization
bookFolderEntry = Path(config.configuration["PATH"]["rootPath"]) \
        / config.configuration["PATH"]["bookPath"]

if not bookFolderEntry.exists():
    print("Error : the book folder (rootPath+bookPath) doesn't exist")
    print("Please check your configuration file")
    exit(1)


bookPathInput = sys.argv[1]
#print(bookPathInput)
#print(tools.break_path(str(bookPathInput)))
#exit(1)

bookPath = Path(bookPathInput)
if not bookPath.exists():
    print("Error : the file doesn't exist")
    exit(1)
if bookPath.is_dir():
    print("Error : the file provided is a directory")
    exit(1)

bookNameInDb = tools.construct_filename(*tools.break_path(str(bookPathInput)))
print("The file '{}' will be copied to '{}'".format(bookPath,bookFolderEntry))

destination = bookFolderEntry / bookNameInDb
source = bookPath

print("Destination : {}".format(destination))
print("Source : {}".format(source))
if destination.exists():
    print("Error the file {} already exist".format(destination))
    exit(1)
shutil.copyfile(source, destination)

if destination.exists():
    print("The file {} has been successfully copied".format(destination))
else:
    print("Error unable to copy the file")
    exit(1)

newBook = factory_table.factory_table('book',
        tools.break_path(str(bookPathInput))[0])
bookFiletype = factory_table.factory_table('filetype',
        tools.break_path(str(bookPathInput))[1])

print(tools.break_path(str(bookPathInput))[1])
print(type(bookFiletype))
print(bookFiletype.name)
print(bookFiletype.rowid)
newBook.filetype_id = bookFiletype
print(newBook.filetype_id)
print(newBook.name)
print(bookFiletype)

#newBook.add()
#print(newBook.name," added to the database")

#subjects = input("Please, enter the subjects of the book, comma separated : \n")
#subjectEntries = []
#for index, subject in enumerate(subjects.split(',')):
#    subjectEntries[index] = factory_table.factory_table('subject', subject)
#
#for subject in subjectEntries:
#    if subject.rowid == None:
#        yesorno = input("Do you want to add {} \
#                subject to the database ? [Y/N]".format(subject.name))
#        if yesorno.lower() == 'y':
#            subject.add()
#        else:
#            print("discard {}".)

#Bind subjects to the book

#author = input("Please enter ther authors, comma separated : \n")
#genre = input("Please enter the genre, comma separated : \n")

#print("Book: {}".format(bookNameInDb))
#print("Subjects : {}".format(subjects))
#print("Author : {}".format(author))
#print("Genre : {}".format(genre))

