import shutil
import os
import sys
import argparse

import tools
from tables import factory_table
from tables.complex_table import Book
from pathlib import Path
import config
from typing import List

"""
Todo:
    - Use Levenstein distance or other fuzzy finding algo when
      adding Author/Subject/Genre/Book etc.
    - Refactor things
    - Rename already existing book
"""

def bindElementsToBook(entries: List[str], tableType: str, bookEntry: Book):
    for name in entries:
        entry = factory_table.factory_table(tableType, name.title())
        if not entry.rowid:
            yesorno = input("'{}' is not in the database, should we add it ?"
                    " [y/n] : ".format(name))
            if yesorno.lower() == 'y':
                entry.add()
                bindTable = factory_table.factory_bind(entry, bookEntry)
                bindTable.add()
            else:
                continue
        else:
            print("{} already in the database".format(entry.name))
            bindTable = factory_table.factory_bind(entry, bookEntry)
            bindTable.add()

def unbindElementsToBook(entries: List[str], tableType: str, bookEntry: Book):
    for name in entries:
        entry = factory_table.factory_table(tableType, name.title())
        if not entry.rowid:
            print("Error, The {} {} is not in the database".format(
                tableType, name))
            continue
        else:
            bindTable = factory_table.factory_bind(entry, bookEntry)
            if not bindTable.rowid:
                print("Error, The bind for {} - {} doesn't exist".format(bookEntry.name, name.title()))
            else:
                bindTable.remove()

def parser():
    parser = argparse.ArgumentParser(
            prog="cli.py",
            description="CLI tool for book_lib_new",
            allow_abbrev=False)

    parser.add_argument('path',
                        metavar='path',
                        action="store",
                        type=str,
                        help="the path to list",
                        nargs='?')

    parser.add_argument('--data-name',
                        metavar='data-name',
                        action="store",
                        type=str,
                        help="the name of the book in database")

    parser.add_argument('--name',
                        metavar='name',
                        action="store",
                        type=str,
                        help="name of the file in the database")

    parser.add_argument('--delete',
                        action="store_true",
                        help="will delete the original file")

    parser.add_argument('-s', '--subject',
                        metavar="subject",
                        action="store",
                        type=str,
                        default=[],
                        help="add subjects to book",
                        nargs="+")

    parser.add_argument('-a', '--author',
                        metavar="author",
                        action="store",
                        type=str,
                        default=[],
                        help="add authors to book",
                        nargs="+")

    parser.add_argument('-g', '--genre',
                        metavar="genre",
                        action="store",
                        type=str,
                        default=[],
                        help="add genre to book",
                        nargs="+")
    parser.add_argument('--unbind-subject',
                        metavar="subject",
                        action="store",
                        type=str,
                        default=[],
                        help="remove subjects from book",
                        nargs="+")

    parser.add_argument('--unbind-author',
                        metavar="author",
                        action="store",
                        type=str,
                        default=[],
                        help="remove authors from book",
                        nargs="+")

    parser.add_argument('--unbind-genre',
                        metavar="genre",
                        action="store",
                        type=str,
                        default=[],
                        help="remove genre from book",
                        nargs="+")
    return parser.parse_args()

def addBook(bookPathInput, bookPathDb, name=None):
    bookPath = Path(bookPathInput)

    if not bookPath.exists():
        print("Error : the file doesn't exist")
        exit(1)
    if bookPath.is_dir():
        print("Error : the file provided is a directory")
        exit(1)

    if name:
        typename = tools.break_path(str(bookPathInput))[1]
        bookNameInDb = tools.construct_filename(args.name, typename)
    else:
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

    if args.delete:
        yesorno = input("Are you sure you want to delete {} ? [y/n]".format(bookPath))
        if yesorno.lower() == 'y':
            os.remove(bookPath)

    # Add book in the database
    newBook = factory_table.factory_table('book',
            tools.break_path(str(bookPathInput))[0])
    bookFiletype = factory_table.factory_table('filetype',
            tools.break_path(str(bookPathInput))[1])
    newBook.filetype_id = bookFiletype

    newBook.add()
    print(newBook.name," added to the database")

    return newBook


if __name__ == '__main__':

    args = parser()

    if args.path is None and args.data_name is None:
        parser.error("path to file or --data-name option must be provided")

    # Book copy
    bookFolderEntry = Path(config.configuration["PATH"]["rootPath"]) \
            / config.configuration["PATH"]["bookPath"]

    if not bookFolderEntry.exists():
        print("Error : the book folder (rootPath+bookPath) doesn't exist")
        print("Please check your configuration file")
        exit(1)

    if args.path:
        newBook = addBook(args.path, bookFolderEntry, name=args.name)
    elif args.data_name:
        newBook = factory_table.factory_table('book', args.data_name.title())
        if (args.name): #if we rename the book
            pass

    # bindElements
    bindElementsToBook(args.author, 'author', newBook)
    bindElementsToBook(args.subject, 'subject', newBook)
    bindElementsToBook(args.genre, 'genre', newBook)

    # bindElements
    unbindElementsToBook(args.unbind_author, 'author', newBook)
    unbindElementsToBook(args.unbind_subject, 'subject', newBook)
    unbindElementsToBook(args.unbind_genre, 'genre', newBook)
