"""
Metadata: <set name>: <term type> -> <definition type>
Entry: <tags> | <term> -> <definitions>
Lists: <entry>, <entry>, ..., <entry>

Metadata is kept on the first line of a .set file
Entries are separated by newlines
<tags> and <definitions> can be lists
"""
from __future__ import annotations
import data
import os

class Parser:
    def parse_set(self, filepath: str) -> data.Set:
        """
        Arguments:
            filepath: The filepath relative to the data directory for the set
        
        Returns:
            A set object representing the specified set
        """
        with open(filepath, "r") as file:
            meta = file.readline()
            lines = file.readlines()
        set_object = self.parse_meta(meta)
        self.parse_body(lines, set_object)

        return set_object
    
    def parse_meta(self, meta: str) -> data.Set:
        """
        Arguments:
            meta: The string containing the set metadata

        Returns:
            A set object with metadata but no entries 
        """
        parts = meta.split(":")
        name = parts[0].strip()

        parts = parts[1].split("->")
        term = data.Utilities.get_language(parts[0])
        definition = data.Utilities.get_language(parts[1])

        return data.Set(name, term, definition)
    
    def parse_body(self, lines: list[str], set_object: data.Set) -> None:
        """
        Parses the entries in the given lines. Adds them to the given set object

        Arguments:
            lines: A list of strings. Each string represents an entry.
            set_object: The set to add the entries to
        
        Returns:
            None
        """
        for line in lines:
            parts = line.split("|")
            tags = set(data.Utilities.string_to_list(parts[0]))
            entry = self.parse_entry(parts[1], tags)

            set_object.add_entry(entry, tags)

    def parse_entry(self, string: str, tags: list[str]) -> data.Entry:
        """
        Arguments:
            string: The string representing the term and definition
            tags: The tags for the given entry
        
        Returns:
            A data.Entry object for the given string
        """
        parts = string.split("->")
        term = parts[0].strip()
        definition = parts[1].strip()
        
        return data.Entry(term, definition, tags)
