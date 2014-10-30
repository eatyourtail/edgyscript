#!/usr/bin/env python
# 
# edgyscript - A DSL for generating XML markup for the Edge80 (TM) platform.
#
# Todo:
#   - export parse tree to XML
#   - import XML to edgeyscript
#
# Author: Paul Mackin
#
"""
    Example DSL:

        UserForm
        name:CharField -> label:Username size:25
        email:EmailField -> size:32
        password:PasswordField

    Example grammar definition:

        form ::= form_name newline field+
        field ::= field_name colon field_type [arrow property+]
        property ::= key colon value
        form_name ::= word
        field_name ::= word
        field_type ::= CharField | EmailField | PasswordField
        key ::= word
        value ::= alphanumeric+
        word ::= alpha+
        newline ::= \n
        colon ::= :
        arrow ::= -> 

    My DSL:

        Resource -> ttl:300
            Rule simple_rule1 -> comment:"Example rule"
                SetCache -> aggressive:true

                Compose default_buffer ->
                    Literal -> value:"<html><head><title>Example output</title></head><body><h1>Example output</h1></body>"
                    Debug -> message:"we are debugging"
                

    My grammar:

        <super_statement> ::= <name_definition> arrow {statement_property}+ newline <simple_statement> | <super_statement>
        <simple_statement> ::= <name_definition> arrow {statement_property}+
        <name_definition> ::= attribute {value}
        <statement_property> ::= attribute colon value
        attribute ::= alphanumeric+
        value ::= alphanumeric+ | quoted_string
        colon ::= ':'
        newline ::= '\n'
        whitespace ::= '\n' | '\t' | ' ' 
        arrow ::= '->'


"""

from pyparsing import (Word, oneOf, OneOrMore, alphanums, alphas, QuotedString,
                       Optional, Suppress, Group, White, Or, ZeroOrMore, Forward,
                       LineEnd, indentedBlock)

arrow = Suppress('->')
whitespace = Suppress(White())
newline = Suppress('\n')
colon = Suppress(':')
eol = Suppress(LineEnd())

attribute = Word(alphanums + '_-')
value = (Word(alphanums+ '._-') ^ QuotedString('"'))

command = oneOf('Resource Attr Replace Apply SetCache Set Rule Insert Compose Copy Debug Literal Defmac Fetch Script Deliver Prerequisite Modify')
named_command = command + Optional(value)
command_property  = Group(attribute + colon + value)

def printCommandName(parse_string, location, matched_tokens_list):
    import time
    print 'COMMAND (%s):' % str(time.clock()), matched_tokens_list

# This recursive statement form taken from http://w3facility.info/question/simple-demonstration-of-using-pyparsings-indentedblock-recursively/
statement = ((command + newline) ^ (command + arrow) ^ (named_command + arrow)) + ZeroOrMore(command_property)
statement.setParseAction(printCommandName)
statementBlock = Forward()
statementBlock << statement + Optional(indentedBlock(statementBlock, [1]))

if __name__ == '__main__':
    from pyparsing import *
    import pprint
    import sys

    #statement.setDebug(True)

    FILE = sys.argv[1]
    for i, l in enumerate(file(FILE).read().split('\n')):
        print i+1, l
    parseTree = statementBlock.parseFile(FILE)
    print '\n'
    pprint.pprint(parseTree.asList())
