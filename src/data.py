"""Datatypes used by StudyTool"""
from __future__ import annotations
from enum import Enum
from typing import Callable, Union


class Language(Enum):
    KOREAN = "Korean"
    ENGLISH = "English"

class Utilities:
    def get_language(string: str) -> Language:
        """
        Arguments:
            string: The string to convert
        
        Raises:
            ValueError: If the string does not match any Language

        Returns:
            The Language enum corresponding to the given string
        """
        clean_string = string.strip().lower()

        for language in Language:
            language_string = language.value
            assert isinstance(language_string, str)

            if language_string.lower() == clean_string:
                return language

        raise ValueError(f"Language not supported: {string}")

    def set_list_to_string(container: Union[list, set], delimiter: str = ", ") -> str:
        """
        Arguments:
            container: The set or list to turn into a string
            delimiter: The string to separate the entries with

        Returns:
            A delimited string representing the given set or list
        """
        string = ""

        for entry in container:
            string = f"{string}{entry}{delimiter}"
        
        string = string[:-len(delimiter)]
        return string
    
    def default_sanitizer(string: str) -> str:
        """
        Arguments:
            string: The string to sanitize
        
        Returns:
            A sanitized string
        """
        return string.strip().lower()
    
    def string_to_list(string: str, delimiter: str = ",", sanitizer: Callable[[str], str] = default_sanitizer) -> list[str]:
        """
        Arguments:
            string: The string to convert into a list
            delimiter: The delimiting character
            sanitizer: The function to sanitize each entry with

        Returns:
            A list representation of the string
        """
        values = string.split(delimiter)

        for i in range(len(values)):
            values[i] = sanitizer(values[i])
        
        return values

class Entry:
    def __init__(self, term: str, definition: str, tags: set[str]):
        """
        Constructs an entry

        Member Variables:
            term: The value of the term
            definition: The value of the definition
            tags: The tags associated with the entry
        """
        self.term = term
        self.definition = definition
        self.tags = tags

    def __str__(self) -> str:
        """
        Returns:
            The string representation of the entry
        """
        tag_string = Utilities.set_list_to_string(self.tags)
        return f"{tag_string} | {self.term} -> {self.definition}"

class Set:
    def __init__(self, name: str, term_type: Language, definition_type: Language):
        """
        Constructs a set.
        TODO: There can be multiple entries with the same term, but they must have different definitions

        Member Variables:
            name: The name of the set
            term_type: The language of the terms
            definition_type: The language of the definitions
        """
        self.name = name
        self.term_type = term_type
        self.definition_type = definition_type

        self.entries: list[Entry] = []
        self.entries_by_tag: dict[str, list[Entry]] = {}
    
    def meta_string(self) -> str:
        """
        Returns:
            The string representing the metadata of the set
        """
        return f"{self.name}: {self.term_type.value} -> {self.definition_type.value}"
    
    def entries_string(self) -> str:
        """
        Returns:
            The string representing the entries of the set
        """
        return Utilities.set_list_to_string(self.entries, "\n")
    
    def __str__(self) -> str:
        """
        Returns:
            The string representation of the set
        """
        return f"{self.meta_string()}\n{self.entries_string()}"
    
    def add_entry(self, entry: Entry, tags: list[str]) -> None:
        """
        Adds the given entry to the set

        Arguments:
            entry: The entry to be added
            tags: Tags associated with that entry

        Returns:
            None
        """
        self.entries.append(entry)

        for tag in tags:
            if tag in self.entries_by_tag:
                self.entries_by_tag[tag].append(entry)
            else:
                self.entries_by_tag[tag] = [entry]