# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__all__ = [ 'gencxx', 'genipdl', 'parse', 'typecheck', 'writeifmodified' ]

import os, sys
from cStringIO import StringIO

from ipdl.cgen import IPDLCodeGen
from ipdl.lower import LowerToCxx
from ipdl.parser import Parser
from ipdl.type import TypeCheck

from ipdl.cxx.cgen import CxxCodeGen


def parse(specstring, filename='/stdin', includedirs=[ ], errout=sys.stderr):
    '''Return an IPDL AST if parsing was successful.  Print errors to |errout|
    if it is not.'''
    return Parser().parse(specstring, os.path.abspath(filename), includedirs, errout)


def typecheck(ast, errout=sys.stderr):
    '''Return True iff |ast| is well typed.  Print errors to |errout| if
    it is not.'''
    return TypeCheck().check(ast, errout)


def gencxx(ipdlfilename, ast, outheadersdir, outcppdir):
    headers, cpps = LowerToCxx().lower(ast)

    def resolveHeader(hdr):
        return [
            hdr, 
            os.path.join(
                outheadersdir,
                *([ns.name for ns in ast.protocol.namespaces] + [hdr.name]))
        ]
    def resolveCpp(cpp):
        return [ cpp, os.path.join(outcppdir, cpp.name) ]

    for ast, filename in ([ resolveHeader(hdr) for hdr in headers ]
                          + [ resolveCpp(cpp) for cpp in cpps ]):
        tempfile = StringIO()
        CxxCodeGen(tempfile).cgen(ast)
        writeifmodified(tempfile.getvalue(), filename)


def genipdl(ast, outdir):
    return IPDLCodeGen().cgen(ast)


def writeifmodified(contents, file):
    dir = os.path.dirname(file)
    os.path.exists(dir) or os.makedirs(dir)

    oldcontents = None
    if os.path.exists(file):
        fd = open(file, 'rb')
        oldcontents = fd.read()
        fd.close()
    if oldcontents != contents:
        fd = open(file, 'wb')
        fd.write(contents)
        fd.close()
