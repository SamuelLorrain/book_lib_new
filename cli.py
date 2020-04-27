import shutil
import sys
import argparse

import tools
from tables import factory_table
from pathlib import Path
import config
"""
Todo:
    - Make if works even if the book already exist in the database
"""

# Parser
parser = argparse.ArgumentParser(
        prog="cli.py",
        description="CLI tool for book_lib_new",
        allow_abbrev=False)

parser.add_argument('path',
                    metavar='path',
                    action="store",
                    type=str,
                    help="the path to list",
                    )

parser.add_argument('-s',
                    '--subject',
                    metavar="subject",
                    action="store",
                    type=str,
                    default=[],
                    help="add subjects to book",
                    nargs="+"
                    )

parser.add_argument('-a',
                    '--author',
                    metavar="author",
                    action="store",
                    type=str,
                    default=[],
                    help="add authors to book",
                    nargs="+"
                    )

parser.add_argument('-g',
                    '--genre',
                    metavar="genre",
                    action="store",
                    type=str,
                    default=[],
                    help="add genre to book",
                    nargs="+"
                    )
args = parser.parse_args()

print(args)

# Initialization
bookFolderEntry = Path(config.configuration["PATH"]["rootPath"]) \
        / config.configuration["PATH"]["bookPath"]

if not bookFolderEntry.exists():
    print("Error : the book folder (rootPath+bookPath) doesn't exist")
    print("Please check your configuration file")
    exit(1)

bookPathInput = args.path
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
newBook.filetype_id = bookFiletype

newBook.add()
print(newBook.name," added to the database")

# authors
for name in args.author:
    authorEntry = factory_table.factory_table('author', name.title())
    if not authorEntry.rowid:
        yesorno = input("'{}' is not in the database, should we add it ?"
                " [y/n] : ".format(name))
        if yesorno.lower() == 'y':
            authorEntry.add()
            bindTable = factory_table.factory_bind(authorEntry, newBook)
            bindTable.add()
        else:
            continue
    else:
        print("{} already in the database".format(authorEntry.name))
        bindTable = factory_table.factory_bind(authorEntry, newBook)
        bindTable.add()

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

